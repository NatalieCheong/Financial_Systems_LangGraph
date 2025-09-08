# Financial Analysis AI Agents with LangSmith

A comprehensive financial analysis system that uses LangGraph to orchestrate AI agents for stock analysis and automated report generation. The system fetches real-time financial data using yfinance, performs technical and fundamental analysis, and generates professional investment reports with workflow visualizations.

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

### Phase 3: Workflow Visualization
- **LangGraph Workflow Diagrams**: Visual representation of analysis processes
- **Execution Traces**: Step-by-step workflow progress tracking
- **Analysis Dashboards**: Combined view of results and process flow
- **Interactive Charts**: Professional financial charts with technical indicators

## 📊 Sample Analysis Results

### Example: Apple Inc. (AAPL) Analysis
![AAPL Stock Chart](https://github.com/NatalieCheong/Financial_Systems_using_LangGraph/blob/master/chart/AAPL_chart.png)

**Key Findings from Recent Analysis:**
- **Recommendation**: HOLD with moderate confidence
- **Profit Margin**: 24.3% (Strong profitability)
- **Return on Equity**: 149.8% (Excellent efficiency)
- **P/E Ratio**: 36.37 (Potentially overvalued)
- **Risk Level**: High volatility (39.93%) with high debt levels

### Multi-Stock Comparison Example
The system successfully analyzed AAPL, MSFT, and GOOGL with the following key recommendations:
- **AAPL**: HOLD - Strong profitability but overvalued
- **MSFT**: BUY - Strong fundamentals with recent price drop opportunity
- **GOOGL**: HOLD - Bullish trend but overbought conditions

### NVIDIA Analysis Highlights
- **Profit Margin**: 52.4% (Exceptional profitability)
- **Revenue Growth**: 55.6% (Outstanding growth)
- **Recommendation**: HOLD - Wait for better entry point due to high volatility

## 📁 Project Structure

```
financial-ai-agents/
├── requirements.txt              # Python dependencies
├── config.py                    # Configuration settings
├── .env.template                # Environment variables template
├── financial_data_agent.py      # Core financial data fetching and analysis
├── langgraph_financial_agent.py # LangGraph workflow for financial analysis
├── financial_report_writer.py       # AI report generation agent (optimized)
├── graph_visualizer.py          # Workflow visualization tools
├── main.py                      # Main application and CLI interface
├── reports/                     # Generated reports (auto-created)
├── charts/                      # Generated charts (auto-created)
└── .gitignore                   # Git ignore file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Create project directory
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

### 3. Usage Examples

#### Command Line Interface

```bash
# Analyze a single stock
python main.py --symbols AAPL --period 6mo

# Compare multiple stocks
python main.py --symbols AAPL MSFT GOOGL --analysis-type comparison --period 1y

# Portfolio analysis
python main.py --symbols AAPL MSFT GOOGL AMZN TSLA --analysis-type portfolio

# View workflow graphs only
python main.py --view-graphs

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

# Custom analysis with specific parameters
results = app.run_analysis(
    symbols=["NVDA"],
    analysis_type="single",
    period="6mo",
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

## 🎯 Generated Outputs

### Report Examples
The system generates comprehensive financial reports with:

1. **Executive Summary**: Key findings and investment thesis
2. **Market Analysis**: Current market environment and trends
3. **Technical Analysis**: Chart patterns and technical indicators
4. **Fundamental Analysis**: Financial metrics and valuation
5. **Risk Assessment**: Risk factors and mitigation strategies
6. **Investment Recommendations**: Specific buy/hold/sell recommendations

### Visualization Files
- **Financial Reports**: Professional text reports with comprehensive analysis
- **Analysis Data**: JSON files with structured analysis results
- **Price Charts**: PNG charts with technical indicators and volume analysis
- **Workflow Diagrams**: Visual representations of the LangGraph processes

### Successful Test Results
The system has been successfully tested with:
- **AAPL**: Technology sector analysis
- **MSFT**: Software and cloud services
- **GOOGL**: Internet and advertising services
- **NVDA**: Semiconductor and AI technology
- **Multi-stock comparisons**: Portfolio analysis capabilities

## 📋 Requirements

### API Keys
- **OpenAI API Key**: Required for LLM-powered analysis and report generation

## 🔐 Security and Best Practices

- Environment variables for API key management
- Comprehensive `.gitignore` for sensitive data protection
- Separate configuration management
- Error handling and validation throughout the system
- Professional disclaimers in all generated reports

## 🚀 Performance and Optimization

- **Efficient Data Processing**: Optimized yfinance data retrieval
- **Streamlined Report Generation**: Sequential processing to eliminate duplication
- **Memory Management**: Proper state management in LangGraph workflows
- **Cost Optimization**: Minimized API calls through efficient prompt design

## 🤝 Contributing and Customization

The system is designed for extensibility:

1. **Add new analysis indicators** in `financial_data_agent.py`
2. **Extend LangGraph workflows** in `langgraph_financial_agent.py`
3. **Customize report formats** in `fixed_report_writer.py`
4. **Add new CLI options** in `main.py`
5. **Create custom visualizations** in `graph_visualizer.py`

## ⚠️ Important Disclaimers

**INVESTMENT DISCLAIMER**: This software is for educational and informational purposes only and does not constitute investment advice. All investments carry risk of loss. Past performance does not guarantee future results. The financial analysis and recommendations provided by this system should not be used as the sole basis for investment decisions.

**RISK WARNINGS**:
- All investments involve risk, including potential loss of principal
- Stock prices can be volatile and unpredictable
- AI-generated analysis may contain errors or biases
- Market conditions can change rapidly
- Always consult with qualified financial professionals before making investment decisions

**TECHNICAL DISCLAIMERS**:
- Financial data accuracy depends on third-party sources (yfinance)
- AI analysis is based on historical data and current market conditions
- System recommendations are not guaranteed to be profitable
- Users are responsible for conducting their own due diligence

**LIABILITY LIMITATION**: The developers and contributors of this system assume no responsibility for any financial losses or damages resulting from the use of this software. Users assume all risks associated with their investment decisions.

## 📄 License

This project is provided as an educational example for building AI agents with LangGraph for financial analysis. Use at your own risk and in accordance with applicable financial regulations in your jurisdiction.
