# Flask Backend API - Next.js TypeScript Integration Guide

Complete guide for integrating this Flask multimodal AI API with your Next.js TypeScript frontend.

## 📋 Table of Contents

- [Base URL Configuration](#base-url-configuration)
- [TypeScript Types](#typescript-types)
- [API Routes Overview](#api-routes-overview)
- [Next.js API Client Setup](#nextjs-api-client-setup)
- [React Hooks Examples](#react-hooks-examples)
- [Server Actions (Next.js 14+)](#server-actions-nextjs-14)
- [Error Handling](#error-handling)
- [Complete Component Examples](#complete-component-examples)

---

## 🔧 Base URL Configuration

### Environment Variables

Create `.env.local` in your Next.js project root:

```env
# For local development
NEXT_PUBLIC_API_URL=http://localhost:8080

# For production (replace with your Vercel deployment URL)
# NEXT_PUBLIC_API_URL=https://your-flask-app.vercel.app
```

---

## 📦 TypeScript Types

Create `types/api.ts` in your Next.js project:

```typescript
// types/api.ts

// Standard API Types
export interface SampleItem {
  id: number;
  name: string;
  value: number;
}

export interface SampleDataResponse {
  data: SampleItem[];
  total: number;
  timestamp: string;
}

export interface ItemResponse {
  item: SampleItem;
  timestamp: string;
}

// Multimodal API Types
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
  duration_seconds?: number; // 1-30 seconds
}

export interface MusicGenerationResponse {
  prompt: string;
  image_url: string;
  audio_data_uri: string; // Base64 encoded audio data
  image_model_used: string;
  music_model_used: string;
  duration_used_seconds: number;
}

export interface VideoStartRequest {
  prompt: string;
  duration_seconds?: number; // 1-10 seconds
  aspect_ratio?: '16:9' | '9:16' | '1:1';
}

export interface VideoStartResponse {
  operation_id: string;
}

export interface VideoStatusResponse {
  status: 'pending' | 'completed' | 'failed';
  video_url?: string;
  error?: string;
  details?: string;
}

// Error Response
export interface ApiError {
  error: string;
  details?: string | Record<string, string>;
}
```

---

## 🌐 API Routes Overview

### Standard Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Home page (HTML) | No |
| `GET` | `/api/data` | Get sample data array | No |
| `GET` | `/api/items/:id` | Get item by ID | No |

### Multimodal AI Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/multimodal` | API guide (text) | No |
| `POST` | `/api/generate-image` | Generate an image | No* |
| `POST` | `/api/generate-music` | Generate music + image | No* |
| `POST` | `/api/video/start` | Start video generation | No* |
| `GET` | `/api/video/status/:id` | Check video status | No* |

*Requires proper environment variables configured on the Flask backend.

---

## 🛠 Next.js API Client Setup

### Create API Client

Create `lib/api-client.ts`:

```typescript
// lib/api-client.ts

import {
  SampleDataResponse,
  ItemResponse,
  ImageGenerationRequest,
  ImageGenerationResponse,
  MusicGenerationRequest,
  MusicGenerationResponse,
  VideoStartRequest,
  VideoStartResponse,
  VideoStatusResponse,
  ApiError,
} from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async fetchApi<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          (data as ApiError).error || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return data as T;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unknown error occurred');
    }
  }

  // Standard API Methods
  async getSampleData(): Promise<SampleDataResponse> {
    return this.fetchApi<SampleDataResponse>('/api/data');
  }

  async getItemById(id: number): Promise<ItemResponse> {
    return this.fetchApi<ItemResponse>(`/api/items/${id}`);
  }

  // Multimodal API Methods
  async generateImage(
    request: ImageGenerationRequest
  ): Promise<ImageGenerationResponse> {
    return this.fetchApi<ImageGenerationResponse>('/api/generate-image', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateMusic(
    request: MusicGenerationRequest
  ): Promise<MusicGenerationResponse> {
    return this.fetchApi<MusicGenerationResponse>('/api/generate-music', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async startVideoGeneration(
    request: VideoStartRequest
  ): Promise<VideoStartResponse> {
    return this.fetchApi<VideoStartResponse>('/api/video/start', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getVideoStatus(operationId: string): Promise<VideoStatusResponse> {
    return this.fetchApi<VideoStatusResponse>(
      `/api/video/status/${operationId}`
    );
  }

  // Polling helper for video generation
  async pollVideoStatus(
    operationId: string,
    maxAttempts: number = 60,
    intervalMs: number = 5000
  ): Promise<VideoStatusResponse> {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const status = await this.getVideoStatus(operationId);

      if (status.status === 'completed' || status.status === 'failed') {
        return status;
      }

      // Wait before next poll
      await new Promise((resolve) => setTimeout(resolve, intervalMs));
    }

    throw new Error('Video generation timeout - max polling attempts reached');
  }
}

// Export singleton instance
export const apiClient = new ApiClient(API_BASE_URL);
```

---

## 🎣 React Hooks Examples

### useImageGeneration Hook

Create `hooks/useImageGeneration.ts`:

```typescript
// hooks/useImageGeneration.ts

import { useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { ImageGenerationRequest, ImageGenerationResponse } from '@/types/api';

export function useImageGeneration() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ImageGenerationResponse | null>(null);

  const generateImage = async (request: ImageGenerationRequest) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await apiClient.generateImage(request);
      setData(result);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate image';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { generateImage, loading, error, data };
}
```

### useMusicGeneration Hook

```typescript
// hooks/useMusicGeneration.ts

import { useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { MusicGenerationRequest, MusicGenerationResponse } from '@/types/api';

export function useMusicGeneration() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<MusicGenerationResponse | null>(null);

  const generateMusic = async (request: MusicGenerationRequest) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await apiClient.generateMusic(request);
      setData(result);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate music';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { generateMusic, loading, error, data };
}
```

### useVideoGeneration Hook (with Polling)

```typescript
// hooks/useVideoGeneration.ts

import { useState, useCallback } from 'react';
import { apiClient } from '@/lib/api-client';
import { VideoStartRequest, VideoStatusResponse } from '@/types/api';

export function useVideoGeneration() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<VideoStatusResponse | null>(null);
  const [operationId, setOperationId] = useState<string | null>(null);
  const [progress, setProgress] = useState<string>('');

  const startGeneration = async (request: VideoStartRequest) => {
    setLoading(true);
    setError(null);
    setData(null);
    setProgress('Starting video generation...');

    try {
      const result = await apiClient.startVideoGeneration(request);
      setOperationId(result.operation_id);
      setProgress('Video generation started. Polling for status...');
      
      // Start polling
      const finalStatus = await apiClient.pollVideoStatus(
        result.operation_id,
        60, // max attempts
        5000 // 5 second intervals
      );
      
      setData(finalStatus);
      setProgress('');
      return finalStatus;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate video';
      setError(errorMessage);
      setProgress('');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const checkStatus = useCallback(async (opId: string) => {
    try {
      const status = await apiClient.getVideoStatus(opId);
      setData(status);
      return status;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to check status';
      setError(errorMessage);
      throw err;
    }
  }, []);

  return {
    startGeneration,
    checkStatus,
    loading,
    error,
    data,
    operationId,
    progress,
  };
}
```

### useSampleData Hook

```typescript
// hooks/useSampleData.ts

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { SampleDataResponse } from '@/types/api';

export function useSampleData() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<SampleDataResponse | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await apiClient.getSampleData();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}
```

---

## 🚀 Server Actions (Next.js 14+)

Create `app/actions/ai.ts`:

```typescript
// app/actions/ai.ts
'use server';

import { apiClient } from '@/lib/api-client';
import {
  ImageGenerationRequest,
  MusicGenerationRequest,
  VideoStartRequest,
} from '@/types/api';

export async function generateImageAction(request: ImageGenerationRequest) {
  try {
    const result = await apiClient.generateImage(request);
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to generate image',
    };
  }
}

export async function generateMusicAction(request: MusicGenerationRequest) {
  try {
    const result = await apiClient.generateMusic(request);
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to generate music',
    };
  }
}

export async function startVideoGenerationAction(request: VideoStartRequest) {
  try {
    const result = await apiClient.startVideoGeneration(request);
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to start video generation',
    };
  }
}

export async function checkVideoStatusAction(operationId: string) {
  try {
    const result = await apiClient.getVideoStatus(operationId);
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to check video status',
    };
  }
}
```

---

## ⚠️ Error Handling

### Global Error Handler

```typescript
// lib/error-handler.ts

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function handleApiError(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message;
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'An unexpected error occurred';
}
```

### Usage in Components

```typescript
import { handleApiError } from '@/lib/error-handler';

try {
  await apiClient.generateImage({ prompt: 'A sunset' });
} catch (error) {
  const errorMessage = handleApiError(error);
  toast.error(errorMessage);
}
```

---

## 🎨 Complete Component Examples

### Image Generation Component

```typescript
// components/ImageGenerator.tsx
'use client';

import { useState } from 'react';
import { useImageGeneration } from '@/hooks/useImageGeneration';
import { ImageGenerationRequest } from '@/types/api';

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState('');
  const [aspectRatio, setAspectRatio] = useState<ImageGenerationRequest['aspect_ratio']>('16:9');
  const { generateImage, loading, error, data } = useImageGeneration();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    await generateImage({ prompt, aspect_ratio: aspectRatio });
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Image Generator</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="prompt" className="block text-sm font-medium mb-2">
            Prompt
          </label>
          <input
            id="prompt"
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="A beautiful sunset over mountains..."
            className="w-full px-4 py-2 border rounded-lg"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="aspect-ratio" className="block text-sm font-medium mb-2">
            Aspect Ratio
          </label>
          <select
            id="aspect-ratio"
            value={aspectRatio}
            onChange={(e) => setAspectRatio(e.target.value as any)}
            className="w-full px-4 py-2 border rounded-lg"
            disabled={loading}
          >
            <option value="1:1">1:1 (Square)</option>
            <option value="16:9">16:9 (Landscape)</option>
            <option value="9:16">9:16 (Portrait)</option>
            <option value="4:3">4:3</option>
            <option value="3:4">3:4</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading || !prompt.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate Image'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {data && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-2">Generated Image</h3>
          <img
            src={data.image_url}
            alt={data.prompt}
            className="w-full rounded-lg shadow-lg"
          />
          <p className="mt-2 text-sm text-gray-600">Model: {data.model_used}</p>
        </div>
      )}
    </div>
  );
}
```

### Music Generation Component

```typescript
// components/MusicGenerator.tsx
'use client';

import { useState, useRef } from 'react';
import { useMusicGeneration } from '@/hooks/useMusicGeneration';

export default function MusicGenerator() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(20);
  const audioRef = useRef<HTMLAudioElement>(null);
  const { generateMusic, loading, error, data } = useMusicGeneration();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    await generateMusic({ prompt, duration_seconds: duration });
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Music Generator</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="music-prompt" className="block text-sm font-medium mb-2">
            Music Description
          </label>
          <textarea
            id="music-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Upbeat electronic music with synthesizers..."
            className="w-full px-4 py-2 border rounded-lg h-24"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="duration" className="block text-sm font-medium mb-2">
            Duration: {duration} seconds
          </label>
          <input
            id="duration"
            type="range"
            min="1"
            max="30"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            className="w-full"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !prompt.trim()}
          className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate Music'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {data && (
        <div className="mt-6 space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Album Cover</h3>
            <img
              src={data.image_url}
              alt="Album cover"
              className="w-full rounded-lg shadow-lg"
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">Generated Music</h3>
            <audio
              ref={audioRef}
              controls
              src={data.audio_data_uri}
              className="w-full"
            />
          </div>

          <div className="text-sm text-gray-600">
            <p>Music Model: {data.music_model_used}</p>
            <p>Image Model: {data.image_model_used}</p>
            <p>Duration: {data.duration_used_seconds}s</p>
          </div>
        </div>
      )}
    </div>
  );
}
```

### Video Generation Component (with Polling)

```typescript
// components/VideoGenerator.tsx
'use client';

import { useState } from 'react';
import { useVideoGeneration } from '@/hooks/useVideoGeneration';
import { VideoStartRequest } from '@/types/api';

export default function VideoGenerator() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(8);
  const [aspectRatio, setAspectRatio] = useState<VideoStartRequest['aspect_ratio']>('16:9');
  const { startGeneration, loading, error, data, progress } = useVideoGeneration();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    await startGeneration({
      prompt,
      duration_seconds: duration,
      aspect_ratio: aspectRatio,
    });
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Video Generator</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="video-prompt" className="block text-sm font-medium mb-2">
            Video Description
          </label>
          <textarea
            id="video-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="A drone flying over a tropical beach at sunset..."
            className="w-full px-4 py-2 border rounded-lg h-24"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="video-duration" className="block text-sm font-medium mb-2">
            Duration: {duration} seconds
          </label>
          <input
            id="video-duration"
            type="range"
            min="1"
            max="10"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            className="w-full"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="video-aspect" className="block text-sm font-medium mb-2">
            Aspect Ratio
          </label>
          <select
            id="video-aspect"
            value={aspectRatio}
            onChange={(e) => setAspectRatio(e.target.value as any)}
            className="w-full px-4 py-2 border rounded-lg"
            disabled={loading}
          >
            <option value="16:9">16:9 (Landscape)</option>
            <option value="9:16">9:16 (Portrait)</option>
            <option value="1:1">1:1 (Square)</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading || !prompt.trim()}
          className="w-full bg-green-600 text-white py-2 px-4 rounded-lg disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate Video'}
        </button>
      </form>

      {progress && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
          {progress}
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {data?.status === 'completed' && data.video_url && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-2">Generated Video</h3>
          <video
            controls
            src={data.video_url}
            className="w-full rounded-lg shadow-lg"
          />
        </div>
      )}
    </div>
  );
}
```

### Sample Data Display Component

```typescript
// components/SampleDataDisplay.tsx
'use client';

import { useSampleData } from '@/hooks/useSampleData';

export default function SampleDataDisplay() {
  const { data, loading, error } = useSampleData();

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">Error: {error}</div>;
  }

  if (!data) {
    return null;
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Sample Data</h2>
      <div className="space-y-4">
        {data.data.map((item) => (
          <div
            key={item.id}
            className="p-4 border rounded-lg hover:shadow-md transition-shadow"
          >
            <h3 className="font-semibold">{item.name}</h3>
            <p className="text-sm text-gray-600">ID: {item.id}</p>
            <p className="text-sm text-gray-600">Value: {item.value}</p>
          </div>
        ))}
      </div>
      <p className="mt-4 text-sm text-gray-500">
        Total items: {data.total} | Last updated: {data.timestamp}
      </p>
    </div>
  );
}
```

---

## 📱 Usage in Next.js Pages/App Router

### App Router Example (app/page.tsx)

```typescript
// app/page.tsx
import ImageGenerator from '@/components/ImageGenerator';
import MusicGenerator from '@/components/MusicGenerator';
import VideoGenerator from '@/components/VideoGenerator';
import SampleDataDisplay from '@/components/SampleDataDisplay';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-12">
        <h1 className="text-4xl font-bold text-center mb-12">
          Multimodal AI Platform
        </h1>
        
        <div className="grid gap-8">
          <ImageGenerator />
          <MusicGenerator />
          <VideoGenerator />
          <SampleDataDisplay />
        </div>
      </div>
    </main>
  );
}
```

### Pages Router Example (pages/index.tsx)

```typescript
// pages/index.tsx
import type { NextPage } from 'next';
import ImageGenerator from '@/components/ImageGenerator';
import MusicGenerator from '@/components/MusicGenerator';

const Home: NextPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto py-12">
        <h1 className="text-4xl font-bold text-center mb-12">
          Multimodal AI Platform
        </h1>
        
        <div className="grid gap-8">
          <ImageGenerator />
          <MusicGenerator />
        </div>
      </main>
    </div>
  );
};

export default Home;
```

---

## 🧪 Testing

### Jest Test Example

```typescript
// __tests__/api-client.test.ts
import { apiClient } from '@/lib/api-client';

describe('API Client', () => {
  it('should fetch sample data', async () => {
    const data = await apiClient.getSampleData();
    expect(data).toHaveProperty('data');
    expect(data).toHaveProperty('total');
    expect(Array.isArray(data.data)).toBe(true);
  });

  it('should fetch item by ID', async () => {
    const item = await apiClient.getItemById(1);
    expect(item).toHaveProperty('item');
    expect(item.item.id).toBe(1);
  });
});
```

---

## 🔐 CORS Configuration

The Flask backend already has CORS enabled via `flask-cors`. If you need custom CORS settings, you can configure them in the Flask app.

---

## 🚀 Deployment Checklist

- [ ] Set `NEXT_PUBLIC_API_URL` in Vercel environment variables
- [ ] Configure Flask backend environment variables (API keys, credentials)
- [ ] Test all endpoints in production
- [ ] Set up error monitoring (e.g., Sentry)
- [ ] Configure rate limiting if needed
- [ ] Add authentication if required

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [React Hooks Documentation](https://react.dev/reference/react)

---

## 🐛 Common Issues

### Issue: CORS errors in browser

**Solution**: Ensure `flask-cors` is installed and configured in your Flask app (already done in this boilerplate).

### Issue: API requests fail with network error

**Solution**: 
1. Check that `NEXT_PUBLIC_API_URL` is set correctly
2. Verify Flask server is running
3. Check browser console for specific error messages

### Issue: TypeScript errors with API responses

**Solution**: Ensure your types in `types/api.ts` match the actual API responses. Use type guards for runtime validation.

### Issue: Video generation timeout

**Solution**: The video polling mechanism has a default timeout of 5 minutes (60 attempts × 5 seconds). Increase `maxAttempts` in `pollVideoStatus` if needed.

---

## 📞 Support

For issues or questions:
1. Check the Flask backend logs
2. Review browser console errors
3. Verify environment variables are set correctly
4. Test endpoints directly with cURL or Postman

---

**Happy coding! 🎉**
