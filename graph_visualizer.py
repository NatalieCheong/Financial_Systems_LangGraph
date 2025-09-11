#!/usr/bin/env python3
"""
Graph Visualization utilities for LangGraph Financial Analysis workflows
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
from typing import Dict, List, Tuple, Any
import os
from datetime import datetime
from config import Config

class LangGraphVisualizer:
    """Visualize LangGraph workflows and execution traces"""
    
    def __init__(self):
        self.config = Config()
        
    def visualize_financial_workflow(self, save_path: str = None) -> str:
        """
        Create a visual representation of the Financial Analysis workflow
        
        Args:
            save_path: Path to save the graph image
            
        Returns:
            Path to the saved graph image
        """
        # Create figure and axis
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Define workflow nodes and their positions
        nodes = {
            "START": (5, 11, "start"),
            "Data Collection": (5, 9.5, "process"),
            "Technical Analysis": (2, 8, "analysis"),
            "Fundamental Analysis": (5, 8, "analysis"),
            "Market Sentiment": (8, 8, "analysis"),
            "Generate Insights": (5, 6.5, "ai"),
            "Create Visualizations": (2, 5, "output"),
            "Final Recommendations": (8, 5, "output"),
            "END": (5, 3.5, "end")
        }
        
        # Define edges (connections between nodes)
        edges = [
            ("START", "Data Collection"),
            ("Data Collection", "Technical Analysis"),
            ("Data Collection", "Fundamental Analysis"),
            ("Data Collection", "Market Sentiment"),
            ("Technical Analysis", "Generate Insights"),
            ("Fundamental Analysis", "Generate Insights"),
            ("Market Sentiment", "Generate Insights"),
            ("Generate Insights", "Create Visualizations"),
            ("Generate Insights", "Final Recommendations"),
            ("Create Visualizations", "END"),
            ("Final Recommendations", "END")
        ]
        
        # Color scheme for different node types
        colors = {
            "start": "#4CAF50",      # Green
            "process": "#2196F3",    # Blue
            "analysis": "#FF9800",   # Orange
            "ai": "#9C27B0",         # Purple
            "output": "#F44336",     # Red
            "end": "#607D8B"         # Blue Grey
        }
        
        # Draw nodes
        for name, (x, y, node_type) in nodes.items():
            # Create rounded rectangle for node
            bbox = FancyBboxPatch(
                (x-0.8, y-0.3), 1.6, 0.6,
                boxstyle="round,pad=0.1",
                facecolor=colors[node_type],
                edgecolor='black',
                linewidth=1.5,
                alpha=0.8
            )
            ax.add_patch(bbox)
            
            # Add text
            ax.text(x, y, name, ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='white')
        
        # Draw edges
        for start_node, end_node in edges:
            start_pos = nodes[start_node][:2]
            end_pos = nodes[end_node][:2]
            
            # Calculate arrow position
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            
            # Adjust start and end points to node edges
            if abs(dx) > abs(dy):  # Horizontal connection
                if dx > 0:  # Right
                    start_x, start_y = start_pos[0] + 0.8, start_pos[1]
                    end_x, end_y = end_pos[0] - 0.8, end_pos[1]
                else:  # Left
                    start_x, start_y = start_pos[0] - 0.8, start_pos[1]
                    end_x, end_y = end_pos[0] + 0.8, end_pos[1]
            else:  # Vertical connection
                if dy > 0:  # Up
                    start_x, start_y = start_pos[0], start_pos[1] + 0.3
                    end_x, end_y = end_pos[0], end_pos[1] - 0.3
                else:  # Down
                    start_x, start_y = start_pos[0], start_pos[1] - 0.3
                    end_x, end_y = end_pos[0], end_pos[1] + 0.3
            
            # Draw arrow
            ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        
        # Add title
        ax.text(5, 11.8, 'LangGraph Financial Analysis Workflow', 
               ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Add legend
        legend_elements = [
            mpatches.Patch(color=colors['start'], label='Start/Entry'),
            mpatches.Patch(color=colors['process'], label='Data Processing'),
            mpatches.Patch(color=colors['analysis'], label='Analysis'),
            mpatches.Patch(color=colors['ai'], label='AI/LLM Processing'),
            mpatches.Patch(color=colors['output'], label='Output Generation'),
            mpatches.Patch(color=colors['end'], label='End/Exit')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
        
        # Save the graph
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"{Config.CHART_OUTPUT_DIR}/financial_workflow_{timestamp}.png"
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"📊 Financial workflow graph saved to: {save_path}")
        
        return save_path
    
    def visualize_report_workflow(self, save_path: str = None) -> str:
        """
        Create a visual representation of the Report Writer workflow
        
        Args:
            save_path: Path to save the graph image
            
        Returns:
            Path to the saved graph image
        """
        # Create figure and axis
        fig, ax = plt.subplots(1, 1, figsize=(12, 14))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # Define workflow nodes and their positions
        nodes = {
            "START": (5, 15, "start"),
            "Analyze Data": (5, 13.5, "process"),
            "Executive Summary": (5, 12, "writing"),
            "Market Analysis": (5, 10.5, "writing"),
            "Technical Analysis": (5, 9, "writing"),
            "Fundamental Analysis": (5, 7.5, "writing"),
            "Risk Assessment": (5, 6, "writing"),
            "Recommendations": (5, 4.5, "writing"),
            "Compile Report": (5, 3, "output"),
            "END": (5, 1.5, "end")
        }
        
        # Define edges (linear workflow)
        edges = [
            ("START", "Analyze Data"),
            ("Analyze Data", "Executive Summary"),
            ("Executive Summary", "Market Analysis"),
            ("Market Analysis", "Technical Analysis"),
            ("Technical Analysis", "Fundamental Analysis"),
            ("Fundamental Analysis", "Risk Assessment"),
            ("Risk Assessment", "Recommendations"),
            ("Recommendations", "Compile Report"),
            ("Compile Report", "END")
        ]
        
        # Color scheme for different node types
        colors = {
            "start": "#4CAF50",      # Green
            "process": "#2196F3",    # Blue
            "writing": "#FF9800",    # Orange
            "output": "#F44336",     # Red
            "end": "#607D8B"         # Blue Grey
        }
        
        # Draw nodes
        for name, (x, y, node_type) in nodes.items():
            # Create rounded rectangle for node
            bbox = FancyBboxPatch(
                (x-1, y-0.3), 2, 0.6,
                boxstyle="round,pad=0.1",
                facecolor=colors[node_type],
                edgecolor='black',
                linewidth=1.5,
                alpha=0.8
            )
            ax.add_patch(bbox)
            
            # Add text
            ax.text(x, y, name, ha='center', va='center', 
                   fontsize=10, fontweight='bold', color='white')
        
        # Draw edges
        for start_node, end_node in edges:
            start_pos = nodes[start_node][:2]
            end_pos = nodes[end_node][:2]
            
            # Vertical connections
            start_x, start_y = start_pos[0], start_pos[1] - 0.3
            end_x, end_y = end_pos[0], end_pos[1] + 0.3
            
            # Draw arrow
            ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Add title
        ax.text(5, 15.8, 'LangGraph Report Writer Workflow', 
               ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Add legend
        legend_elements = [
            mpatches.Patch(color=colors['start'], label='Start/Entry'),
            mpatches.Patch(color=colors['process'], label='Data Processing'),
            mpatches.Patch(color=colors['writing'], label='Report Writing'),
            mpatches.Patch(color=colors['output'], label='Output Generation'),
            mpatches.Patch(color=colors['end'], label='End/Exit')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        # Save the graph
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"{Config.CHART_OUTPUT_DIR}/report_workflow_{timestamp}.png"
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"📝 Report workflow graph saved to: {save_path}")
        
        return save_path
    
    def create_execution_trace(self, messages: List[str], save_path: str = None) -> str:
        """
        Create a visual execution trace showing workflow progress
        
        Args:
            messages: List of execution messages from the workflow
            save_path: Path to save the trace image
            
        Returns:
            Path to the saved trace image
        """
        if not messages:
            print("No execution messages to visualize")
            return ""
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(12, max(8, len(messages) * 0.6)))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(messages) + 2)
        ax.axis('off')
        
        # Add title
        ax.text(5, len(messages) + 1.5, 'Workflow Execution Trace', 
               ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Draw execution steps
        for i, message in enumerate(reversed(messages)):
            y_pos = i + 1
            
            # Create step box
            bbox = FancyBboxPatch(
                (0.5, y_pos - 0.2), 9, 0.4,
                boxstyle="round,pad=0.05",
                facecolor='lightblue',
                edgecolor='darkblue',
                linewidth=1,
                alpha=0.7
            )
            ax.add_patch(bbox)
            
            # Add step number and message
            ax.text(1, y_pos, f"Step {len(messages) - i}:", 
                   ha='left', va='center', fontsize=10, fontweight='bold')
            ax.text(2.5, y_pos, message, 
                   ha='left', va='center', fontsize=9)
            
            # Add checkmark
            ax.text(9.5, y_pos, "✓", ha='center', va='center', 
                   fontsize=12, color='green', fontweight='bold')
        
        # Save the trace
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"{Config.CHART_OUTPUT_DIR}/execution_trace_{timestamp}.png"
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"📋 Execution trace saved to: {save_path}")
        
        return save_path
    
    def create_combined_dashboard(self, analysis_summary: Dict[str, Any], save_path: str = None) -> str:
        """
        Create a comprehensive dashboard showing workflow and results
        
        Args:
            analysis_summary: Summary from financial analysis
            save_path: Path to save the dashboard
            
        Returns:
            Path to the saved dashboard
        """
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        
        # Create grid layout
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.2)
        
        # Title
        fig.suptitle('LangGraph Financial Analysis Dashboard', fontsize=20, fontweight='bold', y=0.95)
        
        # Workflow diagram (top section)
        ax1 = fig.add_subplot(gs[0, :])
        self._draw_mini_workflow(ax1)
        
        # Analysis summary (middle left)
        ax2 = fig.add_subplot(gs[1, 0])
        self._draw_analysis_summary(ax2, analysis_summary)
        
        # Execution status (middle center)
        ax3 = fig.add_subplot(gs[1, 1])
        self._draw_execution_status(ax3, analysis_summary)
        
        # Output files (middle right)
        ax4 = fig.add_subplot(gs[1, 2])
        self._draw_output_files(ax4, analysis_summary)
        
        # Messages/logs (bottom section)
        ax5 = fig.add_subplot(gs[2, :])
        self._draw_messages_log(ax5, analysis_summary.get('messages', []))
        
        # Save dashboard
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"{Config.CHART_OUTPUT_DIR}/analysis_dashboard_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"📊 Analysis dashboard saved to: {save_path}")
        
        return save_path
    
    def _draw_mini_workflow(self, ax):
        """Draw a simplified workflow diagram"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 2)
        ax.axis('off')
        ax.set_title('Workflow Progress', fontsize=14, fontweight='bold', pad=20)
        
        # Simple linear workflow
        steps = ["Data", "Analysis", "Insights", "Charts", "Report"]
        colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336"]
        
        for i, (step, color) in enumerate(zip(steps, colors)):
            x = 1 + i * 1.8
            
            # Draw circle
            circle = plt.Circle((x, 1), 0.3, facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(circle)
            
            # Add text
            ax.text(x, 1, str(i+1), ha='center', va='center', 
                   fontsize=10, fontweight='bold', color='white')
            ax.text(x, 0.5, step, ha='center', va='center', fontsize=8)
            
            # Draw arrow (except for last step)
            if i < len(steps) - 1:
                ax.annotate('', xy=(x + 1.2, 1), xytext=(x + 0.6, 1),
                           arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    def _draw_analysis_summary(self, ax, analysis_summary):
        """Draw analysis summary box"""
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Analysis Summary', fontsize=12, fontweight='bold')
        
        # Create summary text
        symbols = analysis_summary.get('symbols_analyzed', ['N/A'])
        period = analysis_summary.get('period', 'N/A')
        analysis_type = analysis_summary.get('analysis_type', 'N/A')
        
        summary_text = f"""
Symbols: {', '.join(symbols)}
Period: {period}
Type: {analysis_type.title()}
Charts: {len(analysis_summary.get('chart_paths', []))}
        """.strip()
        
        ax.text(0.05, 0.95, summary_text, ha='left', va='top', fontsize=10,
               transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", 
               facecolor='lightgray', alpha=0.5))
    
    def _draw_execution_status(self, ax, analysis_summary):
        """Draw execution status"""
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Execution Status', fontsize=12, fontweight='bold')
        
        # Check status
        has_technical = bool(analysis_summary.get('technical_analysis'))
        has_fundamental = bool(analysis_summary.get('fundamental_analysis'))
        has_sentiment = bool(analysis_summary.get('sentiment_analysis'))
        has_insights = bool(analysis_summary.get('insights'))
        
        status_items = [
            ("Technical Analysis", has_technical),
            ("Fundamental Analysis", has_fundamental),
            ("Sentiment Analysis", has_sentiment),
            ("AI Insights", has_insights)
        ]
        
        y_positions = [0.8, 0.6, 0.4, 0.2]
        
        for (item, status), y_pos in zip(status_items, y_positions):
            color = "green" if status else "red"
            symbol = "✓" if status else "✗"
            ax.text(0.05, y_pos, f"{symbol} {item}", ha='left', va='center',
                   fontsize=10, color=color, transform=ax.transAxes)
    
    def _draw_output_files(self, ax, analysis_summary):
        """Draw output files information"""
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Generated Files', fontsize=12, fontweight='bold')
        
        chart_count = len(analysis_summary.get('chart_paths', []))
        
        file_info = f"""
Charts: {chart_count} files
Reports: Available
JSON Data: Available
        """.strip()
        
        ax.text(0.05, 0.8, file_info, ha='left', va='top', fontsize=10,
               transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", 
               facecolor='lightgreen', alpha=0.5))
    
    def _draw_messages_log(self, ax, messages):
        """Draw execution messages log"""
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Execution Log', fontsize=12, fontweight='bold')
        
        if not messages:
            ax.text(0.5, 0.5, "No execution messages", ha='center', va='center',
                   fontsize=10, style='italic', transform=ax.transAxes)
            return
        
        # Show last few messages
        recent_messages = messages[-5:] if len(messages) > 5 else messages
        
        log_text = "\n".join([f"• {msg}" for msg in recent_messages])
        
        ax.text(0.05, 0.95, log_text, ha='left', va='top', fontsize=9,
               transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", 
               facecolor='lightyellow', alpha=0.7))

