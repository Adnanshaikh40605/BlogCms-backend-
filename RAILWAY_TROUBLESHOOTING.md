# Railway Deployment Troubleshooting Guide

This guide will help you fix common issues with Django deployments on Railway, particularly the "400 Bad Request" error that you're experiencing.

## Quick Fixes for the 400 Bad Request Error

If you're seeing a 400 Bad Request error when visiting your Railway app, try these quick fixes:

1. **Update your code with the latest changes we've made**
   ```bash
   git add .
   git commit -m "Fix media serving and add diagnostic endpoints"
   git push
   ```

2. **Add these environment variables in Railway**
   - `ALLOWED_HOSTS=.railway.app,web-production-f03ff.up.railway.app`
   - `FRONTEND_URL=https://your-frontend-url.com` (replace with your actual frontend URL)

3. **Try visiting these URLs to diagnose the issue**
   - `/debug-info/` endpoint: https://web-production-f03ff.up.railway.app/debug-info/
   - Test page: Open the `test_connection.html` file in your browser

## Emergency Mode

If you're still having issues, you can switch to emergency diagnostic mode:

1. **Rename your Procfile.emergency to Procfile**
   ```bash
   mv Procfile.emergency Procfile
   git add Procfile
   git commit -m "Switch to emergency diagnostic mode"
   git push
   ```

2. **Visit your Railway app**
   - This will now use our minimal WSGI application that bypasses Django
   - View detailed environment information at `/debug-env`

3. **Switch back to normal mode after diagnosing**
   ```bash
   # Check what your original Procfile contained
   # Usually: web: gunicorn backend.wsgi:application --log-file -
   echo "web: gunicorn backend.wsgi:application --log-file -" > Procfile
   git add Procfile
   git commit -m "Revert to normal mode"
   git push
   ```

## Common Railway Deployment Issues

### 1. ALLOWED_HOSTS Configuration

Django's `ALLOWED_HOSTS` setting needs to include your Railway domain.

**Fix:**
```
ALLOWED_HOSTS=.railway.app,web-production-f03ff.up.railway.app
```

### 2. Static and Media Files Serving

Railway doesn't serve static/media files automatically.

**Fix:**
We've already added the necessary code to `urls.py` to serve media files in production.

### 3. Database Configuration

Ensure your database URL is correctly parsed.

**Fix:**
Check the `/debug-info/` endpoint to verify your database connection.

### 4. CSRF and CORS Issues

Make sure your frontend domain is properly configured for both CSRF and CORS.

**Fix:**
Add your frontend URL to the `FRONTEND_URL` environment variable in Railway.

## Debugging Steps

If you're still having issues, follow these debugging steps:

1. **Check Railway Logs**
   - Go to your Railway dashboard
   - Select your service
   - Click on the "Logs" tab

2. **Enable Debug Mode Temporarily**
   - Add `DEBUG=True` to your Railway environment variables
   - Check for detailed error messages
   - **IMPORTANT:** Remember to set `DEBUG=False` after troubleshooting!

3. **Use the Diagnostic HTML Page**
   - Open `test_connection.html` in your browser
   - Enter your Railway URL and run the tests
   - Check each endpoint for detailed error information

4. **Check WSGI Configuration**
   - Ensure your Procfile is correct: `web: gunicorn backend.wsgi:application --log-file -`
   - Make sure `backend.wsgi` exists and is correctly configured

## Railway-Specific Configuration

Railway has some specific requirements:

1. **PORT Environment Variable**
   - Railway sets a `PORT` environment variable that your app should use
   - Our Django application automatically uses this via Gunicorn

2. **Database URL**
   - Railway provides a `DATABASE_URL` environment variable
   - We're using `dj-database-url` to parse this correctly

3. **Static Files**
   - We're using Whitenoise for static files
   - Make sure `python manage.py collectstatic` runs during deployment

## Final Checklist

If you're still having issues:

- [ ] Check if your Railway app has the correct environment variables
- [ ] Verify that your code changes have been pushed and deployed
- [ ] Check Railway logs for any specific error messages
- [ ] Try the emergency diagnostic mode to bypass Django
- [ ] Contact Railway support with specific error details

## Need More Help?

If you've tried everything and still have issues:

1. Switch to emergency mode to gather diagnostic information
2. Take screenshots of any error messages
3. Collect the output from the `/debug-env` endpoint
4. Share this information when asking for help 