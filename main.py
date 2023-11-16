from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# create the extension
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)


class Books(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, unique=True, nullable=False)
  author = db.Column(db.String, nullable=False)
  rating = db.Column(db.Integer, nullable=False)


with app.app_context():
  db.create_all()


@app.route('/')
def home():
  result = db.session.execute(db.select(Books).order_by(Books.title))
  all_books = result.scalars()
  return render_template("index.html", books=all_books)


@app.route('/add', methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
    new_book = Books(title=request.form['title'],
                     author=request.form['author'],
                     rating=request.form['rating'])
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('home'))
  return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
  if request.method == 'POST':
    book_id = request.form['id']
    book_to_update = db.get_or_404(Books, book_id)
    book_to_update.rating = request.form['rating']
    db.session.commit()
    return redirect(url_for('home'))
  book_id = request.args.get('id')
  book_selected = db.get_or_404(Books, book_id)
  return render_template("edit.html", book=book_selected)


@app.route('/delete')
def delete():
  book_id = request.args.get('id')
  book_to_delete = db.get_or_404(Books, book_id)
  db.session.delete(book_to_delete)
  db.session.commit()
  return redirect(url_for('home'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
