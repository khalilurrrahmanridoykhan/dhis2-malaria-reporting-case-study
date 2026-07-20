#!/usr/bin/env python3
"""Generate reproducible, aggregate-only malaria demonstration data.

The output is fictional and must never be merged with operational health data.
"""

from __future__ import annotations

import csv
import math
import random
from datetime import date
from pathlib import Path

SEED = 20260719
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

FACILITIES = [
    ("OuLamaHC001", "Lama Health Complex", "Lama", 46500, 1.30),
    ("OuFasyaHC01", "Fasyakhali Health Centre", "Lama", 24100, 1.05),
    ("OuAziznHC01", "Aziznagar Health Centre", "Lama", 21300, 0.90),
    ("OuAlikaHC01", "Alikadam Health Complex", "Alikadam", 38200, 1.25),
    ("OuKurukHC01", "Kurukpata Health Centre", "Alikadam", 17600, 1.40),
    ("OuNaikhHC01", "Naikhongchhari Health Complex", "Naikhongchhari", 41100, 1.15),
    ("OuKaptaiHC1", "Kaptai Health Complex", "Kaptai", 49200, 0.75),
    ("OuChandrHC1", "Chandraghona Health Centre", "Kaptai", 27300, 0.70),
    ("OuBaghaiHC1", "Baghaichhari Health Complex", "Baghaichhari", 52500, 1.35),
    ("OuMarishHC1", "Marishya Health Centre", "Baghaichhari", 28600, 1.20),
    ("OuBelaicHC1", "Belaichhari Health Complex", "Belaichhari", 31900, 1.10),
    ("OuJurachHC1", "Jurachhari Health Complex", "Jurachhari", 29400, 1.18),
]

DATA_ELEMENTS = {
    "suspected_cases": "DeMalSus001",
    "tests_rdt": "DeMalRdt001",
    "tests_microscopy": "DeMalMic001",
    "confirmed_cases": "DeMalPos001",
    "pf_cases": "DeMalPf0001",
    "pv_cases": "DeMalPv0001",
    "mixed_cases": "DeMalMix001",
    "severe_cases": "DeMalSev001",
    "malaria_deaths": "DeMalDth001",
    "cases_treated": "DeMalTrt001",
    "llins_distributed": "DeMalLln001",
    "stockout_days": "DeMalStk001",
    "reports_expected": "DeMalExp001",
    "reports_received": "DeMalRec001",
    "indigenous_cases": "DeMalInd001",
    "imported_cases": "DeMalImp001",
    "population": "DePopEst001",
}


def months(start_year: int, start_month: int, count: int):
    year, month = start_year, start_month
    for _ in range(count):
        yield date(year, month, 1)
        month += 1
        if month == 13:
            month = 1
            year += 1


