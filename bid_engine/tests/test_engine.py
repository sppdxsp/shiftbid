"""
Tests for the core bidding engine functionality.
"""
import pytest
from pathlib import Path
import csv
from bid_engine.core.engine import BidEngine, ValidationError


@pytest.fixture
def temp_csv_files(tmp_path):
    """Creates temporary CSV files for testing."""
    # Create selections CSV
    selections_file = tmp_path / "selections.csv"
    with open(selections_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'selection_1', 'selection_2', 'selection_3'])
        writer.writerow(['1', 'Shift A', 'Shift B', 'Shift C'])
        writer.writerow(['2', 'Shift B', 'Shift A', 'Shift D'])
        writer.writerow(['3', 'Shift C', 'Shift D', 'Shift A'])

    # Create rankings CSV
    rankings_file = tmp_path / "rankings.csv"
    with open(rankings_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'rank'])
        writer.writerow(['1', '2'])
        writer.writerow(['2', '1'])
        writer.writerow(['3', '3'])

    return selections_file, rankings_file


def test_import_user_selections(temp_csv_files):
    """Test importing user selections from CSV."""
    selections_file, _ = temp_csv_files
    engine = BidEngine()
    engine.import_user_selections(str(selections_file))
    
    assert len(engine.user_selections) == 3
    assert engine.user_selections[1] == ['Shift A', 'Shift B', 'Shift C']
    assert engine.user_selections[2] == ['Shift B', 'Shift A', 'Shift D']


def test_import_user_rankings(temp_csv_files):
    """Test importing user rankings from CSV."""
    _, rankings_file = temp_csv_files
    engine = BidEngine()
    engine.import_user_rankings(str(rankings_file))
    
    assert len(engine.user_rankings) == 3
    assert (2, 1) in engine.user_rankings  # User 2 has rank 1
    assert (1, 2) in engine.user_rankings  # User 1 has rank 2


def test_assign_items(temp_csv_files):
    """Test the assignment algorithm."""
    selections_file, rankings_file = temp_csv_files
    engine = BidEngine()
    
    engine.import_user_selections(str(selections_file))
    engine.import_user_rankings(str(rankings_file))
    
    assignments = engine.assign_items()
    
    assert len(assignments) == 3
    # User 2 (rank 1) should get their first choice
    assert assignments[2][0] == 'Shift B'
    assert assignments[2][1] == 1  # First choice


def test_validation_error_on_missing_data():
    """Test that appropriate errors are raised for missing data."""
    engine = BidEngine()
    
    with pytest.raises(ValidationError):
        engine.assign_items()  # Should fail without data


def test_export_assignments(temp_csv_files, tmp_path):
    """Test exporting assignments to CSV."""
    selections_file, rankings_file = temp_csv_files
    engine = BidEngine()
    
    engine.import_user_selections(str(selections_file))
    engine.import_user_rankings(str(rankings_file))
    engine.assign_items()
    
    output_file = tmp_path / "assignments.csv"
    engine.export_assignments(str(output_file), "TestGroup", "UTC")
    
    assert output_file.exists()
    with open(output_file) as f:
        content = f.read()
        assert "User" in content
        assert "Assigned Item" in content
        assert "Choice #" in content 