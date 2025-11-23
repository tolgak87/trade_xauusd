import json
from dataclasses import dataclass, asdict

@dataclass
class AccountInfoModel:
    login: int
    trade_mode: int
    leverage: int
    balance: float
    equity: float
    trade_allowed: bool
    server: str
    currency: str
    company: str
    margin_level: float
    profit: float
    margin_free: float

    def print_pretty(self) -> None:
        """Prints to screen in a formatted way with descriptions."""
        print(f"login (Account number): {self.login}")
        print(f"trade_mode (Demo=0 / Real=1): {self.trade_mode}")
        print(f"leverage (Leverage ratio): {self.leverage}")
        print(f"balance (Balance): {self.balance}")
        print(f"equity (Equity): {self.equity}")
        print(f"trade_allowed (Trading permission): {self.trade_allowed}")
        print(f"server (Server): {self.server}")
        print(f"currency (Currency): {self.currency}")
        print(f"company (Broker / Company): {self.company}")
        print(f"margin_level (Margin level): {self.margin_level}")
        print(f"profit (Total profit/loss): {self.profit}")
        print(f"margin_free (Available margin): {self.margin_free}")

    def to_json_file(self, filepath: str = "account_info.json") -> None:
        """Writes data as JSON to the given path (overwrite)."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4, ensure_ascii=False)
