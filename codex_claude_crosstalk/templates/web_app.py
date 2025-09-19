"""
Web Application Template

This template provides a foundation for web applications using Flask.
"""

from flask import Flask, render_template, request, jsonify
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='{{ project_name }}')


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': '{{ project_name }}'})


@app.route('/api/data', methods=['GET', 'POST'])
def data():
    """Data endpoint for CRUD operations."""
    if request.method == 'GET':
        # Return data
        return jsonify({'message': 'Data retrieved successfully', 'data': []})
    
    elif request.method == 'POST':
        # Create new data
        data = request.get_json()
        logger.info(f"Received data: {data}")
        
        # Process the data here
        response = {
            'message': 'Data created successfully',
            'id': 1,  # Example ID
            'data': data
        }
        
        return jsonify(response), 201


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == "__main__":
    logger.info("Starting {{ project_name }} web application")
    
    # Configuration
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    
    app.run(debug=debug, host=host, port=port)