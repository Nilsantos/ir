import os
import pandas as pd
from src.utils import validate_columns, validate_files
from src.constants import COMPANY_CNPJ_COLUMN, FUND_CNPJ_COLUMN, PRODUCT_COLUMN, PRODUCT_TYPE_COLUMN, QUANTITY_COLUMN, TICKER_COLUMN

FOLDER_PATH = './input/consolidado/'
FILE_EXTENSION='.xlsx'

STOCKS_SHEET='Posição - Ações'
BDR_SHEET='Posição - BDR'
FUNDS_SHEET='Posição - Fundos'

STOCKS_REQUIRED_COLUMNS = [PRODUCT_COLUMN, TICKER_COLUMN, QUANTITY_COLUMN, COMPANY_CNPJ_COLUMN]
FUNDS_REQUIRED_COLUMNS = [TICKER_COLUMN, QUANTITY_COLUMN, FUND_CNPJ_COLUMN]
BDR_REQUIRED_COLUMNS = [TICKER_COLUMN, QUANTITY_COLUMN]

def import_resume():
    validate_files(FOLDER_PATH, FILE_EXTENSION, "O arquivo consolidado não foi encontrado no caminho")
    
    file_list = [f for f in os.listdir(FOLDER_PATH) if f.endswith(FILE_EXTENSION)]
    file_path = os.path.join(FOLDER_PATH, file_list[0])
    resume = pd.read_excel(
        file_path, 
        dtype={COMPANY_CNPJ_COLUMN: str, FUND_CNPJ_COLUMN: str },
        sheet_name=[STOCKS_SHEET, BDR_SHEET, FUNDS_SHEET], 
    )

    validate_columns(resume[STOCKS_SHEET], STOCKS_REQUIRED_COLUMNS)
    validate_columns(resume[FUNDS_SHEET], FUNDS_REQUIRED_COLUMNS)
    validate_columns(resume[BDR_SHEET], BDR_REQUIRED_COLUMNS)


    # Remove n/a rows
    resume[STOCKS_SHEET] =  resume[STOCKS_SHEET][resume[STOCKS_SHEET][TICKER_COLUMN].notna()]
    resume[BDR_SHEET] = resume[BDR_SHEET][resume[BDR_SHEET][TICKER_COLUMN].notna()]
    resume[FUNDS_SHEET] = resume[FUNDS_SHEET][resume[FUNDS_SHEET][TICKER_COLUMN].notna()]
    
    # Normalize CPNJ Column
    resume[FUNDS_SHEET][COMPANY_CNPJ_COLUMN] = resume[FUNDS_SHEET][FUND_CNPJ_COLUMN]
    resume[BDR_SHEET][COMPANY_CNPJ_COLUMN] = ''
    
    # Fill type column based on sheet
    resume[STOCKS_SHEET][PRODUCT_TYPE_COLUMN] = 'Ação'
    resume[BDR_SHEET][PRODUCT_TYPE_COLUMN] = 'BDR'
    resume[FUNDS_SHEET][PRODUCT_TYPE_COLUMN] = 'Fundo Imobiliário'
    
    # Trim
    resume[STOCKS_SHEET][PRODUCT_COLUMN] = resume[STOCKS_SHEET][PRODUCT_COLUMN].str.strip()
    resume[BDR_SHEET][PRODUCT_COLUMN] = resume[BDR_SHEET][PRODUCT_COLUMN].str.strip()
    resume[FUNDS_SHEET][PRODUCT_COLUMN] = resume[FUNDS_SHEET][PRODUCT_COLUMN].str.strip()
    
    # Merge Sheets
    resume = pd.concat([resume[STOCKS_SHEET], resume[BDR_SHEET], resume[FUNDS_SHEET]], ignore_index=True) 
    
    return resume