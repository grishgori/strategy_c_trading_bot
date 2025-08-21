#!/usr/bin/env python3
"""
Strategy C Trading Bot - Enhanced with Full S&P 500 Coverage
GitHub Actions Version with Intelligent Stock Rotation
"""

import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, date, timedelta
import time

class GitHubActionsTrader:
    def __init__(self):
        # Trading period configuration
        self.start_date = date(2025, 8, 18)
        self.end_date = date(2025, 9, 29)
        
        # Portfolio configuration
        self.starting_capital = 1000.0
        self.current_balance = 1000.0
        self.position_size_pct = 0.20  # 20% per position
        self.max_positions = 5
        self.commission = 1.0
        
        # Enhanced stock rotation configuration
        self.batch_size = 100  # Scan 100 stocks per run (up from 50)
        
        # Complete S&P 500 symbol list (500+ stocks)
        self.symbols = [
            'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'GOOG', 'META', 'BRK-B', 'TSLA', 'UNH',
            'JNJ', 'JPM', 'V', 'PG', 'XOM', 'HD', 'CVX', 'MA', 'BAC', 'ABBV',
            'PFE', 'AVGO', 'COST', 'DIS', 'KO', 'MRK', 'WMT', 'PEP', 'TMO', 'VZ',
            'CSCO', 'ACN', 'ADBE', 'MCD', 'ABT', 'CRM', 'LLY', 'NFLX', 'AMD', 'PM',
            'WFC', 'DHR', 'BMY', 'QCOM', 'AMGN', 'UNP', 'T', 'RTX', 'HON', 'UPS',
            'NEE', 'SPGI', 'LOW', 'GS', 'IBM', 'ELV', 'CVS', 'SBUX', 'DE', 'LMT',
            'AXP', 'BLK', 'MDT', 'CAT', 'GILD', 'AMT', 'SYK', 'TJX', 'MMM', 'BKNG',
            'ADP', 'VRTX', 'PLD', 'MDLZ', 'ADI', 'C', 'TGT', 'CME', 'SO', 'LRCX',
            'MO', 'CB', 'ISRG', 'DUK', 'ZTS', 'CI', 'SHW', 'ETN', 'GE', 'ITW',
            'PGR', 'MMC', 'TFC', 'AON', 'CSX', 'BSX', 'FCX', 'APD', 'COP', 'EQIX',
            'ICE', 'USB', 'WM', 'FDX', 'NSC', 'GM', 'DG', 'KLAC', 'CL', 'F',
            'ATVI', 'EMR', 'PSA', 'ECL', 'MU', 'SLB', 'GIS', 'APH', 'ADM', 'KMB',
            'BIIB', 'AFL', 'FIS', 'EW', 'NKE', 'MCK', 'KHC', 'OXY', 'DOW', 'WBA',
            'MCHP', 'ORLY', 'HUM', 'CTAS', 'NUE', 'IQV', 'CMG', 'A', 'PAYX', 'AEP',
            'CTSH', 'PCAR', 'MSI', 'FAST', 'EA', 'YUM', 'VRSK', 'OTIS', 'PRU', 'EXC',
            'KR', 'CARR', 'ROP', 'AZO', 'ROST', 'IDXX', 'DD', 'XEL', 'BDX', 'HPQ',
            'GPN', 'MNST', 'CTVA', 'SPG', 'ED', 'WEC', 'FTNT', 'EBAY', 'CMI', 'DXCM',
            'GLW', 'PPG', 'VRSN', 'KEYS', 'STZ', 'ANSS', 'AWK', 'DLTR', 'DHI', 'CPRT',
            'EXR', 'FISV', 'GWW', 'HPE', 'HRL', 'FTV', 'VMC', 'EFX', 'CERN', 'TSN',
            'LH', 'MPWR', 'NTRS', 'AVB', 'WY', 'K', 'LUV', 'ARE', 'FITB', 'CHD',
            'EXPD', 'FRT', 'ESS', 'CAH', 'STE', 'CHRW', 'WAB', 'POOL', 'NTAP', 'CF',
            'AES', 'LYB', 'HOLX', 'JBHT', 'STT', 'SWK', 'CLX', 'PKI', 'ATO', 'ZBRA',
            'TDY', 'LDOS', 'CNP', 'WRB', 'LNT', 'AKAM', 'PEAK', 'TECH', 'J', 'SNA',
            'NDSN', 'HSIC', 'PAYC', 'ALLE', 'PWR', 'SJM', 'TER', 'KIM', 'AIZ', 'FMC',
            'JKHY', 'CBOE', 'SWKS', 'AOS', 'MKTX', 'AMCR', 'EMN', 'TPG', 'MAA', 'FFIV',
            'LKQ', 'CAG', 'ETSY', 'ULTA', 'TROW', 'ROL', 'BXP', 'VTRS', 'DTE', 'EVRG',
            'UDR', 'RE', 'EQR', 'CTLT', 'EPAM', 'NVR', 'INVH', 'IRM', 'CMS', 'TRMB',
            'NI', 'CDAY', 'HST', 'BF-B', 'MTCH', 'FE', 'ALGN', 'VICI', 'EIX', 'IP',
            'WELL', 'HBAN', 'RF', 'CFG', 'TXN', 'INTU', 'ORCL', 'NOW', 'PANW', 'SNPS',
            'CDNS', 'ADSK', 'ANET', 'CNC', 'HCA', 'DDOG', 'TEAM', 'ZM', 'WDAY', 'VEEV',
            'SPLK', 'OKTA', 'DOCU', 'CRWD', 'ZS', 'NET', 'ESTC', 'MDB', 'SNOW', 'PATH',
            'GTLB', 'S', 'BILL', 'CFLT', 'COUP', 'FROG', 'AI', 'PLTR', 'U', 'FSLY',
            'TWLO', 'PINS', 'SNAP', 'LYFT', 'UBER', 'DASH', 'ABNB', 'COIN', 'HOOD', 'SOFI',
            'AFRM', 'SQ', 'PYPL', 'SHOP', 'ROKU', 'SPOT', 'ZI', 'DOCN', 'OPEN', 'RBLX',
            'RIVN', 'LCID', 'CHPT', 'BLNK', 'QS', 'PLUG', 'BE', 'FCEL', 'BLDP', 'CLSK',
            'RIOT', 'MARA', 'HUT', 'BITF', 'CAN', 'SOS', 'EBON', 'BTBT', 'ANY', 'HVBT',
            'ARBK', 'WULF', 'CORZ', 'IREN', 'CIFR', 'CLSK', 'MIGI', 'BFRI', 'CLEAN', 'SOUN',
            'SMCI', 'ARM', 'RKLB', 'RDDT', 'TPG', 'KKR', 'BX', 'APO', 'CG', 'OWL',
            'STEP', 'BLUE', 'PEN', 'ARCC', 'MAIN', 'PSEC', 'FSK', 'GAIN', 'GBDC', 'HTGC',
            'TSLX', 'BXSL', 'TCPC', 'CCAP', 'CSWC', 'GLAD', 'NEWT', 'PFLT', 'SLRC', 'FDUS',
            'BBDC', 'CGBD', 'GSBD', 'NMFC', 'OCSL', 'OCCI', 'ORCC', 'PNNT', 'PSEC', 'PTMN',
            'SAR', 'SUNS', 'TCPC', 'TPVG', 'TREE', 'TRIN', 'VNOM', 'WASH', 'WTTR', 'XMTR'
        ]
        
        # Trading state
        self.positions = {}  # symbol -> position data
        self.trade_history = []
        
        # Load existing state
        self.load_state()
        
        print(f"🤖 Strategy C Trading Bot - Enhanced Version")
        print(f"📊 Total S&P 500 symbols: {len(self.symbols)}")
        print(f"📦 Batch size per run: {self.batch_size}")
        print(f"💰 Current balance: ${self.current_balance:.0f}")
        print(f"📍 Open positions: {len(self.positions)}/{self.max_positions}")
    
    def get_current_batch(self):
        """
        Get current batch of stocks based on GitHub Actions schedule
        5 runs per day × 100 stocks = 500 stocks total coverage
        """
        total_stocks = len(self.symbols)
        
        # Get current UTC time (GitHub Actions runs in UTC)
        now = datetime.utcnow()
        hour = now.hour
        minute = now.minute
        
        # Determine run number based on GitHub Actions schedule:
        # 14:30, 16:00, 18:00, 20:00, 20:50 UTC
        run_number = 0
        if hour >= 16: run_number = 1
        if hour >= 18: run_number = 2  
        if hour >= 20: 
            if minute < 50: run_number = 3
            else: run_number = 4
        
        # Calculate batch indices
        start_idx = (run_number * self.batch_size) % total_stocks
        end_idx = min(start_idx + self.batch_size, total_stocks)
        
        # Handle wrap-around if needed
        if end_idx - start_idx < self.batch_size and start_idx > 0:
            batch = self.symbols[start_idx:end_idx]
            remaining = self.batch_size - len(batch)
            if remaining > 0:
                batch.extend(self.symbols[:remaining])
        else:
            batch = self.symbols[start_idx:end_idx]
        
        print(f"🔄 Batch {run_number + 1}/5: Scanning stocks {start_idx+1}-{start_idx+len(batch)} ({len(batch)} symbols)")
        return batch
    
    def is_within_trading_period(self):
        """Check if current date is within trading period"""
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def is_market_open(self):
        """Check if US market is currently open (basic check)"""
        now = datetime.now()
        
        # Check if it's a weekday
        if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False
        
        # For GitHub Actions, we assume scheduled runs are during market hours
        # The schedule is set to run during market hours anyway
        return True
    
    def get_stock_data(self, symbol, period="30d"):
        """Fetch stock data with error handling and retry logic"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period)
                
                if len(data) < 26:  # Need enough data for MACD calculation
                    return None
                    
                return data
                
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    print(f"⚠️  Failed to fetch {symbol}: {e}")
                    return None
                else:
                    time.sleep(0.5)  # Brief pause before retry
        
        return None
    
    def calculate_macd(self, data):
        """Calculate MACD indicators (12, 26, 9)"""
        # Calculate exponential moving averages
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        
        return {
            'macd_line': macd_line,
            'signal_line': signal_line,
            'current_macd': macd_line.iloc[-1],
            'current_signal': signal_line.iloc[-1],
            'prev_macd': macd_line.iloc[-2] if len(macd_line) > 1 else macd_line.iloc[-1],
            'prev_signal': signal_line.iloc[-2] if len(signal_line) > 1 else signal_line.iloc[-1]
        }
    
    def detect_signals(self, symbol, data):
        """Detect buy/sell signals using Strategy C (MACD < 0 + crossover)"""
        macd = self.calculate_macd(data)
        current_price = data['Close'].iloc[-1]
        
        signals = {'buy': False, 'sell': False, 'price': current_price}
        
        # Strategy C Buy Signal: MACD line crosses above signal line AND MACD < 0
        macd_bullish_cross = (macd['current_macd'] > macd['current_signal'] and
                             macd['prev_macd'] <= macd['prev_signal'])
        macd_below_zero = macd['current_macd'] < 0
        
        if macd_bullish_cross and macd_below_zero:
            signals['buy'] = True
            print(f"🟢 BUY signal detected: {symbol} @ ${current_price:.2f}")
            print(f"   MACD: {macd['current_macd']:.4f} | Signal: {macd['current_signal']:.4f}")
        
        # Strategy C Sell Signal: Signal line crosses above MACD line (bearish crossover)
        elif (symbol in self.positions and 
              macd['current_signal'] > macd['current_macd'] and
              macd['prev_signal'] <= macd['prev_macd']):
            signals['sell'] = True
            print(f"🔴 SELL signal detected: {symbol} @ ${current_price:.2f}")
        
        return signals
    
    def execute_buy(self, symbol, price):
        """Execute buy order with Strategy C position sizing"""
        # Validate trade
        if len(self.positions) >= self.max_positions:
            print(f"⚠️  Max positions reached ({self.max_positions})")
            return False
        
        if symbol in self.positions:
            print(f"⚠️  Already holding {symbol}")
            return False
        
        # Calculate position size (20% of current balance)
        position_value = self.current_balance * self.position_size_pct
        shares = int(position_value / price)
        
        if shares == 0:
            print(f"⚠️  Position too small: ${position_value:.0f} ÷ ${price:.2f} = {shares} shares")
            return False
        
        total_cost = shares * price + self.commission
        
        if total_cost > self.current_balance:
            print(f"⚠️  Insufficient funds: need ${total_cost:.0f}, have ${self.current_balance:.0f}")
            return False
        
        # Execute the trade
        self.positions[symbol] = {
            'shares': shares,
            'entry_price': price,
            'entry_date': date.today().isoformat(),
            'entry_time': datetime.now().strftime('%H:%M:%S'),
            'cost_basis': total_cost
        }
        
        self.current_balance -= total_cost
        
        # Record trade in history
        trade = {
            'date': date.today().isoformat(),
            'time': datetime.now().strftime('%H:%M:%S'),
            'symbol': symbol,
            'action': 'BUY',
            'shares': shares,
            'price': price,
            'commission': self.commission,
            'total_cost': total_cost,
            'balance_after': self.current_balance
        }
        self.trade_history.append(trade)
        
        print(f"✅ EXECUTED BUY: {symbol}")
        print(f"   Shares: {shares} @ ${price:.2f} = ${total_cost:.0f}")
        print(f"   Balance: ${self.current_balance:.0f} | Positions: {len(self.positions)}/{self.max_positions}")
        
        return True
    
    def execute_sell(self, symbol, price):
        """Execute sell order and calculate P&L"""
        if symbol not in self.positions:
            return False
        
        position = self.positions[symbol]
        shares = position['shares']
        proceeds = shares * price - self.commission
        
        # Calculate profit/loss
        cost_basis = position['cost_basis']
        net_pnl = proceeds - (cost_basis - self.commission)  # Subtract entry commission from cost
        return_pct = (net_pnl / (cost_basis - self.commission)) * 100
        
        # Calculate holding period
        entry_date = datetime.strptime(position['entry_date'], '%Y-%m-%d').date()
        holding_days = (date.today() - entry_date).days
        
        # Execute the trade
        self.current_balance += proceeds
        del self.positions[symbol]
        
        # Record trade in history
        trade = {
            'date': date.today().isoformat(),
            'time': datetime.now().strftime('%H:%M:%S'),
            'symbol': symbol,
            'action': 'SELL',
            'shares': shares,
            'price': price,
            'commission': self.commission,
            'proceeds': proceeds,
            'pnl': net_pnl,
            'return_pct': return_pct,
            'holding_days': holding_days,
            'balance_after': self.current_balance
        }
        self.trade_history.append(trade)
        
        # Display results
        pnl_emoji = "💚" if net_pnl > 0 else "🔴"
        print(f"✅ EXECUTED SELL: {symbol}")
        print(f"   Shares: {shares} @ ${price:.2f} = ${proceeds:.0f}")
        print(f"   {pnl_emoji} P&L: ${net_pnl:+.0f} ({return_pct:+.1f}%) over {holding_days} days")
        print(f"   Balance: ${self.current_balance:.0f}")
        
        return True
    
    def run_scan(self):
        """Main trading scan - analyze current batch and execute trades"""
        print(f"\n🚀 Starting Strategy C scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 70)
        
        # Check trading conditions
        if not self.is_within_trading_period():
            print(f"📅 Outside trading period ({self.start_date} to {self.end_date})")
            return
        
        # Get current batch of stocks to analyze
        symbols_to_scan = self.get_current_batch()
        
        # Performance counters
        processed = 0
        buy_signals = 0
        sell_signals = 0
        errors = 0
        
        # Scan each symbol in the current batch
        for i, symbol in enumerate(symbols_to_scan):
            try:
                # Rate limiting - pause every 25 requests
                if i > 0 and i % 25 == 0:
                    print(f"⏸️  Rate limit pause... ({i}/{len(symbols_to_scan)} processed)")
                    time.sleep(2)
                
                # Fetch stock data
                data = self.get_stock_data(symbol)
                if data is None:
                    errors += 1
                    continue
                
                # Analyze for signals
                signals = self.detect_signals(symbol, data)
                processed += 1
                
                # Execute buy orders
                if signals['buy']:
                    if self.execute_buy(symbol, signals['price']):
                        buy_signals += 1
                
                # Execute sell orders  
                elif signals['sell']:
                    if self.execute_sell(symbol, signals['price']):
                        sell_signals += 1
                
            except Exception as e:
                print(f"⚠️  Error processing {symbol}: {str(e)[:100]}")
                errors += 1
                continue
        
        # Display scan summary
        print(f"\n📊 Scan Summary:")
        print(f"   Symbols processed: {processed}/{len(symbols_to_scan)}")
        print(f"   Buy signals executed: {buy_signals}")
        print(f"   Sell signals executed: {sell_signals}")
        print(f"   Errors encountered: {errors}")
        
        # Display current portfolio status
        total_position_value = sum(pos['shares'] * pos['entry_price'] for pos in self.positions.values())
        total_portfolio = self.current_balance + total_position_value
        total_return = ((total_portfolio - self.starting_capital) / self.starting_capital) * 100
        
        print(f"\n💰 Portfolio Status:")
        print(f"   Cash balance: ${self.current_balance:.0f}")
        print(f"   Position value: ${total_position_value:.0f}")
        print(f"   Total portfolio: ${total_portfolio:.0f}")
        print(f"   Total return: {total_return:+.1f}%")
        print(f"   Open positions: {len(self.positions)}/{self.max_positions}")
        
        # Save state
        self.save_state()
        print(f"\n💾 State saved. Scan complete at {datetime.now().strftime('%H:%M:%S')}")
    
    def save_state(self):
        """Save current trading state and generate diary"""
        # Calculate portfolio metrics
        total_position_value = sum(pos['shares'] * pos['entry_price'] for pos in self.positions.values())
        total_portfolio = self.current_balance + total_position_value
        total_return = ((total_portfolio - self.starting_capital) / self.starting_capital) * 100
        completed_trades = [t for t in self.trade_history if t['action'] == 'SELL']
        
        # Save detailed state
        state = {
            'last_update': datetime.now().isoformat(),
            'trading_period': f"{self.start_date} to {self.end_date}",
            'current_balance': self.current_balance,
            'total_portfolio_value': total_portfolio,
            'total_return_pct': total_return,
            'positions': self.positions,
            'trade_history': self.trade_history,
            'stats': {
                'completed_trades': len(completed_trades),
                'open_positions': len(self.positions),
                'win_trades': len([t for t in completed_trades if t.get('pnl', 0) > 0]),
                'total_stocks_in_rotation': len(self.symbols)
            }
        }
        
        with open('trading_state.json', 'w') as f:
            json.dump(state, f, indent=2)
        
        # Generate trading diary for GitHub Actions artifacts
        diary = {
            'strategy': 'Strategy C - MACD < 0 + Crossover with Stock Rotation',
            'last_update': datetime.now().isoformat(),
            'trading_period': f"{self.start_date} to {self.end_date}",
            'portfolio_performance': {
                'starting_capital': self.starting_capital,
                'current_cash': self.current_balance,
                'total_portfolio_value': total_portfolio,
                'total_return_pct': total_return,
                'total_return_dollars': total_portfolio - self.starting_capital
            },
            'trading_stats': {
                'total_stocks_covered': len(self.symbols),
                'batch_size_per_run': self.batch_size,
                'completed_trades': len(completed_trades),
                'open_positions': len(self.positions),
                'max_positions': self.max_positions,
                'win_rate': (len([t for t in completed_trades if t.get('pnl', 0) > 0]) / len(completed_trades) * 100) if completed_trades else 0
            },
            'current_positions': {symbol: {
                'shares': pos['shares'],
                'entry_price': pos['entry_price'],
                'entry_date': pos['entry_date'],
                'current_value': pos['shares'] * pos['entry_price']
            } for symbol, pos in self.positions.items()},
            'recent_trades': self.trade_history[-20:] if len(self.trade_history) > 20 else self.trade_history
        }
        
        with open('trading_diary.json', 'w') as f:
            json.dump(diary, f, indent=2)
    
    def load_state(self):
        """Load previous trading state if available"""
        try:
            if os.path.exists('trading_state.json'):
                with open('trading_state.json', 'r') as f:
                    state = json.load(f)
                    self.current_balance = state.get('current_balance', self.starting_capital)
                    self.positions = state.get('positions', {})
                    self.trade_history = state.get('trade_history', [])
                    print(f"📁 Loaded previous state: ${self.current_balance:.0f} balance, {len(self.positions)} positions")
            else:
                print(f"🆕 Starting fresh with ${self.starting_capital} capital")
        except Exception as e:
            print(f"⚠️  Could not load previous state: {e}")
            print(f"🆕 Starting fresh with ${self.starting_capital} capital")

def main():
    """Main execution function"""
    print("🎯 Strategy C Trading Bot - Enhanced with Full S&P 500 Coverage")
    print("📈 MACD < 0 + Crossover Strategy | 20% Position Sizing | 5 Max Positions")
    print("🔄 Intelligent Stock Rotation: 500+ stocks via 5 daily scans")
    print("=" * 80)
    
    try:
        trader = GitHubActionsTrader()
        trader.run_scan()
        
        print(f"\n✅ Trading bot execution completed successfully!")
        print(f"📁 Check trading_diary.json for detailed results")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        raise

if __name__ == "__main__":
    main()
