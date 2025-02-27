"""
Core engine for the shift bidding system.
"""
import csv
from typing import Dict, List, Tuple, Set
import pandas as pd
from pathlib import Path


class ValidationError(Exception):
    """Raised when input data validation fails."""
    pass


class BidEngine:
    def __init__(self):
        self.user_selections: Dict[int, List[str]] = {}
        self.user_rankings: List[Tuple[int, int]] = []
        self.assignments: Dict[int, Tuple[str, int]] = {}

    @staticmethod
    def validate_csv_format(file_path: str, expected_columns: List[str]) -> None:
        """
        Validates CSV file format and structure.
        
        Args:
            file_path: Path to the CSV file
            expected_columns: List of expected column names
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            df = pd.read_csv(file_path)
            if not all(col in df.columns for col in expected_columns):
                raise ValidationError(f"Missing required columns. Expected: {expected_columns}")
        except Exception as e:
            raise ValidationError(f"Error validating CSV file: {str(e)}")

    def import_user_selections(self, filename: str) -> None:
        """
        Imports user selections from a CSV file.
        
        Args:
            filename: Path to the CSV file
            
        Raises:
            ValidationError: If file format is invalid
        """
        try:
            self.validate_csv_format(filename, ['user_id'])
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                if len(header) < 2:
                    raise ValidationError("CSV must contain at least user_id and one selection")
                
                for row in reader:
                    if not row[0].isdigit():
                        raise ValidationError(f"Invalid user ID format: {row[0]}")
                    user = int(row[0])
                    selections = row[1:]
                    if not selections:
                        raise ValidationError(f"No selections found for user {user}")
                    self.user_selections[user] = selections
        except Exception as e:
            raise ValidationError(f"Error importing user selections: {str(e)}")

    def import_user_rankings(self, filename: str) -> None:
        """
        Imports user rankings from a CSV file.
        
        Args:
            filename: Path to the CSV file
            
        Raises:
            ValidationError: If file format is invalid
        """
        try:
            self.validate_csv_format(filename, ['user_id', 'rank'])
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if not all(val.isdigit() for val in row[:2]):
                        raise ValidationError(f"Invalid data format in row: {row}")
                    user = int(row[0])
                    rank = int(row[1])
                    self.user_rankings.append((user, rank))
        except Exception as e:
            raise ValidationError(f"Error importing user rankings: {str(e)}")

    def assign_items(self) -> Dict[int, Tuple[str, int]]:
        """
        Assigns items based on user rankings and preferences.
        Users with rankings but no selections will be skipped.
        
        Returns:
            Dictionary mapping users to their assignments and choice numbers
            
        Raises:
            ValidationError: If assignment cannot be completed
        """
        if not self.user_selections or not self.user_rankings:
            raise ValidationError("Must import both selections and rankings before assignment")

        user_rankings_sorted = sorted(self.user_rankings, key=lambda x: x[1])
        assigned_items: Set[str] = set()
        self.assignments = {}

        for user, _ in user_rankings_sorted:
            if user not in self.user_selections:
                # Skip users that have rankings but no selections
                continue

            assignment_made = False
            for index, item in enumerate(self.user_selections[user]):
                if item not in assigned_items:
                    self.assignments[user] = (item, index + 1)
                    assigned_items.add(item)
                    assignment_made = True
                    break

            if not assignment_made:
                # If no assignment could be made, skip this user
                continue

        return self.assignments

    def export_assignments(self, filename: str, queue_group: str, timezone: str) -> None:
        """
        Exports assignments to a CSV file.
        
        Args:
            filename: Output file path
            queue_group: Queue group identifier
            timezone: Timezone identifier
            
        Raises:
            ValidationError: If export fails
        """
        try:
            output_path = Path(filename)
            if not output_path.parent.exists():
                output_path.parent.mkdir(parents=True)

            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["User", "Assigned Item", "Choice #", "Rank", "All Selections"])
                
                for user, (item, choice_num) in self.assignments.items():
                    rank = next((rank for u, rank in self.user_rankings if u == user), None)
                    selections = ', '.join(self.user_selections[user])
                    writer.writerow([
                        user,
                        item,
                        f"{choice_num} ({self._ordinal(choice_num)})",
                        rank,
                        selections
                    ])

                # Add unassigned users to the output
                assigned_users = set(self.assignments.keys())
                ranked_users = set(u for u, _ in self.user_rankings)
                unassigned_users = ranked_users - assigned_users
                
                for user in unassigned_users:
                    rank = next((rank for u, rank in self.user_rankings if u == user), None)
                    selections = ', '.join(self.user_selections.get(user, ['No selections']))
                    writer.writerow([
                        user,
                        "No assignment",
                        "N/A",
                        rank,
                        selections
                    ])

        except Exception as e:
            raise ValidationError(f"Error exporting assignments: {str(e)}")

    @staticmethod
    def _ordinal(n: int) -> str:
        """Returns the ordinal string representation of an integer."""
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}" 