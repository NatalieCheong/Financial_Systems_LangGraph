import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from config import Config

@dataclass
class FinancialData:
    """Data structure to hold financial information"""
    symbol: str
    company_name: str
    current_price: float
    price_history: pd.DataFrame
    financial_metrics: Dict[str, Any]
    news: List[Dict[str, Any]]
    analysis_summary: Dict[str, Any]

class FinancialDataAgent:
    """Agent responsible for fetching and processing financial data"""
    
    def __init__(self):
        self.config = Config()
    
    def fetch_stock_data(self, symbol: str, period: str = None, interval: str = None) -> FinancialData:
        """
        Fetch comprehensive stock data for a given symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            FinancialData object containing all relevant financial information
        """
        period = period or self.config.DEFAULT_PERIOD
        interval = interval or self.config.DEFAULT_INTERVAL
        
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get basic info
            info = ticker.info
            company_name = info.get('longName', symbol)
            current_price = info.get('currentPrice', 0)
            
            # Get historical data
            hist_data = ticker.history(period=period, interval=interval)
            
            # Get financial metrics
            financial_metrics = self._extract_financial_metrics(info)
            
            # Get recent news
            try:
                news = ticker.news[:5] if hasattr(ticker, 'news') else []
            except:
                news = []
            
            # Perform technical analysis
            analysis_summary = self._perform_technical_analysis(hist_data, financial_metrics)
            
            return FinancialData(
                symbol=symbol.upper(),
                company_name=company_name,
                current_price=current_price,
                price_history=hist_data,
                financial_metrics=financial_metrics,
                news=news,
                analysis_summary=analysis_summary
            )
            
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def _extract_financial_metrics(self, info: Dict) -> Dict[str, Any]:
        """Extract key financial metrics from yfinance info"""
        metrics = {
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'price_to_book': info.get('priceToBook'),
            'debt_to_equity': info.get('debtToEquity'),
            'roe': info.get('returnOnEquity'),
            'roa': info.get('returnOnAssets'),
            'profit_margin': info.get('profitMargins'),
            'revenue_growth': info.get('revenueGrowth'),
            'earnings_growth': info.get('earningsGrowth'),
            'dividend_yield': info.get('dividendYield'),
            'beta': info.get('beta'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'avg_volume': info.get('averageVolume'),
            'sector': info.get('sector'),
            'industry': info.get('industry')
        }
        
        # Clean up None values
        return {k: v for k, v in metrics.items() if v is not None}
    
    def _perform_technical_analysis(self, hist_data: pd.DataFrame, financial_metrics: Dict) -> Dict[str, Any]:
        """Perform basic technical analysis on historical data"""
        if hist_data.empty:
            return {}
        
        try:
            # Calculate moving averages
            hist_data['MA_20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['MA_50'] = hist_data['Close'].rolling(window=50).mean()
            
            # Calculate RSI
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            current_price = hist_data['Close'].iloc[-1]
            ma_20 = hist_data['MA_20'].iloc[-1] if not pd.isna(hist_data['MA_20'].iloc[-1]) else None
            ma_50 = hist_data['MA_50'].iloc[-1] if not pd.isna(hist_data['MA_50'].iloc[-1]) else None
            current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None
            
            # Price change analysis
            price_change_1d = ((current_price - hist_data['Close'].iloc[-2]) / hist_data['Close'].iloc[-2]) * 100 if len(hist_data) > 1 else 0
            price_change_1w = ((current_price - hist_data['Close'].iloc[-7]) / hist_data['Close'].iloc[-7]) * 100 if len(hist_data) > 7 else 0
            price_change_1m = ((current_price - hist_data['Close'].iloc[-30]) / hist_data['Close'].iloc[-30]) * 100 if len(hist_data) > 30 else 0
            
            # Volatility
            volatility = hist_data['Close'].pct_change().std() * np.sqrt(252) * 100  # Annualized
            
            return {
                'current_price': current_price,
                'ma_20': ma_20,
                'ma_50': ma_50,
                'rsi': current_rsi,
                'price_change_1d': price_change_1d,
                'price_change_1w': price_change_1w,
                'price_change_1m': price_change_1m,
                'volatility': volatility,
                'trend_signal': self._determine_trend_signal(current_price, ma_20, ma_50, current_rsi),
                'volume_trend': self._analyze_volume_trend(hist_data)
            }
            
        except Exception as e:
            print(f"Error in technical analysis: {e}")
            return {'error': str(e)}
    
    def _determine_trend_signal(self, price: float, ma_20: Optional[float], ma_50: Optional[float], rsi: Optional[float]) -> str:
        """Determine basic trend signal"""
        signals = []
        
        if ma_20 and ma_50:
            if price > ma_20 > ma_50:
                signals.append("bullish")
            elif price < ma_20 < ma_50:
                signals.append("bearish")
            else:
                signals.append("neutral")
        
        if rsi:
            if rsi > 70:
                signals.append("overbought")
            elif rsi < 30:
                signals.append("oversold")
        
        return ", ".join(signals) if signals else "neutral"
    
    def _analyze_volume_trend(self, hist_data: pd.DataFrame) -> str:
        """Analyze volume trend"""
        if len(hist_data) < 10:
            return "insufficient_data"
        
        recent_volume = hist_data['Volume'].tail(5).mean()
        historical_volume = hist_data['Volume'].head(-5).mean()
        
        if recent_volume > historical_volume * 1.2:
            return "increasing"
        elif recent_volume < historical_volume * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def compare_stocks(self, symbols: List[str], period: str = None) -> Dict[str, FinancialData]:
        """Compare multiple stocks"""
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.fetch_stock_data(symbol, period)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                continue
        return results
    
    def create_price_chart(self, financial_data: FinancialData, save_path: str = None) -> str:
        """Create a price chart for the financial data"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Price chart
        ax1.plot(financial_data.price_history.index, financial_data.price_history['Close'], label='Close Price')
        if 'MA_20' in financial_data.price_history.columns:
            ax1.plot(financial_data.price_history.index, financial_data.price_history['MA_20'], label='MA 20', alpha=0.7)
        if 'MA_50' in financial_data.price_history.columns:
            ax1.plot(financial_data.price_history.index, financial_data.price_history['MA_50'], label='MA 50', alpha=0.7)
        
        ax1.set_title(f'{financial_data.company_name} ({financial_data.symbol}) - Stock Price')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Volume chart
        ax2.bar(financial_data.price_history.index, financial_data.price_history['Volume'], alpha=0.7, color='orange')
        ax2.set_title('Trading Volume')
        ax2.set_ylabel('Volume')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            return save_path
        else:
            save_path = f"{Config.CHART_OUTPUT_DIR}/{financial_data.symbol}_chart.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            return save_path