from src.utils import find_ticker, normalize_price, normalize_quantity
from src.constants import (
    ADJUSTED_QUANTITY_COLUMN,
    ADJUSTED_TOTAL_PRICE_COLUMN,
    AVG_PRICE_COLUMN,
    COMPANY_CNPJ_COLUMN,
    EVENT_TYPE_COLUMN,
    INTITUTION_COLUMN,
    PRODUCT_COLUMN,
    PRODUCT_TYPE_COLUMN,
    TICKER_COLUMN
)

class PositionConsolidator:
    movements = None        # Dataframe to store movements
    consolidated = None     # Consolidated position dataframe
    
    def __init__(self, movements):
        self.movements = movements
        
    def complement_data(self, resume):
        ticker_list = resume[TICKER_COLUMN].unique()
        resume = resume[[COMPANY_CNPJ_COLUMN, PRODUCT_TYPE_COLUMN, TICKER_COLUMN]]
        self.movements[TICKER_COLUMN] = self.movements[PRODUCT_COLUMN].apply(lambda x: find_ticker(x, ticker_list))
        self.movements = self.movements.merge(resume, on=TICKER_COLUMN, how="left")
        
    def filter_data(self):
        not_in = ['Cessão de Direitos - Solicitada', 'Cessão de Direitos', 'Juros Sobre Capital Próprio', 'Rendimento', 'Recibo de Subscrição']
        self.movements = self.movements[~self.movements[EVENT_TYPE_COLUMN].isin(not_in)]
    
    def consolidate(self):
        consolidated = self.movements.copy()
        consolidated[ADJUSTED_QUANTITY_COLUMN] = consolidated.apply(lambda row: normalize_quantity(row), axis=1)
        consolidated[ADJUSTED_TOTAL_PRICE_COLUMN] = consolidated.apply(lambda row: normalize_price(row), axis=1)
        consolidated = consolidated.groupby(TICKER_COLUMN).agg({ 
            ADJUSTED_TOTAL_PRICE_COLUMN: 'sum', 
            ADJUSTED_QUANTITY_COLUMN: 'sum', 
            PRODUCT_TYPE_COLUMN: 'first',
            COMPANY_CNPJ_COLUMN: 'first',
            INTITUTION_COLUMN: 'first'
        }).reset_index()
        consolidated = consolidated[consolidated[ADJUSTED_QUANTITY_COLUMN] != 0]
        consolidated[AVG_PRICE_COLUMN] = consolidated[ADJUSTED_TOTAL_PRICE_COLUMN] / consolidated[ADJUSTED_QUANTITY_COLUMN]
        self.consolidated = consolidated
        
    def get_consolidated_stocks(self):
        return self.consolidated[self.consolidated[PRODUCT_TYPE_COLUMN] == 'Ação']
    
    def get_consolidated_bdrs(self):
        return self.consolidated[self.consolidated[PRODUCT_TYPE_COLUMN] == 'BDR']
    
    def get_consolidated_funds(self):
        return self.consolidated[self.consolidated[PRODUCT_TYPE_COLUMN] == 'Fundo Imobiliário']
