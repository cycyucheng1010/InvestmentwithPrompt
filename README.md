# LLM-Based Automated Financial Report Generation System

This project is a financial investment analysis system based on **Prompt Engineering** and a **Multi-Agent Joint Meeting, Critique & Reflection** mechanism.

By inputting the Python scripts and decision-making workflow prompts (Prompts) from this project to a Large Language Model (LLM) equipped with code execution capabilities (Code Interpreter/Sandbox) such as GPT-4o, Claude 3.5 Sonnet, or Gemini 1.5 Pro/Advanced, the LLM will automatically perform real-time data scraping, cross-department simulated reviews, and critique & reflection loops within its sandbox environment. It then directly compiles a beautifully designed **7-page A4 PDF professional investment evaluation report** for you to download.

---

## 🚀 Core Workflow: How to Perform Analysis?

You **do not need** to perform complex configurations or run commands locally. Simply enter the following command in your conversation with the LLM:

```text
please read workflow.md and analyze [stock name or ticker] to complete the report 
```

### 🔍 Automated Execution Steps in the LLM Sandbox:
1. **Read Charter and Resolve Ticker**: The LLM reads and loads [Prompt/workflow.md](./Prompt/workflow.md), and automatically resolves the stock name you enter (e.g., TSMC) into the correct exchange ticker symbol (e.g., `0050.tw` or `2330.tw`).
2. **Multi-Role Joint Meeting and Data Retrieval**:
   - Activates the **Volatile Real-Time Data Mechanism**, forcing the retrieval of the latest real-time market data (e.g., closing prices, moving averages, institutional net buy/sell volume, revenues, etc.) through the sandbox or web search.
   - Simulates draft reports from three professional departments: **CFO** (Fundamentals & Financial Model), **AR** (Technical Analysis & Institutional Chips), and **IR** (Industrial Competitiveness & Moat).
3. **Critique & Reflection Loop**:
   - Executes a **5 to 10-round interactive review and error-correction loop**.
   - The **CFO** and **FAG** strictly challenge other departments' data, prediction loopholes, competitor profiles, and product comparisons until the content is flawless or an early termination condition is met.
4. **Sandbox Compilation and Output**:
   - Organizes the final approved data into JSON and dynamically loads [finance_team.py](./finance_team.py) and [pdf_generator.py](./pdf_generator.py).
   - Runs the Python program within the sandbox to generate technical charts and compile the professional 7-page A4 PDF report.
   - Automatically deletes temporary JSON files to keep the environment clean.
5. **Download Link**: The LLM outputs the generated PDF download link directly in the chat window.

---

## 📂 Project Directory Structure

```text
Finance/
├── Prompt/                         # Agent prompts and workflow charters
│   ├── workflow.md                 # Core workflow prompt (The master charter guiding the LLM)
│   ├── DataAnalyticsReporter/      # Analytics Reporter (AR) Technical/Institutional Chips Expert Prompt
│   │   └── SKILL.md
│   ├── FinanceAnalyst/             # Financial Analyst Agent (FAG) Decision Officer Prompt
│   │   └── SKILL.md
│   ├── FinancialHeader/            # CFO Financial Allocation Reviewer Prompt
│   │   └── SKILL.md
│   └── InvestedResarcher/          # Invested Researcher (IR) Competitiveness & News Expert Prompt
│       └── SKILL.md
├── FinanceReport/                  # Archiving directory for PDF reports and charts (Automatically sorted by month and ticker)
│   └── YYYY_MM/
│       └── TICKER_CLEAN/
│           ├── TICKER_CLEAN_chart.png          # Stock price trend and volume chart
│           └── TICKER_CLEAN_deep_analysis.pdf  # Final output: 7-page A4 PDF investment report
├── finance_team.py                 # Controller and data loader script (Includes technical chart drawing, simulation testing, and CLI entry point)
├── pdf_generator.py                # PDF report generator (ReportLab-based advanced A4 layout)
├── requirements.txt                # Project Python dependencies
└── README.md                       # Project description file (This file)
```

---

## 📄 7-Page PDF Report Chapter Structure

The generated PDF report strictly follows a professional financial report format, spanning 7 pages of A4 layout:

| Page | Section Name | Content Highlights |
| :---: | :--- | :--- |
| **P1** | **Cover Page & Core Strategy Dashboard** | Includes individual stock rating (distinguished by rating color), and short/medium/long-term trading ranges with a stop-loss trigger table. |
| **P2** | **I. Technical Trends and Institutional Chips Chart** | Plotted chart of the last 6 months' closing prices, MA20 (monthly moving average), MA60 (quarterly moving average), and volume histograms, accompanied by a summary from the AR department. |
| **P3** | **II. Executive Decision Review & Reflection Log** | Full disclosure of the multi-round "veto-reflection-amendment" process executed by the FAG and CFO on each department's draft, eliminating hallucinations and blind spots. |
| **P4** | **III. CFO Fundamentals and Capital Allocation Review Report** | In-depth evaluation of capital structure, depreciation sensitivity stress tests for overseas factory construction, and historical financial/dividend tables for the **past 3 years**. |
| **P5** | **IV. Data Analysis and Market Chips Cross-Monitoring Report** | Quantitative statistics of technical indicators, along with precise **key technical and chip support/resistance tables**. |
| **P6** | **V. Systematic and Unsystematic Risk Monitoring Dashboard** | Utilizing **HIGH / MED / LOW** dual-risk rating badges, providing hedging and position sizing recommendations. |
| **P7** | **VI. Competitive Moat and Industry News Analysis**<br>**VII. References and Citations** | SWOT analysis, **product comparisons with at least 3 major competitors**, and detailed citations of literature or earnings call transcripts. |

---

## 🛡️ Decision Charter and Security Mechanisms

> [!IMPORTANT]
> **1. Constitutional Skepticism**
> The FAG and CFO must maintain high skepticism toward any optimistic or bullish news. Reports must include stress tests such as foundry price declines or overseas factory construction depreciation overruns.
>
> **2. Volatile Real-Time Data Mechanism**
> The use of outdated pre-trained model data is strictly prohibited. All stock prices and financial metrics must align with the real-time market data of the query day to ensure the timeliness of the investment report.
>
> **3. Competitor Specification**
> The IR report must explicitly identify at least 3 major competitors and compare core technologies and product characteristics in a table or list format, avoiding vague descriptions.