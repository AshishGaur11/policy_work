from app import db

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(1))
    sum_assured = db.Column(db.Integer)
    modal_premium = db.Column(db.Integer)
    premium_frequency = db.Column(db.String(10))
    pt = db.Column(db.Integer)
    ppt = db.Column(db.Integer)

    def __repr__(self):
        return f'<Policy {self.id}>'