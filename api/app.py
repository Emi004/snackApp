from turtledemo.sorting_animate import instructions1

from flask import Flask, jsonify,request
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db

from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.association import recipe_category

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)




@app.route('/')
def hello_world():
    return 'welcome to my snack app!'


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes=[]

    for recipe in db.session.query(Recipe).all():

        recipes.append(recipe.as_dict())


    return jsonify(recipes)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):

    for recipe in db.session.query(Recipe).all():

        if recipe.as_dict()['id'] == recipe_id:
            return jsonify(recipe.as_dict())
    return jsonify({'error': 'recipe not found'}), 404


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    categories=[]

    for cat_name in request.json.get('categories'):
        category=db.session.query(Category).filter_by(name=cat_name).first()
        if category:
            categories.append(category)

    new_recipe = Recipe(

        name= request.json.get('name'),
        duration= request.json.get('duration'),
        pictures= request.json.get('pictures'),
        instructions= request.json.get('instructions'),

        categories=categories
    )
    db.session.add(new_recipe)
    db.session.flush()

    for ing in request.json.get('ingredients'):
        ingredient = Ingredient(
            name=ing['name'],
            unit=ing['unit'],
            quantity=ing['quantity'],
            recipe_id=new_recipe.id

        )
        db.session.add(ingredient)

    db.session.commit()

    return jsonify(new_recipe.as_dict()),201
@app.route('/api/recipes/<int:recipe_id>',methods=['DELETE'])

def delete_recipe(recipe_id):
    i=0
    for recipe in recipes:

        if recipe['id'] == recipe_id:
            delete= recipes[i]
            recipes.pop(i)
            return jsonify(delete),200
        i=i+1
    return jsonify({'errors':'id not found'}),404

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):


    try:
        recipe=recipes[recipe_id-1]
    except:
        return jsonify({'errors':'id not found'}),404

    for key in recipe:
        recipe[key]=value if(value:=request.json.get(key)) else recipe[key]

    return jsonify(recipe)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
