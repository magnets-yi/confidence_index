"""Write fixtures/prices.csv and fixtures/nyse_holidays.csv."""

from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "fixtures"
NY = ZoneInfo("America/New_York")

# First NYSE session of 2024 through the day after the latest close we want.
START = datetime(2024, 1, 2, tzinfo=timezone.utc)
# Exclusive end: keep only completed sessions (drop an in-progress bar if run mid-day).
END = datetime(2026, 9, 8, tzinfo=timezone.utc)


def fetch_spx() -> list[tuple[str, str]]:
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC"
        f"?period1={int(START.timestamp())}&period2={int(END.timestamp())}&interval=1d"
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    result = payload["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]
    rows: list[tuple[str, str]] = []
    for ts, close in zip(timestamps, closes):
        if close is None:
            continue
        day = datetime.fromtimestamp(ts, tz=NY).date().isoformat()
        rows.append((day, f"{close:.2f}"))
    return rows


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    prices = fetch_spx()
    prices_path = OUT_DIR / "prices.csv"
    with prices_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "spx_close"])
        writer.writerows(prices)

    # Full-day NYSE closures only (early closes still have an official close).
    holidays = [
        ("2024-01-01", "New Year's Day"),
        ("2024-01-15", "Martin Luther King, Jr. Day"),
        ("2024-02-19", "Washington's Birthday"),
        ("2024-03-29", "Good Friday"),
        ("2024-05-27", "Memorial Day"),
        ("2024-06-19", "Juneteenth National Independence Day"),
        ("2024-07-04", "Independence Day"),
        ("2024-09-02", "Labor Day"),
        ("2024-11-28", "Thanksgiving Day"),
        ("2024-12-25", "Christmas Day"),
        ("2025-01-01", "New Year's Day"),
        ("2025-01-20", "Martin Luther King, Jr. Day"),
        ("2025-02-17", "Washington's Birthday"),
        ("2025-04-18", "Good Friday"),
        ("2025-05-26", "Memorial Day"),
        ("2025-06-19", "Juneteenth National Independence Day"),
        ("2025-07-04", "Independence Day"),
        ("2025-09-01", "Labor Day"),
        ("2025-11-27", "Thanksgiving Day"),
        ("2025-12-25", "Christmas Day"),
        ("2026-01-01", "New Year's Day"),
        ("2026-01-19", "Martin Luther King, Jr. Day"),
        ("2026-02-16", "Washington's Birthday"),
        ("2026-04-03", "Good Friday"),
        ("2026-05-25", "Memorial Day"),
        ("2026-06-19", "Juneteenth National Independence Day"),
        ("2026-07-03", "Independence Day (observed)"),
        ("2026-09-07", "Labor Day"),
        ("2026-11-26", "Thanksgiving Day"),
        ("2026-12-25", "Christmas Day"),
    ]
    holidays_path = OUT_DIR / "nyse_holidays.csv"
    with holidays_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "holiday"])
        writer.writerows(holidays)

    print(f"wrote {prices_path} ({len(prices)} rows)")
    print(f"first={prices[0]} last={prices[-1]}")
    print(f"wrote {holidays_path} ({len(holidays)} rows)")

    holiday_dates = {d for d, _ in holidays}
    overlap = [d for d, _ in prices if d in holiday_dates]
    if overlap:
        raise SystemExit(f"price rows on holidays: {overlap}")
    print("no price rows fall on listed NYSE holidays")


if __name__ == "__main__":
    main()
