# guardrails.py

import re
import pandas as pd

# Example sensitive fields/columns
SENSITIVE_FIELDS = ["email", "ssn", "credit_card", "password", "salary"]

def check_input(user_input):
    """
    Check the user's input for sensitive data requests.
    Returns True if input is safe, False if it contains sensitive info.
    """
    text = user_input.lower()

    # Block requests to sensitive keywords
    for field in SENSITIVE_FIELDS:
        if field in text:
            print(f"[GUARDRAIL ALERT] Attempt to access sensitive field: {field}")
            return False

    # Simple regex check for emails
    if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", user_input):
        print("[GUARDRAIL ALERT] Attempt to access emails")
        return False

    # Optional: block dangerous commands like delete/drop
    if any(cmd in text for cmd in ["delete", "drop", "truncate", "update"]):
        print("[GUARDRAIL ALERT] Potentially dangerous command detected")
        return False

    return True


def check_dataframe(df: pd.DataFrame):
    """
    Check pandas DataFrame for sensitive columns.
    Returns True if safe, False if sensitive columns exist.
    """
    if any(col.lower() in SENSITIVE_FIELDS for col in df.columns):
        sensitive_cols = [col for col in df.columns if col.lower() in SENSITIVE_FIELDS]
        print(f"[GUARDRAIL ALERT] DataFrame contains sensitive columns: {sensitive_cols}")
        return False
    return True


def sanitize_dataframe(df: pd.DataFrame):
    """
    Remove sensitive columns from DataFrame.
    """
    safe_cols = [col for col in df.columns if col.lower() not in SENSITIVE_FIELDS]
    return df[safe_cols]


def check_output(output):
    """
    General output check to prevent leaking sensitive data.
    """
    text = str(output).lower()
    for field in SENSITIVE_FIELDS:
        if field in text:
            print(f"[GUARDRAIL ALERT] Output contains sensitive field: {field}")
            return False
    return True
