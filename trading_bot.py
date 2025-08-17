import os
import sys
import json
import time
from datetime import datetime, date, timedelta

try:
      import yfinance as yf
      import pandas as pd
      import numpy as np
      print("✅ All packages loaded!")
except ImportError as e:
      print(f"📦 Installing missing package: {e}")
      os.system("pip install yfinance pandas numpy python-dateutil")
      import yfinance as yf
      import pandas as pd
      import numpy as np

class GitHubActionsTrader:
      def __init__(self):
          self.start_date = date(2025, 8, 18)
          self.end_date = date(2025, 9, 29)
          self.capital = 1000
          self.balance = 1000
          self.positions = {}
          self.trades = []
          self.position_size = 0.20
          self.max_positions = 5
          self.commission = 1.0

          self.symbols = [
              'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP',
              'AES', 'AFL', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD',
              'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ATO',
              'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BALL', 'BAX', 'BBWI', 'BBY', 'BDX', 'BEN',
              'BF.B', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BMY', 'BR', 'BRK.B', 'BRO', 'BSX', 'BWA', 'BXP', 'C',
              'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDAY', 'CDNS', 'CDW', 'CE', 'CEG', 'CF',
              'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC',
              'CNP', 'COF', 'COG', 'COO', 'COP', 'COST', 'CPB', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH',
              'CTVA', 'CVS', 'CVX', 'CZR', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISH', 'DLR',
              'DLTR', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXC', 'DXCM', 'EA', 'EBAY', 'ECL',
              'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR',
              'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX', 'FDS', 'FDX',
              'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTNT', 'FTV', 'GD', 'GE',
              'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS',
              'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST',
              'HSY', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'INVH', 'IP',
              'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBHT', 'JCI', 'JKHY', 'JNJ', 'JNPR',
              'JPM', 'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'L', 'LDOS', 'LEG', 'LEN',
              'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB',
              'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'META', 'MGM', 'MHK',
              'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS',
              'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE',
              'NLOK', 'NLSN', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA',
              'NXPI', 'O', 'ODFL', 'OGN', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PARA', 'PAYC', 'PAYX', 'PCAR',
              'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW',
              'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE',
              'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX', 'SBAC', 'SBNY',
              'SBUX', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT',
              'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC',
              'TFX', 'TGT', 'TJX', 'TMO', 'TMUS', 'TPG', 'TPR', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TXN',
              'TXT', 'TYL', 'UA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC', 'VICI',
              'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WBD', 'WDC', 'WEC',
              'WELL', 'WFC', 'WHR', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WU', 'WY', 'WYNN', 'XEL', 'XOM',
              'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS'
          ]

          self.load_state()

      def load_state(self):
          try:
              with open('trading_state.json', 'r') as f:
                  state = json.load(f)
                  self.balance = state.get('balance', self.capital)
                  self.positions = state.get('positions', {})
                  self.trades = state.get('trades', [])
          except FileNotFoundError:
              pass

      def save_state(self):
          state = {
              'balance': self.balance,
              'positions': self.positions,
              'trades': self.trades,
              'last_update': datetime.now().isoformat()
          }
          with open('trading_state.json', 'w') as f:
              json.dump(state, f, indent=2, default=str)

          diary = {
              'balance': self.balance,
              'positions': self.positions,
              'trades': self.trades
          }
          with open(f"trading_diary_{self.start_date}_{self.end_date}.json", 'w') as f:
              json.dump(diary, f, indent=2, default=str)

      def is_within_trading_period(self):
          today = date.today()
          return self.start_date <= today <= self.end_date

      def is_market_open(self):
          now = datetime.now()
          if now.weekday() >= 5:
              return False
          market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
          market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
          return market_open <= now <= market_close

      def calculate_macd(self, prices):
          if len(prices) < 26:
              return None, None, None
          exp1 = prices.ewm(span=12).mean()
          exp2 = prices.ewm(span=26).mean()
          macd_line = exp1 - exp2
          signal_line = macd_line.ewm(span=9).mean()
          return macd_line, signal_line, macd_line.iloc[-1]

      def detect_signals(self, prices):
          macd_line, signal_line, current_macd = self.calculate_macd(prices)
          if macd_line is None or len(macd_line) < 2:
              return False, False

          # Entry: MACD crossover + MACD < 0
          entry = (macd_line.iloc[-1] > signal_line.iloc[-1] and
                  macd_line.iloc[-2] <= signal_line.iloc[-2] and
                  macd_line.iloc[-1] < 0)

          # Exit: Signal crosses above MACD
          exit_signal = (signal_line.iloc[-1] > macd_line.iloc[-1] and
                        signal_line.iloc[-2] <= macd_line.iloc[-2])

          return entry, exit_signal

      def execute_buy(self, symbol, price):
          cost = self.balance * self.position_size
          shares = int(cost / price)
          if shares > 0 and len(self.positions) < self.max_positions:
              total_cost = shares * price + self.commission
              if total_cost <= self.balance:
                  self.positions[symbol] = {
                      'shares': shares,
                      'entry_price': price,
                      'entry_date': datetime.now().isoformat()
                  }
                  self.balance -= total_cost
                  self.trades.append({
                      'action': 'BUY',
                      'symbol': symbol,
                      'shares': shares,
                      'price': price,
                      'timestamp': datetime.now().isoformat()
                  })
                  print(f"✅ BUY {symbol}: {shares} shares @ ${price:.2f}")

      def execute_sell(self, symbol, price):
          if symbol in self.positions:
              pos = self.positions[symbol]
              proceeds = pos['shares'] * price - self.commission
              pnl = proceeds - (pos['shares'] * pos['entry_price'] + self.commission)
              self.balance += proceeds
              del self.positions[symbol]
              self.trades.append({
                  'action': 'SELL',
                  'symbol': symbol,
                  'shares': pos['shares'],
                  'price': price,
                  'pnl': pnl,
                  'timestamp': datetime.now().isoformat()
              })
              emoji = "💚" if pnl > 0 else "🔴"
              print(f"{emoji} SELL {symbol}: {pos['shares']} shares @ ${price:.2f} (P&L: ${pnl:.2f})")

      def run_scan(self):
          if not self.is_within_trading_period():
              print("🎉 Trading period complete!")
              return

          if not self.is_market_open():
              print("🔴 Market closed")
              return

          print("🟢 Market open - scanning...")

          for symbol in self.symbols[:50]:  # Limit for demo
              try:
                  ticker = yf.Ticker(symbol)
                  data = ticker.history(period="30d")
                  if len(data) > 26:
                      entry, exit_signal = self.detect_signals(data['Close'])
                      price = data['Close'].iloc[-1]

                      if entry and symbol not in self.positions:
                          self.execute_buy(symbol, price)
                      elif exit_signal and symbol in self.positions:
                          self.execute_sell(symbol, price)
              except:
                  continue

          self.save_state()
          print(f"💰 Balance: ${self.balance:.0f} | Positions: {len(self.positions)}")

if __name__ == "__main__":
      bot = GitHubActionsTrader()
      bot.run_scan()
