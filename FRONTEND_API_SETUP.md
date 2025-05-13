# Frontend API Connection Guide

This guide explains how to connect your frontend application to the Django API backend deployed on Railway.

## API Base URL

Your Django API is now deployed at:

```
https://web-production-f03ff.up.railway.app
```

## API Endpoints

All API endpoints are prefixed with `/api/`, for example:

- Blog Posts: `https://web-production-f03ff.up.railway.app/api/posts/`
- Comments: `https://web-production-f03ff.up.railway.app/api/comments/`
- Images: `https://web-production-f03ff.up.railway.app/api/images/`

## Media Files

Media files (uploads, images) are available at:

```
https://web-production-f03ff.up.railway.app/media/
```

## React/Vite Frontend Setup

### 1. Create a `.env` file in your React project root:

```
VITE_API_URL=https://web-production-f03ff.up.railway.app
VITE_MEDIA_URL=https://web-production-f03ff.up.railway.app/media/
```

### 2. Use these environment variables in your API service:

```javascript
// src/api/apiService.js

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const MEDIA_URL = import.meta.env.VITE_MEDIA_URL || 'http://localhost:8000/media/';

// For API requests
const fetchPosts = async () => {
  const response = await fetch(`${API_URL}/api/posts/`);
  return response.json();
};

// For image URLs
const getImageUrl = (imagePath) => {
  return `${MEDIA_URL}${imagePath}`;
};

export { API_URL, MEDIA_URL, fetchPosts, getImageUrl };
```

### 3. Set up CORS (already configured on backend)

The backend has been configured to accept requests from your frontend. If you're encountering CORS issues, make sure:

1. Your frontend application URL is correctly set in the backend's `CORS_ALLOWED_ORIGINS` setting
2. You're including the required credentials in your requests if using authentication

### 4. Example of a POST request with CSRF token handling:

```javascript
const createPost = async (postData) => {
  const csrfToken = getCookie('csrftoken'); // You'll need to implement getCookie
  
  const response = await fetch(`${API_URL}/api/posts/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include', // Important for sending cookies
    body: JSON.stringify(postData),
  });
  
  return response.json();
};

// Helper function to get cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
```

## Deploying Your Frontend

You can deploy your frontend to services like:

1. **Vercel**: Excellent for React apps
2. **Netlify**: Good alternative with easy deployment
3. **Firebase Hosting**: Google's hosting service

After deploying your frontend, make sure to:

1. Add your frontend URL to the backend settings by setting the `FRONTEND_URL` environment variable in Railway
2. Update any hardcoded URLs in your frontend code to use environment variables

## Testing the Connection

To verify the API connection is working:

1. Open your browser console
2. Try a simple fetch request to `https://web-production-f03ff.up.railway.app/api/posts/`
3. Check that the response contains your blog post data 