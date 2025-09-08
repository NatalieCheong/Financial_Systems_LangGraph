#!/usr/bin/env python3
"""
Test script to verify the report duplication fix
"""

def test_report_generation():
    """Test the fixed report generation"""
    try:
        from financial_report_writer import FinancialReportWriter
        
        # Sample analysis data (minimal for testing)
        sample_analysis = {
            'symbols_analyzed': ['AAPL'],
            'period': '6mo',
            'analysis_type': 'single',
            'technical_analysis': {
                'AAPL': {'signals': ['Test signal'], 'trend': 'bullish'}
            },
            'fundamental_analysis': {
                'AAPL': {'valuation': {'pe_ratio': 30}, 'profitability': {'profit_margin': 25}}
            },
            'sentiment_analysis': {
                'AAPL': {'sentiment': 'Positive test sentiment', 'news_count': 5}
            },
            'insights': 'Test insights for AAPL analysis',
            'recommendations': ['HOLD - Test recommendation'],
            'chart_paths': ['test_chart.png'],
            'messages': ['Test message 1', 'Test message 2'],
            'errors': []
        }
        
        print("🧪 Testing report generation...")
        
        # Create report writer
        report_writer = FinancialReportWriter()
        
        # Generate report
        report_result = report_writer.generate_report(
            analysis_data=sample_analysis,
            report_type="detailed",
            target_audience="investors"
        )
        
        # Check report content
        final_report = report_result["final_report"]
        
        # Count section occurrences
        section_counts = {
            "EXECUTIVE SUMMARY": final_report.count("EXECUTIVE SUMMARY"),
            "MARKET ANALYSIS": final_report.count("MARKET ANALYSIS"), 
            "TECHNICAL ANALYSIS": final_report.count("TECHNICAL ANALYSIS"),
            "FUNDAMENTAL ANALYSIS": final_report.count("FUNDAMENTAL ANALYSIS"),
            "RISK ASSESSMENT": final_report.count("RISK ASSESSMENT"),
            "INVESTMENT RECOMMENDATIONS": final_report.count("INVESTMENT RECOMMENDATIONS")
        }
        
        print("\n📊 Section Count Analysis:")
        print("-" * 40)
        
        all_good = True
        for section, count in section_counts.items():
            status = "✅ GOOD" if count == 1 else f"❌ DUPLICATE ({count}x)"
            print(f"{section:25} {status}")
            if count != 1:
                all_good = False
        
        print("-" * 40)
        
        if all_good:
            print("🎉 SUCCESS: All sections appear exactly once!")
            print(f"📄 Report length: {len(final_report)} characters")
            return True
        else:
            print("⚠️ ISSUE: Some sections are still duplicated")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_sections_structure():
    """Test the report sections structure"""
    try:
        from financial_report_writer import ReportSection
        
        # Test section creation
        section = ReportSection(
            title="Test Section",
            content="Test content",
            order=1,
            section_type="test"
        )
        
        print(f"✅ Section structure test passed: {section.title}")
        return True
        
    except Exception as e:
        print(f"❌ Section structure test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Report Generation Fix")
    print("=" * 50)
    
    # Test 1: Section structure
    print("\n1. Testing section structure...")
    struct_ok = test_sections_structure()
    
    # Test 2: Report generation
    print("\n2. Testing report generation...")
    report_ok = test_report_generation()
    
    # Summary
    print(f"\n{'=' * 50}")
    print("TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Section Structure: {'✅ PASS' if struct_ok else '❌ FAIL'}")
    print(f"Report Generation: {'✅ PASS' if report_ok else '❌ FAIL'}")
    
    if struct_ok and report_ok:
        print("\n🎉 All tests passed! The duplication issue is fixed.")
        print("\nYou can now run:")
        print("   python main.py --symbols AAPL --period 6mo")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")