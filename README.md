# Blogging API

A simple Restful API with basic CRUD operations for a personal blogging platform.

---

## Features

- **Create a blog post** (`POST /blogs`)
- **Retrieve all blog posts** (`GET /blogs`)
  - Supports optional search query: `/blogs?search=keyword`
- **Retrieve a single blog post** by ID (`GET /blogs/<id>`)
- **Update a blog post** by ID (`PUT /blogs/<id>`)
- **Delete a blog post** by ID (`DELETE /blogs/<id>`)
- JSON responses are **pretty-printed** for readability
- Tags stored as JSON arrays
- Automatic timestamps for creation and updates

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Simply-Blessing/Blogging-API.git
cd Blogging-API
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the virtual environment

```bash
source .venv/Scripts/activate
```

4. Install dependencies

```bash
pip install flask flask_sqlalchemy
```

---

## Running the API

1. Set environment variables

```bash
export FLASK_APP=main.py
export FLASK_ENV=development
```

2. Run the Flask server

```bash
flask run
```

---

## API Endpoints

Create a new blog post

```bash
curl -X POST http://127.0.0.1:5000/blogs \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Debugging in Python",
           "content": "How to effectively debug Python applications using pdb and logging.",
           "category": "Programming",
           "tags": ["debugging", "python", "pdb"]
         }'
```

Get all blogs

```bash
curl http://127.0.0.1:5000/blogs
```

Get one blog via id

```bash
curl "http://127.0.0.1:5000/blogs/1
```

Search blogs

```bash
curl "http://127.0.0.1:5000/blogs?search=flask"
```

Update blog

```bash
curl -X PUT http://127.0.0.1:5000/blogs/1 \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Updated Blog",
           "content": "I just updated this post."
         }'
```

Delete Blog via id

```bash
curl -X DELETE http://127.0.0.1:5000/blogs/1
```

---

## ⚙️ Notes

- Flask runs at: http://127.0.0.1:5000
- You must activate your .venv before running the app (flask run)
- Each curl command assumes your Flask server is running
- The API uses SQLite (data.db) for storage.
- createdAt and updatedAt fields are automatically managed.
- If a blog post is not found, the API returns a 404 error.

---

## Project Inspiration

[Blogging API Roadmap](https://roadmap.sh/projects/blogging-platform-api)

[REST API tutorial](https://youtu.be/qbLc5a9jdXo)
