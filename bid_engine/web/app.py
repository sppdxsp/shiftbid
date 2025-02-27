"""
Web interface for the Shift Bidding Engine.
"""
import os
import argparse
from pathlib import Path
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import pytz
from ..core.engine import BidEngine, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page."""
    print("Accessing index page")  # Debug output
    timezones = pytz.common_timezones
    return render_template('index.html', timezones=timezones)

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and process assignments."""
    print("Processing file upload")  # Debug output
    if 'selections' not in request.files or 'rankings' not in request.files:
        flash('Both files are required', 'error')
        return redirect(url_for('index'))

    selections_file = request.files['selections']
    rankings_file = request.files['rankings']
    queue_group = request.form.get('queue_group', '')
    timezone = request.form.get('timezone', 'UTC')

    if not queue_group:
        flash('Queue group is required', 'error')
        return redirect(url_for('index'))

    if not all([selections_file.filename, rankings_file.filename]):
        flash('Please select both files', 'error')
        return redirect(url_for('index'))

    if not all(allowed_file(f.filename) for f in [selections_file, rankings_file]):
        flash('Only CSV files are allowed', 'error')
        return redirect(url_for('index'))

    try:
        print(f"Processing files: {selections_file.filename}, {rankings_file.filename}")  # Debug output
        # Save uploaded files
        selections_path = app.config['UPLOAD_FOLDER'] / secure_filename(selections_file.filename)
        rankings_path = app.config['UPLOAD_FOLDER'] / secure_filename(rankings_file.filename)
        
        selections_file.save(str(selections_path))
        rankings_file.save(str(rankings_path))

        # Process assignments
        engine = BidEngine()
        engine.import_user_selections(str(selections_path))
        engine.import_user_rankings(str(rankings_path))
        assignments = engine.assign_items()

        # Generate output file
        output_filename = f"user_item_assignments_{queue_group}_{timezone}.csv"
        output_path = app.config['UPLOAD_FOLDER'] / output_filename
        engine.export_assignments(str(output_path), queue_group, timezone)

        # Clean up input files
        selections_path.unlink()
        rankings_path.unlink()

        print(f"Generated output file: {output_filename}")  # Debug output
        # Send the output file
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='text/csv'
        )

    except ValidationError as e:
        print(f"Validation error: {str(e)}")  # Debug output
        flash(f'Error processing files: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug output
        flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

def main():
    """Entry point for the console script."""
    parser = argparse.ArgumentParser(description='Start the Shift Bidding Engine web interface.')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5001, help='Port to listen on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"Starting Shift Bidding Engine on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main() 