import json
import os
import re

from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy

from config import Config


def ingredient_delta(recipe_ingredients, existing_ingredients):
    uses = len(set(existing_ingredients) & set(recipe_ingredients))
    doesnt_use = len(existing_ingredients) - uses
    extra = len(recipe_ingredients) - uses

    return uses, doesnt_use, extra


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.jinja_env.globals.update(ingredient_delta=ingredient_delta)

from models import Recipe

db.create_all()

# index all the recipes in the directory
for recipe_file in os.listdir('recipes'):
    with open('recipes/{}'.format(recipe_file)) as f:
        content = json.load(f)

    new_recipe = Recipe(
        filename=recipe_file.rsplit('.', 2)[0],

        name=content['name'],
        description=content['description'],

        _tags=','.join(content['tags']),
        _ingredients=','.join(content['ingredients'].keys())
    )

    db.session.add(new_recipe)

db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipe/<name>')
def recipe(name):

    recipe_row = Recipe.query.filter(Recipe.filename == name).first()

    if recipe_row is None:
        abort(404)

    else:
        try:
            recipe_content = json.load(open('recipes/{}.json'.format(recipe_row.filename), 'r'))

        except FileNotFoundError:
            abort(400)

        else:
            return render_template('recipe.html', recipe=recipe_content, title=recipe_content['name'])


@app.route('/search')
def search():
    query_string = request.args.get('query')

    if query_string is not None:
        recipes = Recipe.query.filter(Recipe.name.ilike('%{}%'.format(query_string)))
    else:
        recipes = Recipe.query

    return render_template('search_results.html', results=recipes)


@app.route('/ingredient_search')
def ingredient_search():
    def ingredient_sort(existing):
        def _sort(r):
            return len(set(existing) & set(r.ingredients()))

        return _sort

    ingredients = request.args.get('query')

    if ingredients is None:
        return render_template('search_results.html')

    else:
        ingredients_split = [x.strip().lower() for x in ingredients.split(',')]

        all_recipes = Recipe.query.all()

        all_recipes.sort(key=ingredient_sort(ingredients_split))

        return render_template('search_results.html',
                               results=all_recipes,
                               ingredients=ingredients_split,
                               ingredient_search=True)


@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html')


if __name__ == '__main__':
    app.run()
