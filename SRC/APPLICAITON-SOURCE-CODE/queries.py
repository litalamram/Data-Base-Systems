# -*- coding: utf-8 -*-

# !/usr/bin/python
import MySQLdb as mdb


# 1

def searchRecipeByName(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT ID, name, img 
                               FROM Recipe 
                               WHERE MATCH (name) AGAINST (+%s IN BOOLEAN MODE) 
                               """, [param])
        return cur.fetchall()


def searchRecipeByID(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT ID, name, GROUP_CONCAT(Recipe_Ingredient.ingredient SEPARATOR '\n'), time_needed/60, rating, number_serving, url, calories, img 
                       FROM (
                       SELECT ID, name, time_needed, rating, number_serving, url, calories, img 
                       FROM Recipe 
                       WHERE ID = %s
                       ) as a
                       JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = a.ID""", [param])
        return cur.fetchall()


# 2
def searchRecipeByDiet(name, vegan, vegetrian, peanutFree, treeNutFree, alchoholFree):
    params = []
    filterName = ""
    filterDiet = []
    if name != "":
        filterName = "WHERE MATCH (Recipe.name) AGAINST (%s IN BOOLEAN MODE)"
        params.append(name)
    if vegan: filterDiet.append("Ingredient_tags.VEGAN=0")
    if vegetrian: filterDiet.append("Ingredient_tags.VEGETARIAN=0")
    if peanutFree: filterDiet.append("Ingredient_tags.PEANUT_FREE=0")
    if treeNutFree: filterDiet.append("Ingredient_tags.TREE_NUT_FREE=0")
    if alchoholFree: filterDiet.append("Ingredient_tags.ALCOHOL_FREE=0")
    filterDiet = " WHERE " + " OR ".join(filterDiet)

    query = """SELECT a.ID, a.name, a.img 
               FROM
               (
               SELECT DISTINCT Recipe.ID, Recipe.name, Recipe.img
               FROM Recipe """
    query += filterName
    query += """) as a
               LEFT join
               (
               SELECT Recipe_Ingredient.recipe_id 
               FROM Recipe_Ingredient
               JOIN Ingredient_tags ON Ingredient_tags.ingredient_name = Recipe_Ingredient.ingredient """
    query += filterDiet
    query += """) as b
               ON a.ID = b.recipe_id
               WHERE b.recipe_id is NULL
               """

    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()


# 3
def searchProductsInRecipe(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT DISTINCT Product.ingredient_name, Product.brand_name, Product.calories, Product.total_fat, Product.saturated_fat,
                               Product.cholesterol, Product.sodium, Product.sugars, Product.protein
                               FROM (
                               SELECT Recipe_Ingredient.ingredient
                               FROM Recipe_Ingredient
                               WHERE recipe_id = %s
                               ) as a
                               JOIN Product ON a.ingredient = Product.ingredient_name
                               ORDER BY Product.ingredient_name;""", [param])
        return cur.fetchall()


# 4
def searchProdMinCalories(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT p1.ingredient_name, p1.brand_name, p1.calories, p1.total_fat, p1.saturated_fat,
                            p1.cholesterol, p1.sodium, p1.sugars, p1.protein
                            FROM (SELECT ingredient FROM Recipe_Ingredient WHERE recipe_id = %s) as a
                            JOIN Product as p1 ON a.ingredient = p1.ingredient_name
                            JOIN
                            (SELECT p2.ingredient_name, min(p2.calories) as min_cal
                            FROM Product as p2
                            GROUP BY p2.ingredient_name) as b ON b.ingredient_name = p1.ingredient_name
                            WHERE p1.calories = b.min_cal""", [param])
        return cur.fetchall()


