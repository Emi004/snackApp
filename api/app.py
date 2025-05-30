from import_script import get_all_recipes, populate_db
from flask import Flask, jsonify, request
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


def add_ingredients_to_db(ingredients, recipe_id):
    for ing in ingredients:
        try:
            quantity = float(ing['quantity'])
        except ValueError as exc:
            return jsonify({'error': f'quantity is not of type float: {exc}'}), 400

        ingredient = Ingredient(
            name=ing['name'],
            quantity=quantity,
            unit=ing['unit'],
            recipe_id=recipe_id,
        )
        db.session.add(ingredient)

@app.route('/')
def hello_world():
    return 'welcome to my snack app!'


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = []

    for recipe in db.session.query(Recipe).all():
        recipes.append(recipe.as_dict())

    return jsonify(recipes)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    if recipe := Recipe.query.get(recipe_id):
        return jsonify(recipe.as_dict()), 200
    return jsonify({'error': 'recipe not found'}), 404


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    request_body = {
        'name': request.json.get('name'),
        'duration': request.json.get('duration'),
        'pictures': request.json.get('pictures'),
        'instructions': request.json.get('instructions'),
        'categories': request.json.get('categories'),
        'ingredients': request.json.get('ingredients'),
    }
    for key, value in request_body.items():
        if not value:
            return jsonify({'error': f'{key} is required'}), 400
    for cat in request_body['categories']:
        if 'name' not in cat:
            return jsonify({'error': 'categories must contain a name'}), 400
    for ing in request_body['ingredients']:
        if 'name' not in ing or 'quantity' not in ing:
            return jsonify({'error': 'ingredients must contain a name, quantity and unit (optional)'}), 400

    try:
        category_objs = []
        for cat in request_body['categories']:
            # Check if the category exists
            category = Category.query.filter_by(name=cat['name']).first()
            if not category:
                return jsonify({'error': f'category {cat["name"]} not found'}), 400
            category_objs.append(category)

        # Create a recipe object
        recipe = Recipe(
            name=request_body['name'],
            duration=request_body['duration'],
            pictures=request_body['pictures'],
            instructions=request_body['instructions'],
            categories=category_objs,
        )
        db.session.add(recipe)
        db.session.flush()  # Ensure recipe.id is available

        # Add ingredients
        add_ingredients_to_db(request_body['ingredients'], recipe.id)

        db.session.commit()
        print(f'Inserted recipe: {recipe.name}')
        return jsonify(recipe.as_dict()), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': f'something went wrong: {exc}'}), 500



@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()

    if recipe:
        db.session.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).delete()
        db.session.query(recipe_category).filter_by(recipe_id=recipe_id).delete()
        db.session.delete(recipe)
        db.session.commit()
        return '', 204

    return jsonify({'errors': 'id not found'}), 404


@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    categories_list = []

    for cat_name in request.json.get('categories'):
        category = db.session.query(Category).filter_by(name=cat_name).first()
        if category:
            categories_list.append(category)
        else:
            return jsonify({'error': f'{cat_name} does not exist'}), 400

    for col in recipe.__table__.columns:

        name = col.name
        if name != 'id':
            setattr(recipe, name, value if (value := request.json.get(name)) else getattr(recipe, name))

    recipe.categories = categories_list

    for ing in request.json.get('ingredients'):
        ingredient = Ingredient(
            name=ing['name'],
            unit=ing['unit'],
            quantity=ing['quantity'],
            recipe_id=recipe_id

        )
        if db_ing := db.session.query(Ingredient).filter_by(name=ingredient.name, recipe_id=recipe_id).first():
            for col in db_ing.__table__.columns:
                col_name = col.name
                if col_name != 'id':
                    setattr(db_ing, col_name, getattr(ingredient, col_name))
        else:
            db.session.add(ingredient)

    db.session.commit()
    return jsonify(recipe.as_dict()), 200


@app.route('/api/categories', methods=["GET"])
def get_categories():
    categories = []

    for category in db.session.query(Category).all():
        categories.append(category.as_dict())

    return jsonify(categories), 200


@app.route('/api/categories', methods=["POST"])
def create_category():
    keywords = {}
    for col in Category.__table__.columns:
        if col.name != 'id':
            value = request.json.get(col.name)
            if value is None or value == '':
                return jsonify({'error': f'{col.name} is Null'}), 400
            keywords[col.name] = value
    # NOTE(interesting find): ** turns dic key:value into keyword arguments ("nume":"blabla" -> nume="blabla")
    category = Category(**keywords)
    if db.session.query(Category).filter_by(name=category.name).first():
        return jsonify({'error': "already exists"}), 403
    db.session.add(category)
    db.session.commit()
    return jsonify(category.as_dict()), 200



if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    # Use the following line if you want to populate the database with sample data
    # populate_db(get_all_recipes(), app, db)

    app.run(host='0.0.0.0')
