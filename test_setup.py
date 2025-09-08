#!/usr/bin/env python3
"""
Test script to verify all dependencies and basic functionality
"""

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import yfinance as yf
        print("✅ yfinance imported successfully")
    except ImportError as e:
        print(f"❌ yfinance import failed: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        print("✅ pandas and numpy imported successfully")
    except ImportError as e:
        print(f"❌ pandas/numpy import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain-openai imported successfully")
    except ImportError as e:
        print(f"❌ langchain-openai import failed: {e}")
        return False
    
    try:
        from langgraph.graph import StateGraph, END
        print("✅ langgraph imported successfully")
    except ImportError as e:
        print(f"❌ langgraph import failed: {e}")
        return False
    
    return True

def test_yfinance():
    """Test yfinance basic functionality"""
    print("\n📊 Testing yfinance data retrieval...")
    
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        hist = ticker.history(period="5d")
        
        if len(hist) > 0:
            print(f"✅ Successfully retrieved {len(hist)} days of AAPL data")
            print(f"   Current price: ${info.get('currentPrice', 'N/A')}")
            return True
        else:
            print("❌ No historical data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ yfinance test failed: {e}")
        return False

def test_config():
    """Test configuration setup"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        Config.validate()
        print("✅ Configuration validated successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        print("   Make sure you have a .env file with OPENAI_API_KEY")
        return False

def test_financial_data_agent():
    """Test the financial data agent"""
    print("\n💼 Testing Financial Data Agent...")
    
    try:
        from financial_data_agent import FinancialDataAgent
        agent = FinancialDataAgent()
        
        # Test with minimal data
        data = agent.fetch_stock_data("AAPL", period="5d")
        
        if data.symbol == "AAPL":
            print("✅ Financial Data Agent working correctly")
            print(f"   Company: {data.company_name}")
            print(f"   Current Price: ${data.current_price}")
            return True
        else:
            print("❌ Financial Data Agent returned unexpected data")
            return False
            
    except Exception as e:
        print(f"❌ Financial Data Agent test failed: {e}")
        return False

def test_langraph_agent():
    """Test the LangGraph agent (basic initialization)"""
    print("\n🔗 Testing LangGraph Agent initialization...")
    
    try:
        from langgraph_financial_agent import LangGraphFinancialAgent
        agent = LangGraphFinancialAgent()
        print("✅ LangGraph Financial Agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ LangGraph Agent test failed: {e}")
        return False

def test_graph_visualizer():
    """Test the graph visualizer"""
    print("\n🎨 Testing Graph Visualizer...")
    
    try:
        from graph_visualizer import LangGraphVisualizer
        visualizer = LangGraphVisualizer()
        print("✅ Graph Visualizer initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Graph Visualizer test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting system tests...\n")
    
    tests = [
        ("Imports", test_imports),
        ("YFinance", test_yfinance),
        ("Configuration", test_config),
        ("Financial Data Agent", test_financial_data_agent),
        ("LangGraph Agent", test_langraph_agent),
        ("Graph Visualizer", test_graph_visualizer)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready to use.")
        print("\nYou can now run:")
        print("   python main.py --symbols AAPL --period 6mo")
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the main application.")
        
        if not results.get("Configuration", False):
            print("\n📝 To fix configuration:")
            print("   1. Copy .env.template to .env")
            print("   2. Add your OpenAI API key to the .env file")
        
        if not results.get("Imports", False):
            print("\n📦 To fix import issues:")
            print("   pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)