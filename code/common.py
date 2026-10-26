"""Shared helpers: settings, CSV input/output and dataset loading."""

import csv
import os
import sys
from decimal import Decimal

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CODE_DIR, "data")
RESULTS_DIR = os.path.join(CODE_DIR, "results")
SETTINGS_FILE = os.path.join(CODE_DIR, "settings.txt")
SETTINGS_EXAMPLE = os.path.join(CODE_DIR, "settings.example.txt")


def load_settings():
    path = SETTINGS_FILE if os.path.exists(SETTINGS_FILE) else SETTINGS_EXAMPLE
    settings = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            settings[key.strip()] = value.strip()
    for key in list(settings):
        if os.environ.get(key):
            settings[key] = os.environ[key]
    return settings


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def dataset_dir(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.isdir(path):
        sys.exit(f"Dataset folder not found: {path}\n"
                 f"For the automatic dataset, run 2_BUILD_DATASET.bat first.")
    return path


def load_dataset(name):
    """Return (documents by id, facts, claims) for data/<name>/."""
    folder = dataset_dir(name)
    documents = {d["doc_id"]: d for d in read_csv(os.path.join(folder, "documents.csv"))}
    facts = read_csv(os.path.join(folder, "facts.csv"))
    for fact in facts:
        fact["value"] = Decimal(fact["value"])
        fact["step"] = Decimal(fact["step"])
    claims = read_csv(os.path.join(folder, "claims.csv"))
    for claim in claims:
        claim["claimed_value"] = Decimal(claim["claimed_value"])
        claim["claim_step"] = Decimal(claim["claim_step"])
        claim["packet_ids"] = [p for p in claim["packet"].replace(";", "+").split("+") if p]
    return documents, facts, claims
