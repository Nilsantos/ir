import locale
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from src.constants import (
    ADJUSTED_QUANTITY_COLUMN,
    ADJUSTED_TOTAL_PRICE_COLUMN,
    AVG_PRICE_COLUMN,
    PRODUCT_TYPE_COLUMN,
    TICKER_COLUMN,
    COMPANY_CNPJ_COLUMN,
    INTITUTION_COLUMN,
    TOTAL_PRICE_COLUMN,
)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class PDFGenerator:
    doc = None
    content = []
    position_consolidator = None
    earnings_consolidator = None
    
    def __init__(self, position_consolidator, earnings_consolidator, file_name, title):
        self.position_consolidator = position_consolidator
        self.earnings_consolidator = earnings_consolidator
        self.doc = SimpleDocTemplate(file_name, title=title, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
        self.content = []
     
    def parse_goods_data(self, dataset):
        data = [["Código", "CNPJ", "Quantidade", "Preço Médio", "Custo Total", "Discriminação"]]
        templates = {
            'Ação': "{} Ações de {}\nPreço médio de {}\nCusto total de {}\nNa corretora {}\n",
            'Fundo Imobiliário': "{} Cotas do fundo imobiliário {}\nPreço médio de {}\nCusto total de {}\nNa corretora {}\n",
            "BDR": "{} BDR's de {}\nPreço médio de {}\nCusto total de {}\nNa corretora {}\n"
        }
        
        for _, row in dataset.iterrows():
            data.append([
                row[TICKER_COLUMN], 
                row[COMPANY_CNPJ_COLUMN],
                locale.currency(row[ADJUSTED_QUANTITY_COLUMN], symbol=False),
                locale.currency(row[AVG_PRICE_COLUMN], grouping=True, symbol=True),
                locale.currency(row[ADJUSTED_TOTAL_PRICE_COLUMN], grouping=True, symbol=True),
                templates[row[PRODUCT_TYPE_COLUMN]].format(
                    locale.currency(row[ADJUSTED_QUANTITY_COLUMN], symbol=False), 
                    row[TICKER_COLUMN],
                    locale.currency(row[AVG_PRICE_COLUMN], grouping=True, symbol=True),
                    locale.currency(row[ADJUSTED_TOTAL_PRICE_COLUMN], grouping=True, symbol=True),
                    row[INTITUTION_COLUMN]
                )
            ])
            
        return data
    
    def parse_earnings_data(self, earnings_data):
        data = [["Código", "CNPJ", "Valor"]]
        
        for _, row in earnings_data.iterrows():
            data.append([
                row[TICKER_COLUMN], 
                row[COMPANY_CNPJ_COLUMN],
                locale.currency(row[TOTAL_PRICE_COLUMN], grouping=True, symbol=True),
            ])
            
        return data
    
    def generate(self):
        #------------------------------------------------------STYLES------------------------------------------------------
        
        # Add custom font
        pdfmetrics.registerFont(TTFont('Montserrat', './assets/fonts/Montserrat-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Montserrat-Bold', './assets/fonts/Montserrat-Bold.ttf'))
        
        # Create title styles
        styles = getSampleStyleSheet()
        title_styles = ParagraphStyle("Titulo", parent=styles["Title"])
        title_styles.alignment = 0
        title_styles.fontSize = 36
        title_styles.textColor = colors.HexColor('#00008B')
        
        # Create subtitle styles
        subtitle_style = ParagraphStyle("Subtitulo", parent=styles["Normal"])
        title_styles.alignment = 0
        title_styles.fontSize = 12
        subtitle_style.textColor = colors.HexColor('#00008B')
        
        # Creat table styles
        table_styles = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Montserrat-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        
        #------------------------------------------------------STOCKS------------------------------------------------------
        
        self.content.append(Paragraph("<b>Bens e Direitos</b>", title_styles))

        self.content.append(Paragraph("Grupo 04 - Aplicações e Investimentos", subtitle_style))
        self.content.append(Paragraph("Código: 01 – Ações (inclusive as listadas em bolsa)", subtitle_style))

        for _ in range(3):
            self.content.append(Paragraph("<br/>", title_styles))

        data = self.parse_goods_data(self.position_consolidator.get_consolidated_stocks())
        table = Table(data, colWidths=[50, 90, "*", "*", "*", 220], repeatRows=1)
        table.setStyle(table_styles)
        self.content.append(table)
        
        #------------------------------------------------------FUNDS------------------------------------------------------
        
        self.content.append(PageBreak())
        
        self.content.append(Paragraph("<b>Bens e Direitos</b>", title_styles))
        
        self.content.append(Paragraph("<p>Grupo: 07 – Fundos</p>", subtitle_style))
        self.content.append(Paragraph("<p>Código:  03 – Fundos de Investimento Imobiliário (FII)</p>", subtitle_style))

        for _ in range(3):
            self.content.append(Paragraph("<br/>", title_styles))

        data = self.parse_goods_data(self.position_consolidator.get_consolidated_funds())
        table = Table(data, colWidths=[50, 90, "*", "*", "*", 220], repeatRows=1)
        table.setStyle(table_styles)
        self.content.append(table)
        
        #------------------------------------------------------BDR------------------------------------------------------

        self.content.append(PageBreak())
        
        self.content.append(Paragraph("<b>Bens e Direitos</b>", title_styles))
        
        self.content.append(Paragraph("Grupo: 04 – Aplicações e investimentos", subtitle_style))
        self.content.append(Paragraph("Código: 04 – Ativos negociados em bolsa no Brasil (BDRs, opções e outros – exceto ações e fundos)", subtitle_style))

        for _ in range(3):
            self.content.append(Paragraph("<br/>", title_styles))
        
        data = self.parse_goods_data(self.position_consolidator.get_consolidated_bdrs())
        table = Table(data, colWidths=[50, 90, "*", "*", "*", 220], repeatRows=1)
        table.setStyle(table_styles)
        self.content.append(table)
        
        #------------------------------------------------------Dividends------------------------------------------------------

        self.content.append(PageBreak())
        
        self.content.append(Paragraph("<b>Rendimentos Isentos e Não Tributáveis</b>", title_styles))
        self.content.append(Paragraph("Código 09 - Lucros e dividendos recebidos", subtitle_style))

        for _ in range(3):
            self.content.append(Paragraph("<br/>", title_styles))
        
        data = self.parse_earnings_data(self.earnings_consolidator.get_consolidated_stocks_dividends())
        table = Table(data, colWidths=["*", "*", "*"], repeatRows=1)
        table.setStyle(table_styles)
        self.content.append(table)
        
        #------------------------------------------------------Interest On Equity------------------------------------------------------

        self.content.append(PageBreak())
        
        self.content.append(Paragraph("<b>Rendimentos Sujeitos à Tributação Exclusiva/Definitiva</b>", title_styles))
        self.content.append(Paragraph("Código 10 - Juros sobre capital próprio", subtitle_style))

        for _ in range(3):
            self.content.append(Paragraph("<br/>", title_styles))
        
        data = self.parse_earnings_data(self.earnings_consolidator.get_consolidated_interest_on_equity())
        table = Table(data, colWidths=["*", "*", "*"], repeatRows=1)
        table.setStyle(table_styles)
        self.content.append(table)
        
        #------------------------------------------------------Dividends Funds------------------------------------------------------
        
        self.content.append(PageBreak())
        
        self.content.append(Paragraph("<b>Rendimentos Isentos e Não Tributáveis</b>", title_styles))
        self.content.append(Paragraph("Código 99 - Outros", subtitle_style))

        for _ in range(3):
            self.content.append(Paragraph("<br/>", title_styles))
        
        data = self.parse_earnings_data(self.earnings_consolidator.get_consolidated_funds_dividends())
        table = Table(data, colWidths=["*", "*", "*"], repeatRows=1)
        table.setStyle(table_styles)
        self.content.append(table)
        
        self.doc.build(self.content)
