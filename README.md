# 💼 金融投資 AI 專家團隊聯席決策與 PDF 報表生成系統
> **Financial AI Multi-Agent Collaboration & PDF Report Generator**

本專案是一個基於 **Prompt Engineering** 與 **多智能體聯席會議與省思機制 (Multi-Agent Critique & Reflection)** 的金融投資分析系統。

藉由將專案內的 Python 腳本與決策工作流提示詞（Prompts）提供給具備程式碼執行能力（Code Interpreter/Sandbox）的大語言模型（如 GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro/Advanced 等），LLM 將會自動在其沙盒環境中進行即時資料抓取、跨部門模擬審查、省思修正，並直接編譯出排版極其精美的 **7 頁 A4 PDF 專業投資評估報告** 供您下載。

---

## 🚀 核心工作流：如何進行分析？

您**不需要**在本地執行複雜的配置或指令，只需在與 LLM 的對話中輸入以下指令：

```text
please read workflow.md and analysis [股票名稱或代碼]
```
*(例如：`please read workflow.md and analysis 台積電` 或 `please read workflow.md and analysis AAPL`)*

### 🔍 LLM 沙盒內的自動化執行步驟：
1. **讀取憲章與解析代碼**：LLM 讀取並載入 [Prompt/workflow.md](./Prompt/workflow.md)，並自動將您輸入的股票名稱（如台積電）解析為正確的交易所代碼（如 `2330.TW`）。
2. **多角色聯席會議與數據獲取**：
   - 啟動 **Volatile 即時數據機制**，強制透過沙盒或網路抓取最新真實市場數據（如收盤價、均線、法人買賣超、營收等）。
   - 模擬三個專業部門初稿：**CFO** (基本面與財務模型)、**AR** (技術分析與籌碼面)、**IR** (產業競爭力與護城河)。
3. **審查與省思修正 (Critique & Reflection)**：
   - 執行 **5 至 10 輪的交互審查與糾錯循環**。
   - **CFO** 與 **FAG** 會針對其他部門的數據、預測漏洞、競爭對手與競品分析等進行嚴格質疑，直到無懈可擊或觸發提前結束條件。
4. **沙盒編譯與產出**：
   - 將最終定稿數據整理為 JSON，動態載入 [finance_team.py](./finance_team.py) 與 [pdf_generator.py](./pdf_generator.py)。
   - 在沙盒中執行 Python 程式，生成技術走勢圖並編譯出專業的 7 頁 PDF 報告。
   - 自動刪除臨時 JSON 檔案以保持環境整潔。
5. **提供下載**：LLM 在對話框中直接輸出生成好的 PDF 下載連結。

---

## 📂 專案目錄結構

```text
Finance/
├── Prompt/                         # 智能體提示詞與工作流憲章
│   ├── workflow.md                 # 核心工作流 Prompt (引導 LLM 的總憲章)
│   ├── DataAnalyticsReporter/      # Analytics Reporter (AR) 技術/籌碼面專家 Prompt
│   │   └── SKILL.md
│   ├── FinanceAnalyst/             # Financial Analyst Agent (FAG) 決策官 Prompt
│   │   └── SKILL.md
│   ├── FinancialHeader/            # CFO 財務配置審查長 Prompt
│   │   └── SKILL.md
│   └── InvestedResarcher/          # Invested Researcher (IR) 競爭力與消息面專家 Prompt
│       └── SKILL.md
├── FinanceReport/                  # PDF 報告與技術圖表歸檔目錄 (自動按月與代碼分類)
│   └── YYYY_MM/
│       └── TICKER_CLEAN/
│           ├── TICKER_CLEAN_chart.png          # 股票走勢與成交量圖表
│           └── TICKER_CLEAN_deep_analysis.pdf  # 最終產出的 7 頁 A4 PDF 投資報告
├── finance_team.py                 # 主控與資料載入腳本 (包含技術線圖繪製、模擬測試與 CLI 進入點)
├── pdf_generator.py                # PDF 報告生成器 (基於 ReportLab 進行 A4 進階排版)
├── requirements.txt                # 專案 Python 依賴包列表
└── README.md                       # 專案說明文件 (本檔案)
```

---

## 📄 7 頁 PDF 報告章節規劃

產出的 PDF 報告嚴格遵循專業的金融報告格式，共 7 頁 A4 排版：

| 頁碼 | 章節名稱 | 內容亮點 |
| :---: | :--- | :--- |
| **P1** | **封面與核心策略面板** | 包含個股評等 (評級顏色區分)、短期/中期/長期的操作區間與止損觸發條件表格。 |
| **P2** | **一、 技術走勢與法人籌碼圖表** | 自動繪製的近 6 個月收盤價、MA20 (月線)、MA60 (季線) 及成交量柱狀圖，附帶 AR 部門摘要。 |
| **P3** | **二、 最高決策審核與省思機制紀錄** | 完整披露 FAG 與 CFO 針對各部門初稿執行的多輪「否決-省思-補正」歷程，杜絕幻覺與盲區。 |
| **P4** | **三、 財務長基本面與資本配置審查報告** | 深度評估資本結構、海外建廠折舊敏感性壓力測試，並包含**最近 3 年歷史財務/股利表格**。 |
| **P5** | **四、 數據分析與市場籌碼交叉監測報告** | 量化統計技術指標，並提供精確的**關鍵技術與籌碼支撐壓力表**。 |
| **P6** | **五、 系統性與非系統性風險監測儀表板** | 採用 **HIGH / MED / LOW** 雙重風險評級徽章，提供避險與倉位配置建議。 |
| **P7** | **六、 競爭力護城河與產業消息面分析**<br>**七、 參考資料來源與引用說明** | SWOT 競爭力分析、**至少 3 家主要競爭對手與競品產品對比**，以及詳細的文獻/法說會引用。 |

---

## 🛡️ 決策憲章與安全機制

> [!IMPORTANT]
> **1. Constitutional Skepticism (憲政懷疑論)**
> FAG 與 CFO 必須對任何樂觀的利多訊息保持高度懷疑。報告中必須附帶代工價格下滑、海外建廠折舊超支等壓力測試。
>
> **2. Volatile 即時數據機制**
> 嚴格禁止使用預訓練模型中的過期數據。所有股價、財務數值必須與查詢當日的真實市場數據對齊，以確保投資報告的時效性。
>
> **3. 競爭對手具體化**
> IR 報告中必須明確指出至少 3 家主要競爭對手，並針對核心技術、產品特點進行表格或清單化對比，拒絕空泛的敘述。