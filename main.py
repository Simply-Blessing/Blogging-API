from flask import Flask,request,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import JSON, or_
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
db = SQLAlchemy(app)
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),unique = True, nullable=False)
    content = db.Column(db.String(500))
    category = db.Column(db.String(80))
    tags = db.Column(JSON)
    createdAt = db.Column(db.DateTime,default=datetime.now)
    updatedAt = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

def json_response(data, status=200):
    return Response(
        json.dumps(data,indent=4),
        status=status,
        mimetype='application'
    )
with app.app_context():
    db.create_all()

@app.route('/blogs',methods=['GET'])
def filter_blog():
    '''
    Retrieve all blog posts.
    Optional query parameter 'search' can filter posts by title, content, or category.
    Example: GET /blogs?search=tech
    '''
    search = request.args.get("search","").strip() 
    query = Blog.query

    if search:
        query = query.filter(
            or_(
                Blog.title.ilike(f"%{search}%"),
                Blog.content.ilike(f"%{search}%"),
                Blog.category.ilike(f"%{search}%")
            )
        )
    blogs = query.all()
    output = []
    for blog in blogs:
        blog_data={
            'id':blog.id,
            'title':blog.title,
            'content':blog.content,
            'category':blog.category,
            'tags':blog.tags,
            'createdAt':blog.createdAt.isoformat(),
            'updatedAt':blog.updatedAt.isoformat()
        }
        output.append(blog_data)
    return json_response(output)

@app.route('/blogs/<id>')
def get_blog(id):
    '''
    Retrieve a single blog post by its ID.
    Returns 404 if not found.
    '''
    blog = Blog.query.get_or_404(id)
    output= {
        'id':blog.id,
        'title':blog.title,
        'content':blog.content,
        'category':blog.category,
        'tags':blog.tags,
        'createdAt':blog.createdAt.isoformat(),
        'updatedAt':blog.updatedAt.isoformat()
    }
    return json_response(output)


@app.route('/blogs',methods=['POST'])
def new_blog():
    '''
    Create a new blog post.
    Expects JSON body with keys: title, content, category, tags.
    Returns 201 on success, 400 if creation fails (e.g., duplicate title).
    '''
    data = request.get_json()
    try:
        blog = Blog(
            title=data['title'],
            content=data['content'],
            category=data['category'],
            tags=data.get('tags',[])
        )
        db.session.add(blog)
        db.session.commit()
        output= {
            'id':blog.id,
            'title':blog.title,
            'content':blog.content,
            'category':blog.category,
            'tags':blog.tags,
            'createdAt':blog.createdAt.isoformat(),
            'updatedAt':blog.updatedAt.isoformat()
        }
        return json_response(output)
    except Exception as e:
        db.session.rollback()
        return json_response({
            'error':'Blog post could not be created',
            'details': str(e)
            }, 
            status=400
        )

@app.route('/blogs/<id>', methods=['PUT'])
def update_blog(id):
    '''
    Update an existing blog post by ID.
    Accepts JSON with any combination of title, content, category, tags.
    Returns updated blog post.
    Returns 404 if post does not exist.
    '''
    blog = Blog.query.get_or_404(id)
    updated_blog = request.get_json()

    try:
        if 'title' in updated_blog:
            blog.title = updated_blog['title']
        if 'content' in updated_blog:
            blog.content = updated_blog['content']
        if 'category' in updated_blog:
            blog.category = updated_blog['category']
        if 'tags' in updated_blog:
            blog.tags = updated_blog['tags']
        
        db.session.commit()
        output = {
            'id':blog.id,
            'title':blog.title,
            'content':blog.content,
            'category':blog.category,
            'tags':blog.tags,
            'createdAt':blog.createdAt.isoformat(),
            'updatedAt':blog.updatedAt.isoformat()
        }
        return json_response(output)
    except Exception as e:
        return json_response({
            'error':'Blog post cannot be found',
            'details': str(e)
            },
            status=404
        )


@app.route('/blogs/<id>',methods=['DELETE'])
def delete_blog(id):
    '''
    Delete a blog post by ID.
    Returns 204 No Content on success.
    Returns 404 if post does not exist.
    '''
    blog = Blog.query.get_or_404(id)
    try:
        db.session.delete(blog)
        db.session.commit()
        return '', 204
    except Exception as e:
        return json_response({
            'error':'Blog post cannot be found',
            'details': str(e)
            },
            status=404
        )
