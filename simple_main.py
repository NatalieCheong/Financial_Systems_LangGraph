#!/usr/bin/env python3
"""
Simplified main application that works with basic dependencies
"""

import sys
import argparse
from typing import List

def test_basic_functionality():
    """Test if basic functionality works"""
    try:
        # Test yfinance
        import yfinance as yf
        print("✅ yfinance imported successfully")
        
        # Test basic data retrieval
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="5d")
        print(f"✅ Retrieved {len(hist)} days of data")
        
        # Test financial data agent
        from financial_data_agent import FinancialDataAgent
        agent = FinancialDataAgent()
        data = agent.fetch_stock_data("AAPL", period="5d")
        print(f"✅ Financial agent working: {data.company_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def simple_analysis(symbols: List[str], period: str = "6mo"):
    """Run a simplified analysis without LangGraph"""
    try:
        from financial_data_agent import FinancialDataAgent
        
        print(f"🚀 Starting simple analysis for: {', '.join(symbols)}")
        
        agent = FinancialDataAgent()
        results = {}
        
        for symbol in symbols:
            print(f"\n📊 Analyzing {symbol}...")
            data = agent.fetch_stock_data(symbol, period=period)
            
            # Create chart
            chart_path = agent.create_price_chart(data)
            
            results[symbol] = {
                'company_name': data.company_name,
                'current_price': data.current_price,
                'analysis': data.analysis_summary,
                'chart_path': chart_path
            }
            
            print(f"✅ {symbol} analysis completed")
            print(f"   Company: {data.company_name}")
            print(f"   Current Price: ${data.current_price:.2f}")
            print(f"   Chart saved: {chart_path}")
        
        # Simple summary
        print(f"\n{'='*50}")
        print("ANALYSIS SUMMARY")
        print(f"{'='*50}")
        
        for symbol, result in results.items():
            analysis = result['analysis']
            print(f"\n{symbol} ({result['company_name']}):")
            print(f"  Current Price: ${result['current_price']:.2f}")
            
            if analysis.get('price_change_1d'):
                print(f"  1-Day Change: {analysis['price_change_1d']:.2f}%")
            if analysis.get('price_change_1w'):
                print(f"  1-Week Change: {analysis['price_change_1w']:.2f}%")
            if analysis.get('rsi'):
                print(f"  RSI: {analysis['rsi']:.1f}")
            if analysis.get('trend_signal'):
                print(f"  Trend: {analysis['trend_signal']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Simple Financial Analysis")
    parser.add_argument('--symbols', nargs='+', required=True, help='Stock symbols')
    parser.add_argument('--period', default='6mo', help='Analysis period')
    parser.add_argument('--test', action='store_true', help='Run basic functionality test')
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running basic functionality test...")
        success = test_basic_functionality()
        return 0 if success else 1
    
    # Run simple analysis
    symbols = [s.upper() for s in args.symbols]
    success = simple_analysis(symbols, args.period)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Analysis interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)