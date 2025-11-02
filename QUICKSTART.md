# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit .env and add your API credentials
```

Required variables (get these from your service providers):
- Google Cloud (Vertex AI + Service Account)
- Gemini API Key
- Cloudinary Account

### Step 3: Verify Setup

```bash
python test_setup.py
```

### Step 4: Run Locally

```bash
# Development mode
python main.py

# Production mode (with Gunicorn)
gunicorn main:app
```

Visit: http://localhost:5000

### Step 5: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variables via Vercel Dashboard or CLI
vercel env add VERTEX_PROJECT_ID
# ... (add all environment variables)

# Deploy to production
vercel --prod
```

## 📚 Documentation

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Integration Summary**: See `SUMMARY.md`

## 🆘 Need Help?

Run the test script to diagnose issues:
```bash
python test_setup.py
```

Check the documentation files for detailed troubleshooting.
