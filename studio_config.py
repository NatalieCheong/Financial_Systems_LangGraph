from langgraph_financial_agent import LangGraphFinancialAgent

# Export your graph for Studio
agent = LangGraphFinancialAgent()
graph = agent.graph

# This makes it available to Studio
__all__ = ["graph"]