def searchProdMinCholesterol(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT p1.ingredient_name, p1.brand_name, p1.calories, p1.total_fat, p1.saturated_fat,
                            p1.cholesterol, p1.sodium, p1.sugars, p1.protein
                            FROM (SELECT ingredient FROM Recipe_Ingredient WHERE recipe_id = %s) as a
                            JOIN Product as p1 ON a.ingredient = p1.ingredient_name
                            JOIN
                            (SELECT p2.ingredient_name, min(p2.cholesterol) as min_choles
                            FROM Product as p2
                            GROUP BY p2.ingredient_name) as b ON b.ingredient_name = p1.ingredient_name
                            WHERE p1. cholesterol = b.min_choles""", [param])
        return cur.fetchall()


def searchProdMinFat(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT p1.ingredient_name, p1.brand_name, p1.calories, p1.total_fat, p1.saturated_fat,
                            p1.cholesterol, p1.sodium, p1.sugars, p1.protein
                            FROM (SELECT ingredient FROM Recipe_Ingredient WHERE recipe_id = %s) as a
                            JOIN Product as p1 ON a.ingredient = p1.ingredient_name
                            JOIN
                            (SELECT p2.ingredient_name, min(p2.total_fat) as min_fat
                            FROM Product as p2
                            GROUP BY p2.ingredient_name) as b ON b.ingredient_name = p1.ingredient_name
                            WHERE p1. total_fat= b.min_fat""", [param])
        return cur.fetchall()


# 5
def searchRecipeWithIngredient(recipeName, ingName, maxIng):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")

    filterName = ""
    filterIng = ""
    filterMaxIng = ""
    params = []

    if ingName != "":
        if recipeName == "":
            params.append(ingName)
            query = """SELECT b.ID, b.name, b.img
                FROM(
                SELECT recipe_id
                FROM Recipe_Ingredient
                WHERE ingredient = %s) as a
                JOIN
                Recipe as b
                ON b.ID = a.recipe_id
                JOIN
                Recipe_Ingredient as c
                ON c.recipe_id = a.recipe_id
                GROUP BY b.ID """
            query1 = """ORDER BY b.rating DESC"""

    if recipeName != "":
        params.append(recipeName)
        query = """SELECT a.ID, a.name, a.img
                FROM
                (SELECT DISTINCT Recipe.ID, Recipe.name, Recipe.img, Recipe.rating
                FROM Recipe
                WHERE MATCH (Recipe.name) AGAINST (%s IN BOOLEAN MODE)) as a
                LEFT join(
                SELECT recipe_id
                FROM Recipe_Ingredient """
        if ingName != "":
            params.append(ingName)
            query += "WHERE ingredient = %s"
        query += """) as b ON  a.ID = b.recipe_id
                JOIN Recipe_Ingredient as c ON c.recipe_id = b.recipe_id
                GROUP BY a.ID """
        query1 = """ORDER BY a.rating DESC"""

    if maxIng!="":
        params.append(maxIng)
        query += """HAVING count(DISTINCT c.ingredient) <= %s"""
        query = query + query1
	

    with con:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()


# 6
def searchByCuisine(cuisine, minCalories):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    params = [cuisine]
    query = """SELECT Recipe.ID, Recipe.name, Recipe.img
               FROM (SELECT Recipe_Cuisine.recipe_id FROM Recipe_Cuisine WHERE Recipe_Cuisine.cuisine = %s) as a
               JOIN Recipe ON a.recipe_id = Recipe.ID """

    if minCalories:
        params.append(cuisine)
        query += """WHERE Recipe.calories =(
               SELECT min(Recipe.calories) as min_calories
               FROM Recipe
               JOIN Recipe_Cuisine ON Recipe_Cuisine.recipe_id = Recipe.ID
               WHERE Recipe_Cuisine.cuisine = %s
               GROUP BY Recipe_Cuisine.cuisine
               ) """

    with con:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()


def searchByHoliday(holiday, minCalories):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    params = [holiday]
    query = """SELECT Recipe.ID, Recipe.name, Recipe.img
                   FROM (SELECT Recipe_Holiday.recipe_id FROM Recipe_Holiday WHERE Recipe_Holiday.holiday = %s) as a
                   JOIN Recipe ON a.recipe_id = Recipe.ID """

    if minCalories:
        params.append(holiday)
        query += """WHERE Recipe.calories =(
                   SELECT min(Recipe.calories) as min_calories
                   FROM Recipe
                   JOIN Recipe_Holiday ON Recipe_Holiday.recipe_id = Recipe.ID
                   WHERE Recipe_Holiday.holiday = %s
                   GROUP BY Recipe_Holiday.holiday
                   ) """

    with con:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()


