# Blog CMS API Endpoints Documentation

Base URL: `https://web-production-f03ff.up.railway.app`

## Authentication

The API currently does not require authentication for GET requests. For POST, PUT, PATCH, and DELETE operations, the Django admin session must be active.

## CORS Configuration

The API supports Cross-Origin Resource Sharing (CORS) with the following configurations:
- Allowed origins: 
  - `http://localhost:3000` (local development)
  - `https://web-production-f03ff.up.railway.app` (backend)
  - `https://blog-cms-frontend-ten.vercel.app` (frontend deployment)
- Credentials are allowed (important for CSRF)
- All standard HTTP methods are supported (GET, POST, PUT, PATCH, DELETE, OPTIONS)

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
      "published": true,
      "approved_comments": [
        {
          "id": 1,
          "content": "Great post!",
          "created_at": "2023-05-16T12:30:00Z"
        }
      ]
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
  - `Content-Type`: `application/json` or `multipart/form-data` (if uploading image)
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
- **Method**: `PATCH` or `PUT`
- **Headers**:
  - `Content-Type`: `application/json` or `multipart/form-data` (if updating image)
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
  - `Content-Type`: `multipart/form-data`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  - Form data with `images[]` field containing one or more image files
- **Success Response**:
  - **Code**: 201
  - **Content**: Array of created image objects

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

### Get All Comments for a Post (Approved and Pending)

Retrieves all comments for a post, separated into approved and pending.

- **URL**: `/api/comments/all/`
- **Method**: `GET`
- **URL Parameters**:
  - `post` (required): Post ID to get comments for
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "approved": [
        {
          "id": 1,
          "post": 1,
          "content": "This is a great post!",
          "created_at": "2023-05-20T15:30:00Z",
          "approved": true
        }
      ],
      "pending": [
        {
          "id": 2,
          "post": 1,
          "content": "This is a pending comment",
          "created_at": "2023-05-21T10:15:00Z",
          "approved": false
        }
      ],
      "total": 2
    }
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
    "content": "This is my comment on the blog post."
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: The created comment object

### Approve a Comment

Approves a comment.

- **URL**: `/api/comments/:id/approve/`
- **Method**: `POST` or `PATCH`
- **Headers**:
  - `X-CSRFToken`: CSRF token (from cookie)
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "status": "comment approved" }`

### Reject a Comment

Rejects (deletes) a comment.

- **URL**: `/api/comments/:id/reject/`
- **Method**: `POST` or `PATCH`
- **Headers**:
  - `X-CSRFToken`: CSRF token (from cookie)
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "status": "comment rejected and deleted" }`

### Bulk Approve Comments

Approves multiple comments at once.

- **URL**: `/api/comments/bulk_approve/`
- **Method**: `POST`
- **Headers**:
  - `Content-Type`: `application/json`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  ```json
  {
    "comment_ids": [1, 2, 3]
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "status": "3 comments approved" }`

### Bulk Reject Comments

Rejects (deletes) multiple comments at once.

- **URL**: `/api/comments/bulk_reject/`
- **Method**: `POST`
- **Headers**:
  - `Content-Type`: `application/json`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  ```json
  {
    "comment_ids": [1, 2, 3]
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "status": "3 comments rejected" }`

### Get Pending Comment Count

Returns the count of unapproved comments.

- **URL**: `/api/comments/pending_count/`
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
  - `Content-Type`: `multipart/form-data`
  - `X-CSRFToken`: CSRF token (from cookie)
- **Data Params**:
  - Form data with:
    - `post`: The ID of the post (integer)
    - `image`: The image file
- **Success Response**:
  - **Code**: 201
  - **Content**: The created image object

## CKEditor Configuration

The CKEditor is configured with these features:
- Rich text formatting (bold, italic, underline)
- Headings (h1-h6)
- Lists (bulleted, numbered)
- Tables with properties
- Image upload and alignment
- Code blocks
- Blockquotes
- Custom color palettes

## Media Files

All uploaded media files are available at `/media/` path:

- Featured images: `/media/featured_images/`
- Blog post images: `/media/blog_images/`
- CKEditor uploads: `/media/uploads/`

## Static Files

Static files (CSS, JavaScript, etc.) are served from `/static/` path. 