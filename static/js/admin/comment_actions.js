/**
 * Comment management JavaScript functions for WordPress-like row actions
 */

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Reload page after action
function reloadPage() {
    window.location.reload();
}

// Perform comment action via API
function performCommentAction(commentId, action, data = {}) {
    const csrftoken = getCookie('csrftoken');
    
    // Default data with comment ID
    const requestData = {
        comment_id: commentId,
        ...data
    };
    
    // Send request to appropriate endpoint
    fetch(`/api/comments/${action}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(requestData),
    })
    .then(response => {
        if (response.ok) {
            reloadPage();
        } else {
            alert('Error performing comment action. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error performing comment action.');
    });
}

// Approve comment
function approveComment(commentId) {
    if (confirm('Are you sure you want to approve this comment?')) {
        performCommentAction(commentId, 'approve');
    }
    return false; // Prevent default link action
}

// Unapprove comment
function unapproveComment(commentId) {
    if (confirm('Are you sure you want to unapprove this comment?')) {
        performCommentAction(commentId, 'unapprove');
    }
    return false;
}

// Trash comment
function trashComment(commentId) {
    if (confirm('Are you sure you want to move this comment to trash?')) {
        performCommentAction(commentId, 'trash');
    }
    return false;
}

// Delete comment permanently
function deleteComment(commentId) {
    if (confirm('Are you sure you want to permanently delete this comment? This action cannot be undone.')) {
        performCommentAction(commentId, 'delete');
    }
    return false;
}

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    console.log('Comment actions script loaded');
}); 