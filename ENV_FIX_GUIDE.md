# Environment Variables Fix Guide

## ✅ Issues Fixed

### 1. **`.env` File Format** - ✅ FIXED
**Problem**: Quotes and semicolons in `.env` caused parsing errors

**Before:**
```bash
GEMINI="AIzaSy...";
VERTEX_PROJECT_ID="friday-458605"
```

**After:**
```bash
GEMINI=AIzaSy...
VERTEX_PROJECT_ID=friday-458605
```

**Solution**: Removed quotes and semicolons from all environment variables.

---

### 2. **`python-dotenv` Missing** - ✅ FIXED
**Problem**: `python-dotenv` was in optional dev dependencies, not loaded in production

**Before:** In `pyproject.toml`:
```toml
[project.optional-dependencies]
dev = [
  "python-dotenv>=1.0.0",
]
```

**After:**
```toml
[project]
dependencies = [
  ...
  "python-dotenv>=1.0.0",
  ...
]
```

**Solution**: Moved `python-dotenv` to main dependencies and ran `uv sync`.

---

### 3. **Google Credentials Format** - ✅ CONFIGURED
**Problem**: Multimodal API needed `GOOGLE_CREDENTIALS_BASE64` which didn't exist

**Solution**: Generated base64-encoded service account JSON from existing credentials:
```bash
GOOGLE_CREDENTIALS_BASE64=eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjog...
```

---

### 4. **Missing Environment Variables** - ✅ ADDED
**Added to `.env`:**
```bash
VERTEX_PROJECT_ID=friday-458605
VERTEX_LOCATION=us-central1
GOOGLE_CREDENTIALS_BASE64=...
GEMINI_API_KEY=AIzaSy...
CLOUDINARY_CLOUD_NAME=demo
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

---

## 🎯 Current Status

### Local Development
- ✅ Flask server starts successfully
- ✅ Multimodal services initialize
- ✅ Standard API endpoints work
- ⚠️  Multimodal endpoints partially work (see issues below)

### Vercel Deployment
- ✅ Deployed and accessible
- ✅ Standard API endpoints work
- ❌ Multimodal endpoints need env vars configured in Vercel dashboard

---

## ⚠️ Remaining Issues

### Issue 1: Invalid Google Service Account Credentials

**Error:**
```
Invalid JWT Signature
```

**Cause**: The service account private key needs to be from a properly configured Google Cloud service account with Vertex AI permissions.

**Solution**: 
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to IAM & Admin → Service Accounts
3. Create a new service account or use existing `friday-better-auth@friday-458605.iam.gserviceaccount.com`
4. Grant roles:
   - Vertex AI User
   - Service Account Token Creator
5. Create a new JSON key
6. Convert to base64 and update `GOOGLE_CREDENTIALS_BASE64`

---

### Issue 2: Cloudinary Credentials Are Placeholders

**Current Values:**
```bash
CLOUDINARY_CLOUD_NAME=demo
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

**Solution Options:**

#### Option A: Sign up for FREE Cloudinary Account (Recommended)
1. Visit https://cloudinary.com/users/register/free
2. Get your credentials from the Dashboard
3. Update `.env`:
```bash
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
```

#### Option B: Use for Testing Without Media Storage
- Keep placeholder values
- APIs will work but fail at upload step
- You'll get base64 encoded media in responses instead of URLs

---

### Issue 3: Vercel Environment Variables Not Set

**Problem**: Vercel deployment doesn't have environment variables

**Solution**:

#### Using Vercel CLI:
```bash
vercel env add VERTEX_PROJECT_ID
vercel env add VERTEX_LOCATION
vercel env add GOOGLE_CREDENTIALS_BASE64
vercel env add GEMINI_API_KEY
vercel env add CLOUDINARY_CLOUD_NAME
vercel env add CLOUDINARY_API_KEY
vercel env add CLOUDINARY_API_SECRET
```

#### Using Vercel Dashboard:
1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable:
   - `VERTEX_PROJECT_ID` = `friday-458605`
   - `VERTEX_LOCATION` = `us-central1`
   - `GOOGLE_CREDENTIALS_BASE64` = (your base64 string)
   - `GEMINI_API_KEY` = `AIzaSy...`
   - `CLOUDINARY_CLOUD_NAME` = (your cloudinary name)
   - `CLOUDINARY_API_KEY` = (your cloudinary key)
   - `CLOUDINARY_API_SECRET` = (your cloudinary secret)
5. Redeploy:
```bash
vercel --prod
```

---

## 🧪 Testing Results

### Local Server

#### Standard Endpoints ✅
```bash
$ curl http://localhost:8080/api/data
# Works perfectly
```

