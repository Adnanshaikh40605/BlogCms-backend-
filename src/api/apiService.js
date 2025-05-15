// Comment API functions
const commentAPI = {
  // Get all comments (with optional post ID filter)
  getAll: async (postId = null) => {
    let url = `${API_URL}/api/comments/`;
    if (postId) {
      // Ensure postId is a string/number value, not an object
      const safePostId = String(postId);
      url += `?post=${safePostId}`;
    }
    const response = await fetch(url);
    return response.json();
  },
  
  // Get approved comments for a post
  getApproved: async (postId) => {
    try {
      if (!postId) {
        console.error('No post ID provided to getApproved');
        return { results: [], count: 0 };
      }
      
      // Ensure postId is a string to avoid [object Object] in URL
      const safePostId = String(postId);
      console.log(`Fetching approved comments for post ${safePostId} - ${new Date().toISOString()}`);
      
      // Try fallback method first (more reliable)
      try {
        const fallbackUrl = `${API_URL}/api/comments/?post=${safePostId}&approved=true`;
        console.log('Request URL:', fallbackUrl);
        
        const fallbackResponse = await fetch(fallbackUrl);
        if (!fallbackResponse.ok) {
          throw new Error(`Failed with status ${fallbackResponse.status}`);
        }
        
        const fallbackData = await fallbackResponse.json();
        console.log('Approved comments response (query params):', fallbackData);
        
        return {
          results: Array.isArray(fallbackData) ? fallbackData : [],
          count: Array.isArray(fallbackData) ? fallbackData.length : 0
        };
      } catch (fallbackError) {
        console.warn('Standard endpoint failed:', fallbackError);
        // Return empty results as ultimate fallback
        return { results: [], count: 0 };
      }
    } catch (error) {
      console.error('Error fetching approved comments:', error);
      // Return empty results to avoid UI breaking
      return { results: [], count: 0 };
    }
  },
  
  // Get pending comments for a post
  getPending: async (postId) => {
    try {
      console.log(`Fetching pending comments for post ${postId} - ${new Date().toISOString()}`);
      // Use explicit query parameter for approved=false
      // Ensure postId is a string
      const safePostId = String(postId);
      const url = `${API_URL}/api/comments/?post=${safePostId}&approved=false`;
      console.log('Request URL:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      console.log('Pending comments response:', data);
      
      // Format the response to match what the component expects
      return {
        results: Array.isArray(data) ? data : [],
        count: Array.isArray(data) ? data.length : 0
      };
    } catch (error) {
      console.error('Error fetching pending comments:', error);
      return { results: [], count: 0 };
    }
  },
}; 