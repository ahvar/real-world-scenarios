import os


class Config:
    ACCOUNT_ID = os.getenv("ACCOUNT_ID", "abc123")
    START_DATE = os.getenv("START_DATE", "12-19-2024")
    END_DATE = os.getenv("END_DATE", "12-19-2025")
    BROKER_A_URL = os.getenv("BROKER_A_URL", "api.brokera.json")
    BROKER_B_URL = os.getenv("BROKER_B_URL", "api.brokerb.json")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "tbd")
    TIMEOUT = int(os.getenv("TIMEOUT", 30))
