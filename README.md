[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fvercel%2Ftree%2Fmain%2Fexamples%2Fflask&demo-title=Flask%20API&demo-description=Use%20Flask%20API%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fvercel-plus-flask.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994600/random/python.png)

# Flask + Vercel - Multimodal AI API

This Flask application provides a REST API for multimodal AI content generation (images, music, and videos) using Google Vertex AI and Gemini APIs, deployed on Vercel with Serverless Functions.

## Features

- 🎨 **Image Generation** - Generate images using Vertex AI Imagen and Gemini models
- 🎵 **Music Generation** - Create music with Google's Lyria model
- 🎬 **Video Generation** - Generate videos with Veo model (async job processing)
- ☁️ **Cloud Storage** - Automatic media upload to Cloudinary
- 🚀 **Serverless** - Deploy on Vercel with zero configuration
- 📦 **UV Package Manager** - Fast dependency management

## API Endpoints

### Standard Endpoints
- `GET /` - Home page with API documentation
- `GET /api/data` - Sample data endpoint
- `GET /api/items/<id>` - Get item by ID

### Multimodal AI Endpoints
- `POST /api/generate-image` - Generate an image
- `POST /api/generate-music` - Generate music with accompanying image
- `POST /api/video/start` - Start video generation job
- `GET /api/video/status/<operation_id>` - Check video generation status

## Setup

### Prerequisites

- Python 3.9 or higher
- [UV](https://github.com/astral-sh/uv) (recommended) or pip
- Google Cloud Project with Vertex AI API enabled
- Gemini API key
- Cloudinary account

### Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:
- `VERTEX_PROJECT_ID` - Your Google Cloud project ID
- `VERTEX_LOCATION` - GCP region (e.g., us-central1)
- `GOOGLE_CREDENTIALS_BASE64` - Base64-encoded service account JSON
- `GEMINI_API_KEY` - Your Gemini API key
- `CLOUDINARY_CLOUD_NAME` - Cloudinary cloud name
- `CLOUDINARY_API_KEY` - Cloudinary API key
- `CLOUDINARY_API_SECRET` - Cloudinary API secret

### Getting Google Credentials Base64

```bash
# Linux/Mac
cat service-account-key.json | base64 -w 0

# Windows (PowerShell)
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("service-account-key.json"))
```

## Running Locally

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (CMD)
.venv\Scripts\activate.bat
# Linux/Mac
source .venv/bin/activate

# Run with Flask development server
python main.py

# Or run with Gunicorn (production-like)
gunicorn main:app
```

Your Flask application is now available at `http://localhost:5000` (Flask) or `http://localhost:8000` (Gunicorn).

## Deployment to Vercel

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables
vercel env add VERTEX_PROJECT_ID
vercel env add VERTEX_LOCATION
vercel env add GOOGLE_CREDENTIALS_BASE64
vercel env add GEMINI_API_KEY
vercel env add CLOUDINARY_CLOUD_NAME
vercel env add CLOUDINARY_API_KEY
vercel env add CLOUDINARY_API_SECRET

# Redeploy with environment variables
vercel --prod
```

### Option 2: Vercel Dashboard

1. Push your code to GitHub
2. Import the repository in Vercel
3. Add environment variables in Project Settings → Environment Variables
4. Deploy!

## API Usage Examples

### Generate Image

```bash
curl -X POST https://your-app.vercel.app/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "aspect_ratio": "16:9"
  }'
```

### Generate Music

```bash
curl -X POST https://your-app.vercel.app/api/generate-music \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Upbeat electronic music with synthesizers",
    "duration_seconds": 20
  }'
```

### Start Video Generation

```bash
curl -X POST https://your-app.vercel.app/api/video/start \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A drone flying over a tropical beach",
    "duration_seconds": 8,
    "aspect_ratio": "16:9"
  }'
```

### Check Video Status

```bash
curl https://your-app.vercel.app/api/video/status/<operation_id>
```

## Project Structure

```
.
├── api/
│   ├── index.py          # Vercel entry point
│   └── index.md          # Original API code reference
├── endpoints/
│   ├── __init__.py       # Blueprint registration
│   ├── routes.py         # Standard API routes
│   └── multimodal.py     # Multimodal AI routes
├── main.py               # Flask application
├── pyproject.toml        # UV/pip dependencies
├── vercel.json           # Vercel configuration
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Configuration

### Aspect Ratios

**Images**: 1:1, 9:16, 16:9, 3:4, 4:3  
**Videos**: 16:9, 9:16, 1:1

### Duration Limits

**Music**: 1-30 seconds (default: 20)  
**Video**: 1-10 seconds (default: 8)

## Troubleshooting

### Multimodal routes not available

If you see "Multimodal routes not available" in logs, ensure all dependencies are installed:

```bash
uv sync
```

### Service account authentication issues

1. Verify your service account has the required permissions
2. Check that the base64 encoding is correct (no line breaks)
3. Ensure the service account has these roles:
   - Vertex AI User
   - Service Account Token Creator

### Vercel deployment timeout

Video generation is async - use the `/api/video/start` and `/api/video/status/<id>` endpoints to avoid timeouts.

## Tech Stack

- **Framework**: Flask 3.1
- **Package Manager**: UV
- **Hosting**: Vercel (Serverless Functions)
- **AI Services**: Google Vertex AI, Gemini
- **Storage**: Cloudinary
- **Python**: 3.9+

## License

MIT

## One-Click Deploy

Deploy the example using [Vercel](https://vercel.com):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)
