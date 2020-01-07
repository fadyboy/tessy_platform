from studentapp import db


class AdminUsers(db.Model):
    __tablename__ = "AdminUsers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(16))


    def __repr__(self):
        return f"Admin User: {self.username}"