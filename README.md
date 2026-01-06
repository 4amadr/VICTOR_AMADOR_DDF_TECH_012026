# Documentação — Case Técnico (Supabase + Dadosfera)

Este documento descreve, de ponta a ponta, as etapas executadas no projeto de dados usando um dataset de e-commerce (varejo) como base.

## Visão geral do que foi feito

Fluxo geral do projeto:

- Fonte: Kaggle (dataset de e-commerce varejo)
- Staging/armazenamento: Supabase (PostgreSQL)
- Plataforma de dados: Dadosfera (conexões, pipelines, catálogo)
- Tratamento: Jupyter Notebook (Python)
- Data Quality: Soda
- Visualização: Metabase (módulo Visualização da Dadosfera)

---

## Passo a passo executado

### 1) Coleta do dataset
1. Coletei os dados de e-commerce de varejo pelo Kaggle como exemplo.

### 2) Carga inicial (RAW) no Supabase
2. Usando Jupyter Notebook, executei um script para enviar os dados **assim como chegaram (raw)** para a plataforma Supabase.

### 3) Join no Supabase (para facilitar análise)
3. Dentro do Supabase, executei uma query de **JOIN** para unir os dados em uma nova tabela, facilitando análises posteriores.

### 4) Integração RAW na Dadosfera
4. Na Dadosfera:
- Criei a **conexão** com o Supabase.
- Criei a **pipeline** para ingestão dos dados raw.
- Documentei/cataloguei os dados no ambiente.

### 5) Tratamento (TRUSTED) via Jupyter Notebook
5. Voltei ao Jupyter Notebook, tratei os dados e salvei em um subdiretório `trusted/`.  
Principais limpezas realizadas:

- **Tabela de avaliação (reviews)**:
  - Identifiquei comentários ausentes como `NaN` e substituí por `"não comentou"`.
- **Todas as tabelas**:
  - Busquei valores **nulos** e **duplicados** em colunas estratégicas para encontrar inconsistências.
  - Exemplo: procurei duplicatas nas colunas `ID_cliente`, `ID_vendedor` e `ID_produto`, pois devem conter valores únicos.
- **Tabelas de pedidos e produtos**:
  - Converti valores monetários que estavam com separação estrangeira (ex.: `12.99`) para o padrão brasileiro (ex.: `12,99`).
- **Tabelas de informações de pedidos (datas/horas)**:
  - Encontrei colunas de “data de envio” contendo **data + hora** e colunas de “hora de envio” contendo **data**.
  - Removi a **hora** das colunas cujo objetivo é armazenar apenas datas.
  - Removi a **data** das colunas cujo objetivo principal é armazenar apenas horas.
  - Objetivo: padronizar valores e reduzir bugs/problemas em análises futuras.

### 6) Carga TRUSTED no Supabase e integração na Dadosfera
6. Após o tratamento:
- Salvei todos os dados em `.csv`.
- Enviei novamente ao Supabase.
- Refiz a **conexão** e a **pipeline** na Dadosfera para os dados tratados (trusted).

### 7) Data Quality (Soda)
7. Executei a etapa de **Data Quality** em 4 datasets como amostra utilizando a biblioteca **Soda**, com foco em verificar qualidade geral e encontrar possíveis inconsistências.

#### Padrão Inicial de Data Quality

Este documento descreve o padrão inicial de verificações de qualidade de dados aplicado às tabelas do projeto.  
O objetivo é garantir consistência, confiabilidade e transparência no uso dos dados.

##### 🎯 Objetivos do Data Quality
O conjunto de verificações foi pensado para:
- Detectar problemas estruturais cedo
- Evitar análises baseadas em dados incorretos
- Documentar regras de negócio essenciais
- Padronizar critérios entre tabelas

Categorias principais de validação:
- Completude
- Unicidade
- Consistência temporal
- Limites e faixas válidas
- Conformidade com regras de negócio

##### 🧩 Tabelas monitoradas

| Tabela       | Descrição                                       |
|-------------|---------------------------------------------------|
| pedidos     | Informações dos pedidos e status                  |
| itens_pedido| Detalhamento dos itens vinculados aos pedidos     |
| avaliacao   | Avaliações dos clientes                           |
| vendedores  | Informações de vendedores                         |

##### ✅ Checks aplicados

**1️⃣ Completude**  
Garantimos que colunas críticas não apresentem níveis elevados de ausência:

- `missing_percent(coluna) < 50`

Acima disso, um alerta é gerado indicando possível problema de ingestão ou de origem.

**2️⃣ Unicidade de identificadores**  
Cada entidade precisa ser única dentro da sua tabela:

- `duplicate_count(order_id) = 0`
- `duplicate_count(review_id) = 0`
- `duplicate_count(seller_id) = 0`
- `duplicate_count(order_id, order_item_id) = 0`

Isso evita:
- Linhas duplicadas
- Contagens distorcidas
- Inconsistências em joins

**3️⃣ Regras de negócio**

Status de pedidos:
- `values in order_status must be in: [delivered, shipped, canceled, approved, invoiced, processing, unavailable, created]`

Avaliações:
- `review_score between 1 and 5`
- `max_length(review_comment_message) < 2000`

**4️⃣ Coerência temporal**  
Garantimos que eventos respeitam a ordem lógica:

- `order_purchase_timestamp <= order_approved_at`
- `order_approved_at <= order_delivered_customer_date`

Se quebrar, é sinal de erro de origem ou transformação.

**5️⃣ Valores numéricos**  
Valores financeiros não podem ser negativos:

- `min(price) >= 0`
- `min(freight_value) >= 0`

**6️⃣ Colunas técnicas**  
A coluna `Unnamed: 0` é reconhecida como índice técnico e não usada nas análises:

- `missing_percent(unnamed: 0) >= 0  # coluna técnica`

*(Ela poderá ser removida futuramente.)*

##### 🚦 Interpretação dos resultados

| Resultado | Significado |
|----------|-------------|
| ✔️ Passou | Dentro do padrão esperado |
| ⚠️ Alerta | Pode indicar problema pontual |
| ❌ Falhou | Requer investigação imediata |

##### 🔜 Próximos passos (Roadmap)
- Validação de chaves estrangeiras entre tabelas
- Detecção automática de anomalias históricas
- Documentação automática por coluna
- Validação de datas no futuro

##### 🏁 Conclusão
Este padrão inicial estabelece uma base sólida para:
- Monitoramento contínuo
- Rastreabilidade
- Confiança no consumo de dados

Ele será evoluído conforme o projeto cresce e novas necessidades surgem.

### 8) Visualização (Dashboard)
8. Criei um dashboard com os dados mais importantes, organizado nas abas:
- **Clientes**
- **Vendas**
- **Produtos**

### 9) Organização dos gráficos
9. Separei os gráficos que fazem mais sentido em cada aba e que julguei mais importantes para análise de negócio.

---

## Links dos ativos

- Dashboard (Visualização):  
  https://metabase-treinamentos.dadosfera.ai/dashboard/239?tab=28-produtos

- Conexão de dados (Dadosfera):  
  https://app.dadosfera.ai/pt-BR/collect/connections/1767467983664_c3ah3ktd_postgresql-1.0.0

- Pipeline de dados (refined pós processamento):  
  https://app.dadosfera.ai/pt-BR/collect/pipelines/a8fc2e3d-8e19-48f6-84c8-828d6ed1037a
