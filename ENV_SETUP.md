# Environment Variables Configuration

## Development vs Production

This project uses different approaches for environment variables based on the environment:

### 🔧 Development (Local)
- **Uses:** `.env` file
- **Tool:** `python-dotenv` package
- **How it works:** The app automatically loads variables from `.env` file when `VERCEL` environment variable is not set

### ☁️ Production (Vercel)
- **Uses:** Vercel Environment Variables (Dashboard or CLI)
- **Tool:** Vercel platform
- **How it works:** Vercel injects environment variables directly into the runtime

## How It Works

The code in `main.py` detects the environment:

```python
# Load .env ONLY in development
if os.getenv("VERCEL") != "1":  # Not on Vercel
    from dotenv import load_dotenv
    load_dotenv()
```

This ensures:
- ✅ Local development loads from `.env` file
- ✅ Production on Vercel uses dashboard-configured variables
- ✅ No `.env` file needed in production
- ✅ Better security (no .env in git)

## Development Setup

### 1. Install Dependencies (including dev dependencies)

```bash
# Install all dependencies including python-dotenv
uv sync --all-extras

# Or manually install
uv pip install python-dotenv
```

### 2. Create `.env` File

```bash
cp .env.template .env
```

### 3. Edit `.env` with Your Credentials

```env
# Google Cloud / Vertex AI
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_LOCATION=us-central1
GOOGLE_CREDENTIALS_BASE64=your-base64-credentials

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 4. Run the App

```bash
source .venv/Scripts/activate  # Windows Git Bash
python main.py
```

The app will automatically load variables from `.env`!

## Production Setup (Vercel)

### Method 1: Vercel Dashboard

1. Go to your project on Vercel
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable:
   - Variable name: `VERTEX_PROJECT_ID`
   - Value: `your-gcp-project-id`
   - Environment: Select **Production**, **Preview**, and **Development**
4. Repeat for all variables
5. Redeploy: `vercel --prod`

### Method 2: Vercel CLI

```bash
# Add variables one by one
vercel env add VERTEX_PROJECT_ID
# When prompted, enter the value and select environments

vercel env add VERTEX_LOCATION
vercel env add GOOGLE_CREDENTIALS_BASE64
vercel env add GEMINI_API_KEY
vercel env add CLOUDINARY_CLOUD_NAME
vercel env add CLOUDINARY_API_KEY
vercel env add CLOUDINARY_API_SECRET

# Deploy
vercel --prod
```

### Method 3: Vercel CLI (Bulk Import)

```bash
# Create a file with environment variables (don't commit this!)
cat > .env.production << EOF
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_LOCATION=us-central1
GOOGLE_CREDENTIALS_BASE64=your-base64-credentials
GEMINI_API_KEY=your-gemini-api-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
EOF

# Import to Vercel
vercel env pull .env.production

# Clean up
rm .env.production
```

## Required Environment Variables

| Variable | Required For | Description | Example |
|----------|--------------|-------------|---------|
| `VERTEX_PROJECT_ID` | Image, Video | Google Cloud project ID | `friday-458605` |
| `VERTEX_LOCATION` | Image, Video | GCP region | `us-central1` |
| `GOOGLE_CREDENTIALS_BASE64` | Image, Video | Base64-encoded service account JSON | `eyJhbGc...` |
| `GEMINI_API_KEY` | Music (cover art) | Gemini API key | `AIzaSy...` |
| `CLOUDINARY_CLOUD_NAME` | All media | Cloudinary cloud name | `mycloud` |
| `CLOUDINARY_API_KEY` | All media | Cloudinary API key | `123456789` |
| `CLOUDINARY_API_SECRET` | All media | Cloudinary API secret | `abc123...` |

## Verifying Configuration

### Local Development

```bash
# Run the verification script
python test_setup.py

# Or check manually
python check_env.py
```

### Production (Vercel)

```bash
# List all environment variables
vercel env ls

# Pull environment variables to check
vercel env pull .env.vercel
cat .env.vercel
rm .env.vercel
```

## Security Best Practices

### ✅ DO:
- Use `.env` file for local development only
- Add `.env` to `.gitignore` (already done)
- Use Vercel Dashboard/CLI for production variables
- Use `.env.template` or `.env.example` for documentation
- Rotate API keys regularly

### ❌ DON'T:
- Commit `.env` file to git
- Share `.env` file in public channels
- Hard-code credentials in source code
- Use same credentials for dev and production
- Include production credentials in `.env` file

## Troubleshooting

### "Environment variable not set" in Development

**Problem:** Variables not loading from `.env` file

**Solution:**
```bash
# Make sure python-dotenv is installed
uv pip install python-dotenv

# Verify .env file exists
ls -la .env

# Check for syntax errors in .env
cat .env
```

### "Environment variable not set" on Vercel

**Problem:** Variables not available in production

**Solution:**
1. Check Vercel Dashboard → Settings → Environment Variables
2. Ensure variables are set for "Production" environment
3. Redeploy after adding variables: `vercel --prod`

### App loads `.env` on Vercel (wrong!)

**Problem:** App is loading `.env` file on Vercel

**Solution:**
- This shouldn't happen - Vercel sets `VERCEL=1` automatically
- If it does, check that you're using the latest `main.py`
- The code should have: `if os.getenv("VERCEL") != "1":`

## Example Workflow

### Development Flow
```bash
# 1. Create .env file
cp .env.template .env

# 2. Edit .env with your credentials
nano .env

# 3. Install dev dependencies
uv sync --all-extras

# 4. Run the app
python main.py

# ✅ Variables loaded from .env automatically!
```

### Production Flow
```bash
# 1. Add variables to Vercel
vercel env add VERTEX_PROJECT_ID
# ... add other variables

# 2. Deploy
vercel --prod

# ✅ Vercel injects variables at runtime!
```

## Summary

- **Development:** `.env` file (automatic with `python-dotenv`)
- **Production:** Vercel Environment Variables (dashboard/CLI)
- **Security:** `.env` never committed to git
- **Separation:** Different credentials for dev/prod recommended

This approach follows industry best practices and ensures secure, environment-specific configuration! 🔒
