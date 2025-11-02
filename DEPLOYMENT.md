# Deployment Guide for Vercel

## Prerequisites

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **Environment Variables** - Prepare your API credentials
3. **UV Package Manager** - Recommended for local development

## Quick Deploy to Vercel

### Method 1: Using Vercel Dashboard (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add multimodal API routes"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Git Repository"
   - Select your repository
   - Click "Import"

3. **Configure Environment Variables**
   - In the "Configure Project" screen, expand "Environment Variables"
   - Add each variable from `.env.example`:
     - `VERTEX_PROJECT_ID`
     - `VERTEX_LOCATION`
     - `GOOGLE_CREDENTIALS_BASE64`
     - `GEMINI_API_KEY`
     - `CLOUDINARY_CLOUD_NAME`
     - `CLOUDINARY_API_KEY`
     - `CLOUDINARY_API_SECRET`

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (usually 1-2 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Method 2: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - What's your project's name? `your-project-name`
   - In which directory is your code located? `./`
   - Want to override the settings? `N`

4. **Add Environment Variables**
   ```bash
   # Add each variable
   vercel env add VERTEX_PROJECT_ID
   vercel env add VERTEX_LOCATION
   vercel env add GOOGLE_CREDENTIALS_BASE64
   vercel env add GEMINI_API_KEY
   vercel env add CLOUDINARY_CLOUD_NAME
   vercel env add CLOUDINARY_API_KEY
   vercel env add CLOUDINARY_API_SECRET
   ```
   
   When prompted:
   - Select environment: Choose `Production`, `Preview`, and `Development`
   - Enter the value for each variable

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Verifying Deployment

### Test Basic Routes

```bash
# Test home page
curl https://your-app.vercel.app/

# Test sample API
curl https://your-app.vercel.app/api/data

# Test multimodal API guide
curl https://your-app.vercel.app/api/multimodal
```

### Test Multimodal Routes

```bash
# Generate an image
curl -X POST https://your-app.vercel.app/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset over mountains", "aspect_ratio": "16:9"}'

# Generate music
curl -X POST https://your-app.vercel.app/api/generate-music \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Upbeat electronic music", "duration_seconds": 20}'

# Start video generation
curl -X POST https://your-app.vercel.app/api/video/start \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A drone flying over beach", "duration_seconds": 8, "aspect_ratio": "16:9"}'
```

## Troubleshooting

### Environment Variables Not Loading

**Problem**: API returns 503 or "not configured" errors

**Solution**:
1. Check environment variables in Vercel Dashboard → Settings → Environment Variables
2. Ensure they're set for "Production" environment
3. Redeploy after adding variables: `vercel --prod`

### Import Errors for Multimodal Routes

**Problem**: "Multimodal routes not available" in logs

**Solution**:
- This is expected if environment variables aren't set
- Standard API routes (`/api/data`, `/`) will still work
- Add environment variables and redeploy to enable multimodal routes

### Base64 Credentials Error

**Problem**: "Invalid Google credentials format"

**Solution**:
1. Re-encode your service account key without line breaks:
   ```bash
   # Linux/Mac
   cat service-account-key.json | base64 -w 0
   
   # Windows PowerShell
   [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("service-account-key.json"))
   ```
2. Copy the entire output (should be one long line)
3. Update the environment variable in Vercel

### Function Timeout for Video Generation

**Problem**: 504 timeout errors

**Solution**:
- Use async endpoints: `/api/video/start` and `/api/video/status/<id>`
- Don't use synchronous video generation on serverless platforms
- Poll the status endpoint every 5-10 seconds

### CORS Errors

**Problem**: CORS errors when calling from frontend

**Solution**:
- CORS is already enabled in the app (`flask_cors`)
- If issues persist, update allowed origins in `main.py`:
  ```python
  CORS(app, origins=["https://your-frontend.com"])
  ```

## Local Development

```bash
# Install dependencies
uv sync

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run with Flask dev server
python main.py

# Or run with Gunicorn
gunicorn main:app
```

## Production Checklist

- [ ] All environment variables set in Vercel
- [ ] Google Cloud service account has required permissions
- [ ] Cloudinary account configured
- [ ] `.env` file added to `.gitignore` (already done)
- [ ] Test all endpoints after deployment
- [ ] Monitor function execution time in Vercel dashboard
- [ ] Set up error monitoring (optional: Sentry, LogRocket)

## Updating Your Deployment

```bash
# Make code changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel auto-deploys from main branch
# Or manually trigger: vercel --prod
```

## Monitoring

- **Vercel Dashboard**: View deployment logs, function execution, errors
- **Analytics**: Enable Vercel Analytics in project settings
- **Logs**: View real-time logs with `vercel logs`

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Google Vertex AI: https://cloud.google.com/vertex-ai/docs
- Cloudinary Docs: https://cloudinary.com/documentation
- Flask Docs: https://flask.palletsprojects.com/
