import os
from src.constants import MOVEMENT_TYPE_COLUMN, QUANTITY_COLUMN, TOTAL_PRICE_COLUMN

def validate_columns(df, columns):
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise SystemExit(f"As seguintes colunas são obrigatórias: {missing_columns}")
    
def validate_files(path, extention, error_message):
    if os.path.exists(path) == False:
        raise SystemExit(f"{error_message}: {path}")
    
    file_list = [f for f in os.listdir(path) if f.endswith(extention)]
    
    if len(file_list) == 0:
        raise SystemExit(f"{error_message}: {path}")
    
def find_ticker(produto, tickers):
    for ticker in tickers:
        if ticker in produto:
            return ticker
    return None

def normalize_quantity(row):
    if row[MOVEMENT_TYPE_COLUMN] == 'Debito':
        return row[QUANTITY_COLUMN] * -1
    
    return row[QUANTITY_COLUMN]

def normalize_price(row):
    if row[MOVEMENT_TYPE_COLUMN] == 'Debito':
        return 0
    
    return row[TOTAL_PRICE_COLUMN]