def searchByCuisineHolidayMin(cuisine, holiday):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    params = [holiday, cuisine]
    query = """SELECT ID, name, img, calories
                FROM
                (
                SELECT a.holiday, b.cuisine, min(c.calories)  as min_cal
                FROM
                (
                SELECT Recipe_Holiday.recipe_id, Recipe_Holiday.holiday
                FROM Recipe_Holiday
                WHERE Recipe_Holiday.holiday = %s
                ) as a
                JOIN
                (
                SELECT Recipe_Cuisine.recipe_id, Recipe_Cuisine.cuisine
                FROM Recipe_Cuisine
                WHERE Recipe_Cuisine.cuisine = %s
                ) as b ON a.recipe_id = b.recipe_id
                JOIN Recipe as c ON c.ID = b.recipe_id
                ) as internal
                JOIN Recipe_Cuisine ON Recipe_Cuisine.cuisine = internal.cuisine
                JOIN Recipe_Holiday ON Recipe_Holiday.holiday = internal.holiday and Recipe_Holiday.recipe_id = Recipe_Cuisine.recipe_id
                JOIN Recipe ON Recipe.ID = Recipe_Holiday.recipe_id
                WHERE Recipe.calories = internal.min_cal"""
    with con:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()


def searchByCuisineHoliday(cuisine, holiday):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    params = [holiday, cuisine]
    query = """SELECT ID, name, img
            FROM((
            SELECT Recipe_Holiday.recipe_id
            FROM Recipe_Holiday
            WHERE Recipe_Holiday.holiday = %s
            ) as a
            JOIN
            (
            SELECT Recipe_Cuisine.recipe_id
            FROM Recipe_Cuisine
            WHERE Recipe_Cuisine.cuisine = %s
            ) as b ON a.recipe_id = b.recipe_id 
            JOIN Recipe as c ON c.ID = b.recipe_id)"""
    with con:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()


def searchRecipeHolidayCuisineMinCalories(cuisine, holiday, minCalories):
    if cuisine != "" and holiday == "": return searchByCuisine(cuisine, minCalories)
    if (cuisine == "" and holiday != ""): return searchByHoliday(holiday, minCalories)
    if (minCalories): return searchByCuisineHolidayMin(cuisine, holiday)
    return searchByCuisineHoliday(cuisine, holiday)


# 7
def searchHolidayMain(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT Recipe.ID, Recipe.name, Recipe.img
                    FROM Recipe_Ingredient
                    JOIN (SELECT Recipe_Holiday.recipe_id
                    FROM Recipe_Holiday
                    WHERE Recipe_Holiday.holiday = %s) as a ON  Recipe_Ingredient.recipe_id = a.recipe_id
                    JOIN (SELECT Ingredient_tags.ingredient_name
                    FROM Ingredient_tags
                    WHERE Ingredient_tags.VEGETARIAN = 0 ) as b ON Recipe_Ingredient.ingredient = b.ingredient_name
                    JOIN Recipe on Recipe.id = Recipe_Ingredient.recipe_id""", [param])
        return cur.fetchall()


def searchHolidayDessert(param):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15', use_unicode=True, charset="utf8")
    with con:
        cur = con.cursor()
        cur.execute("""SELECT Recipe.ID, Recipe.name, Recipe.img
                    FROM Recipe
                    JOIN (SELECT Recipe_Holiday.recipe_id
                    FROM Recipe_Holiday
                    WHERE Recipe_Holiday.holiday = %s
                    ) as a ON Recipe.ID=a.recipe_id
                    WHERE MATCH (Recipe.name) AGAINST ('cake cookie' IN BOOLEAN MODE) """, [param])
        return cur.fetchall()
