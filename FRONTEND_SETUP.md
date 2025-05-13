# Setting Up a React Frontend for the Blog CMS

This guide will help you set up a new React project that connects to your Django API deployed on Railway.

## Prerequisites

- Node.js (v14+)
- npm or yarn
- Git

## Step 1: Create a New React Project with Vite

Vite is a modern, fast build tool for React. Let's create a new React project:

```bash
# Using npm
npm create vite@latest blog-cms-frontend -- --template react

# Or using yarn
yarn create vite blog-cms-frontend --template react
```

## Step 2: Navigate to the Project Directory

```bash
cd blog-cms-frontend
```

## Step 3: Install Dependencies

```bash
# Using npm
npm install

# Or using yarn
yarn
```

## Step 4: Add Required Packages

```bash
# Using npm
npm install react-router-dom axios @headlessui/react @heroicons/react tailwindcss postcss autoprefixer

# Or using yarn
yarn add react-router-dom axios @headlessui/react @heroicons/react tailwindcss postcss autoprefixer
```

## Step 5: Set Up TailwindCSS (Optional but Recommended)

Initialize Tailwind CSS:

```bash
npx tailwindcss init -p
```

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Add Tailwind to your CSS in `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Your custom styles below */
```

## Step 6: Create Environment Configuration

Create a `.env` file in the root of your project:

```
VITE_API_URL=https://web-production-f03ff.up.railway.app
VITE_MEDIA_URL=https://web-production-f03ff.up.railway.app/media/
```

For local development, you can create a `.env.development` file:

```
VITE_API_URL=http://localhost:8000
VITE_MEDIA_URL=http://localhost:8000/media/
```

## Step 7: Create API Service

Create a new file at `src/api/apiService.js` with the content from the `FRONTEND_API_SERVICE.js` example file.

## Step 8: Create Components

1. Create a directory structure:

```
src/
  ├── api/
  │   └── apiService.js
  ├── components/
  │   ├── BlogPosts.jsx
  │   ├── BlogPostDetail.jsx
  │   └── Header.jsx
  ├── pages/
  │   ├── HomePage.jsx
  │   ├── PostPage.jsx
  │   └── NotFoundPage.jsx
  └── App.jsx
```

2. Use the `BlogPosts.jsx` example from the `FRONTEND_EXAMPLE.jsx` file.

## Step 9: Set Up Routing

Update `App.jsx`:

```jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PostPage from './pages/PostPage';
import NotFoundPage from './pages/NotFoundPage';
import Header from './components/Header';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/posts/:id" element={<PostPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
```

## Step 10: Create Page Components

Create basic page components in the `pages` directory.

## Step 11: Start the Development Server

```bash
# Using npm
npm run dev

# Or using yarn
yarn dev
```

## Step 12: Build for Production

When ready to deploy:

```bash
# Using npm
npm run build

# Or using yarn
yarn build
```

This will create a `dist` directory with your production-ready files.

## Step 13: Deploy Your Frontend

You can deploy the frontend to platforms like:

1. **Vercel**:
   - Sign up for Vercel
   - Install Vercel CLI: `npm i -g vercel`
   - Deploy: `vercel`

2. **Netlify**:
   - Sign up for Netlify
   - Install Netlify CLI: `npm i -g netlify-cli`
   - Deploy: `netlify deploy`

3. **GitHub Pages**:
   - Install gh-pages: `npm i -g gh-pages`
   - Add to package.json:
     ```json
     "scripts": {
       "deploy": "gh-pages -d dist"
     }
     ```
   - Deploy: `npm run deploy`

## Important Notes

1. **CORS**: The backend is already set up to accept requests from your frontend.
2. **Environment Variables**: Make sure to set the correct API URL in your production environment.
3. **Authentication**: If you implement authentication, you'll need to handle cookies or tokens.

## Further Resources

- [React Router Documentation](https://reactrouter.com/docs/en/v6)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) 