# Cloudinary Setup Instructions

Since you don't have Cloudinary credentials yet, here are your options:

## Option 1: Sign up for Cloudinary (Recommended - FREE)

1. Go to https://cloudinary.com/users/register/free
2. Sign up for a free account (no credit card required)
3. After signup, go to your Dashboard
4. Copy these values:
   - Cloud Name
   - API Key
   - API Secret
5. Update your `.env` file with these values

## Option 2: Use a temporary mock for testing

If you just want to test the API without actually storing media, you can:
1. Keep the placeholder values in `.env`
2. The API will work but fail at the upload step
3. You'll see the generated content in base64 format in responses

## Option 3: Use alternative storage

Modify `endpoints/multimodal.py` to use:
- AWS S3
- Google Cloud Storage
- Local file storage (for testing only)

## Current Status

Your `.env` file now has:
- ✅ Google Vertex AI credentials (configured)
- ✅ Gemini API key (configured)
- ⚠️  Cloudinary credentials (need to be added)

## Quick Test Without Cloudinary

You can test image/music generation locally and get base64 data without Cloudinary.
The API will return base64-encoded media that you can display directly in your frontend.

## Free Cloudinary Tier Includes:

- 25 GB storage
- 25 GB bandwidth/month
- Image & video transformations
- More than enough for development and small projects!
