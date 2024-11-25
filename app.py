from flask import Flask, request, jsonify
from src.timeline import Timeline

import os

app = Flask(__name__)

@app.route('/search-terms', methods=['GET'])
def search_terms():
    # Extract parameters from the request
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    geo = request.args.get('geo')
    freq = request.args.get('freq')
    terms = request.args.getlist('terms')  # List of terms
    search = Timeline()

    if not all([start_date, end_date, geo, terms, freq]):
        return jsonify({"error": "Missing required parameters"}), 400
    

    data = search.get_search_volumes(
        start_date=start_date,
        end_date=end_date,
        geo_restriction='country',
        geo_restriction_option='US',
        terms=terms,
        frequency=freq
    )
    
    # Validate and process input
   
    # Return the parsed parameters as a JSON response (for demo purposes)
    response = {
        'data': data
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=os.getenv("ENVIRONMENT") == 'development')
