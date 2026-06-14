# -*- coding: utf-8 -*-
import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    A canvas that enables dynamic two-pass page numbering: 'Page X of Y'
    and adds a professional running header and footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        
        # Don't draw headers/footers on the cover page (Page 1)
        if self._pageNumber == 1:
            self.restoreState()
            return

        # Colors
        primary_color = colors.HexColor('#1B365D') # Navy
        text_gray = colors.HexColor('#718096')
        line_gray = colors.HexColor('#E2E8F0')

        # Running Header
        self.setFont("MSJH", 8)
        self.setFillColor(text_gray)
        ticker = getattr(NumberedCanvas, 'ticker', '2330.TW')
        self.drawString(54, 800, f"金融投資團隊 AI 聯席會議報告 | {ticker} 深度分析")
        
        # Header Line
        self.setStrokeColor(line_gray)
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792) # 54 to 541 (A4 width 595 - 54)

        # Running Footer
        self.line(54, 55, 541, 55)
        self.setFont("MSJH", 8)
        self.drawString(54, 42, "機密性：內部投資決策參考，禁止外流")
        
        # Page Number Right Aligned
        page_str = f"頁碼 {self._pageNumber} / {page_count}"
        self.drawRightString(541, 42, page_str)
        
        self.restoreState()


def build_pdf(filename, data):
    """
    Builds the final PDF report.
    data is a dictionary containing:
        - ticker (str)
        - company_name (str)
        - date (str)
        - chart_path (str)
        - short_term_strategy (str)
        - med_term_strategy (str)
        - long_term_strategy (str)
        - short_term_trigger (str)
        - med_term_trigger (str)
        - long_term_trigger (str)
        - executive_rating (str)
        - executive_rating_color (str)
        - ar_intro (str)
        - ar_bullets (list of str)
        - final_approval_conclusion (str)
        - cfo_intro (str)
        - cfo_table_source (str)
        - fin_table_data (list of list of str)
        - tech_table_data (list of list of str)
        - risk_intro (str)
        - risk_dashboard (dict with 'systemic' and 'nonsystemic' lists)
        - risk_conclusion_and_hedging (str)
        - cfo_report (str)
        - ar_report (str)
        - ir_report (str)
        - reflection_log (list of dicts with 'round', 'critique', 'revision')
        - references (list of dicts with 'category' and 'items')
    """
    # Set static properties on canvas class for header
    NumberedCanvas.ticker = data.get('ticker', '2330.TW')
    NumberedCanvas.company_name = data.get('company_name', 'TSMC')

    # Register Chinese font
    font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msjh.ttc')
    font_name = 'Helvetica'
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('MSJH', font_path))
            font_name = 'MSJH'
        except Exception as e:
            print(f"Error registering MSJH: {e}")
            
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    f_normal = font_name
    f_bold = font_name

    # Modify existing styles to avoid collisions
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName=f_bold,
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#1B365D'),
        alignment=1, # Centered
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName=f_normal,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=30
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontName=f_bold,
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1B365D'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Heading2'],
        fontName=f_bold,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2C5282'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName=f_normal,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName=f_normal,
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName=f_bold,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1B365D')
    )

    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName=f_normal,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("金融投資 AI 專家團隊", subtitle_style))
    story.append(Paragraph(f"{data['company_name']} ({data['ticker']}) 深度投資評估報告", title_style))
    story.append(Paragraph("基於 Prompt Engineering 聯席決策與審核省思機制", subtitle_style))
    story.append(Spacer(1, 20))

    # Metadata Table
    rating_color = data.get('executive_rating_color', '#2F855A')
    rating_text = data.get('executive_rating', '強力買進 (Strong Buy)')
    meta_data = [
        [Paragraph("評估標的", meta_label_style), Paragraph(f"{data['company_name']} ({data['ticker']})", meta_val_style),
         Paragraph("評估日期", meta_label_style), Paragraph(data['date'], meta_val_style)],
        [Paragraph("決策單位", meta_label_style), Paragraph("金融分析專家聯絡會 (FAG)", meta_val_style),
         Paragraph("團隊成員", meta_label_style), Paragraph("AR, IR, CFO, FAG", meta_val_style)],
        [Paragraph("最高決策者", meta_label_style), Paragraph("Financial Analyst Agent (FAG)", meta_val_style),
         Paragraph("評等結論", meta_label_style), Paragraph(f"<b>{rating_text}</b>", ParagraphStyle('BuyRating', parent=meta_val_style, textColor=colors.HexColor(rating_color), fontName=f_bold))]
    ]
    meta_table = Table(meta_data, colWidths=[80, 160, 80, 167])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 30))

    # Executive Summary Strategy Panel
    summary_header_style = ParagraphStyle(
        'SummaryHeader',
        parent=styles['Normal'],
        fontName=f_bold,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1B365D'),
        spaceAfter=8
    )
    
    strategy_table_data = [
        [Paragraph("投資週期", meta_label_style), Paragraph("核心策略建議", meta_label_style), Paragraph("關鍵觸發與止損條件", meta_label_style)],
        [
            Paragraph("短期 (Day & Week)", meta_label_style),
            Paragraph(data['short_term_strategy'], body_style),
            Paragraph(data.get('short_term_trigger', ''), body_style)
        ],
        [
            Paragraph("中期 (1-3 Months)", meta_label_style),
            Paragraph(data['med_term_strategy'], body_style),
            Paragraph(data.get('med_term_trigger', ''), body_style)
        ],
        [
            Paragraph("晚期 / 長期 (Over 3 M.)", meta_label_style),
            Paragraph(data['long_term_strategy'], body_style),
            Paragraph(data.get('long_term_trigger', ''), body_style)
        ]
    ]
    
    strategy_table = Table(strategy_table_data, colWidths=[110, 240, 137])
    strategy_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
    ]))
    
    story.append(Paragraph("■ 核心決策：投資週期策略配置", summary_header_style))
    story.append(strategy_table)
    
    story.append(PageBreak())

    # ================= PAGE 2: VISUALIZED CHART & TECHNICAL DATA =================
    story.append(Paragraph("一、 技術走勢與法人籌碼圖表化 (AR 報告圖表)", h1_style))
    ar_intro = data.get('ar_intro', f"本章節展示 {data['company_name']} ({data['ticker']}) 近期的日K線走勢及法人籌碼變化。數據由 Analytics Reporter (AR) 進行技術指標與籌碼交叉分析後得出。")
    story.append(Paragraph(ar_intro, body_style))
    story.append(Spacer(1, 10))
    
    # Embed Matplotlib chart
    if os.path.exists(data['chart_path']):
        story.append(Image(data['chart_path'], width=6.5*inch, height=4.5*inch))
        story.append(Paragraph(f"圖 1.1：{data['company_name']} ({data['ticker']}) 股價走勢與交易量圖表 (數據來源：Yahoo Finance)", ParagraphStyle('FigCaption', parent=body_style, fontName=f_normal, fontSize=8, alignment=1, textColor=colors.HexColor('#718096'))))
    else:
        story.append(Paragraph("[圖表加載失敗：找不到圖表路徑]", ParagraphStyle('ErrorStyle', parent=body_style, textColor=colors.red)))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph("AR 籌碼與技術面核心摘要：", h2_style))
    for bullet in data.get('ar_bullets', []):
        story.append(Paragraph(bullet, bullet_style))

    story.append(PageBreak())

    # ================= PAGE 3: FAG STRATEGY & REFLECTION LOG =================
    story.append(Paragraph("二、 最高決策審核與省思機制紀錄 (FAG & Re-evaluation Log)", h1_style))
    story.append(Paragraph("根據團隊的決策憲章，最高決策者 <b>Financial Analyst Agent (FAG)</b> 具備獨立審查與否決權利。當 FAG 否決其餘成員 (AR, IR, CFO) 的初始策略或報告時，會明確指出論證漏洞並限期修正。以下為本次分析的「提案 - 否決省思 - 修正再議」完整歷程，確保數據真實無造假、邏輯無盲區。", body_style))
    story.append(Spacer(1, 10))

    # Re-evaluation log loop
    for i, log in enumerate(data['reflection_log']):
        round_title = f"◎ 省思審查回合：第 {log['round']} 輪交互審查"
        story.append(Paragraph(round_title, h2_style))
        
        # Critique Box (Light red background)
        critique_data = [[
            Paragraph("<b>FAG 否決與質詢意見 (FAG Critique)：</b>", ParagraphStyle('C1', parent=body_style, fontName=f_bold, textColor=colors.HexColor('#9B2C2C'))),
        ], [
            Paragraph(log['critique'], body_style)
        ]]
        critique_table = Table(critique_data, colWidths=[487])
        critique_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF5F5')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FEB2B2')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(critique_table)
        story.append(Spacer(1, 8))
        
        # Revision Box (Light green background)
        revision_data = [[
            Paragraph("<b>各部門 (AR, IR, CFO) 聯合答覆與修正說明 (Revisions & Evidence)：</b>", ParagraphStyle('R1', parent=body_style, fontName=f_bold, textColor=colors.HexColor('#22543D'))),
        ], [
            Paragraph(log['revision'], body_style)
        ]]
        revision_table = Table(revision_data, colWidths=[487])
        revision_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FFF4')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#9AE6B4')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(revision_table)
        story.append(Spacer(1, 15))

    story.append(Paragraph(f"<b>最終核准結論：</b> {data.get('final_approval_conclusion', '')}", body_style))
    story.append(PageBreak())

    # ================= PAGE 4: CFO FUNDAMENTAL REPORT =================
    story.append(Paragraph("三、 財務長基本面與資本配置審查報告 (CFO Report)", h1_style))
    cfo_intro = data.get('cfo_intro', f"本章節由財務長 (CFO) 提交，聚焦於 {data['company_name']} 的資產負債表實力、現金流流動性、資本支出分配效率及財務結構。CFO 秉持憲章中「現金流高於營收，嚴防樂觀預測」的審慎態度進行評估。")
    story.append(Paragraph(cfo_intro, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(data['cfo_report'], body_style))
    
    # Financial indicators table
    fin_table_raw = data.get('fin_table_data', [])
    fin_table_rows = []
    for r_idx, row in enumerate(fin_table_raw):
        row_cells = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                row_cells.append(Paragraph(cell, meta_label_style))
            else:
                row_cells.append(Paragraph(cell, body_style))
        fin_table_rows.append(row_cells)
        
    fin_table = Table(fin_table_rows, colWidths=[160, 105, 105, 117])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>表 3.1：{data['company_name']}財務基本數據與預估 (資料來源：{data.get('cfo_table_source', '')}，CFO 整理)</b>", ParagraphStyle('TableTitle', parent=body_style, fontName=f_normal, fontSize=8, textColor=colors.HexColor('#718096'))))
    story.append(fin_table)

    # Historical 3-year table
    hist_table_raw = data.get('hist_table_data', [])
    if hist_table_raw:
        hist_table_rows = []
        for r_idx, row in enumerate(hist_table_raw):
            row_cells = []
            for c_idx, cell in enumerate(row):
                if r_idx == 0:
                    row_cells.append(Paragraph(cell, meta_label_style))
                else:
                    row_cells.append(Paragraph(cell, body_style))
            hist_table_rows.append(row_cells)
            
        hist_table = Table(hist_table_rows, colWidths=[160, 105, 105, 117])
        hist_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(Spacer(1, 15))
        story.append(Paragraph(f"<b>表 3.2：{data['company_name']}過去三年歷史財務指標與股利分派 (CFO 整理)</b>", ParagraphStyle('TableTitle3', parent=body_style, fontName=f_normal, fontSize=8, textColor=colors.HexColor('#718096'))))
        story.append(hist_table)

    story.append(PageBreak())

    # ================= PAGE 5: AR TECHNICAL & CHIPS REPORT =================
    story.append(Paragraph("四、 數據分析與市場籌碼交叉監測報告 (AR Report)", h1_style))
    story.append(Paragraph("本章節由數據分析專家 (Analytics Reporter) 撰寫，利用量化統計方法，將技術面價格指標與三大法人籌碼的資金流向進行交叉比對，以確定短中期的進出場防守價位。", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(data['ar_report'], body_style))
    
    # Technical resistance levels table
    tech_table_raw = data.get('tech_table_data', [])
    tech_table_rows = []
    for r_idx, row in enumerate(tech_table_raw):
        row_cells = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                row_cells.append(Paragraph(cell, meta_label_style))
            else:
                row_cells.append(Paragraph(cell, body_style))
        tech_table_rows.append(row_cells)
        
    tech_table = Table(tech_table_rows, colWidths=[100, 70, 180, 137])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>表 4.1：{data['company_name']}關鍵技術與籌碼支撐壓力表 (AR 整理)</b>", ParagraphStyle('TableTitle2', parent=body_style, fontName=f_normal, fontSize=8, textColor=colors.HexColor('#718096'))))
    story.append(tech_table)

    story.append(PageBreak())

    # ================= PAGE 6: RISK ASSESSMENT DASHBOARD =================
    story.append(Paragraph("五、 系統性與非系統性風險監測儀表板 (Risk Assessment Dashboard)", h1_style))
    risk_intro = data.get('risk_intro', f"本章節展示針對 {data['company_name']} ({data['ticker']}) 的雙重風險評估儀表板。<b>系統性風險</b>著重於總體經濟、匯率、利率及地緣政治等無法透過分散投資消除的市場因素；<b>非系統性風險</b>則聚焦於公司特有之客戶集中度、良率研發、研發開支以及發射產能限制等營運因子。指標已進行量化評級。")
    story.append(Paragraph(risk_intro, body_style))
    story.append(Spacer(1, 10))

    # Helper function to generate risk badges inside pdf_generator
    def make_badge(text, level, f_bold, base_style):
        # HIGH = Red, MED = Orange, LOW = Green
        bg_color = '#FED2D2' if level == 'HIGH' else ('#FEEBC8' if level == 'MED' else '#C6F6D5')
        text_color = '#9B2C2C' if level == 'HIGH' else ('#9C4221' if level == 'MED' else '#22543D')
        style = ParagraphStyle(
            'Badge',
            parent=base_style,
            fontName=f_bold,
            fontSize=8,
            leading=10,
            textColor=colors.HexColor(text_color),
            alignment=1
        )
        p = Paragraph(f"<b>{text}</b>", style)
        t = Table([[p]], colWidths=[48])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(text_color)),
        ]))
        return t

    dash_header_style = ParagraphStyle(
        'DashHeader',
        parent=styles['Normal'],
        fontName=f_bold,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1B365D')
    )
    
    dash_cell_style = ParagraphStyle(
        'DashCell',
        parent=body_style,
        fontSize=9,
        leading=13
    )

    risk_db = data['risk_dashboard']
    sys_risks = risk_db['systemic']
    nonsys_risks = risk_db['nonsystemic']
    
    dash_table_data = [
        [
            Paragraph("<b>系統性風險監測面板</b>", dash_header_style), "", "",
            Paragraph("<b>非系統性風險監測面板</b>", dash_header_style), "", ""
        ],
        [
            Paragraph("指標項目", meta_label_style), Paragraph("當前數值 / 狀態", meta_label_style), Paragraph("評級", meta_label_style),
            Paragraph("指標項目", meta_label_style), Paragraph("當前數值 / 狀態", meta_label_style), Paragraph("評級", meta_label_style)
        ]
    ]

    for i in range(4):
        sys_item = sys_risks[i]
        nonsys_item = nonsys_risks[i]
        
        row = [
            Paragraph(sys_item['name'], dash_cell_style),
            Paragraph(sys_item['val'], dash_cell_style),
            make_badge(sys_item['level_text'], sys_item['level'], f_bold, styles['Normal']),
            
            Paragraph(nonsys_item['name'], dash_cell_style),
            Paragraph(nonsys_item['val'], dash_cell_style),
            make_badge(nonsys_item['level_text'], nonsys_item['level'], f_bold, styles['Normal'])
        ]
        dash_table_data.append(row)

    dash_table = Table(dash_table_data, colWidths=[95, 90, 55, 100, 92, 55])
    dash_table.setStyle(TableStyle([
        # Spanning headers
        ('SPAN', (0,0), (2,0)),
        ('SPAN', (3,0), (5,0)),
        
        # Grid and borders
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        
        # Backgrounds
        ('BACKGROUND', (0,0), (2,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (3,0), (5,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#EDF2F7')),
        
        # Alignments
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,2), (2,-1), 'CENTER'),
        ('ALIGN', (5,2), (5,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        
        # Padding adjustments
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        
        # Zero margin for badges to fit
        ('LEFTPADDING', (2,2), (2,-1), 2),
        ('RIGHTPADDING', (2,2), (2,-1), 2),
        ('LEFTPADDING', (5,2), (5,-1), 2),
        ('RIGHTPADDING', (5,2), (5,-1), 2),
    ]))

    story.append(dash_table)
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"<b>評估結論與避險建議：</b><br/>{data['risk_conclusion_and_hedging']}", body_style))

    story.append(PageBreak())

    # ================= PAGE 7: IR INVESTED RESEARCHER REPORT & SOURCES =================
    story.append(Paragraph("六、 競爭力護城河與產業消息面分析報告 (IR Report)", h1_style))
    story.append(Paragraph(f"本章節由投資研究員 (Investment Researcher) 提交，著重於 {data['company_name']} 的產業競爭壁壘、關鍵技術領先優勢、市場 TAM (總可尋址市場) 以及消息面催化劑的驗證。", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(data['ir_report'], body_style))
    story.append(Spacer(1, 15))

    # Sources and Citations Section
    story.append(Paragraph("七、 參考資料來源與引用說明 (References & Citations)", h1_style))
    story.append(Paragraph("本報告中所有數據與事實均來自公開可查證之管道，無虛假造假內容，主要參考依據如下：", body_style))
    
    ref_idx = 1
    for cat in data.get('references', []):
        story.append(Paragraph(f"{ref_idx}. <b>{cat['category']}</b>：", ParagraphStyle('RefCat', parent=body_style, fontName=f_bold, spaceBefore=4, spaceAfter=2)))
        for item in cat['items']:
            story.append(Paragraph(f"• {item}", bullet_style))
        ref_idx += 1

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")
