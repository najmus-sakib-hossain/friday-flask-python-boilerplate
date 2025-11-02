# ✅ Vercel Deployment Checklist

## Pre-Deployment Verification

### 1. ✅ Core Files Present
- [x] `vercel.json` - Vercel configuration
- [x] `api/index.py` - Serverless entry point
- [x] `main.py` - Flask application
- [x] `pyproject.toml` - Dependencies
- [x] `.gitignore` - Excludes .env and sensitive files

### 2. ✅ Routes Working Locally
Test these URLs in your browser while Flask is running:

**Standard Routes (Always Work):**
- [ ] http://localhost:8080/ - Home page
- [ ] http://localhost:8080/api/data - Sample data
- [ ] http://localhost:8080/api/items/1 - Get item by ID

**Multimodal Routes (Require Env Vars):**
- [ ] http://localhost:8080/api/multimodal - API guide (text response)

### 3. 🔐 Environment Variables

#### Required for Multimodal Features:
```
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_LOCATION=us-central1
GOOGLE_CREDENTIALS_BASE64=your-base64-credentials
GEMINI_API_KEY=your-gemini-api-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**Status:** See `.env.template` for setup instructions

### 4. 📦 Dependencies Check
- [x] All packages in `pyproject.toml`
- [x] `python-dotenv` for local dev
- [x] `google-genai` for Gemini image generation
- [x] `google-auth` for Vertex AI
- [x] `cloudinary` for media storage
- [x] `flask-cors` for CORS support

## Deployment Steps

### Option 1: Vercel Dashboard (Recommended)

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com/new
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt` or leave default

4. **Add Environment Variables**
   In Vercel Dashboard → Settings → Environment Variables, add:
   - `VERTEX_PROJECT_ID`
   - `VERTEX_LOCATION`
   - `GOOGLE_CREDENTIALS_BASE64`
   - `GEMINI_API_KEY`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`

   **Important:** Select all environments (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Your app will be live!

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Add environment variables
vercel env add VERTEX_PROJECT_ID
vercel env add VERTEX_LOCATION
vercel env add GOOGLE_CREDENTIALS_BASE64
vercel env add GEMINI_API_KEY
vercel env add CLOUDINARY_CLOUD_NAME
vercel env add CLOUDINARY_API_KEY
vercel env add CLOUDINARY_API_SECRET

# Deploy to production
vercel --prod
```

## Post-Deployment Testing

Once deployed, test these URLs (replace `your-app` with your Vercel URL):

### Standard Endpoints
```bash
# Home page
curl https://your-app.vercel.app/

# Sample data
curl https://your-app.vercel.app/api/data

# Get item
curl https://your-app.vercel.app/api/items/1
```

### Multimodal Endpoints (if env vars configured)

```bash
# Generate image
curl -X POST https://your-app.vercel.app/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset", "aspect_ratio": "16:9"}'

# Generate music
curl -X POST https://your-app.vercel.app/api/generate-music \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Upbeat electronic music", "duration_seconds": 20}'

# Start video generation
curl -X POST https://your-app.vercel.app/api/video/start \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A drone flying over beach", "duration_seconds": 8}'
```

## Current Status

### ✅ Ready for Deployment
- Flask app structure is correct
- Routes are properly configured
- Vercel configuration is in place
- Dependencies are defined
- Error handling is implemented
- CORS is enabled

### ⚠️ Configuration Needed (Optional)
If you want multimodal features to work, you need to:
1. Set up Google Cloud project with Vertex AI enabled
2. Get Gemini API key from Google AI Studio
3. Create Cloudinary account
4. Add all environment variables to Vercel

**Without these:** Standard routes will work fine!

### ✅ What Works Without Env Vars
- Home page (/)
- Sample data endpoint (/api/data)
- Get item endpoint (/api/items/<id>)
- API guide (/api/multimodal)

### 🔐 What Needs Env Vars
- POST /api/generate-image
- POST /api/generate-music
- POST /api/video/start
- GET /api/video/status/<id>

## Troubleshooting

### App Returns 503 for Multimodal Routes
**Solution:** Add environment variables in Vercel Dashboard → Settings → Environment Variables

### Build Fails on Vercel
**Solution:** Ensure `pyproject.toml` has all dependencies listed

### CORS Errors
**Solution:** Already handled! `flask-cors` is enabled for all origins

### Function Timeout
**Solution:** Video generation uses async pattern - use start/status endpoints

## Quick Deploy Commands

```bash
# 1. Commit your changes
git add .
git commit -m "Ready for deployment"
git push

# 2. Deploy with Vercel CLI
vercel --prod

# 3. Check deployment
vercel ls
```

## Success Criteria

Your deployment is successful if:
- ✅ Home page loads
- ✅ `/api/data` returns JSON
- ✅ `/api/items/1` returns item data
- ✅ No build errors in Vercel dashboard
- ✅ (Optional) Multimodal routes work if env vars are set

## Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Vercel Support:** https://vercel.com/support
- **Check Logs:** Vercel Dashboard → Deployments → Click deployment → View Function Logs

---

## 🚀 You're Ready!

Your Flask application is **deployment-ready**. The standard routes will work immediately. Add environment variables when you're ready to enable AI features.

**Deploy now with:** `vercel --prod`
