from app import db


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True)

    name = db.Column(db.String, index=True)
    description = db.Column(db.String)

    _ingredients = db.Column(db.String)
    _tags = db.Column(db.String)

    def ingredients(self):
        return self._ingredients.split(',')

    def tags(self):
        return self._tags.split(',')
