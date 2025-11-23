import MetaTrader5 as mt5
from typing import Optional
from src.account_info import AccountInfoModel


class MT5Client:
    def __init__(self):
        self.initialized = False

    def connect(self) -> bool:
        if not mt5.initialize():
            print("❌ MT5 init error:", mt5.last_error())
            self.initialized = False
            return False
        self.initialized = True
        return True

    def disconnect(self) -> None:
        if self.initialized:
            mt5.shutdown()
            self.initialized = False

    def get_account_info(self) -> Optional[AccountInfoModel]:
        if not self.initialized:
            raise RuntimeError("MT5 is not connected. Call connect() first.")
        info = mt5.account_info()
        if info is None:
            print("⚠️ Could not get account_info:", mt5.last_error())
            return None

        return AccountInfoModel(
            login=info.login,
            trade_mode=info.trade_mode,
            leverage=info.leverage,
            balance=info.balance,
            equity=info.equity,
            trade_allowed=info.trade_allowed,
            server=info.server,
            currency=info.currency,
            company=info.company,
            margin_level=info.margin_level,
            profit=info.profit,
            margin_free=info.margin_free,
        )
