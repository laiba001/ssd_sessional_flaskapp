from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolios.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    profile_picture = db.Column(db.String(200))
    short_bio = db.Column(db.Text)
    skills = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create-portfolio', methods=['GET', 'POST'])
def create_portfolio():
    if request.method == 'POST':
        profile_picture = request.files['profile_picture']
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            profile_picture_path = None

        portfolio = Portfolio(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            profile_picture=profile_picture_path,
            short_bio=request.form['short_bio'],
            skills=request.form['skills'],
            linkedin=request.form['linkedin'],
            github=request.form['github']
        )
        db.session.add(portfolio)
        db.session.commit()
        return redirect(url_for('view_portfolio', portfolio_id=portfolio.id))
    return render_template('create_portfolio.html')

@app.route('/view-portfolio/<int:portfolio_id>')
def view_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    return render_template('view_portfolio.html', portfolio=portfolio)

@app.route('/contact_me/<int:portfolio_id>')
def contact_me(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    return render_template('contact_me.html', portfolio=portfolio)

if __name__ == '__main__':
    app.run(debug=True)

