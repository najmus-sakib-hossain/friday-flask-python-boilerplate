# Quick API Reference

Fast reference guide for all Flask API endpoints.

## 🌐 Base URL

```
Local:      http://localhost:8080
Production: https://your-app.vercel.app
```

---

## 📍 Endpoints Overview

### Standard API

```http
GET  /                    # Home page (HTML)
GET  /api/data            # Get sample data
GET  /api/items/:id       # Get item by ID
```

### Multimodal AI API

```http
GET  /api/multimodal           # API documentation
POST /api/generate-image       # Generate image
POST /api/generate-music       # Generate music + cover art
POST /api/video/start          # Start video generation
GET  /api/video/status/:id     # Check video status
```

---

## 🔥 Quick Examples

### 1. Get Sample Data

```bash
curl http://localhost:8080/api/data
```

```typescript
const data = await fetch('http://localhost:8080/api/data').then(r => r.json());
```

**Response:**
```json
{
  "data": [{"id": 1, "name": "Sample Item 1", "value": 100}],
  "total": 3,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

### 2. Get Item by ID

```bash
curl http://localhost:8080/api/items/5
```

```typescript
const item = await fetch('http://localhost:8080/api/items/5').then(r => r.json());
```

**Response:**
```json
{
  "item": {"id": 5, "name": "Sample Item 5", "value": 500},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

### 3. Generate Image

```bash
curl -X POST http://localhost:8080/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A sunset", "aspect_ratio": "16:9"}'
```

```typescript
const response = await fetch('http://localhost:8080/api/generate-image', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'A beautiful sunset over mountains',
    aspect_ratio: '16:9'
  })
});
const data = await response.json();
```

**Request Body:**
| Field | Type | Required | Options |
|-------|------|----------|---------|
| `prompt` | string | ✅ | Any text |
| `aspect_ratio` | string | ❌ | `1:1`, `9:16`, `16:9`, `3:4`, `4:3` |

**Response:**
```json
{
  "prompt": "A beautiful sunset over mountains",
  "image_url": "https://res.cloudinary.com/...",
  "model_used": "imagen-4.0-fast-generate-preview-06-06",
  "aspect_ratio_used": "16:9"
}
```

---

### 4. Generate Music

```bash
curl -X POST http://localhost:8080/api/generate-music \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Upbeat electronic music", "duration_seconds": 20}'
```

```typescript
const response = await fetch('http://localhost:8080/api/generate-music', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Upbeat electronic music with synthesizers',
    duration_seconds: 20
  })
});
const data = await response.json();
```

**Request Body:**
| Field | Type | Required | Range |
|-------|------|----------|-------|
| `prompt` | string | ✅ | Any text |
| `duration_seconds` | number | ❌ | 1-30 (default: 20) |

**Response:**
```json
{
  "prompt": "Upbeat electronic music",
  "image_url": "https://res.cloudinary.com/...",
  "audio_data_uri": "data:audio/wav;base64,UklGRiQ...",
  "image_model_used": "gemini-2.0-flash-preview-image-generation",
  "music_model_used": "lyria-002",
  "duration_used_seconds": 20
}
```

---

### 5. Generate Video (Async)

**Step 1: Start Generation**

```bash
curl -X POST http://localhost:8080/api/video/start \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A drone flying over beach", "duration_seconds": 8}'
```

```typescript
const startResponse = await fetch('http://localhost:8080/api/video/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'A drone flying over a tropical beach',
    duration_seconds: 8,
    aspect_ratio: '16:9'
  })
});
const { operation_id } = await startResponse.json();
```

**Request Body:**
| Field | Type | Required | Options/Range |
|-------|------|----------|---------------|
| `prompt` | string | ✅ | Any text |
| `duration_seconds` | number | ❌ | 1-10 (default: 8) |
| `aspect_ratio` | string | ❌ | `16:9`, `9:16`, `1:1` |

**Response:**
```json
{
  "operation_id": "1234567890"
}
```

**Step 2: Poll for Status**

```bash
curl http://localhost:8080/api/video/status/1234567890
```

```typescript
// Poll every 5 seconds
const pollStatus = async (operationId: string) => {
  while (true) {
    const response = await fetch(
      `http://localhost:8080/api/video/status/${operationId}`
    );
    const status = await response.json();
    
    if (status.status === 'completed') {
      return status.video_url;
    }
    
    if (status.status === 'failed') {
      throw new Error('Video generation failed');
    }
    
    // Wait 5 seconds before next check
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
};
```

**Response (Pending):**
```json
{
  "status": "pending"
}
```

**Response (Completed):**
```json
{
  "status": "completed",
  "video_url": "https://res.cloudinary.com/..."
}
```

---

## 🎨 Next.js/React Usage

### Using fetch (Client Component)

```typescript
'use client';

