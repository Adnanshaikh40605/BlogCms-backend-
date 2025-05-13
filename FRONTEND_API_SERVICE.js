// src/api/apiService.js

// Get environment variables with fallback to development values
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const MEDIA_URL = import.meta.env.VITE_MEDIA_URL || 'http://localhost:8000/media/';

// Helper function to get cookies (for CSRF token)
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Default request headers
const getHeaders = (includeContentType = true) => {
  const headers = {};
  const csrfToken = getCookie('csrftoken');
  
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken;
  }
  
  if (includeContentType) {
    headers['Content-Type'] = 'application/json';
  }
  
  return headers;
};

// Post API functions
const postAPI = {
  // Get all posts
  getAll: async () => {
    const response = await fetch(`${API_URL}/api/posts/`);
    return response.json();
  },
  
  // Get single post by ID
  getById: async (id) => {
    const response = await fetch(`${API_URL}/api/posts/${id}/`);
    return response.json();
  },
  
  // Create new post
  create: async (postData) => {
    const response = await fetch(`${API_URL}/api/posts/`, {
      method: 'POST',
      headers: getHeaders(),
      credentials: 'include',
      body: JSON.stringify(postData)
    });
    return response.json();
  },
  
  // Update existing post
  update: async (id, postData) => {
    const response = await fetch(`${API_URL}/api/posts/${id}/`, {
      method: 'PATCH',
      headers: getHeaders(),
      credentials: 'include',
      body: JSON.stringify(postData)
    });
    return response.json();
  },
  
  // Delete post
  delete: async (id) => {
    const response = await fetch(`${API_URL}/api/posts/${id}/`, {
      method: 'DELETE',
      headers: getHeaders(),
      credentials: 'include'
    });
    return response.status === 204; // Returns true if successfully deleted
  },
  
  // Upload images for a post
  uploadImage: async (id, imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await fetch(`${API_URL}/api/posts/${id}/upload_images/`, {
      method: 'POST',
      headers: getHeaders(false), // Don't include Content-Type for file uploads
      credentials: 'include',
      body: formData
    });
    return response.json();
  }
};

// Comment API functions
const commentAPI = {
  // Get all comments (with optional post ID filter)
  getAll: async (postId = null) => {
    let url = `${API_URL}/api/comments/`;
    if (postId) {
      url += `?post=${postId}`;
    }
    const response = await fetch(url);
    return response.json();
  },
  
  // Create new comment
  create: async (commentData) => {
    const response = await fetch(`${API_URL}/api/comments/`, {
      method: 'POST',
      headers: getHeaders(),
      credentials: 'include',
      body: JSON.stringify(commentData)
    });
    return response.json();
  },
  
  // Approve a comment
  approve: async (id) => {
    const response = await fetch(`${API_URL}/api/comments/${id}/approve/`, {
      method: 'POST',
      headers: getHeaders(),
      credentials: 'include'
    });
    return response.json();
  },
  
  // Get pending comment count
  getPendingCount: async () => {
    const response = await fetch(`${API_URL}/api/comments/pending-count/`);
    return response.json();
  }
};

// Media handling
const mediaAPI = {
  getImageUrl: (imagePath) => {
    if (!imagePath) return null;
    return `${MEDIA_URL}${imagePath}`;
  }
};

export {
  API_URL,
  MEDIA_URL,
  postAPI,
  commentAPI,
  mediaAPI
}; 