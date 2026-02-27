"""
dates.py
Practice 4 — Dates & Time
"""

from __future__ import annotations
from datetime import date, datetime, time, timedelta, timezone

try:
    from zoneinfo import ZoneInfo  
except Exception:
    ZoneInfo = None  


def demo_create_dates() -> None:
    today = date.today()
    now = datetime.now()
    custom_date = date(2026, 2, 27)
    custom_dt = datetime(2026, 2, 27, 12, 30, 0)

    print("Today:", today)
    print("Now:", now)
    print("Custom date:", custom_date)
    print("Custom datetime:", custom_dt)
    print()


def demo_formatting() -> None:
    now = datetime.now()
    print("Formatting:")
    print("ISO:", now.isoformat())
    print("Pretty:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Day/Month:", now.strftime("%d.%m.%Y"))
    print()


def demo_time_differences() -> None:
    start = datetime(2026, 2, 1, 9, 0, 0)
    end = datetime(2026, 2, 27, 11, 0, 0)
    diff = end - start

    print("Time differences:")
    print("Start:", start)
    print("End:", end)
    print("Difference:", diff)
    print("Days:", diff.days)
    print("Total seconds:", int(diff.total_seconds()))
    print()

    print("Add 10 days:", start + timedelta(days=10))
    print("Minus 3 hours:", end - timedelta(hours=3))
    print()


def demo_timezones() -> None:
    print("Timezones:")

    utc_now = datetime.now(timezone.utc)
    print("UTC now:", utc_now.isoformat())

    tz_plus5 = timezone(timedelta(hours=5))
    local_fixed = utc_now.astimezone(tz_plus5)
    print("Fixed +05:00:", local_fixed.isoformat())

    if ZoneInfo is not None:
        qyz = ZoneInfo("Asia/Qyzylorda")
        local_zone = utc_now.astimezone(qyz)
        print("Asia/Qyzylorda:", local_zone.isoformat())
    else:
        print("ZoneInfo not available (need Python 3.9+).")

    print()


def main() -> None:
    demo_create_dates()
    demo_formatting()
    demo_time_differences()
    demo_timezones()


if __name__ == "__main__":
    main()