import { useState } from 'react';

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/generate-image`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt, aspect_ratio: '16:9' })
        }
      );
      const data = await response.json();
      setImageUrl(data.image_url);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter prompt..."
      />
      <button onClick={generateImage} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {imageUrl && <img src={imageUrl} alt="Generated" />}
    </div>
  );
}
```

### Using Server Actions (Next.js 14+)

```typescript
// app/actions.ts
'use server';

export async function generateImage(prompt: string) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/generate-image`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, aspect_ratio: '16:9' })
    }
  );
  return response.json();
}
```

```typescript
// app/page.tsx
'use client';

import { generateImage } from './actions';

export default function Page() {
  const handleGenerate = async (formData: FormData) => {
    const prompt = formData.get('prompt') as string;
    const result = await generateImage(prompt);
    console.log(result);
  };

  return (
    <form action={handleGenerate}>
      <input name="prompt" placeholder="Enter prompt..." />
      <button type="submit">Generate</button>
    </form>
  );
}
```

---

## ⚠️ Error Responses

### Not Configured (503)

```json
{
  "error": "Multimodal API not configured. Please set required environment variables."
}
```

### Bad Request (400)

```json
{
  "error": "Bad Request: 'prompt' is required."
}
```

### Invalid Parameter (400)

```json
{
  "error": "Invalid 'aspect_ratio'. Allowed: {'1:1', '9:16', '16:9', '3:4', '4:3'}"
}
```

### Service Error (502)

```json
{
  "error": "Image generation service failed.",
  "details": "Vertex AI API request failed: Unauthorized"
}
```

---

## 🔑 Environment Variables (Backend)

Required for multimodal features:

```env
VERTEX_PROJECT_ID=your-project-id
VERTEX_LOCATION=us-central1
GOOGLE_CREDENTIALS_BASE64=base64_encoded_json
GEMINI_API_KEY=your-gemini-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-secret
```

---

## 📦 TypeScript Types (Frontend)

```typescript
// types/api.ts

export interface ImageGenerationRequest {
  prompt: string;
  aspect_ratio?: '1:1' | '9:16' | '16:9' | '3:4' | '4:3';
}

export interface ImageGenerationResponse {
  prompt: string;
  image_url: string;
  model_used: string;
  aspect_ratio_used: string;
}

export interface MusicGenerationRequest {
  prompt: string;
  duration_seconds?: number; // 1-30
}

export interface MusicGenerationResponse {
  prompt: string;
  image_url: string;
  audio_data_uri: string;
  image_model_used: string;
  music_model_used: string;
  duration_used_seconds: number;
}

export interface VideoStartRequest {
  prompt: string;
  duration_seconds?: number; // 1-10
  aspect_ratio?: '16:9' | '9:16' | '1:1';
}

export interface VideoStartResponse {
  operation_id: string;
}

export interface VideoStatusResponse {
  status: 'pending' | 'completed' | 'failed';
  video_url?: string;
}
```

---

## 💡 Tips

1. **Always handle errors** - Check response status and error messages
2. **Use loading states** - AI generation can take time
3. **Poll wisely** - Use 5-second intervals for video status checks
4. **Set timeouts** - Prevent infinite polling (max 5 minutes recommended)
5. **Validate inputs** - Check aspect ratios and durations before sending
6. **Cache responses** - Store generated media URLs to avoid regeneration

---

## 🚀 Performance

| Endpoint | Response Time |
|----------|---------------|
| `/api/data` | ~50ms |
| `/api/items/:id` | ~50ms |
| `/api/generate-image` | 5-15s |
| `/api/generate-music` | 20-40s |
| `/api/video/start` | <1s |
| Video completion | 2-5min |

---

## 📚 More Documentation

- Full Integration Guide: See `NEXTJS_INTEGRATION.md`
- Test Results: See `API_TEST_RESULTS.md`
- Main README: See `README.md`
