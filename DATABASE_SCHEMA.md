# Database Schema and Relationships

This document provides a detailed overview of the database schema and relationships in the Blog CMS system.

## Entity Relationship Diagram (ERD)

```
+---------------+       +----------------+       +--------------+
|    BlogPost   |       |    Comment     |       |     FAQ      |
+---------------+       +----------------+       +--------------+
| id            |<----->| id             |       | id           |
| title         |       | post (FK)      |       | question     |
| slug          |       | content        |       | answer       |
| content       |       | created_at     |       | order        |
| featured_image|       | approved       |       | created_at   |
| category      |       +----------------+       | updated_at   |
| created_at    |                                +--------------+
| updated_at    |                                       ▲
| published     |                                       |
| read_time     |                                       |
+---------------+                                       |
       ▲                                                |
       |                                                |
       +------------------------------------------------+
                        ManyToMany
```

## Model Details

### BlogPost

The `BlogPost` model is the central entity in the Blog CMS system, representing individual blog articles.

**Fields:**
- `id` (AutoField): Primary key
- `title` (CharField, max_length=200): The title of the blog post
- `slug` (SlugField, max_length=200, unique=True): URL-friendly identifier derived from the title
- `content` (RichTextUploadingField): Rich text content supporting formatting and embedded media
- `featured_image` (ImageField): Main image displayed at the top of the post
- `category` (CharField, max_length=100): Category classification of the post
- `created_at` (DateTimeField): When the post was created
- `updated_at` (DateTimeField): When the post was last updated
- `published` (BooleanField): Whether the post is public (True) or draft (False)
- `read_time` (CharField): Estimated time to read the post

**Relationships:**
- Has many `Comment`s (one-to-many)
- Has many `FAQ`s (many-to-many)

**Indexes:**
- `slug` (unique)
- `created_at` (for ordering)

### Comment

The `Comment` model represents user-submitted comments on blog posts.

**Fields:**
- `id` (AutoField): Primary key
- `post` (ForeignKey to BlogPost): The blog post this comment belongs to
- `content` (TextField): The comment text
- `created_at` (DateTimeField): When the comment was submitted
- `approved` (BooleanField): Whether the comment is approved for public display

**Relationships:**
- Belongs to one `BlogPost` (many-to-one)

**Indexes:**
- `post_id` (for efficient retrieval of comments for a specific post)
- `approved` (for filtering approved/unapproved comments)

### FAQ

The `FAQ` model represents frequently asked questions that can be associated with blog posts.

**Fields:**
- `id` (AutoField): Primary key
- `question` (CharField): The question text
- `answer` (TextField): The answer text
- `order` (IntegerField): Position for display ordering
- `created_at` (DateTimeField): When the FAQ was created
- `updated_at` (DateTimeField): When the FAQ was last updated

**Relationships:**
- Belongs to many `BlogPost`s (many-to-many)

**Indexes:**
- `order` (for sorting)

## Relationship Details

### BlogPost to Comment (One-to-Many)

- A `BlogPost` can have zero or many `Comment`s
- Each `Comment` belongs to exactly one `BlogPost`
- Implemented via a foreign key in the `Comment` model referencing `BlogPost`
- When a `BlogPost` is deleted, all associated `Comment`s are also deleted (CASCADE)

### BlogPost to FAQ (Many-to-Many)

- A `BlogPost` can have zero or many `FAQ`s
- An `FAQ` can be associated with zero or many `BlogPost`s
- Implemented using a junction/pivot table `blog_post_faqs`
- The relationship allows reusing FAQs across multiple blog posts

## Database Migrations

The database schema is managed through Django migrations. All migrations are stored in the `backend/blog/migrations/` directory and should be applied in order.

To apply migrations:

```bash
python manage.py migrate
```

To create a new migration after model changes:

```bash
python manage.py makemigrations
```

## Query Optimization

The following strategies are used to optimize database queries:

1. **Indexed Fields**: Key fields used in filtering and ordering are indexed
2. **Select Related**: When retrieving blog posts with comments, `select_related` is used to minimize queries
3. **Prefetch Related**: When retrieving blog posts with FAQs, `prefetch_related` is used to batch queries

## Example Queries

### Get all published blog posts with their comments

```python
BlogPost.objects.filter(published=True).prefetch_related('comment_set')
```

### Get a specific blog post with its FAQs

```python
BlogPost.objects.filter(slug='example-post').prefetch_related('faqs')
```

### Get pending comments for moderation

```python
Comment.objects.filter(approved=False).select_related('post')
``` 