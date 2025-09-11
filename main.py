#!/usr/bin/env python3
"""
Main application for Financial Analysis AI Agents with LangGraph
Integrates data collection, analysis, and report generation
"""

import argparse
import sys
from typing import List, Optional
from config import Config
from langgraph_financial_agent import LangGraphFinancialAgent
from financial_report_writer import FinancialReportWriter
from graph_visualizer import LangGraphVisualizer
import json

class FinancialAnalysisApp:
    """Main application class orchestrating the financial analysis workflow"""
    
    def __init__(self):
        """Initialize the application with agents"""
        try:
            Config.validate()
            self.financial_agent = LangGraphFinancialAgent()
            self.report_writer = FinancialReportWriter()
            self.visualizer = LangGraphVisualizer()
            print("✅ Financial Analysis Application initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize application: {e}")
            sys.exit(1)
    
    def run_analysis(self, 
                    symbols: List[str], 
                    analysis_type: str = "single",
                    period: str = "1y",
                    generate_report: bool = True,
                    report_type: str = "detailed",
                    save_results: bool = True) -> dict:
        """
        Run complete financial analysis workflow
        
        Args:
            symbols: List of stock symbols to analyze
            analysis_type: Type of analysis ('single', 'comparison', 'portfolio')
            period: Analysis period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y')
            generate_report: Whether to generate a written report
            report_type: Type of report ('executive', 'detailed', 'investor_presentation')
            save_results: Whether to save results to files
        
        Returns:
            Dictionary containing analysis results and file paths
        """
        results = {
            'success': False,
            'analysis_data': None,
            'report_data': None,
            'files_created': [],
            'errors': []
        }
        
        try:
            print(f"\n🚀 Starting Financial Analysis Workflow")
            print(f"Symbols: {', '.join(symbols)}")
            print(f"Analysis Type: {analysis_type}")
            print(f"Period: {period}")
            print("-" * 50)
            
            # Step 1: Run financial analysis
            print("Step 1: Running financial analysis...")
            analysis_state = self.financial_agent.analyze_stocks(
                symbols=symbols,
                analysis_type=analysis_type,
                period=period
            )
            
            analysis_summary = self.financial_agent.get_analysis_summary(analysis_state)
            results['analysis_data'] = analysis_summary
            
            # Check for analysis errors
            if analysis_summary['errors']:
                print(f"⚠️ Analysis completed with warnings: {analysis_summary['errors']}")
                results['errors'].extend(analysis_summary['errors'])
            
            print("✅ Financial analysis completed successfully")
            
            # Step 2: Generate report (if requested)
            if generate_report:
                print("\nStep 2: Generating financial report...")
                
                report_state = self.report_writer.generate_report(
                    analysis_data=analysis_summary,
                    report_type=report_type,
                    target_audience="investors"
                )
                
                results['report_data'] = report_state
                print("✅ Report generation completed successfully")
                
                # Step 3: Save files (if requested)
                if save_results:
                    print("\nStep 3: Saving results...")
                    
                    # Save report
                    report_filepath = self.report_writer.save_report(report_state)
                    results['files_created'].append(report_filepath)
                    
                    # Save analysis data as JSON
                    json_filepath = self._save_analysis_json(analysis_summary)
                    results['files_created'].append(json_filepath)
                    
                    # Chart files are already saved by the financial agent
                    results['files_created'].extend(analysis_summary.get('chart_paths', []))
                    
                    print("✅ All files saved successfully")
            
            # Step 4: Create visualizations
            print("\nStep 4: Creating workflow visualizations...")
            viz_files = self.create_workflow_visualizations(analysis_summary)
            results['files_created'].extend(viz_files)
            
            results['success'] = True
            
            # Display summary
            self._display_summary(results)
            
        except Exception as e:
            error_msg = f"Error in analysis workflow: {str(e)}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def _save_analysis_json(self, analysis_data: dict) -> str:
        """Save analysis data as JSON file"""
        from datetime import datetime
        
        symbols = analysis_data.get('symbols_analyzed', ['unknown'])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if len(symbols) == 1:
            filename = f"{symbols[0]}_analysis_{timestamp}.json"
        else:
            filename = f"multi_stock_analysis_{timestamp}.json"
        
        filepath = f"{Config.REPORT_OUTPUT_DIR}/{filename}"
        
        # Convert analysis data for JSON serialization
        json_data = self._prepare_json_data(analysis_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, default=str)
        
        return filepath
    
    def _prepare_json_data(self, data: dict) -> dict:
        """Prepare data for JSON serialization"""
        # Create a JSON-serializable copy of the data
        json_data = {}
        for key, value in data.items():
            if key == 'chart_paths':
                json_data[key] = value
            elif isinstance(value, dict):
                json_data[key] = {k: str(v) if not isinstance(v, (dict, list, str, int, float, bool, type(None))) else v 
                                 for k, v in value.items()}
            elif isinstance(value, list):
                json_data[key] = [str(item) if not isinstance(item, (dict, list, str, int, float, bool, type(None))) else item 
                                 for item in value]
            else:
                json_data[key] = value
        
        return json_data
    
    def create_workflow_visualizations(self, analysis_summary: dict = None) -> List[str]:
        """Create visual representations of the workflows"""
        created_files = []
        
        try:
            # Create workflow diagrams
            financial_graph = self.visualizer.visualize_financial_workflow()
            report_graph = self.visualizer.visualize_report_workflow()
            
            created_files.extend([financial_graph, report_graph])
            
            print(f"📊 Workflow diagrams created:")
            print(f"   Financial Analysis: {financial_graph}")
            print(f"   Report Writer: {report_graph}")
            
            # Create dashboard if analysis data is available
            if analysis_summary:
                dashboard = self.visualizer.create_combined_dashboard(analysis_summary)
                created_files.append(dashboard)
                print(f"   Analysis Dashboard: {dashboard}")
                
                # Create execution trace
                messages = analysis_summary.get('messages', [])
                if messages:
                    trace = self.visualizer.create_execution_trace(messages)
                    created_files.append(trace)
                    print(f"   Execution Trace: {trace}")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not create visualizations: {e}")
        
        return created_files
    
    def view_graphs_only(self) -> List[str]:
        """Create and display only the workflow graphs without running analysis"""
        print("🎨 Creating workflow visualization graphs...")
        return self.create_workflow_visualizations()
    
    def _display_summary(self, results: dict):
        """Display a summary of the analysis results"""
        print(f"\n{'='*60}")
        print("ANALYSIS WORKFLOW SUMMARY")
        print(f"{'='*60}")
        
        if results['success']:
            print("✅ Status: SUCCESS")
        else:
            print("❌ Status: FAILED")
        
        if results['analysis_data']:
            analysis = results['analysis_data']
            print(f"📊 Symbols Analyzed: {', '.join(analysis.get('symbols_analyzed', []))}")
            print(f"📅 Period: {analysis.get('period', 'N/A')}")
            print(f"📈 Charts Created: {len(analysis.get('chart_paths', []))}")
        
        if results['report_data']:
            print("📄 Report Generated: YES")
        else:
            print("📄 Report Generated: NO")
        
        if results['files_created']:
            print(f"💾 Files Created: {len(results['files_created'])}")
            for file_path in results['files_created']:
                print(f"   - {file_path}")
        
        if results['errors']:
            print(f"⚠️ Errors/Warnings: {len(results['errors'])}")
            for error in results['errors']:
                print(f"   - {error}")
        
        print(f"{'='*60}")

    def quick_analysis(self, symbol: str, period: str = "6mo") -> dict:
        """Run a quick analysis for a single symbol"""
        return self.run_analysis(
            symbols=[symbol.upper()],
            analysis_type="single",
            period=period,
            generate_report=True,
            report_type="detailed",
            save_results=True
        )
    
    def compare_stocks(self, symbols: List[str], period: str = "1y") -> dict:
        """Compare multiple stocks"""
        return self.run_analysis(
            symbols=[s.upper() for s in symbols],
            analysis_type="comparison",
            period=period,
            generate_report=True,
            report_type="detailed",
            save_results=True
        )
    
    def portfolio_analysis(self, symbols: List[str], period: str = "1y") -> dict:
        """Analyze a portfolio of stocks"""
        return self.run_analysis(
            symbols=[s.upper() for s in symbols],
            analysis_type="portfolio",
            period=period,
            generate_report=True,
            report_type="detailed",
            save_results=True
        )

