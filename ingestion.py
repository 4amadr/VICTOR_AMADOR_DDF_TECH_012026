import pandas as pd
from sqlalchemy import create_engine
import os

#Configuração de Conexão
DATABASE_URL = "postgresql://postgres:Vctramad0.r$@zkewqbodirsarubpwpsg:5432/postgres"

engine = create_engine(DATABASE_URL)

#Lista de arquivos do Olist
files = {
    'olist_orders_dataset.csv': 'orders',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_products_dataset.csv': 'products',
    'olist_sellers_dataset.csv': 'sellers',
    'olist_customers_dataset.csv': 'customers',
    'olist_geolocation_dataset.csv': 'geolocation',
    'olist_order_payments_dataset.csv': 'order_payments',
    'olist_order_reviews_dataset.csv': 'order_reviews',
    'olist_order_items_reviews_dataset.csv': 'order_items_reviews',
}

def upload_to_supabase(file_path, table_name):
    print(f"Lendo {file_path}...")
    df = pd.read_csv(f"data/{file_path}")
    
    print(f"Subindo {len(df)} linhas para a tabela '{table_name}'...")
    # 'replace' recria a tabela se ela já existir. 'multi' ajuda na performance.
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)
    print(f"{table_name} finalizada!")

#Execução
for file, table in files.items():
    upload_to_supabase(file, table)

print("Banco inserido com sucesso!")