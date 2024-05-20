from src.utils import find_ticker
from src.constants import COMPANY_CNPJ_COLUMN, EVENT_TYPE_COLUMN, INTITUTION_COLUMN, PRODUCT_COLUMN, PRODUCT_TYPE_COLUMN, TICKER_COLUMN, TOTAL_PRICE_COLUMN

class EarningsConsolidator:
    movements = None        # Dataframe to store movements
    consolidated = None     # Consolidated earnings dataframe
    
    def __init__(self, movements):
        self.movements = movements
        
    def complement_data(self, resume):
        ticker_list = resume[TICKER_COLUMN].unique()
        resume = resume[[COMPANY_CNPJ_COLUMN, PRODUCT_TYPE_COLUMN, TICKER_COLUMN]]
        self.movements[TICKER_COLUMN] = self.movements[PRODUCT_COLUMN].apply(lambda x: find_ticker(x, ticker_list))
        self.movements = self.movements.merge(resume, on=TICKER_COLUMN, how="left")
        
    def filter_data(self):
        IN = ['Juros Sobre Capital Próprio', 'Rendimento', 'Dividendo']
        self.movements = self.movements[self.movements[EVENT_TYPE_COLUMN].isin(IN)]
    
    def consolidate(self):
        self.consolidated = self.movements.groupby([TICKER_COLUMN, EVENT_TYPE_COLUMN]).agg({ 
            TOTAL_PRICE_COLUMN: 'sum',
            PRODUCT_TYPE_COLUMN: 'first',
            COMPANY_CNPJ_COLUMN: 'first',
            INTITUTION_COLUMN: 'first'
        }).reset_index()
    
    def get_consolidated_interest_on_equity(self):
        return self.consolidated[self.consolidated[EVENT_TYPE_COLUMN] == 'Juros Sobre Capital Próprio']
    
    def get_consolidated_stocks_dividends(self):
        return self.consolidated[self.consolidated[EVENT_TYPE_COLUMN] == 'Dividendo']
    
    def get_consolidated_funds_dividends(self):
        return self.consolidated[self.consolidated[EVENT_TYPE_COLUMN] == 'Rendimento']
