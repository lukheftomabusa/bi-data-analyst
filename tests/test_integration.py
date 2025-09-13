import pytest
from agent import DataCollector, DataCleaner, DataAnalyst

def test_integration_pipeline(monkeypatch):
    """
    Integration test for the BI pipeline.
    Ensures that data flows correctly through Collector → Cleaner → Analyst.
    """

    # --- Step 1: Mock Collector ---
    collector = DataCollector()
    monkeypatch.setattr(collector, "run", lambda _: {"raw": ["dirty1", "dirty2", None]})
    raw_data = collector.run("dummy_input")

    assert isinstance(raw_data, dict), "Collector should return a dict"
    assert "raw" in raw_data, "Collector output missing 'raw' key"

    # --- Step 2: Mock Cleaner ---
    cleaner = DataCleaner()
    monkeypatch.setattr(cleaner, "run", lambda data: [d for d in data["raw"] if d is not None])
    cleaned_data = cleaner.run(raw_data)

    assert isinstance(cleaned_data, list), "Cleaner should return a list"
    assert None not in cleaned_data, "Cleaner should remove None values"
    assert len(cleaned_data) > 0, "Cleaner returned empty data"

    # --- Step 3: Mock Analyst ---
    analyst = DataAnalyst()
    monkeypatch.setattr(analyst, "run", lambda data: f"Processed {len(data)} records")
    report = analyst.run(cleaned_data)

    assert isinstance(report, str), "Analyst should return a string"
    assert "Processed" in report, "Analyst output missing keyword 'Processed'"