#### Multimodal Endpoints ⚠️
```bash
$ curl -X POST http://localhost:8080/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A sunset"}'

# Response:
{
  "error": "Image generation service failed.",
  "details": "Invalid JWT Signature"
}
```

**Status**: Environment variables loaded, but credentials need to be valid Google Cloud credentials with proper permissions.

### Vercel Deployment

#### Standard Endpoints ✅
```bash
$ curl https://friday-flask-python-boilerplate.vercel.app/api/data
# Works perfectly
```

#### Multimodal Endpoints ❌
```bash
$ curl -X POST https://friday-flask-python-boilerplate.vercel.app/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A sunset"}'

# Response:
{
  "error": "Multimodal API not configured. Please set required environment variables."
}
```

**Status**: Environment variables not set in Vercel. Need to configure via Vercel dashboard or CLI.

---

## 📋 Next Steps

### For Full Local Testing:

1. **Get Valid Google Cloud Credentials**
   ```bash
   # Go to Google Cloud Console
   # Create/download proper service account JSON
   # Convert to base64 and update .env
   ```

2. **Sign up for Cloudinary (FREE)**
   ```bash
   # Visit https://cloudinary.com/users/register/free
   # Get credentials
   # Update .env
   ```

3. **Restart Flask server**
   ```bash
   python main.py
   ```

### For Vercel Deployment:

1. **Set Environment Variables in Vercel**
   - Use Vercel Dashboard or CLI
   - Add all required variables
   
2. **Redeploy**
   ```bash
   vercel --prod
   ```

3. **Test**
   ```bash
   curl https://your-app.vercel.app/api/generate-image \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Test"}'
   ```

---

## 💡 Quick Test Without Full Setup

If you just want to test the API structure without actual AI generation:

### Option 1: Mock Cloudinary
Update `endpoints/multimodal.py` to skip Cloudinary upload and return base64 data directly.

### Option 2: Use Demo Mode
Keep placeholder credentials - API will return errors at the upload step, but you can verify:
- ✅ Request validation works
- ✅ Environment variables load correctly
- ✅ Error handling works
- ✅ API structure is correct

---

## 📊 Environment Variables Checklist

### Local (.env file)
- [x] `VERTEX_PROJECT_ID` - Added
- [x] `VERTEX_LOCATION` - Added  
- [x] `GOOGLE_CREDENTIALS_BASE64` - Added (needs valid credentials)
- [x] `GEMINI_API_KEY` - Added (using existing key)
- [x] `CLOUDINARY_CLOUD_NAME` - Added (placeholder)
- [x] `CLOUDINARY_API_KEY` - Added (placeholder)
- [x] `CLOUDINARY_API_SECRET` - Added (placeholder)
- [x] `python-dotenv` - Installed

### Vercel Deployment
- [ ] `VERTEX_PROJECT_ID` - **Need to add**
- [ ] `VERTEX_LOCATION` - **Need to add**
- [ ] `GOOGLE_CREDENTIALS_BASE64` - **Need to add**
- [ ] `GEMINI_API_KEY` - **Need to add**
- [ ] `CLOUDINARY_CLOUD_NAME` - **Need to add**
- [ ] `CLOUDINARY_API_KEY` - **Need to add**
- [ ] `CLOUDINARY_API_SECRET` - **Need to add**

---

## 🔧 Files Modified

1. ✅ `.env` - Fixed format, added required variables
2. ✅ `pyproject.toml` - Moved python-dotenv to main dependencies
3. ✅ Dependencies synced with `uv sync`

---

## 🎉 Summary

**What's Working:**
- ✅ Environment variable loading
- ✅ Flask server startup
- ✅ Multimodal service initialization
- ✅ Standard API endpoints (local & Vercel)
- ✅ Request validation
- ✅ Error handling

**What Needs Action:**
- ⚠️  Get valid Google Cloud service account credentials
- ⚠️  Sign up for Cloudinary and get real credentials
- ⚠️  Configure environment variables in Vercel dashboard

**Estimated Time to Full Functionality:**
- Get Cloudinary credentials: 5 minutes (sign up is instant)
- Get Google credentials: 10-15 minutes (if you have GCP project access)
- Configure Vercel: 5 minutes
- **Total: ~20-25 minutes**

---

## 📞 Need Help?

See:
- [CLOUDINARY_SETUP.md](CLOUDINARY_SETUP.md) - Cloudinary setup guide
- [README.md](README.md) - Main documentation
- [NEXTJS_INTEGRATION.md](NEXTJS_INTEGRATION.md) - Frontend integration guide
