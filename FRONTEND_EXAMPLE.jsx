// Example BlogPosts.jsx component
import React, { useState, useEffect } from 'react';
import { API_URL, MEDIA_URL } from '../api/apiService';

const BlogPosts = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch blog posts when component mounts
    fetchBlogPosts();
  }, []);

  const fetchBlogPosts = async () => {
    try {
      setLoading(true);
      
      const response = await fetch(`${API_URL}/api/posts/`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      setPosts(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching blog posts:', err);
      setError('Failed to load blog posts. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Function to get full image URL
  const getImageUrl = (imagePath) => {
    if (!imagePath) return null;
    return `${MEDIA_URL}${imagePath}`;
  };

  if (loading) {
    return <div className="loading">Loading blog posts...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="blog-posts">
      <h1>Blog Posts</h1>
      
      {posts.length === 0 ? (
        <p>No blog posts found.</p>
      ) : (
        <div className="posts-grid">
          {posts.map((post) => (
            <div key={post.id} className="post-card">
              {post.featured_image && (
                <img 
                  src={getImageUrl(post.featured_image)} 
                  alt={post.title} 
                  className="featured-image"
                />
              )}
              
              <div className="post-content">
                <h2>{post.title}</h2>
                
                <div className="post-meta">
                  <span className="date">
                    {new Date(post.created_at).toLocaleDateString()}
                  </span>
                  
                  {post.published ? (
                    <span className="status published">Published</span>
                  ) : (
                    <span className="status draft">Draft</span>
                  )}
                </div>
                
                <div 
                  className="post-excerpt"
                  dangerouslySetInnerHTML={{ 
                    __html: post.content.substring(0, 150) + '...' 
                  }} 
                />
                
                <button onClick={() => navigate(`/posts/${post.id}`)}>
                  Read More
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BlogPosts; 