def make_row(rng: random.Random, facility, period: date, index: int) -> dict[str, object]:
    uid, name, upazila, base_population, facility_risk = facility
    population = round(base_population * (1 + 0.012 * (period.year - 2024)))
    seasonal = 1 + 0.70 * math.sin((period.month - 4) * math.pi / 6)
    seasonal = max(0.28, seasonal)
    rainfall = max(15, round(210 + 175 * math.sin((period.month - 4) * math.pi / 6) + rng.gauss(0, 24)))
    temperature = round(26.5 + 3.2 * math.sin((period.month - 2) * math.pi / 6) + rng.gauss(0, 0.6), 1)
    humidity = min(96, max(48, round(73 + rainfall / 24 + rng.gauss(0, 3))))

    expected_positive = 14 * facility_risk * seasonal + rainfall / 55
    confirmed = max(0, round(rng.gauss(expected_positive, max(2.0, expected_positive * 0.18))))
    # Insert a fictional outbreak-like signal in one facility for demonstration.
    if uid == "OuBaghaiHC1" and period == date(2025, 7, 1):
        confirmed = round(confirmed * 2.4)

    positivity = min(0.34, max(0.05, 0.10 + 0.07 * facility_risk + rng.gauss(0, 0.018)))
    total_tests = max(confirmed, round(confirmed / positivity)) if confirmed else rng.randint(10, 35)
    tests_rdt = round(total_tests * rng.uniform(0.68, 0.88))
    tests_microscopy = total_tests - tests_rdt
    suspected = max(total_tests, round(total_tests * rng.uniform(1.05, 1.32)))

    pf_cases = round(confirmed * rng.uniform(0.72, 0.88))
    mixed_cases = 1 if confirmed >= 12 and rng.random() < 0.25 else 0
    pv_cases = max(0, confirmed - pf_cases - mixed_cases)
    severe = min(confirmed, round(confirmed * rng.uniform(0.02, 0.09)))
    deaths = 1 if severe >= 3 and rng.random() < 0.08 else 0
    treated = max(0, confirmed - rng.choice([0, 0, 0, 1]))
    imported = min(confirmed, round(confirmed * rng.uniform(0.04, 0.16)))
    indigenous = confirmed - imported
    stockout = rng.choice([0, 0, 0, 0, 0, 1, 2, 3])
    received = 0 if (index + period.month) % 31 == 0 else 1

    return {
        "org_unit_uid": uid,
        "facility": name,
        "upazila": upazila,
        "period": period.strftime("%Y%m"),
        "population": population,
        "rainfall_mm": rainfall,
        "temperature_c": temperature,
        "humidity_pct": humidity,
        "suspected_cases": suspected,
        "tests_rdt": tests_rdt,
        "tests_microscopy": tests_microscopy,
        "confirmed_cases": confirmed,
        "pf_cases": pf_cases,
        "pv_cases": pv_cases,
        "mixed_cases": mixed_cases,
        "severe_cases": severe,
        "malaria_deaths": deaths,
        "cases_treated": treated,
        "llins_distributed": rng.randint(0, 180) if period.month in (4, 5, 6) else rng.randint(0, 35),
        "stockout_days": stockout,
        "reports_expected": 1,
        "reports_received": received,
        "indigenous_cases": indigenous,
        "imported_cases": imported,
    }


def quality_flags(row: dict[str, object]) -> list[str]:
    tests = int(row["tests_rdt"]) + int(row["tests_microscopy"])
    confirmed = int(row["confirmed_cases"])
    flags = []
    if confirmed > tests:
        flags.append("confirmed_exceeds_tests")
    if int(row["malaria_deaths"]) > confirmed:
        flags.append("deaths_exceed_confirmed")
    if int(row["pf_cases"]) + int(row["pv_cases"]) + int(row["mixed_cases"]) != confirmed:
        flags.append("species_total_mismatch")
    if int(row["stockout_days"]) > 31:
        flags.append("stockout_days_out_of_range")
    if int(row["reports_received"]) > int(row["reports_expected"]):
        flags.append("received_exceeds_expected")
    return flags


def write_outputs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    rng = random.Random(SEED)
    rows = [
        make_row(rng, facility, period, index)
        for index, facility in enumerate(FACILITIES)
        for period in months(2024, 1, 24)
    ]

    wide_path = DATA_DIR / "synthetic_malaria_monthly.csv"
    with wide_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    long_path = DATA_DIR / "dhis2_data_values_long.csv"
    with long_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["dataElement", "period", "orgUnit", "value"])
        writer.writeheader()
        for row in rows:
            for field, data_element_uid in DATA_ELEMENTS.items():
                writer.writerow({
                    "dataElement": data_element_uid,
                    "period": row["period"],
                    "orgUnit": row["org_unit_uid"],
                    "value": row[field],
                })

    flagged = sum(bool(quality_flags(row)) for row in rows)
    print(f"Generated {len(rows)} aggregate records ({flagged} with validation flags).")
    print(f"Wrote {wide_path}")
    print(f"Wrote {long_path}")


if __name__ == "__main__":
    write_outputs()
