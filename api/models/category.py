from models import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {col.name: getattr(self,col.name) for col in self.__table__.columns}