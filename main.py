import re
import sys
import warnings
import pandas as pd
from src.pdf_generator import PDFGenerator
from src.earnings_consolidator import EarningsConsolidator
from src.resume import import_resume
from src.movements import import_movements
from src.postion_consolidator import PositionConsolidator

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))

if __name__ == "__main__":
    argument = sys.argv[1]
    
    if argument == 'generate-ir-report':
        movements = import_movements()
        resume = import_resume()
        
        position_consolidator = PositionConsolidator(movements)
        position_consolidator.complement_data(resume)
        position_consolidator.filter_data()
        position_consolidator.consolidate()
        
        earnings_consolidator = EarningsConsolidator(movements)
        earnings_consolidator.complement_data(resume)
        earnings_consolidator.filter_data()
        earnings_consolidator.consolidate()
        
        pdf_generator = PDFGenerator(position_consolidator, earnings_consolidator, 'output/Relatório IR.pdf', 'IR 2024')
        pdf_generator.generate()
    