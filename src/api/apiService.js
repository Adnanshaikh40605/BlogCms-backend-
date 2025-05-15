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
  
  // Get all comments for a specific post (both approved and pending)
  getAllForPost: async (postId) => {
    try {
      if (!postId) {
        console.error('No post ID provided to getAllForPost');
        return { approved: [], pending: [], total: 0 };
      }
      
      // Ensure postId is a string
      const safePostId = String(postId);
      console.log(`Fetching all comments for post ${safePostId}`);
      
      try {
        // Try using the all endpoint first
        const url = `${API_URL}/api/comments/all/?post=${safePostId}`;
        console.log('Request URL:', url);
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Failed with status ${response.status}`);
        }
        
        const data = await response.json();
        console.log('All comments response:', data);
        
        return data; // This should already have approved and pending arrays
      } catch (dedicatedEndpointError) {
        console.warn('Dedicated endpoint failed, falling back to query params:', dedicatedEndpointError);
        
        // If the dedicated endpoint fails, fetch approved and pending separately
        const approved = await commentAPI.getApproved(safePostId);
        const pending = await commentAPI.getPending(safePostId);
        
        return {
          approved: approved.results || [],
          pending: pending.results || [],
          total: (approved.results?.length || 0) + (pending.results?.length || 0)
        };
      }
    } catch (error) {
      console.error('Error fetching all comments for post:', error);
      return { approved: [], pending: [], total: 0 };
    }
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
      if (!postId) {
        console.error('No post ID provided to getPending');
        return { results: [], count: 0 };
      }
      
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
  
  // Add placeholder methods for other functions used in CommentContext
  // These will be implemented as needed
  approve: async (commentId) => {
    if (!commentId) {
      console.error('No comment ID provided to approve');
      throw new Error('Comment ID is required');
    }
    
    const safeCommentId = String(commentId);
    const url = `${API_URL}/api/comments/${safeCommentId}/approve/`;
    console.log('Approving comment with URL:', url);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    return response.json();
  },
  
  reject: async (commentId) => {
    if (!commentId) {
      console.error('No comment ID provided to reject');
      throw new Error('Comment ID is required');
    }
    
    const safeCommentId = String(commentId);
    const url = `${API_URL}/api/comments/${safeCommentId}/reject/`;
    console.log('Rejecting comment with URL:', url);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    return response.json();
  },
  
  create: async (commentData) => {
    if (!commentData || !commentData.post) {
      console.error('Invalid comment data or missing post ID');
      throw new Error('Valid comment data with post ID is required');
    }
    
    // Ensure post ID is a string
    commentData.post = String(commentData.post);
    
    const url = `${API_URL}/api/comments/`;
    console.log('Creating comment with URL:', url, commentData);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(commentData)
    });
    
    return response.json();
  },
  
  bulkApprove: async (commentIds) => {
    if (!Array.isArray(commentIds) || commentIds.length === 0) {
      console.error('No comment IDs provided to bulkApprove');
      throw new Error('Comment IDs are required');
    }
    
    const url = `${API_URL}/api/comments/bulk_approve/`;
    console.log('Bulk approving comments with URL:', url, commentIds);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment_ids: commentIds })
    });
    
    return response.json();
  },
  
  bulkReject: async (commentIds) => {
    if (!Array.isArray(commentIds) || commentIds.length === 0) {
      console.error('No comment IDs provided to bulkReject');
      throw new Error('Comment IDs are required');
    }
    
    const url = `${API_URL}/api/comments/bulk_reject/`;
    console.log('Bulk rejecting comments with URL:', url, commentIds);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment_ids: commentIds })
    });
    
    return response.json();
  }
}; 