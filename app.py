from flask import Flask, render_template, g, request
import sqlite3
from rejester import login, signup
#from model import generate_qa_from_document, generate_insight_from_document

app = Flask(__name__, template_folder='template')
app.config['DATABASE'] = 'model.db'

@app.route('/')
def index():
    return render_template('index.html')    

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        try:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
        except Exception as e:
            print("Error in schema:", e)



@app.route('/', methods=['GET', 'POST'])
def handle_login():
    return login(get_db())

@app.route('/signup', methods=['GET', 'POST'])
def handle_signup():
    user_name = request.form['name']
    user_email = request.form['email']
    user_password = request.form['password']
    sin = signup(get_db(),user_name,user_email,user_password)
    if sin:
        return render_template('gen.html')

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    init_db()  # Call init_db to initialize the database before running the app
    app.run(debug=True)
