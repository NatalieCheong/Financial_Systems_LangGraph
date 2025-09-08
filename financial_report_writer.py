from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from datetime import datetime
import json
import os
from dataclasses import dataclass
from config import Config

@dataclass
class ReportSection:
    """Structure for report sections"""
    title: str
    content: str
    order: int
    section_type: str  # 'executive_summary', 'analysis', 'recommendations', etc.

class FinancialReportWriter:
    """AI agent for generating comprehensive financial reports"""
    
    def __init__(self):
        Config.validate()
        self.llm = ChatOpenAI(
            model=Config.DEFAULT_MODEL,
            temperature=0.2,
            api_key=Config.OPENAI_API_KEY
        )
    
    def generate_report(self, analysis_data: Dict[str, Any], 
                       report_type: str = "detailed", 
                       target_audience: str = "investors") -> Dict[str, Any]:
        """
        Generate a comprehensive financial report from analysis data
        
        Args:
            analysis_data: Output from LangGraphFinancialAgent
            report_type: Type of report ('executive', 'detailed', 'investor_presentation')
            target_audience: Target audience ('executives', 'investors', 'analysts')
        
        Returns:
            Complete report state with final report content
        """
        print(f"📝 Starting report generation...")
        print(f"Report Type: {report_type}")
        print(f"Target Audience: {target_audience}")
        
        # Initialize state
        state = {
            "analysis_data": analysis_data,
            "report_type": report_type,
            "target_audience": target_audience,
            "report_sections": [],
            "final_report": "",
            "report_metadata": {},
            "messages": []
        }
        
        try:
            # Execute workflow steps sequentially
            state = self._analyze_input_data(state)
            state = self._create_executive_summary(state)
            state = self._write_market_analysis(state)
            state = self._write_technical_analysis(state)
            state = self._write_fundamental_analysis(state)
            state = self._write_risk_assessment(state)
            state = self._write_recommendations(state)
            state = self._compile_final_report(state)
            
            print("✅ Report generation completed!")
            return state
            
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            state["messages"].append(f"Error: {str(e)}")
            return state
    
    def _analyze_input_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the input financial data to understand scope and structure"""
        print("📊 Analyzing input data for report structure...")
        
        analysis_data = state["analysis_data"]
        
        # Determine report characteristics
        symbols = analysis_data.get('symbols_analyzed', [])
        analysis_type = analysis_data.get('analysis_type', 'single')
        
        metadata = {
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symbols_count': len(symbols),
            'symbols': symbols,
            'analysis_type': analysis_type,
            'data_period': analysis_data.get('period', 'N/A'),
            'has_technical_data': bool(analysis_data.get('technical_analysis')),
            'has_fundamental_data': bool(analysis_data.get('fundamental_analysis')),
            'has_sentiment_data': bool(analysis_data.get('sentiment_analysis')),
            'has_charts': bool(analysis_data.get('chart_paths'))
        }
        
        state["report_metadata"] = metadata
        state["messages"].append("Data analysis completed - report structure determined")
        
        return state
    
    def _create_executive_summary(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create the executive summary section"""
        print("📝 Writing executive summary...")
        
        analysis_data = state["analysis_data"]
        metadata = state["report_metadata"]
        
        prompt = f"""
        Write a professional executive summary for a financial analysis report based on the following data:
        
        Symbols Analyzed: {', '.join(metadata['symbols'])}
        Analysis Period: {metadata['data_period']}
        Analysis Type: {metadata['analysis_type']}
        
        Key Insights: {analysis_data.get('insights', 'N/A')}
        
        Recommendations Summary: {analysis_data.get('recommendations', ['N/A'])[0] if analysis_data.get('recommendations') else 'N/A'}
        
        The executive summary should be:
        - Concise (2-3 paragraphs)
        - Highlight key findings and investment thesis
        - Include primary recommendations
        - Written for senior executives and decision makers
        - Professional and authoritative tone
        
        Do not include technical jargon that executives wouldn't understand.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a senior financial analyst writing for C-suite executives."),
                HumanMessage(content=prompt)
            ])
            
            section = ReportSection(
                title="Executive Summary",
                content=response.content,
                order=1,
                section_type="executive_summary"
            )
            
            state["report_sections"].append(section)
            state["messages"].append("Executive summary completed")
            
        except Exception as e:
            print(f"Error creating executive summary: {e}")
            state["messages"].append(f"Error in executive summary: {str(e)}")
        
        return state
    
    def _write_market_analysis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Write the market analysis section"""
        print("📈 Writing market analysis...")
        
        analysis_data = state["analysis_data"]
        metadata = state["report_metadata"]
        
        # Extract market context
        sentiment_data = analysis_data.get('sentiment_analysis', {})
        technical_data = analysis_data.get('technical_analysis', {})
        
        prompt = f"""
        Write a comprehensive market analysis section for the financial report covering:
        
        Symbols: {', '.join(metadata['symbols'])}
        Analysis Period: {metadata['data_period']}
        
        Sentiment Analysis Data: {json.dumps(sentiment_data, indent=2, default=str)}
        
        Technical Trends: {json.dumps(technical_data, indent=2, default=str)}
        
        The market analysis should include:
        1. Current market environment and conditions
        2. Sector/industry trends affecting these stocks
        3. Market sentiment and investor behavior
        4. Key market drivers and catalysts
        5. Broader economic context (if relevant)
        
        Write in a professional, analytical style suitable for institutional investors.
        Length: 3-4 paragraphs.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a market strategist providing institutional-grade market analysis."),
                HumanMessage(content=prompt)
            ])
            
            section = ReportSection(
                title="Market Analysis",
                content=response.content,
                order=2,
                section_type="market_analysis"
            )
            
            state["report_sections"].append(section)
            state["messages"].append("Market analysis completed")
            
        except Exception as e:
            print(f"Error writing market analysis: {e}")
            state["messages"].append(f"Error in market analysis: {str(e)}")
        
        return state
    
    def _write_technical_analysis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Write the technical analysis section"""
        print("📊 Writing technical analysis...")
        
        analysis_data = state["analysis_data"]
        technical_data = analysis_data.get('technical_analysis', {})
        
        if not technical_data:
            state["messages"].append("Skipped technical analysis - no data available")
            return state
        
        prompt = f"""
        Write a detailed technical analysis section based on the following data:
        
        Technical Analysis Data: {json.dumps(technical_data, indent=2, default=str)}
        
        The technical analysis should cover:
        1. Price trends and momentum indicators
        2. Moving average analysis
        3. RSI and overbought/oversold conditions
        4. Volatility analysis
        5. Volume trends and patterns
        6. Support and resistance levels (if identifiable)
        7. Technical signals and chart patterns
        
        For each stock analyzed, provide:
        - Current technical position
        - Key technical levels to watch
        - Short-term and medium-term technical outlook
        
        Write for readers familiar with technical analysis terminology.
        Length: 4-5 paragraphs.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a technical analyst providing detailed chart analysis."),
                HumanMessage(content=prompt)
            ])
            
            section = ReportSection(
                title="Technical Analysis",
                content=response.content,
                order=3,
                section_type="technical_analysis"
            )
            
            state["report_sections"].append(section)
            state["messages"].append("Technical analysis completed")
            
        except Exception as e:
            print(f"Error writing technical analysis: {e}")
            state["messages"].append(f"Error in technical analysis: {str(e)}")
        
        return state
    
    def _write_fundamental_analysis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Write the fundamental analysis section"""
        print("💼 Writing fundamental analysis...")
        
        analysis_data = state["analysis_data"]
        fundamental_data = analysis_data.get('fundamental_analysis', {})
        
        if not fundamental_data:
            state["messages"].append("Skipped fundamental analysis - no data available")
            return state
        
        prompt = f"""
        Write a comprehensive fundamental analysis section based on:
        
        Fundamental Analysis Data: {json.dumps(fundamental_data, indent=2, default=str)}
        
        The fundamental analysis should cover:
        1. Valuation metrics (P/E, P/B, etc.) and assessment
        2. Profitability analysis (margins, ROE, ROA)
        3. Growth metrics and trends
        4. Financial health and balance sheet strength
        5. Competitive positioning within sector/industry
        6. Business model and revenue drivers
        7. Management quality and corporate governance (if data available)
        
        For each stock, provide:
        - Valuation assessment (undervalued/fairly valued/overvalued)
        - Financial strength rating
        - Growth prospects
        - Key fundamental risks and opportunities
        
        Write for sophisticated investors who understand financial statements.
        Length: 5-6 paragraphs.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a fundamental analyst with deep expertise in financial statement analysis."),
                HumanMessage(content=prompt)
            ])
            
            section = ReportSection(
                title="Fundamental Analysis",
                content=response.content,
                order=4,
                section_type="fundamental_analysis"
            )
            
            state["report_sections"].append(section)
            state["messages"].append("Fundamental analysis completed")
            
        except Exception as e:
            print(f"Error writing fundamental analysis: {e}")
            state["messages"].append(f"Error in fundamental analysis: {str(e)}")
        
        return state
    
    def _write_risk_assessment(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Write the risk assessment section"""
        print("⚠️ Writing risk assessment...")
        
        analysis_data = state["analysis_data"]
        metadata = state["report_metadata"]
        
        # Compile risk data from all analyses
        risk_data = {
            'technical_risks': analysis_data.get('technical_analysis', {}),
            'fundamental_risks': analysis_data.get('fundamental_analysis', {}),
            'sentiment_risks': analysis_data.get('sentiment_analysis', {}),
            'symbols': metadata['symbols']
        }
        
        prompt = f"""
        Write a thorough risk assessment section based on the analysis data:
        
        Risk Analysis Data: {json.dumps(risk_data, indent=2, default=str)}
        
        The risk assessment should identify and analyze:
        1. Market risks (volatility, beta, correlation)
        2. Company-specific risks (financial leverage, profitability)
        3. Sector/industry risks
        4. Technical risks (trend reversals, support/resistance breaks)
        5. Valuation risks (overvaluation concerns)
        6. Liquidity risks
        7. Macroeconomic risks
        8. ESG and regulatory risks (if applicable)
        
        For each risk category:
        - Assess the probability and potential impact
        - Provide risk mitigation strategies
        - Highlight early warning indicators
        
        Risk assessment should be balanced - not overly pessimistic but realistic.
        Length: 4-5 paragraphs.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a risk management specialist providing comprehensive risk analysis."),
                HumanMessage(content=prompt)
            ])
            
            section = ReportSection(
                title="Risk Assessment",
                content=response.content,
                order=5,
                section_type="risk_assessment"
            )
            
            state["report_sections"].append(section)
            state["messages"].append("Risk assessment completed")
            
        except Exception as e:
            print(f"Error writing risk assessment: {e}")
            state["messages"].append(f"Error in risk assessment: {str(e)}")
        
        return state
    
    def _write_recommendations(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Write the recommendations section"""
        print("🎯 Writing investment recommendations...")
        
        analysis_data = state["analysis_data"]
        recommendations = analysis_data.get('recommendations', [])
        
        prompt = f"""
        Write a detailed investment recommendations section based on the complete analysis:
        
        Generated Recommendations: {recommendations[0] if recommendations else 'No specific recommendations available'}
        
        Analysis Summary: {analysis_data.get('insights', 'No insights available')}
        
        The recommendations section should include:
        1. Specific investment recommendations for each stock (Buy/Hold/Sell)
        2. Rationale for each recommendation
        3. Target price ranges (if determinable from analysis)
        4. Time horizon for recommendations
        5. Position sizing suggestions
        6. Portfolio construction considerations
        7. Rebalancing triggers and monitoring criteria
        8. Alternative scenarios and contingency plans
        
        Structure recommendations by:
        - Primary recommendation with confidence level
        - Supporting analysis and key factors
        - Risk-adjusted return expectations
        - Implementation strategy
        
        Be specific and actionable while acknowledging uncertainties.
        Length: 4-5 paragraphs.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a portfolio manager providing actionable investment recommendations."),
                HumanMessage(content=prompt)
            ])
            
            section = ReportSection(
                title="Investment Recommendations",
                content=response.content,
                order=6,
                section_type="recommendations"
            )
            
            state["report_sections"].append(section)
            state["messages"].append("Investment recommendations completed")
            
        except Exception as e:
            print(f"Error writing recommendations: {e}")
            state["messages"].append(f"Error in recommendations: {str(e)}")
        
        return state
    
    def _compile_final_report(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Compile all sections into the final report"""
        print("📄 Compiling final report...")
        
        metadata = state["report_metadata"]
        sections = sorted(state["report_sections"], key=lambda x: x.order)
        
        # Create report header
        header = f"""
FINANCIAL ANALYSIS REPORT
{metadata['symbols'][0] if len(metadata['symbols']) == 1 else f"Multi-Stock Analysis: {', '.join(metadata['symbols'])}"}

Report Date: {metadata['created_date']}
Analysis Period: {metadata['data_period']}
Analysis Type: {metadata['analysis_type'].title()}
Symbols Analyzed: {', '.join(metadata['symbols'])}

{'=' * 80}
"""
        
        # Compile sections - Only add each section once
        report_content = [header]
        
        for section in sections:
            section_header = f"\n{section.title.upper()}\n{'-' * len(section.title)}\n"
            report_content.append(section_header + section.content + "\n")
        
        # Add footer with disclaimers
        footer = f"""
{'=' * 80}

IMPORTANT DISCLAIMERS:
- This report is for informational purposes only and does not constitute investment advice
- Past performance does not guarantee future results
- All investments carry risk of loss
- Consult with a qualified financial advisor before making investment decisions
- Data and analysis are based on information available as of {metadata['created_date']}

Report generated by AI Financial Analysis System
Charts available at: {', '.join(state["analysis_data"].get('chart_paths', ['No charts generated']))}
"""
        
        final_report = '\n'.join(report_content) + footer
        state["final_report"] = final_report
        state["messages"].append("Final report compilation completed")
        
        return state
    
    def save_report(self, report_state: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save the generated report to a file"""
        if not filename:
            symbols = report_state["report_metadata"]["symbols"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if len(symbols) == 1:
                filename = f"{symbols[0]}_financial_report_{timestamp}.txt"
            else:
                filename = f"multi_stock_report_{timestamp}.txt"
        
        filepath = os.path.join(Config.REPORT_OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_state["final_report"])
        
        print(f"📄 Report saved to: {filepath}")
        return filepath

# Example usage and integration
if __name__ == "__main__":
    # Example of complete workflow
    print("🚀 Starting complete financial analysis and report generation workflow...")
    
    # Mock analysis data for testing
    mock_analysis = {
        'symbols_analyzed': ['AAPL'],
        'period': '6mo',
        'analysis_type': 'single',
        'technical_analysis': {
            'AAPL': {'signals': ['Test signal'], 'trend': 'bullish'}
        },
        'fundamental_analysis': {
            'AAPL': {'valuation': {'pe_ratio': 30}}
        },
        'sentiment_analysis': {
            'AAPL': {'sentiment': 'Positive'}
        },
        'insights': 'Test insights',
        'recommendations': ['HOLD'],
        'chart_paths': ['test.png']
    }
    
    # Generate report
    report_writer = FinancialReportWriter()
    report_result = report_writer.generate_report(
        analysis_data=mock_analysis,
        report_type="detailed",
        target_audience="investors"
    )
    
    print("✅ Test completed successfully!")