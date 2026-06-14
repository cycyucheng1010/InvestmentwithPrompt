# -*- coding: utf-8 -*-
"""
金融投資團隊 AI 聯席會議與決策系統
僅保留真實數據抓取與 PDF 編譯核心功能，無任何寫死的股票資訊或模擬數據。
"""

import os
import argparse
import datetime
import json
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import the PDF generator
import pdf_generator

def setup_matplotlib_font():
    """
    Configure matplotlib to support Traditional Chinese characters on Windows.
    """
    font_names = ['Microsoft JhengHei', 'SimSun', 'DFKai-SB', 'sans-serif']
    for font_name in font_names:
        try:
            mpl.rcParams['font.family'] = font_name
            # Test if it works
            fig, ax = plt.subplots()
            ax.set_title("測試")
            plt.close()
            break
        except Exception:
            continue

def generate_stock_chart(ticker, output_path):
    """
    Fetches stock data for the given ticker and generates a professional technical chart.
    """
    print(f"[*] 正在獲取 {ticker} 的歷史數據...")
    
    import yfinance as yf
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")
    if df.empty or len(df) <= 20:
        raise ValueError(f"[-] 無法透過 yfinance 獲取 {ticker} 的真實歷史數據，或數據長度不足 20 筆。")
    
    print("[+] 成功透過 yfinance 獲取真實數據。")
        
    # Calculate MAs
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA60'] = df['Close'].rolling(window=60).mean()
    
    # Setup plotting
    setup_matplotlib_font()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})
    
    # Plot price and MAs
    ax1.plot(df.index, df['Close'], label='收盤價 (Close)', color='#1B365D', linewidth=1.8)
    if not df['MA20'].isnull().all():
        ax1.plot(df.index, df['MA20'], label='月線 (MA20)', color='#E67E22', linewidth=1.2, linestyle='--')
    if not df['MA60'].isnull().all():
        ax1.plot(df.index, df['MA60'], label='季線 (MA60)', color='#27AE60', linewidth=1.4, linestyle='-.')
    
    ax1.set_title(f"{ticker} 股價走勢與移動平均線 (6個月歷史數據)", fontsize=14, fontweight='bold', pad=15, color='#1B365D')
    ax1.set_ylabel("價格 (價格為該股交易貨幣)", fontsize=11, fontweight='bold')
    ax1.legend(loc='upper left', frameon=True, facecolor='#F8F9FA')
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    # Plot Volume
    colors_vol = []
    for i in range(len(df)):
        if i == 0:
            colors_vol.append('#27AE60')
        else:
            if df['Close'].iloc[i] >= df['Close'].iloc[i-1]:
                colors_vol.append('#27AE60')
            else:
                colors_vol.append('#C0392B')
                
    ax2.bar(df.index, df['Volume'] / 1000, color=colors_vol, alpha=0.7, width=0.8)
    ax2.set_ylabel("成交量 (千股/千張)", fontsize=11, fontweight='bold')
    ax2.set_xlabel("日期 (Date)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] 技術圖表已生成並保存至: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="金融投資團隊 AI 聯席會議決策與 PDF 生成系統")
    parser.add_argument("--ticker", type=str, required=True, help="目標股票代碼 (例如: 0050.TW)")
    parser.add_argument("--output", type=str, default=None, help="輸出的 PDF 檔名")
    parser.add_argument("--json", type=str, required=True, help="外部 LLM 生成的 JSON 報告檔案路徑")
    
    args = parser.parse_args()
    
    # 建立歸檔目錄結構: FinanceReport / YYYY_MM / [Ticker_Clean]
    current_ym = datetime.date.today().strftime("%Y_%m")
    ticker_clean = args.ticker.replace(".", "_").upper()
    archive_dir = os.path.join("FinanceReport", current_ym, ticker_clean)
    os.makedirs(archive_dir, exist_ok=True)
    
    # 1. Generate stock chart (儲存於歸檔目錄)
    chart_filename = os.path.join(archive_dir, f"{ticker_clean}_chart.png")
    generate_stock_chart(args.ticker, chart_filename)
    
    # 2. Load JSON
    print(f"[*] 偵測到外部 JSON 報告檔: {args.json}，正在載入並補正欄位...")
    with open(args.json, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    # 建立欄位預設值，防範外部 LLM 回傳 JSON 欄位缺失導致崩潰
    defaults = {
        'ticker': args.ticker,
        'company_name': args.ticker,
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'executive_rating': '買進 (Buy)',
        'executive_rating_color': '#2B6CB0',
        'short_term_strategy': '',
        'med_term_strategy': '',
        'long_term_strategy': '',
        'short_term_trigger': '',
        'med_term_trigger': '',
        'long_term_trigger': '',
        'ar_intro': '',
        'ar_report': '',
        'ar_bullets': [],
        'cfo_intro': '',
        'cfo_report': '',
        'cfo_table_source': '官方數據',
        'fin_table_data': [["關鍵財務指標", "2024", "2025", "2026 E"]],
        'hist_table_data': [],  # 過去 3 年歷史財務表格
        'tech_table_data': [["支撐/壓力", "價格", "說明", "策略"]],
        'risk_intro': '',
        'risk_dashboard': {'systemic': [], 'nonsystemic': []},
        'risk_conclusion_and_hedging': '',
        'ir_report': '',
        'final_approval_conclusion': '',
        'reflection_log': [],
        'references': []
    }
    for k, v in defaults.items():
        if k not in report_data:
            report_data[k] = v
            
    # 強制指定正確的 ticker 與走勢圖
    report_data['ticker'] = args.ticker
    report_data['chart_path'] = os.path.abspath(chart_filename)
    
    # 3. Determine output PDF path
    if args.output is None:
        output_pdf = os.path.join(archive_dir, f"{ticker_clean}_deep_analysis.pdf")
    else:
        output_pdf = args.output
        out_dir = os.path.dirname(output_pdf)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            
    # 4. Compile the PDF report
    print(f"[*] 正在將聯席會議報告編譯為 PDF...")
    pdf_generator.build_pdf(output_pdf, report_data)
    print(f"[+] 報告已成功生成並歸檔至：{output_pdf}")
    print(f"[+] 走勢圖表已保存至：{chart_filename}")
    
    # 5. 刪除臨時 JSON 檔案以保持環境乾淨
    if os.path.exists(args.json):
        try:
            os.remove(args.json)
            print(f"[+] 已成功刪除臨時 JSON 檔案：{args.json}")
        except Exception as e:
            print(f"[-] 無法刪除臨時 JSON 檔案 {args.json}：{e}")

if __name__ == "__main__":
    main()
