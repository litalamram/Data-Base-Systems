from flask import Flask, render_template, redirect, url_for, request, make_response,session, jsonify , json
import datetime
from queries import *
app = Flask(__name__)


#search recipe by id
@app.route('/search_recipe_id', methods=['POST', 'GET'])
def search_recipe_id():
    if request.method == 'GET':
        id = request.args.get('id')
	data = searchRecipeByID(id)
	return render_template("recipe.html",data=data)
  
    return ''

#search for products in specific recipe
@app.route('/search_products_in_recipe', methods=['POST', 'GET'])
def search_ing_product():
    if request.method == 'GET':
        id = request.args.get('id')
        category = request.args.get('category')
        #min calories
        if category == "calories":
            data = searchProdMinCalories(id)
        #min fat
        elif category == "fat":
            data = searchProdMinFat(id)
        #min cholesterol
        elif category == "cholesterol":
            data = searchProdMinCholesterol(id)
        #all products
        else:
	    data = searchProductsInRecipe(id)
	return render_template("ing_prod.html",data=data)
  
    return ''


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        name = request.args.get('recipeName')
        diets = request.args.getlist('diet[]')
        ingName = request.args.get('ingredientName')
        maxNumIngs = request.args.get('maxNumIngs')
        cuisine = request.args.get('cuisineName')
        holiday = request.args.get('holidayName')
        HolidayMealName = request.args.get('HolidayMealName')
        minCalories = (request.args.get('minCalories') != None)
        radioMeal = request.args.get('radioTypeMeal')
        radio = request.args.get('radio')
        
        #search with diet restriction
        if (radio == 'dietsRadio' and len(diets) > 0):
            vegan = 'vegan' in diets
            vegetarian = 'vegetarian' in diets
            peanut_free = 'peanut_free' in diets
            tree_nut_free = 'tree_nut_free' in diets
            alcohol_free = 'alcohol_free' in diets
            data = searchRecipeByDiet(name, vegan, vegetarian, peanut_free, tree_nut_free, alcohol_free)
       
        #search with ingredient restriction
        elif (radio == 'ingRadio' and (ingName != '' or maxNumIngs != '') ):
            data = searchRecipeWithIngredient(name, ingName, maxNumIngs)

        #search with cuisine,holiday,calories restriction
        elif (radio == 'cuisineHolidayRadio' and (cuisine != '' or holiday != '' or minCalories) ):
            data = searchRecipeHolidayCuisineMinCalories(cuisine, holiday, minCalories)

        # search holiday main_course or dessert
        elif (radio == 'HolidayMealRadio' and (HolidayMealName != '')):
            if (radioMeal == 'main_course'):
                data = searchHolidayMain(HolidayMealName)
            else:
                data = searchHolidayDessert(HolidayMealName)
       
        #search by recipe name
        else: #(name != '')
            data = searchRecipeByName(name)

         
        return render_template("res.html", data=data)
  
    return ''


#pages

@app.route('/search_diet')
def search_diet():
    return render_template('search_diet.html')

@app.route('/search_by_ingredient')
def search_by_ingredient():
    return render_template('search_by_ingredient.html')

@app.route('/search_by_cuisine_holiday')
def search_by_cuisine_holiday():
    return render_template('search_by_cuisine_holiday.html')

@app.route('/search_holiday_meal')
def search_holiday_meal():
    return render_template('search_holiday_meal.html')

@app.route('/')
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'itsasecret'
    app.run(port=40567, host="delta-tomcat-vm.cs.tau.ac.il", debug=True)







