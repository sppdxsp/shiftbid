# Shift Bidding Engine

A web application for managing shift bidding and assignments based on user preferences and rankings.

## Features

- Upload and process user shift preferences
- Handle user rankings and priority assignments
- Automated shift assignment based on preferences and rankings
- Web interface for easy data management
- CSV export of final assignments

## CSV File Formats

### User Selections CSV
```csv
user_id,selection_1,selection_2,selection_3,...
1,Shift A,Shift B,Shift C
2,Shift B,Shift A,Shift D
```

### User Rankings CSV
```csv
user_id,rank
1,1
2,2
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the web server:
   ```bash
   python -m bid_engine.web.app
   ```
2. Open your browser to `http://localhost:5000`
3. Upload your CSV files
4. Configure your queue group and timezone
5. Process assignments
6. Download results

## Project Structure

```
bid_engine/
├── core/           # Core bidding engine logic
├── web/           # Web interface
│   ├── static/    # Static assets (CSS, JS)
│   └── templates/ # HTML templates
└── tests/         # Test suite
```

## Development

To run tests:
```bash
pytest
```

## License

MIT License 
