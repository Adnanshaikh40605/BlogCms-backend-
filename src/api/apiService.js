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
      console.log(`Fetching approved comments for post ${postId} - ${new Date().toISOString()}`);
      
      // First try with the dedicated endpoint
      try {
        // Ensure postId is a string
        const safePostId = String(postId);
        const dedicatedUrl = `${API_URL}/api/comments/approved-for-post/?post=${safePostId}`;
        console.log('Trying dedicated endpoint URL:', dedicatedUrl);
        
        const response = await fetch(dedicatedUrl);
        if (!response.ok) {
          throw new Error(`Server returned ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Approved comments response (dedicated endpoint):', data);
        
        return {
          results: Array.isArray(data) ? data : [],
          count: Array.isArray(data) ? data.length : 0
        };
      } catch (dedicatedEndpointError) {
        console.warn('Dedicated endpoint failed, falling back to query params:', dedicatedEndpointError);
        
        // Fall back to using query params if the dedicated endpoint fails
        // Ensure postId is a string
        const safePostId = String(postId);
        const fallbackUrl = `${API_URL}/api/comments/?post=${safePostId}&approved=true`;
        console.log('Trying fallback URL with query params:', fallbackUrl);
        
        const fallbackResponse = await fetch(fallbackUrl);
        if (!fallbackResponse.ok) {
          throw new Error(`Fallback also failed: ${fallbackResponse.status} ${fallbackResponse.statusText}`);
        }
        
        const fallbackData = await fallbackResponse.json();
        console.log('Approved comments response (fallback):', fallbackData);
        
        return {
          results: Array.isArray(fallbackData) ? fallbackData : [],
          count: Array.isArray(fallbackData) ? fallbackData.length : 0
        };
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