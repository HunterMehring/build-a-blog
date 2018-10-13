from flask import Flask, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect("/blog")

@app.route('/blog', methods=['POST','GET'])
def blog():    
    blogs = Blog.query.all()
    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id=id).first()
        return render_template("post.html", title="Build a Blog", blog=blog)
    return render_template('blogs.html',title="Build a Blog", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        if blog_title.strip() == '':
            flash("You forgot to add a blog title", "error")
            return redirect("/newpost")
        if blog_content.strip() == '':
            flash("You forgot to write your post", "error")
            return redirect("/newpost")
        #for some reason i cant get the categories working, does it have to do with redirecting?
        blog = Blog(blog_title, blog_content)
        db.session.add(blog)
        db.session.commit()
        return redirect("./blog?id={0}".format(blog.id)) #this one line took me 3 hours


    return render_template('add_a_new_post.html', title="Build a Blog")


if __name__ == '__main__':
    app.run()