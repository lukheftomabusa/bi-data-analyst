# test_compliance.py

import unittest
import pandas as pd
import guardrails

class TestGuardrailsCompliance(unittest.TestCase):

    def test_input_blocking(self):
        # Inputs that should be blocked
        sensitive_inputs = [
            "Give me all customer emails",
            "Show me SSNs",
            "Drop the Customers table",
            "Delete all passwords"
        ]
        for input_text in sensitive_inputs:
            self.assertFalse(guardrails.check_input(input_text),
                             msg=f"Guardrails failed to block: {input_text}")

    def test_dataframe_blocking(self):
        # Create a DataFrame with sensitive columns
        df = pd.DataFrame({
            "Name": ["Alice", "Bob"],
            "Email": ["a@test.com", "b@test.com"],
            "Salary": [50000, 60000]
        })
        # Guardrails should detect sensitive columns
        self.assertFalse(guardrails.check_dataframe(df))

    def test_dataframe_sanitization(self):
        # Create a DataFrame with sensitive columns
        df = pd.DataFrame({
            "Name": ["Alice", "Bob"],
            "Email": ["a@test.com", "b@test.com"],
            "Salary": [50000, 60000]
        })
        sanitized_df = guardrails.sanitize_dataframe(df)
        # The sanitized DataFrame should **not** contain sensitive columns
        for col in sanitized_df.columns:
            self.assertNotIn(col.lower(), ["email", "salary"])

    def test_output_blocking(self):
        sensitive_output = "Customer emails: a@test.com, b@test.com"
        self.assertFalse(guardrails.check_output(sensitive_output))

if __name__ == "__main__":
    unittest.main()





