# Installation Guide

## Quick Installation

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package:
   ```bash
   pip install shift-bid-engine
   ```

3. Run the application:
   ```bash
   shift-bid-engine
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

## Command Line Options

You can customize the server settings using command line options:

```bash
shift-bid-engine --host 127.0.0.1 --port 8080 --debug
```

Available options:
- `--host`: Host address to bind to (default: 0.0.0.0)
- `--port`: Port to listen on (default: 5001)
- `--debug`: Enable debug mode

## Manual Installation (Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shift-bid-engine.git
   cd shift-bid-engine
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

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

## Troubleshooting

1. Port 5001 is already in use:
   - Use a different port: `shift-bid-engine --port 8080`
   - Or stop the process using port 5001

2. Permission denied when creating uploads directory:
   - Ensure you have write permissions in the installation directory
   - Try running with elevated privileges (not recommended for production)

3. CSV file format errors:
   - Ensure your CSV files match the required format exactly
   - Check for extra columns or missing headers
   - Verify all user IDs are integers
   - Make sure there are no empty rows

## Security Notes

1. This is a development server and should not be used in production without proper security measures
2. Consider setting a secure SECRET_KEY environment variable:
   ```bash
   export SECRET_KEY='your-secure-secret-key'
   ```
3. In production, use a proper WSGI server like Gunicorn or uWSGI

## Support

For issues and feature requests, please visit:
https://github.com/yourusername/shift-bid-engine/issues 