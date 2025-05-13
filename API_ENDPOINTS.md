# Blog CMS API Endpoints Documentation

Base URL: `https://web-production-f03ff.up.railway.app`

## Authentication

The API currently does not require authentication for GET requests. For POST, PUT, PATCH, and DELETE operations, the Django admin session must be active.

## Blog Posts API

### Get All Posts

Retrieves a list of all blog posts with pagination.

- **URL**: `/api/posts/`
- **Method**: `GET`
- **URL Parameters**:
  - `page` (optional): Page number for pagination
  - `published` (optional): Filter by published status (true/false)
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "count": 10,
      "next": "https://web-production-f03ff.up.railway.app/api/posts/?page=2",
      "previous": null,
      "results": [
        {
          "id": 1,
          "title": "Sample Blog Post",
          "content": "<p>This is a sample blog post content with <strong>rich text</strong>.</p>",
          "featured_image": "uploads/featured_images/sample.jpg",
          "created_at": "2023-05-15T14:30:00Z",
          "updated_at": "2023-05-16T10:20:00Z",
          "published": true
        },
        // More posts...
      ]
    }
    ```

### Get a Single Post

Retrieves a specific blog post by ID.

- **URL**: `/api/posts/:id/`
- **Method**: `GET`
- **URL Parameters**:
  - `id`: The ID of the blog post to retrieve
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "id": 1,
      "title": "Sample Blog Post",
      "content": "<p>This is a sample blog post content with <strong>rich text</strong>.</p>",
      "featured_image": "uploads/featured_images/sample.jpg",
      "created_at": "2023-05-15T14:30:00Z",
      "updated_at": "2023-05-16T10:20:00Z",
      "published": true
    }
    ```
- **Error Response**:
  - **Code**: 404
  - **Content**: `{ "detail": "Not found." }`

### Create a Blog Post

Creates a new blog post.

- **URL**: `/api/posts/`
- **Method**: `POST`
- **Headers**:
  - `Content-Type`: `application/json`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  ```json
  {
    "title": "New Blog Post",
    "content": "<p>This is the content of my new blog post.</p>",
    "featured_image": null,
    "published": false
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: The created post object

### Update a Blog Post

Updates an existing blog post.

- **URL**: `/api/posts/:id/`
- **Method**: `PATCH`
- **Headers**:
  - `Content-Type`: `application/json`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  ```json
  {
    "title": "Updated Title",
    "content": "<p>Updated content.</p>",
    "published": true
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: The updated post object

### Delete a Blog Post

Deletes a blog post.

- **URL**: `/api/posts/:id/`
- **Method**: `DELETE`
- **Headers**:
  - `X-CSRFToken`: CSRF token (from cookie)
- **Success Response**:
  - **Code**: 204 (No Content)

### Upload Images for a Post

Uploads additional images for a blog post.

- **URL**: `/api/posts/:id/upload_images/`
- **Method**: `POST`
- **Headers**:
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  - Form data with an `image` field containing the image file
- **Success Response**:
  - **Code**: 201
  - **Content**: The created image object

## Comments API

### Get All Comments

Retrieves a list of comments, optionally filtered by post ID and approval status.

- **URL**: `/api/comments/`
- **Method**: `GET`
- **URL Parameters**:
  - `post` (optional): Filter by post ID
  - `approved` (optional): Filter by approval status (true/false)
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {
        "id": 1,
        "post": 1,
        "content": "This is a great post!",
        "created_at": "2023-05-20T15:30:00Z",
        "approved": true
      },
      // More comments...
    ]
    ```

### Create a Comment

Creates a new comment on a blog post.

- **URL**: `/api/comments/`
- **Method**: `POST`
- **Headers**:
  - `Content-Type`: `application/json`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  ```json
  {
    "post": 1,
    "content": "This is my comment on the blog post.",
    "approved": false
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: The created comment object

### Approve a Comment

Approves a comment.

- **URL**: `/api/comments/:id/approve/`
- **Method**: `POST`
- **Headers**:
  - `X-CSRFToken`: CSRF token (from cookie)
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "status": "comment approved" }`

### Get Pending Comment Count

Returns the count of unapproved comments.

- **URL**: `/api/comments/pending-count/`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "count": 5 }`

## Blog Images API

### Get All Images

Retrieves a list of blog images.

- **URL**: `/api/images/`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {
        "id": 1,
        "post": 1,
        "image": "uploads/blog_images/image1.jpg",
        "created_at": "2023-05-20T15:30:00Z"
      },
      // More images...
    ]
    ```

### Upload an Image

Uploads a new image for a blog post.

- **URL**: `/api/images/`
- **Method**: `POST`
- **Headers**:
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  - Form data with:
    - `post`: The ID of the post (integer)
    - `image`: The image file
- **Success Response**:
  - **Code**: 201
  - **Content**: The created image object

## Media Files

All uploaded media files are available at `/media/` path:

- Featured images: `/media/featured_images/`
- Blog post images: `/media/blog_images/`
- CKEditor uploads: `/media/uploads/`

## Error Handling

All API endpoints return standard HTTP error codes:

- `400 Bad Request`: The request was malformed
- `401 Unauthorized`: Authentication is required
- `403 Forbidden`: The request was not allowed
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

## CORS

The API is configured to accept requests from specified origins, including:

- `http://localhost:3000`
- `http://localhost:5173`
- Your frontend deployment URL (when set in environment variables)

## Additional Notes

1. For any file uploads, ensure you're using `multipart/form-data` and not setting the `Content-Type` header manually.
2. For CSRF protection, ensure that your frontend includes credentials in all requests that change data. 