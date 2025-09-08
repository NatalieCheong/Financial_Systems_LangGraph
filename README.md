# Financial Analysis AI Agents with LangGraph

A comprehensive financial analysis system that uses LangGraph to orchestrate AI agents for stock analysis and automated report generation. The system fetches real-time financial data using yfinance, performs technical and fundamental analysis, and generates professional investment reports.

## 🌟 Features

### Phase 1: Financial Data Analysis with LangGraph
- **Multi-Stock Analysis**: Analyze single stocks, compare multiple stocks, or evaluate entire portfolios
- **Technical Analysis**: RSI, moving averages, volatility analysis, trend signals
- **Fundamental Analysis**: P/E ratios, profitability metrics, growth analysis, financial health
- **Market Sentiment**: AI-powered news sentiment analysis
- **Automated Visualizations**: Price charts with technical indicators
- **Real-time Data**: Live stock data via yfinance API

### Phase 2: AI-Powered Report Writer
- **Professional Reports**: Executive summaries, detailed analysis, investor presentations
- **Multiple Formats**: Structured reports with market analysis, technical/fundamental sections
- **Risk Assessment**: Comprehensive risk analysis and mitigation strategies
- **Investment Recommendations**: Actionable buy/hold/sell recommendations with rationale
- **Automated Compilation**: Multi-section reports with proper formatting and disclaimers

## 📁 Project Structure

```
financial-ai-agents/
├── requirements.txt              # Python dependencies
├── config.py                    # Configuration settings
├── .env.template                # Environment variables template
├── financial_data_agent.py      # Core financial data fetching and analysis
├── langgraph_financial_agent.py # LangGraph workflow for financial analysis
├── financial_report_writer.py   # AI report generation agent
├── main.py                      # Main application and CLI interface
├── reports/                     # Generated reports (auto-created)
└── charts/                      # Generated charts (auto-created)
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or create the project directory
mkdir financial-ai-agents
cd financial-ai-agents

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy the environment template
cp .env.template .env

# Edit .env with your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Basic Usage

#### Command Line Interface

```bash
# Analyze a single stock
python main.py --symbols AAPL --period 6mo

# Compare multiple stocks
python main.py --symbols AAPL MSFT GOOGL --analysis-type comparison --period 1y

# Portfolio analysis
python main.py --symbols AAPL MSFT GOOGL AMZN TSLA --analysis-type portfolio

# Interactive mode
python main.py --interactive
```

#### Python API Usage

```python
from main import FinancialAnalysisApp

# Initialize the application
app = FinancialAnalysisApp()

# Quick single stock analysis
results = app.quick_analysis("AAPL", period="6mo")

# Compare multiple stocks
results = app.compare_stocks(["AAPL", "MSFT", "GOOGL"], period="1y")

