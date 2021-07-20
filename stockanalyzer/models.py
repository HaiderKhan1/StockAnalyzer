from stockanalyzer import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    isAdmin = db.Column(db.Integer)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    watchlists = db.relationship('Watchlist', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(200), nullable=False)
    stock_symbol = db.Column(db.String(20), nullable=False)
    stock_price = db.Column(db.String(20))
    stock_eps = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Stock:('{self.stock_name}', '{self.stock_symbol}', '{self.stock_price}')"
