from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

all_post = [{
    'title': 'post 1',
    'content':'This is the content for post 1'
},
{
    'title': 'post 2',
    'author':'Israel',
    'content':'This is the content for post 2'
}]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post')
    else:
        all_post= BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('post.html', posts=all_post)

@app.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
     post = BlogPost.query.get_or_404(id)  
     if request.method == 'POST':  
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/post')
     else:
         return render_template('edit.html', post=post)

@app.route('/home/user/<string:name>/post/<int:id>')  #calling URL using route 
def hello(name, id): #define a function for the route 
    return "Hello, " + name  + " post " + str(id)

@app.route('/onlyget', methods=['GET'])
def get():
    return 'You can only get'
if __name__ == "__main__": #returning the debug method 
        app.run(debug=True)
    