def main():
    """Main entry point for command line usage"""
    parser = argparse.ArgumentParser(
        description="Financial Analysis AI Agents with LangGraph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze Apple stock
    python main.py --symbols AAPL --period 6mo
    
    # Compare multiple stocks
    python main.py --symbols AAPL MSFT GOOGL --analysis-type comparison --period 1y
    
    # Portfolio analysis
    python main.py --symbols AAPL MSFT GOOGL AMZN TSLA --analysis-type portfolio
    
    # Quick analysis without report
    python main.py --symbols AAPL --no-report
    
    # View workflow graphs only
    python main.py --view-graphs
        """
    )
    
    parser.add_argument(
        '--symbols', 
        nargs='+', 
        help='Stock symbols to analyze (e.g., AAPL MSFT GOOGL)'
    )
    
    parser.add_argument(
        '--analysis-type',
        choices=['single', 'comparison', 'portfolio'],
        default='single',
        help='Type of analysis to perform (default: single)'
    )
    
    parser.add_argument(
        '--period',
        choices=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
        default='1y',
        help='Analysis period (default: 1y)'
    )
    
    parser.add_argument(
        '--report-type',
        choices=['executive', 'detailed', 'investor_presentation'],
        default='detailed',
        help='Type of report to generate (default: detailed)'
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip report generation (analysis only)'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save results to files'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--view-graphs',
        action='store_true',
        help='Only create and view workflow graphs (no analysis)'
    )
    
    args = parser.parse_args()
    
    # Initialize application
    try:
        app = FinancialAnalysisApp()
    except Exception as e:
        print(f"❌ Failed to initialize application: {e}")
        return 1
    
    # Run analysis
    if args.view_graphs:
        # Only create workflow visualizations
        graph_files = app.view_graphs_only()
        print(f"\n📊 Created {len(graph_files)} visualization files")
        return 0
    elif args.interactive:
        run_interactive_mode(app)
        return 0
    else:
        # Validate symbols for non-interactive mode
        if not args.symbols:
            print("❌ Error: --symbols is required for non-interactive mode")
            print("Use --interactive for interactive mode or --view-graphs to see workflow diagrams")
            return 1
        
        symbols = [s.upper().strip() for s in args.symbols]
        
        results = app.run_analysis(
            symbols=symbols,
            analysis_type=args.analysis_type,
            period=args.period,
            generate_report=not args.no_report,
            report_type=args.report_type,
            save_results=not args.no_save
        )
        
        # Return appropriate exit code
        return 0 if results['success'] else 1

def run_interactive_mode(app: FinancialAnalysisApp):
    """Run the application in interactive mode"""
    print("\n🎯 Financial Analysis AI - Interactive Mode")
    print("=" * 50)
    
    while True:
        print("\nAvailable options:")
        print("1. Quick Analysis (single stock)")
        print("2. Compare Stocks")
        print("3. Portfolio Analysis")
        print("4. Custom Analysis")
        print("5. View Workflow Graphs")
        print("6. Exit")
        
        try:
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == "1":
                symbol = input("Enter stock symbol: ").strip().upper()
                period = input("Enter period (1mo/3mo/6mo/1y/2y): ").strip() or "6mo"
                print(f"\n🚀 Running quick analysis for {symbol}...")
                app.quick_analysis(symbol, period)
                
            elif choice == "2":
                symbols_input = input("Enter stock symbols (space-separated): ").strip()
                symbols = [s.upper() for s in symbols_input.split()]
                period = input("Enter period (6mo/1y/2y): ").strip() or "1y"
                print(f"\n🚀 Comparing stocks: {', '.join(symbols)}...")
                app.compare_stocks(symbols, period)
                
            elif choice == "3":
                symbols_input = input("Enter portfolio symbols (space-separated): ").strip()
                symbols = [s.upper() for s in symbols_input.split()]
                period = input("Enter period (6mo/1y/2y): ").strip() or "1y"
                print(f"\n🚀 Analyzing portfolio: {', '.join(symbols)}...")
                app.portfolio_analysis(symbols, period)
                
            elif choice == "4":
                print("\nCustom Analysis Configuration:")
                symbols_input = input("Stock symbols (space-separated): ").strip()
                symbols = [s.upper() for s in symbols_input.split()]
                
                analysis_type = input("Analysis type (single/comparison/portfolio): ").strip() or "single"
                period = input("Period (1mo/3mo/6mo/1y/2y/5y): ").strip() or "1y"
                report_type = input("Report type (executive/detailed/investor_presentation): ").strip() or "detailed"
                
                generate_report = input("Generate report? (y/n): ").strip().lower() != 'n'
                save_results = input("Save results? (y/n): ").strip().lower() != 'n'
                
                print(f"\n🚀 Running custom analysis...")
                app.run_analysis(
                    symbols=symbols,
                    analysis_type=analysis_type,
                    period=period,
                    generate_report=generate_report,
                    report_type=report_type,
                    save_results=save_results
                )
                
            elif choice == "5":
                print(f"\n🎨 Creating workflow visualizations...")
                graph_files = app.view_graphs_only()
                print(f"📊 Created {len(graph_files)} visualization files")
                
            elif choice == "6":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)