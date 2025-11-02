#!/usr/bin/env python3
"""
Test script to verify the Flask app works correctly
Run this after setting up your environment variables
"""
import sys
import os

# Load environment variables from .env file (development only)
# In production, Vercel provides environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded environment variables from .env file (development mode)\n")
except ImportError:
    print("⚠️  python-dotenv not installed. Run: uv sync\n")

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported successfully")
        
        import flask_cors
        print("✓ Flask-CORS imported successfully")
        
        import requests
        print("✓ Requests imported successfully")
        
        # Test optional multimodal dependencies
        try:
            import cloudinary
            print("✓ Cloudinary imported successfully")
            
            import google.auth
            print("✓ Google Auth imported successfully")
            
            import google.generativeai
            print("✓ Google Generative AI imported successfully")
            
            print("\n✅ All dependencies imported successfully!")
            return True
        except ImportError as e:
            print(f"\n⚠️  Multimodal dependencies not available: {e}")
            print("   Standard API routes will work, but multimodal routes require additional setup.")
            return True
            
    except ImportError as e:
        print(f"\n❌ Missing required dependency: {e}")
        print("   Run: uv sync")
        return False

def test_app():
    """Test that the Flask app can be imported and has routes registered"""
    print("\nTesting Flask app...")
    try:
        from main import app
        print("✓ App imported successfully")
        
        # Check registered blueprints
        blueprints = list(app.blueprints.keys())
        print(f"✓ Registered blueprints: {', '.join(blueprints)}")
        
        # Check routes
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"✓ Total routes: {len(routes)}")
        
        print("\n✅ Flask app initialized successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error importing app: {e}")
        return False

def test_env_vars():
    """Test if environment variables are set"""
    print("\nChecking environment variables...")
    
    required_for_multimodal = [
        "VERTEX_PROJECT_ID",
        "VERTEX_LOCATION",
        "GOOGLE_CREDENTIALS_BASE64",
        "GEMINI_API_KEY",
        "CLOUDINARY_CLOUD_NAME",
        "CLOUDINARY_API_KEY",
        "CLOUDINARY_API_SECRET",
    ]
    
    missing = []
    for var in required_for_multimodal:
        if os.getenv(var):
            print(f"✓ {var} is set")
        else:
            print(f"⚠️  {var} is not set")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Missing environment variables for multimodal API: {', '.join(missing)}")
        print("   Copy .env.example to .env and fill in your credentials.")
        print("   Standard API routes will still work.")
    else:
        print("\n✅ All environment variables are set!")
    
    return True

def main():
    print("=" * 60)
    print("Flask + Multimodal AI - Setup Verification")
    print("=" * 60)
    print()
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Flask App", test_app()))
    results.append(("Environment", test_env_vars()))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! You can now run the app with:")
        print("   python main.py")
        print("   or")
        print("   gunicorn main:app")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
