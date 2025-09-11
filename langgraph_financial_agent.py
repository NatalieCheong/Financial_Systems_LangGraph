from typing import Dict, List, Any, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import operator
from financial_data_agent import FinancialDataAgent, FinancialData
from config import Config
import json

class FinancialAnalysisState(TypedDict):
    """State for the financial analysis workflow"""
    symbols: List[str]
    analysis_type: str  # 'single', 'comparison', 'portfolio'
    period: str
    raw_data: Dict[str, FinancialData]
    processed_analysis: Dict[str, Any]
    recommendations: List[str]
    messages: Annotated[List, operator.add]
    chart_paths: List[str]
    error_messages: List[str]

class LangGraphFinancialAgent:
    """LangGraph-based financial analysis agent"""
    
    def __init__(self):
        Config.validate()
        self.llm = ChatOpenAI(
            model=Config.DEFAULT_MODEL,
            temperature=0.1,
            api_key=Config.OPENAI_API_KEY
        )
        self.financial_agent = FinancialDataAgent()
        self.graph = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(FinancialAnalysisState)
        
        # Add nodes
        workflow.add_node("data_collection", self._collect_financial_data)
        workflow.add_node("technical_analysis", self._perform_technical_analysis)
        workflow.add_node("fundamental_analysis", self._perform_fundamental_analysis)
        workflow.add_node("market_sentiment", self._analyze_market_sentiment)
        workflow.add_node("generate_insights", self._generate_insights)
        workflow.add_node("create_visualizations", self._create_visualizations)
        workflow.add_node("final_recommendations", self._generate_recommendations)
        
        # Define the workflow
        workflow.set_entry_point("data_collection")
        
        workflow.add_edge("data_collection", "technical_analysis")
        workflow.add_edge("technical_analysis", "fundamental_analysis")
        workflow.add_edge("fundamental_analysis", "market_sentiment")
        workflow.add_edge("market_sentiment", "generate_insights")
        workflow.add_edge("generate_insights", "create_visualizations")
        workflow.add_edge("create_visualizations", "final_recommendations")
        workflow.add_edge("final_recommendations", END)
        
        return workflow.compile()
    
    def _collect_financial_data(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Collect financial data for the specified symbols"""
        print("📊 Collecting financial data...")
        
        raw_data = {}
        error_messages = []
        
        for symbol in state["symbols"]:
            try:
                data = self.financial_agent.fetch_stock_data(symbol, state.get("period", "1y"))
                raw_data[symbol] = data
                print(f"✅ Data collected for {symbol}")
            except Exception as e:
                error_message = f"Failed to collect data for {symbol}: {str(e)}"
                error_messages.append(error_message)
                print(f"❌ {error_message}")
        
        state["raw_data"] = raw_data
        state["error_messages"] = error_messages
        state["messages"] = [f"Collected data for {len(raw_data)} symbols"]
        
        return state
    
    def _perform_technical_analysis(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Perform technical analysis on the collected data"""
        print("📈 Performing technical analysis...")
        
        technical_analysis = {}
        
        for symbol, data in state["raw_data"].items():
            try:
                analysis = data.analysis_summary
                
                # Enhanced technical signals
                signals = []
                
                if analysis.get('rsi'):
                    rsi = analysis['rsi']
                    if rsi > 70:
                        signals.append("RSI indicates overbought conditions")
                    elif rsi < 30:
                        signals.append("RSI indicates oversold conditions")
                    else:
                        signals.append("RSI in neutral territory")
                
                if analysis.get('ma_20') and analysis.get('ma_50') and analysis.get('current_price'):
                    price = analysis['current_price']
                    ma_20 = analysis['ma_20']
                    ma_50 = analysis['ma_50']
                    
                    if price > ma_20 > ma_50:
                        signals.append("Bullish trend - price above moving averages")
                    elif price < ma_20 < ma_50:
                        signals.append("Bearish trend - price below moving averages")
                
                if analysis.get('volatility'):
                    vol = analysis['volatility']
                    if vol > 30:
                        signals.append("High volatility detected")
                    elif vol < 15:
                        signals.append("Low volatility environment")
                
                technical_analysis[symbol] = {
                    'signals': signals,
                    'trend': analysis.get('trend_signal', 'neutral'),
                    'volatility': analysis.get('volatility'),
                    'rsi': analysis.get('rsi'),
                    'price_changes': {
                        '1d': analysis.get('price_change_1d'),
                        '1w': analysis.get('price_change_1w'),
                        '1m': analysis.get('price_change_1m')
                    }
                }
                
            except Exception as e:
                print(f"Error in technical analysis for {symbol}: {e}")
                continue
        
        if not state.get("processed_analysis"):
            state["processed_analysis"] = {}
        state["processed_analysis"]["technical"] = technical_analysis
        state["messages"].append("Technical analysis completed")
        
        return state
    
    def _perform_fundamental_analysis(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Perform fundamental analysis"""
        print("📊 Performing fundamental analysis...")
        
        fundamental_analysis = {}
        
        for symbol, data in state["raw_data"].items():
            try:
                metrics = data.financial_metrics
                
                analysis = {
                    'valuation': self._analyze_valuation(metrics),
                    'profitability': self._analyze_profitability(metrics),
                    'growth': self._analyze_growth(metrics),
                    'financial_health': self._analyze_financial_health(metrics),
                    'sector': metrics.get('sector'),
                    'industry': metrics.get('industry')
                }
                
                fundamental_analysis[symbol] = analysis
                
            except Exception as e:
                print(f"Error in fundamental analysis for {symbol}: {e}")
                continue
        
        state["processed_analysis"]["fundamental"] = fundamental_analysis
        state["messages"].append("Fundamental analysis completed")
        
        return state
    
    def _analyze_valuation(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze valuation metrics"""
        valuation = {}
        
        if metrics.get('pe_ratio'):
            pe = metrics['pe_ratio']
            if pe < 15:
                valuation['pe_assessment'] = "Potentially undervalued (low P/E)"
            elif pe > 25:
                valuation['pe_assessment'] = "Potentially overvalued (high P/E)"
            else:
                valuation['pe_assessment'] = "Reasonable valuation"
            valuation['pe_ratio'] = pe
        
        if metrics.get('price_to_book'):
            pb = metrics['price_to_book']
            if pb < 1:
                valuation['pb_assessment'] = "Trading below book value"
            elif pb > 3:
                valuation['pb_assessment'] = "Trading at premium to book value"
            valuation['price_to_book'] = pb
        
        return valuation
    
    def _analyze_profitability(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze profitability metrics"""
        profitability = {}
        
        if metrics.get('profit_margin'):
            margin = metrics['profit_margin'] * 100
            profitability['profit_margin'] = margin
            if margin > 20:
                profitability['margin_assessment'] = "Strong profitability"
            elif margin > 10:
                profitability['margin_assessment'] = "Good profitability"
            else:
                profitability['margin_assessment'] = "Low profitability"
        
        if metrics.get('roe'):
            roe = metrics['roe'] * 100
            profitability['roe'] = roe
            if roe > 15:
                profitability['roe_assessment'] = "Strong return on equity"
            elif roe > 10:
                profitability['roe_assessment'] = "Decent return on equity"
            else:
                profitability['roe_assessment'] = "Low return on equity"
        
        return profitability
    
    def _analyze_growth(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze growth metrics"""
        growth = {}
        
        if metrics.get('revenue_growth'):
            rev_growth = metrics['revenue_growth'] * 100
            growth['revenue_growth'] = rev_growth
            if rev_growth > 15:
                growth['growth_assessment'] = "Strong revenue growth"
            elif rev_growth > 5:
                growth['growth_assessment'] = "Moderate revenue growth"
            else:
                growth['growth_assessment'] = "Slow revenue growth"
        
        if metrics.get('earnings_growth'):
            earnings_growth = metrics['earnings_growth'] * 100
            growth['earnings_growth'] = earnings_growth
        
        return growth
    
    def _analyze_financial_health(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze financial health"""
        health = {}
        
        if metrics.get('debt_to_equity'):
            de_ratio = metrics['debt_to_equity']
            health['debt_to_equity'] = de_ratio
            if de_ratio < 0.3:
                health['leverage_assessment'] = "Conservative debt levels"
            elif de_ratio < 0.6:
                health['leverage_assessment'] = "Moderate debt levels"
            else:
                health['leverage_assessment'] = "High debt levels"
        
        if metrics.get('beta'):
            beta = metrics['beta']
            health['beta'] = beta
            if beta > 1.5:
                health['risk_assessment'] = "High volatility vs market"
            elif beta < 0.5:
                health['risk_assessment'] = "Low volatility vs market"
            else:
                health['risk_assessment'] = "Moderate volatility vs market"
        
        return health
    
    def _analyze_market_sentiment(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Analyze market sentiment using LLM"""
        print("🎭 Analyzing market sentiment...")
        
        sentiment_analysis = {}
        
        for symbol, data in state["raw_data"].items():
            try:
                # Prepare news summary for LLM analysis
                news_summary = ""
                if data.news:
                    news_titles = [news.get('title', '') for news in data.news[:3]]
                    news_summary = "; ".join(news_titles)
                
                # Create prompt for sentiment analysis
                prompt = f"""
                Analyze the market sentiment for {symbol} ({data.company_name}) based on:
                
                Recent News Headlines: {news_summary}
                Current Price: ${data.current_price:.2f}
                1-day change: {state['processed_analysis']['technical'][symbol]['price_changes']['1d']:.2f}%
                1-week change: {state['processed_analysis']['technical'][symbol]['price_changes']['1w']:.2f}%
                
                Provide a brief sentiment assessment (Bullish/Bearish/Neutral) with reasoning.
                """
                
                response = self.llm.invoke([
                    SystemMessage(content="You are a financial analyst specializing in market sentiment analysis."),
                    HumanMessage(content=prompt)
                ])
                
                sentiment_analysis[symbol] = {
                    'sentiment': response.content,
                    'news_count': len(data.news)
                }
                
            except Exception as e:
                print(f"Error in sentiment analysis for {symbol}: {e}")
                sentiment_analysis[symbol] = {'sentiment': 'Neutral - Unable to analyze', 'news_count': 0}
        
        state["processed_analysis"]["sentiment"] = sentiment_analysis
        state["messages"].append("Market sentiment analysis completed")
        
        return state
    
    def _generate_insights(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Generate comprehensive insights using LLM"""
        print("💡 Generating insights...")
        
        # Prepare comprehensive analysis for LLM
        analysis_summary = {
            'symbols': state['symbols'],
            'technical': state['processed_analysis']['technical'],
            'fundamental': state['processed_analysis']['fundamental'],
            'sentiment': state['processed_analysis']['sentiment']
        }
        
        prompt = f"""
        Based on the comprehensive financial analysis below, provide key insights and observations:
        
        {json.dumps(analysis_summary, indent=2, default=str)}
        
        Please provide:
        1. Key strengths and weaknesses for each stock
        2. Risk assessment
        3. Investment themes and opportunities
        4. Comparative analysis if multiple stocks
        
        Keep the response concise but informative.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a senior financial analyst providing investment insights."),
                HumanMessage(content=prompt)
            ])
            
            state["processed_analysis"]["insights"] = response.content
            state["messages"].append("Insights generated successfully")
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            state["processed_analysis"]["insights"] = "Unable to generate insights due to an error."
        
        return state
    
    def _create_visualizations(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Create visualizations for the analysis"""
        print("📊 Creating visualizations...")
        
        chart_paths = []
        
        for symbol, data in state["raw_data"].items():
            try:
                chart_path = self.financial_agent.create_price_chart(data)
                chart_paths.append(chart_path)
                print(f"✅ Chart created for {symbol}: {chart_path}")
            except Exception as e:
                print(f"❌ Error creating chart for {symbol}: {e}")
        
        state["chart_paths"] = chart_paths
        state["messages"].append(f"Created {len(chart_paths)} visualizations")
        
        return state
    
    def _generate_recommendations(self, state: FinancialAnalysisState) -> FinancialAnalysisState:
        """Generate final investment recommendations"""
        print("🎯 Generating recommendations...")
        
        # Prepare data for recommendation generation
        recommendation_data = {
            'analysis': state['processed_analysis'],
            'symbols': state['symbols'],
            'analysis_type': state['analysis_type']
        }
        
        prompt = f"""
        Based on the comprehensive financial analysis, provide specific investment recommendations:
        
        Analysis Data: {json.dumps(recommendation_data, indent=2, default=str)}
        
        Please provide:
        1. Investment recommendation for each stock (Buy/Hold/Sell)
        2. Rationale for each recommendation
        3. Risk level assessment
        4. Suggested position sizing or portfolio allocation
        5. Key factors to monitor going forward
        
        Be specific and actionable in your recommendations.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a portfolio manager providing investment recommendations."),
                HumanMessage(content=prompt)
            ])
            
            state["recommendations"] = [response.content]
            state["messages"].append("Investment recommendations generated")
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            state["recommendations"] = ["Unable to generate recommendations due to an error."]
        
        return state
    
    def analyze_stocks(self, symbols: List[str], analysis_type: str = "single", period: str = "1y") -> FinancialAnalysisState:
        """
        Run the complete financial analysis workflow
        
        Args:
            symbols: List of stock symbols to analyze
            analysis_type: Type of analysis ('single', 'comparison', 'portfolio')
            period: Time period for analysis
        
        Returns:
            Complete analysis state
        """
        initial_state = FinancialAnalysisState(
            symbols=symbols,
            analysis_type=analysis_type,
            period=period,
            raw_data={},
            processed_analysis={},
            recommendations=[],
            messages=[],
            chart_paths=[],
            error_messages=[]
        )
        
        print(f"🚀 Starting financial analysis for: {', '.join(symbols)}")
        final_state = self.graph.invoke(initial_state)
        print("✅ Analysis completed!")
        
        return final_state
    
    def get_analysis_summary(self, state: FinancialAnalysisState) -> Dict[str, Any]:
        """Get a structured summary of the analysis results"""
        return {
            'symbols_analyzed': state['symbols'],
            'analysis_type': state['analysis_type'],
            'period': state['period'],
            'technical_analysis': state['processed_analysis'].get('technical', {}),
            'fundamental_analysis': state['processed_analysis'].get('fundamental', {}),
            'sentiment_analysis': state['processed_analysis'].get('sentiment', {}),
            'insights': state['processed_analysis'].get('insights', ''),
            'recommendations': state['recommendations'],
            'chart_paths': state['chart_paths'],
            'messages': state['messages'],
            'errors': state['error_messages']
        }

# Example usage and testing
if __name__ == "__main__":
    # Example usage
    agent = LangGraphFinancialAgent()
    
    # Analyze single stock
    result = agent.analyze_stocks(['AAPL'], analysis_type="single", period="6mo")
    summary = agent.get_analysis_summary(result)
    
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    print(f"Symbols: {summary['symbols_analyzed']}")
    print(f"Period: {summary['period']}")
    print(f"Charts created: {len(summary['chart_paths'])}")
    print(f"Messages: {len(summary['messages'])}")
    
    if summary['insights']:
        print(f"\nInsights:\n{summary['insights']}")
    
    if summary['recommendations']:
        print(f"\nRecommendations:\n{summary['recommendations'][0]}")
    
    # Example of comparing multiple stocks
    # comparison_result = agent.analyze_stocks(['AAPL', 'MSFT', 'GOOGL'], analysis_type="comparison", period="1y")