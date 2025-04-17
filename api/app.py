from flask import Flask
from dotenv import load_dotenv
from config import Config
from models import db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.association import recipe_category

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        db.drop_all()
    app.run(debug=True)