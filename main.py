from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from resultJsonIterator import getVideoIdRelevant
from headerFetcher import getTopicHeader
from ezyZip.finalFile import generate_study_material

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# this end point is for the feature lecture suggester. It takes in tokens and suggests lectures according to the tokens
# sends back youtube video Ids which are then embedded on the frontend
@app.route('/api/videoId')
def home():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    # Example: If you want to process query and return data
    if (query.count(",") != None):
        modified = getTopicHeader(query.split(","))
        print(modified)
    else:
        modified = getTopicHeader([query])
        print(modified)
    result = getVideoIdRelevant(modified)

    return jsonify({"result": result})  # Ensure JSON response

# this feature is for making the worksheets
# it sends a zip file containing 3 files Notes, Tests and Assignment
@app.route('/api/worksheets', methods=['GET'])
def download_pdfs():
    """API Endpoint to generate and return a ZIP file with PDFs."""
    topic = request.args.get('q', '').strip()
    if not topic:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    zip_buffer = generate_study_material(topic)

    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name=f"{topic}_study_material.zip")



if __name__ == '__main__':
    app.run(debug=True)