# Custom analysis
results = app.run_analysis(
    symbols=["AAPL"],
    analysis_type="single",
    period="1y",
    generate_report=True,
    report_type="detailed"
)
```

## 🔧 Configuration Options

### Analysis Types
- **single**: Analyze one stock in detail
- **comparison**: Compare multiple stocks side-by-side
- **portfolio**: Analyze stocks as a portfolio

### Time Periods
- **1d, 5d**: Short-term analysis
- **1mo, 3mo, 6mo**: Medium-term analysis
- **1y, 2y, 5y**: Long-term analysis
- **ytd, max**: Year-to-date or maximum available data

### Report Types
- **executive**: Concise summary for executives
- **detailed**: Comprehensive analysis report
- **investor_presentation**: Structured for investor presentations

## 📊 LangGraph Workflow

The system uses LangGraph to orchestrate a sophisticated analysis workflow:

### Financial Analysis Agent Workflow
1. **Data Collection**: Fetch stock data, news, and financial metrics
2. **Technical Analysis**: Calculate indicators and trend signals
3. **Fundamental Analysis**: Evaluate valuation and financial health
4. **Market Sentiment**: AI-powered news sentiment analysis
5. **Generate Insights**: LLM-powered comprehensive insights
6. **Create Visualizations**: Automated chart generation
7. **Final Recommendations**: Investment recommendations with rationale

### Report Writer Agent Workflow
1. **Analyze Data**: Structure and prepare analysis results
2. **Executive Summary**: High-level findings and recommendations
3. **Market Analysis**: Current market conditions and trends
4. **Technical Analysis**: Detailed technical indicators and signals
5. **Fundamental Analysis**: Financial metrics and valuation
6. **Risk Assessment**: Comprehensive risk analysis
7. **Investment Recommendations**: Specific actionable recommendations
8. **Compile Report**: Final professional report compilation

## 📈 Analysis Components

### Technical Analysis
- Moving averages (20-day, 50-day)
- Relative Strength Index (RSI)
- Price volatility analysis
- Volume trend analysis
- Support/resistance levels
- Trend signal generation

### Fundamental Analysis
- Valuation metrics (P/E, P/B ratios)
- Profitability analysis (margins, ROE, ROA)
- Growth metrics (revenue, earnings growth)
- Financial health (debt ratios, beta)
- Sector and industry positioning

### Risk Assessment
- Market risk (volatility, beta)
- Company-specific risks
- Sector/industry risks
- Valuation risks
- Liquidity considerations

## 🎯 Example Outputs

### Generated Files
- **Financial Reports**: Professional text reports with comprehensive analysis
- **Analysis Data**: JSON files with structured analysis results
- **Price Charts**: PNG charts with technical indicators
- **All files saved to `reports/` and `charts/` directories**

### Report Sections
1. **Executive Summary**: Key findings and investment thesis
2. **Market Analysis**: Current market environment and trends
3. **Technical Analysis**: Chart patterns and technical indicators
4. **Fundamental Analysis**: Financial metrics and valuation
5. **Risk Assessment**: Risk factors and mitigation strategies
6. **Investment Recommendations**: Specific buy/hold/sell recommendations

## 🛠️ Advanced Usage

### Custom Analysis
```python
from langgraph_financial_agent import LangGraphFinancialAgent
from financial_report_writer import FinancialReportWriter

# Direct agent usage
financial_agent = LangGraphFinancialAgent()
analysis_result = financial_agent.analyze_stocks(['AAPL'], 'single', '1y')
analysis_summary = financial_agent.get_analysis_summary(analysis_result)

# Generate custom report
report_writer = FinancialReportWriter()
report_result = report_writer.generate_report(
    analysis_data=analysis_summary,
    report_type="detailed",
    target_audience="investors"
)
```

### Batch Processing
```python
# Analyze multiple stocks separately
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
app = FinancialAnalysisApp()

for stock in stocks:
    print(f"Analyzing {stock}...")
    results = app.quick_analysis(stock, period="1y")
```

## 🔍 Error Handling

The system includes comprehensive error handling:
- Invalid stock symbols are gracefully handled
- Network issues with data fetching are reported
- Missing data is handled without breaking the workflow
- All errors are logged and reported in the final results

## 📋 Requirements

### Python Packages
- `langgraph>=0.2.16`: Workflow orchestration
- `langchain>=0.2.16`: LLM integration
- `langchain-openai>=0.1.25`: OpenAI integration
- `yfinance>=0.2.28`: Financial data fetching
- `pandas>=2.2.0`: Data manipulation
- `numpy>=1.26.0`: Numerical computing
- `matplotlib>=3.8.0`: Chart generation
- `python-dotenv>=1.0.0`: Environment management

### API Keys
- **OpenAI API Key**: Required for LLM-powered analysis and report generation

## 🔐 Security Notes

- Never commit your `.env` file with actual API keys
- Use environment variables for sensitive configuration
- The `.env.template` file shows required variables without exposing secrets
- Generated reports may contain sensitive financial information

## 🤝 Contributing

This is a comprehensive example implementation. To extend the system:

1. **Add new analysis indicators** in `financial_data_agent.py`
2. **Extend LangGraph workflows** in `langgraph_financial_agent.py`
3. **Customize report formats** in `financial_report_writer.py`
4. **Add new CLI options** in `main.py`

## 📄 License

This project is provided as an educational example for building AI agents with LangGraph for financial analysis.

## ⚠️ Disclaimer

**Important**: This software is for educational and informational purposes only. It does not constitute investment advice. All investments carry risk of loss. Past performance does not guarantee future results. Always consult with qualified financial professionals before making investment decisions.

The financial data and analysis provided by this system should not be used as the sole basis for investment decisions. Users are responsible for conducting their own due diligence and risk assessment.