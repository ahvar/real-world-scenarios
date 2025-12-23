from config import Config
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal

import requests


@dataclass
class CanonicalFillRecord:
    broker: str
    fill_id: str
    timestamp: datetime
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: int
    price: float
    order_id: str | None


def parse_iso_utc(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def parse_epoch_ms(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def month_key(dt: datetime) -> datetime:
    return f"{dt.month}-{dt.year}"


def fetch_broker_a(Config.account_id, Config.start_date, Config.end_date, Config.timeout) -> list[dict]:
    response = requests.get()

def fetch_broker_b(Config.account_id, Config.start_date, Config.end_date, Config.timeout) -> list[dict]:
    pass