# Integration functions for existing agents
def add_visualization_to_main():
    """Function to integrate visualization into main.py"""
    return """
# Add this to your main.py imports:
from graph_visualizer import LangGraphVisualizer

# Add this method to FinancialAnalysisApp class:
def create_workflow_visualizations(self, analysis_summary=None):
    '''Create visual representations of the workflows'''
    visualizer = LangGraphVisualizer()
    
    # Create workflow diagrams
    financial_graph = visualizer.visualize_financial_workflow()
    report_graph = visualizer.visualize_report_workflow()
    
    print(f"📊 Workflow diagrams created:")
    print(f"   Financial Analysis: {financial_graph}")
    print(f"   Report Writer: {report_graph}")
    
    # Create dashboard if analysis data is available
    if analysis_summary:
        dashboard = visualizer.create_combined_dashboard(analysis_summary)
        print(f"   Analysis Dashboard: {dashboard}")
        
        # Create execution trace
        messages = analysis_summary.get('messages', [])
        if messages:
            trace = visualizer.create_execution_trace(messages)
            print(f"   Execution Trace: {trace}")
    
    return [financial_graph, report_graph]
"""

if __name__ == "__main__":
    # Example usage
    visualizer = LangGraphVisualizer()
    
    # Create workflow visualizations
    print("Creating workflow visualizations...")
    financial_graph = visualizer.visualize_financial_workflow()
    report_graph = visualizer.visualize_report_workflow()
    
    # Example execution trace
    example_messages = [
        "Collected data for 1 symbols",
        "Technical analysis completed",
        "Fundamental analysis completed", 
        "Market sentiment analysis completed",
        "Insights generated successfully",
        "Created 1 visualizations",
        "Investment recommendations generated"
    ]
    
    trace_graph = visualizer.create_execution_trace(example_messages)
    
    print(f"\n✅ Visualization files created:")
    print(f"📊 Financial workflow: {financial_graph}")
    print(f"📝 Report workflow: {report_graph}")
    print(f"📋 Execution trace: {trace_graph}")