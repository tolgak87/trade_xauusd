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
        """Açıklamalı formatta ekrana basar."""
        print(f"login (Hesap numaran): {self.login}")
        print(f"trade_mode (Demo=0 / Gerçek=1): {self.trade_mode}")
        print(f"leverage (Kaldıraç oranı): {self.leverage}")
        print(f"balance (Bakiye): {self.balance}")
        print(f"equity (Özsermaye): {self.equity}")
        print(f"trade_allowed (İşlem izni): {self.trade_allowed}")
        print(f"server (Sunucu): {self.server}")
        print(f"currency (Para birimi): {self.currency}")
        print(f"company (Broker / Şirket): {self.company}")
        print(f"margin_level (Marjin seviyesi): {self.margin_level}")
        print(f"profit (Toplam kar/zarar): {self.profit}")
        print(f"margin_free (Kullanılabilir teminat): {self.margin_free}")

    def to_json_file(self, filepath: str = "account_info.json") -> None:
        """Veriyi JSON olarak verilen yola yazar (overwrite)."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4, ensure_ascii=False)
