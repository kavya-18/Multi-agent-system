# services/tools.py
"""
Tools and Utilities
-------------------
Contains helpers for logging, JSON parsing, and timing measurements.
Used across all agents and services.
"""

import json
import time
from datetime import datetime
from functools import wraps
from typing import Any, Dict


# -----------------------------------------------------
def log_event(source: str, message: str):
    """
    Simple console logger with timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}][{source}] {message}")


# -----------------------------------------------------
def safe_json_parse(raw: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely parse JSON from an LLM response; fall back if malformed.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        log_event("JSON", "Failed to parse LLM output; using fallback.")
        return fallback


# -----------------------------------------------------
def timeit(func):
    """
    Decorator to measure execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        log_event(func.__name__, f"Executed in {duration:.2f}s")
        return result
    return wrapper
