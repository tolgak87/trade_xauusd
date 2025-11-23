from src.trade_gold import GoldTrader

def main():
    trader = GoldTrader()

    if not trader.connect():
        print("Could not connect to MT5")
        return

    symbol = trader.find_gold_symbol()
    if not symbol:
        print("Gold symbol not found.")
        trader.disconnect()
        return

    # Example: get price first
    price = trader.get_current_price()
    print(f"{symbol} price: {price}")

    # 🔥 BUY trade with 1:2 risk/reward ratio
    trader.buy_with_risk_reward(volume=0.1, risk_usd=3.0, rr_ratio=2.0)

    # 🔥 SELL example in the same way
    # trader.sell_with_risk_reward(volume=0.1, risk_usd=3.0, rr_ratio=2.0)

    trader.disconnect()

if __name__ == "__main__":
    main()
