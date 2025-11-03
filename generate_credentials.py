#!/usr/bin/env python3
"""
Script to generate GOOGLE_CREDENTIALS_BASE64 from existing Google credentials
"""
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Get existing credentials
client_email = os.getenv("GOOGLE_CLIENT_EMAIL")
private_key = os.getenv("GOOGLE_PRIVATE_KEY")
project_id = os.getenv("VERTEX_PROJECT_ID", "friday-458605")  # Extracted from client email

if not client_email or not private_key:
    print("❌ Error: GOOGLE_CLIENT_EMAIL or GOOGLE_PRIVATE_KEY not found in .env")
    exit(1)

# Create service account JSON structure
service_account_json = {
    "type": "service_account",
    "project_id": project_id,
    "private_key_id": "dummy-key-id",
    "private_key": private_key,
    "client_email": client_email,
    "client_id": "",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email.replace('@', '%40')}"
}

# Convert to JSON string
json_string = json.dumps(service_account_json)

# Encode to base64
base64_encoded = base64.b64encode(json_string.encode()).decode()

print("✅ Successfully generated GOOGLE_CREDENTIALS_BASE64!")
print("\n📋 Add this to your .env file:")
print(f"\nGOOGLE_CREDENTIALS_BASE64=\"{base64_encoded}\"")
print(f"\n✅ Detected project_id: {project_id}")
print("\n⚠️  You still need to add:")
print("VERTEX_LOCATION=\"us-central1\"  # or your preferred region")
print("CLOUDINARY_CLOUD_NAME=\"your-cloud-name\"")
print("CLOUDINARY_API_KEY=\"your-api-key\"")
print("CLOUDINARY_API_SECRET=\"your-api-secret\"")
