# utils/data_loader.py
# =====================
# Test data loading utilities.
# Supports reading from JSON, CSV, and Excel files.
# Migrated from utilities/data_reader_util.py

import csv
import json
import logging

import openpyxl

logger = logging.getLogger(__name__)


def load_json_file(file_path: str):
    """
    Load a JSON file and return its content (dict or list) directly.
    """
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file '{file_path}': {e}")
        return None


def read_json_data(file_path: str) -> list[tuple]:
    """
    Read test data from a JSON file and return a list of tuples.

    Example JSON:
    [
        {"email": "test1@example.com", "password": "abc123", "validity": "valid"},
        {"email": "test2@example.com", "password": "xyz123", "validity": "invalid"}
    ]
    """
    data = []
    try:
        with open(file_path) as f:
            json_data = json.load(f)
            for record in json_data:
                data.append(tuple(record.values()))
    except Exception as e:
        logger.error(f"Error reading JSON file '{file_path}': {e}")
    return data


def read_csv_data(file_path: str) -> list[tuple]:
    """
    Read test data from a CSV file and return a list of tuples.
    CSV file should contain headers in the first row.
    """
    data = []
    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(tuple(row.values()))
    except Exception as e:
        logger.error(f"Error reading CSV file '{file_path}': {e}")
    return data


def read_excel_data(file_path: str, sheet_name: str | None = None) -> list[tuple]:
    """
    Read test data from an Excel file and return a list of tuples.
    Assumes the first row contains headers.
    """
    data = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name] if sheet_name else workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
    except Exception as e:
        logger.error(f"Error reading Excel file '{file_path}': {e}")
    return data
