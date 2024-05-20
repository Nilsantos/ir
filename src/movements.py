import os
import pandas as pd
from src.utils import validate_columns, validate_files
from src.constants import (
    DATE_COLUMN,
    EVENT_TYPE_COLUMN,
    INTITUTION_COLUMN,
    MOVEMENT_TYPE_COLUMN,
    PRICE_COLUMN,
    PRODUCT_COLUMN,
    QUANTITY_COLUMN,
    TOTAL_PRICE_COLUMN
)

FOLDER_PATH = './input/movimentações/'
FILE_EXTENSION='.xlsx'
REQUIRED_COLUMNS = [
    MOVEMENT_TYPE_COLUMN,
    DATE_COLUMN,
    EVENT_TYPE_COLUMN,
    PRODUCT_COLUMN,
    INTITUTION_COLUMN,
    QUANTITY_COLUMN,
    PRICE_COLUMN,
    TOTAL_PRICE_COLUMN,
]

def import_movements():
    validate_files(FOLDER_PATH, FILE_EXTENSION, "Os arquivos de movimentações não foram encontrados no caminho")
        
    file_list = [f for f in os.listdir(FOLDER_PATH) if f.endswith(FILE_EXTENSION)]
    dataframes = []

    for file in file_list:
        file_path = os.path.join(FOLDER_PATH, file)
        df = pd.read_excel(file_path)
        validate_columns(df, REQUIRED_COLUMNS)
        dataframes.append(df)

    movements = pd.concat(dataframes, ignore_index=True)
    movements[DATE_COLUMN] = pd.to_datetime(movements[DATE_COLUMN], dayfirst=True).dt.date
    movements[PRODUCT_COLUMN] = movements[PRODUCT_COLUMN].str.strip()
    movements = movements.sort_values(by=DATE_COLUMN, ascending=True)
    movements = movements.replace('-', 0)
    # movements.to_excel("./merged.xlsx")
    return movements