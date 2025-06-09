from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from services.auth_service import SalesforceAuthService
from services.api_service import SalesforceAPIClient

auth_service = SalesforceAuthService()  # which wil help me in authenticating with Salesforce
api_service = SalesforceAPIClient(auth_service)  # wil help me in sending requests to Salesforce API

load_dotenv()

app = Flask(__name__)

@app.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    response = api_service.request(
        method='POST',
        endpoint=f'/services/data/{os.getenv("SALESFORCE_API_VERSION")}/sobjects/Lead/',
        json=data
    )
    if response.status_code == 201:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route('/leads/<lead_id>', methods=['GET'])
def get_lead(lead_id):
    if not lead_id:
        return jsonify({"error": "Lead ID is required"}), 400
    response = api_service.request(
        method='GET',
        endpoint=f'/services/data/{os.getenv("SALESFORCE_API_VERSION")}/sobjects/Lead/{lead_id}'
    )
    if response.status_code == 200:
        return jsonify(response.json()), 200   
    else:
        return jsonify({"error": response.text}), response.status_code
   

@app.route('/leads/<lead_id>', methods=['PATCH'])
def update_lead(lead_id):
    if not lead_id:
        return jsonify({"error": "Lead ID is required"}), 400
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    response = api_service.request(
        method='PATCH',
        endpoint=f'/services/data/{os.getenv("SALESFORCE_API_VERSION")}/sobjects/Lead/{lead_id}',
        json=data
    )
    if response.status_code == 204:
        return jsonify({"message": "Lead updated successfully"}), 200
    else:
        return jsonify({"error": response.text}), response.status_code
    

@app.route('/leads/<lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    if not lead_id:
        return jsonify({"error": "Lead ID is required"}), 400
    response = api_service.request(
        method='DELETE',
        endpoint=f'/services/data/{os.getenv("SALESFORCE_API_VERSION")}/sobjects/Lead/{lead_id}'
    )
    if response.status_code == 204:
        return jsonify({"message": "Lead deleted successfully"}), 200
    else:
        return jsonify({"error": response.text}), response.status_code  
    

if __name__ == '__main__':
    app.run(debug=True,port=int(os.getenv("PORT", 8000)))
