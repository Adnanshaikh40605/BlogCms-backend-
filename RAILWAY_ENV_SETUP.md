# Setting Up Environment Variables in Railway

This guide will help you configure environment variables in your Railway project to properly connect your frontend to your Django backend.

## Required Environment Variables

Railway allows you to set environment variables through their dashboard. Here are the key variables you should configure:

### Basic Settings

| Variable | Value | Description |
|----------|-------|-------------|
| `DEBUG` | `False` | Set to False for production |
| `SECRET_KEY` | `[generated-secure-key]` | A secure random string for Django |
| `ALLOWED_HOSTS` | `.railway.app,your-custom-domain.com` | Domains that can host your Django app |

### Database Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `[Railway auto-generated]` | PostgreSQL connection string (usually auto-provided) |

### CORS Settings

| Variable | Value | Description |
|----------|-------|-------------|
| `CORS_ALLOW_ALL_ORIGINS` | `False` | Set to False in production |
| `FRONTEND_URL` | `https://your-frontend-domain.com` | Your frontend application's URL |

## Steps to Configure Environment Variables

1. Log in to your Railway dashboard at https://railway.app
2. Select your Django backend project
3. Go to the "Variables" tab
4. Add each variable using the "New Variable" button
5. Enter the name and value for each variable
6. Railway will automatically redeploy your app with the new variables

## Example Setup for Vercel Frontend

If your frontend is hosted on Vercel, your configuration might look like:

```
DEBUG=False
SECRET_KEY=your-secure-generated-key
ALLOWED_HOSTS=.railway.app,your-custom-domain.com
CORS_ALLOW_ALL_ORIGINS=False
FRONTEND_URL=https://your-app.vercel.app
```

## Example Setup for Netlify Frontend

If your frontend is hosted on Netlify, your configuration might look like:

```
DEBUG=False
SECRET_KEY=your-secure-generated-key
ALLOWED_HOSTS=.railway.app,your-custom-domain.com
CORS_ALLOW_ALL_ORIGINS=False
FRONTEND_URL=https://your-app.netlify.app
```

## Testing Your Configuration

After setting your environment variables:

1. Railway will automatically redeploy your application
2. Wait for the deployment to complete (check the Deployments tab)
3. Test accessing your API at `https://your-app-name.railway.app/api/posts/`
4. Try connecting from your frontend application
5. Use the `API_TEST.js` script to check connectivity

## Troubleshooting

If you're experiencing issues:

1. **CORS Errors**: Double-check your `FRONTEND_URL` and make sure it exactly matches your frontend's URL (including http/https)
2. **Database Connection Issues**: Verify the `DATABASE_URL` is correctly set (usually managed by Railway)
3. **Application Errors**: Temporarily set `DEBUG=True` to get detailed error messages
4. **Deployment Issues**: Check the deployment logs in Railway for errors

## Security Best Practices

1. Never set `DEBUG=True` in production for extended periods
2. Generate a secure random string for `SECRET_KEY`
3. Limit `ALLOWED_HOSTS` to only the domains you need
4. Keep `CORS_ALLOW_ALL_ORIGINS=False` in production
5. Only list specific frontend domains in `FRONTEND_URL` 