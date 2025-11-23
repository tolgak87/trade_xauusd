import MetaTrader5 as mt5
import os
import json
from datetime import datetime


class GoldTrader:
    CANDIDATE_SYMBOLS = ["XAUUSD", "XAUUSD.", "XAUUSD.m", "GOLD", "GOLD."]

    def __init__(self):
        self.connected = False
        self.symbol = None

    # ----------------------------
    # Bağlantı işlemleri
    # ----------------------------
    def connect(self) -> bool:
        if not mt5.initialize():
            print("❌ MT5 init hata:", mt5.last_error())
            return False
        self.connected = True
        return True

    def disconnect(self):
        if self.connected:
            mt5.shutdown()
            self.connected = False

    # ----------------------------
    # Sembol ve fiyat bilgisi
    # ----------------------------
    def find_gold_symbol(self) -> str | None:
        for candidate in self.CANDIDATE_SYMBOLS:
            info = mt5.symbol_info(candidate)
            if info:
                if not info.visible:
                    mt5.symbol_select(candidate, True)
                self.symbol = candidate
                return candidate
        return None

    def get_current_price(self):
        if not self.symbol:
            print("⚠️ Önce find_gold_symbol çalıştır.")
            return None

        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            print(f"⚠️ {self.symbol} için fiyat alınamadı:", mt5.last_error())
            return None

        return {
            "symbol": self.symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "spread": tick.ask - tick.bid
        }

    # ----------------------------
    # JSON log helper
    # ----------------------------
    def _log_trade(self, trade_data: dict, folder: str = "logs", filename: str = "trades.json"):
        """İşlemi JSON dosyasına kaydeder (append)."""
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        data = []

        # Mevcut log'u oku
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []

        # Zaman damgası ekle
        trade_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Kaydı ekle
        data.append(trade_data)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"🧾 İşlem '{filepath}' dosyasına kaydedildi.")

    # ----------------------------
    # Trade işlemleri
    # ----------------------------
    def buy_with_risk_reward(self, volume: float = 0.1, risk_usd: float = 3.0, rr_ratio: float = 2.0):
        """1:2 risk/ödül oranıyla BUY emri gönderir ve loglar."""
        if not self.symbol:
            raise RuntimeError("Sembol yok, önce find_gold_symbol çağır.")

        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            print("Fiyat alınamadı:", mt5.last_error())
            return None

        entry = tick.ask
        sl = entry - risk_usd
        tp = entry + (risk_usd * rr_ratio)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": entry,
            "sl": sl,
            "tp": tp,
            "deviation": 50,
            "magic": 999,
            "comment": f"Buy {self.symbol} RR={rr_ratio}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        print(f"📈 BUY {self.symbol} @ {entry} | SL={sl} | TP={tp}")
        result = mt5.order_send(request)
        print("Sonuç:", result)

        # JSON log
        trade_log = {
            "action": "BUY",
            "symbol": self.symbol,
            "price": entry,
            "sl": sl,
            "tp": tp,
            "volume": volume,
            "rr_ratio": rr_ratio,
            "result": result._asdict() if hasattr(result, "_asdict") else str(result)
        }
        self._log_trade(trade_log)
        return result

    def sell_with_risk_reward(self, volume: float = 0.1, risk_usd: float = 3.0, rr_ratio: float = 2.0):
        """1:2 risk/ödül oranıyla SELL emri gönderir ve loglar."""
        if not self.symbol:
            raise RuntimeError("Sembol yok, önce find_gold_symbol çağır.")

        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            print("Fiyat alınamadı:", mt5.last_error())
            return None

        entry = tick.bid
        sl = entry + risk_usd
        tp = entry - (risk_usd * rr_ratio)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": entry,
            "sl": sl,
            "tp": tp,
            "deviation": 50,
            "magic": 999,
            "comment": f"Sell {self.symbol} RR={rr_ratio}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        print(f"📉 SELL {self.symbol} @ {entry} | SL={sl} | TP={tp}")
        result = mt5.order_send(request)
        print("Sonuç:", result)

        # JSON log
        trade_log = {
            "action": "SELL",
            "symbol": self.symbol,
            "price": entry,
            "sl": sl,
            "tp": tp,
            "volume": volume,
            "rr_ratio": rr_ratio,
            "result": result._asdict() if hasattr(result, "_asdict") else str(result)
        }
        self._log_trade(trade_log)
        return result
