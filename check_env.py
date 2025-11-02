#!/usr/bin/env python3
"""
Quick test to verify environment variables and API functionality
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 60)
print("Environment Variables Check")
print("=" * 60)

# Map your .env variables to what the app expects
env_mapping = {
    "GEMINI": "GEMINI_API_KEY",
    "GOOGLE_CLIENT_EMAIL": "Service Account Email (for reference)",
    "GOOGLE_PRIVATE_KEY": "Service Account Private Key",
}

# Check what you have
print("\n📋 Variables in your .env file:")
for key in ["GEMINI", "GOOGLE_DRIVE_FOLDER_ID", "GOOGLE_CLIENT_EMAIL", "GOOGLE_PRIVATE_KEY"]:
    value = os.getenv(key)
    if value:
        if "KEY" in key or "SECRET" in key:
            print(f"  ✓ {key}: {value[:20]}... (hidden)")
        else:
            print(f"  ✓ {key}: Set")

# Check what the app needs
print("\n📋 Variables the multimodal API needs:")
needed = [
    "VERTEX_PROJECT_ID",
    "VERTEX_LOCATION", 
    "GOOGLE_CREDENTIALS_BASE64",
    "GEMINI_API_KEY",
    "CLOUDINARY_CLOUD_NAME",
    "CLOUDINARY_API_KEY",
    "CLOUDINARY_API_SECRET",
]

missing = []
for key in needed:
    value = os.getenv(key)
    if value:
        if "KEY" in key or "SECRET" in key or "BASE64" in key:
            print(f"  ✓ {key}: {value[:20]}... (hidden)")
        else:
            print(f"  ✓ {key}: {value}")
    else:
        print(f"  ✗ {key}: NOT SET")
        missing.append(key)

if missing:
    print(f"\n⚠️  Missing variables: {', '.join(missing)}")
    print("\n💡 Quick fixes:")
    
    # Check if GEMINI is set but not GEMINI_API_KEY
    if "GEMINI_API_KEY" in missing and os.getenv("GEMINI"):
        print(f"  - Add: GEMINI_API_KEY=\"{os.getenv('GEMINI')}\"")
    
    print("\n  For Google Cloud (Vertex AI), you need:")
    print("  - VERTEX_PROJECT_ID (your GCP project ID)")
    print("  - VERTEX_LOCATION (e.g., us-central1)")
    print("  - GOOGLE_CREDENTIALS_BASE64 (base64-encoded service account JSON)")
    
    print("\n  For Cloudinary, you need:")
    print("  - CLOUDINARY_CLOUD_NAME")
    print("  - CLOUDINARY_API_KEY")
    print("  - CLOUDINARY_API_SECRET")
else:
    print("\n✅ All required variables are set!")

print("\n" + "=" * 60)
