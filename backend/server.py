import os
from flask import Flask, jsonify
from supabase import create_client, Client

# Initialize Flask app
app = Flask(__name__)

# Get Supabase credentials from environment variables set in Render
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# This is the main route, it just confirms the server is running
@app.route("/")
def hello_world():
    return "<p>Hello! Your Python backend is live!</p>"

# This is a new route to test our database connection
@app.route("/test-db")
def test_db_connection():
    try:
        # Try to fetch the 5 most recent records from the 'call_records' table
        response = supabase.table('call_records').select("id, created_at").limit(5).execute()
        # If successful, return a success message with the data
        return jsonify({
            "status": "success",
            "message": "Successfully connected to Supabase!",
            "data": response.data
        })
    except Exception as e:
        # If it fails, return an error message
        return jsonify({
            "status": "error",
            "message": f"Failed to connect to Supabase: {str(e)}"
        }), 500
