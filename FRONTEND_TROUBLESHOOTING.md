# Railway API Connection Troubleshooting Guide

If you're experiencing issues connecting your frontend to the Railway-deployed Django API, this guide will help you troubleshoot common problems.

## Bad Request (400) Error When Accessing Railway URL Directly

If you see a "Bad Request (400)" error when visiting `https://web-production-f03ff.up.railway.app/` directly in your browser, this issue has been fixed in the backend. Try refreshing the page.

The fix included:
1. Adding error handling to the welcome view
2. Properly configuring media file serving in production
3. Ensuring CORS settings are correctly applied

## Common Frontend Connection Issues

### 1. CORS Issues

**Symptoms:**
- Console errors mentioning "Cross-Origin Request Blocked"
- API requests fail from your frontend application

**Solution:**
- Verify your frontend domain is listed in the `CORS_ALLOWED_ORIGINS` setting in the backend
- Set the `FRONTEND_URL` environment variable in your Railway project
- Make sure you're using the exact URL format (http/https, with/without trailing slash)

Example Railway environment variable:
```
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

### 2. API URL Configuration

**Symptoms:**
- 404 Not Found errors on API requests
- "Failed to fetch" errors in the console

**Solution:**
- Double-check your API URL in the frontend environment variables:

```
VITE_API_URL=https://web-production-f03ff.up.railway.app
VITE_MEDIA_URL=https://web-production-f03ff.up.railway.app/media/
```

- Ensure you're appending `/api/` to your base URL in API requests:

```javascript
// Correct
fetch(`${API_URL}/api/posts/`)

// Incorrect
fetch(`${API_URL}/posts/`) 
```

### 3. CSRF Token Issues for POST/PUT/DELETE Requests

**Symptoms:**
- 403 Forbidden errors when submitting forms
- CSRF verification failed errors

**Solution:**
- For admin interactions, ensure you're logged into the Django admin first
- When making requests that change data, include CSRF token and credentials:

```javascript
const response = await fetch(`${API_URL}/api/posts/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken'),
  },
  credentials: 'include', // This is crucial!
  body: JSON.stringify(data),
});
```

### 4. Media File Access Issues

**Symptoms:**
- Images not loading
- 404 errors for media files

**Solution:**
- Ensure you're using the correct media URL:
```javascript
const imageUrl = `${MEDIA_URL}${imagePath}`;
```

- For CKEditor uploaded images, they should be accessed at:
```
https://web-production-f03ff.up.railway.app/media/uploads/image.jpg
```

## Testing API Connectivity

You can test API connectivity using these simple steps:

1. Open your browser's developer console (F12)
2. Run this command to test the API connection:

```javascript
fetch('https://web-production-f03ff.up.railway.app/api/posts/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

## Debugging Railway Backend Issues

If you suspect issues with the Railway deployment:

1. Check Railway logs for error messages
2. Temporarily toggle `DEBUG=True` in Railway environment variables
3. Add your frontend domain to the `ALLOWED_HOSTS` setting

## Security Considerations

For production deployment, consider:

1. Using secure HTTPS connections only
2. Implementing proper authentication for your API if needed
3. Adding rate limiting to prevent abuse
4. Setting up proper CSRF protection with your frontend domain 