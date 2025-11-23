from src.trade_gold import GoldTrader

def main():
    trader = GoldTrader()

    if not trader.connect():
        print("MT5'e bağlanamadı")
        return

    symbol = trader.find_gold_symbol()
    if not symbol:
        print("Altın sembolü bulunamadı.")
        trader.disconnect()
        return

    # Örnek: önce fiyatı al
    price = trader.get_current_price()
    print(f"{symbol} fiyatı: {price}")

    # 🔥 1:2 risk/ödül oranıyla BUY işlemi
    trader.buy_with_risk_reward(volume=0.1, risk_usd=3.0, rr_ratio=2.0)

    # 🔥 Aynı şekilde SELL örneği
    # trader.sell_with_risk_reward(volume=0.1, risk_usd=3.0, rr_ratio=2.0)

    trader.disconnect()

if __name__ == "__main__":
    main()
