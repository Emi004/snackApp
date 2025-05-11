
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

        if recipe.id == recipe_id:
            return jsonify(recipe.as_dict())
    return jsonify({'error': 'recipe not found'}), 404


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    categories=[]


    categoriesJSON=request.json.get('categories')
    if len(categoriesJSON)==0 or categoriesJSON is None:
        return jsonify({'error': 'categories is empty'}), 400

    for cat_name in categoriesJSON:
        category=db.session.query(Category).filter_by(name=cat_name).first()
        if category:
            categories.append(category)
        else:
            return jsonify({'error': f'{cat_name} does not exist'}), 400

    keywords={}
    for col in Recipe.__table__.columns:

        if col.name!='id':
            value=request.json.get(col.name)
            if value is None or value=='':
                return jsonify({'error': f'{col.name} is empty'}), 400
            keywords[col.name]=value
    new_recipe = Recipe(
            **keywords,
            categories=categories
    )
    db.session.add(new_recipe)
    db.session.flush()

    ingredientsJSON=request.json.get('ingredients')
    if len(ingredientsJSON)==0 or ingredientsJSON is None:
        return jsonify({'error': 'ingredients is empty'}), 400
    else:
        for ing in request.json.get('ingredients'):
            keywords_ing={}
            for col in Ingredient.__table__.columns:
                if col.name!='id' and col.name!='recipe_id':
                    value=ing.get(col.name)
                    if (value is None and col.name!='unit') or value=='' or (value==0 and col.name=='quantity'):
                        return jsonify({'error': f'{ing} {col.name} is empty'}), 400
                    keywords_ing[col.name]=value
            ingredient = Ingredient(
                **keywords_ing,
                recipe_id=new_recipe.id

            )
            db.session.add(ingredient)

    db.session.commit()

    return jsonify(new_recipe.as_dict()),201
@app.route('/api/recipes/<int:recipe_id>',methods=['DELETE'])

def delete_recipe(recipe_id):

    recipe=db.session.query(Recipe).filter_by(id=recipe_id).first()

    if recipe:
            db.session.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).delete()
            db.session.query(recipe_category).filter_by(recipe_id=recipe_id).delete()
            db.session.delete(recipe)
            db.session.commit()
            return jsonify(recipe.as_dict()),200

    return jsonify({'errors':'id not found'}),404

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):

    recipe=db.session.query(Recipe).filter_by(id=recipe_id).first()
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

            name=col.name
            if name != 'id':
                setattr(recipe,name, value if(value:=request.json.get(name)) else getattr(recipe,name))

    recipe.categories = categories_list

    for ing in request.json.get('ingredients'):
        ingredient = Ingredient(
            name=ing['name'],
            unit=ing['unit'],
            quantity=ing['quantity'],
            recipe_id=recipe_id

        )
        if (db_ing:=db.session.query(Ingredient).filter_by(name=ingredient.name,recipe_id=recipe_id).first()):
            for col in db_ing.__table__.columns:
                col_name=col.name
                if col_name != 'id':
                    setattr(db_ing, col_name, getattr(ingredient, col_name))
        else:
            db.session.add(ingredient)

    db.session.commit()
    return jsonify(recipe.as_dict()),200

@app.route('/api/categories', methods=["GET"])
def get_categories():
    categories=[]

    for category in db.session.query(Category).all():
        categories.append(category.as_dict())

    return jsonify(categories),200

@app.route('/api/categories', methods=["POST"])
def create_category():

    keywords={}
    for col in Category.__table__.columns:
        if col.name != 'id':
            value=request.json.get(col.name)
            if value is None or value == '':
                return jsonify({'error':f'{col.name} is Null'}),400
            keywords[col.name]=value
    # NOTE(interesting find): ** turns dic key:value into keyword arguments ("nume":"blabla" -> nume="blabla")
    category=Category(**keywords)
    if db.session.query(Category).filter_by(name=category.name).first():
        return jsonify({'error':"already exists"}),403
    db.session.add(category)
    db.session.commit()
    return jsonify(category.as_dict()),200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
