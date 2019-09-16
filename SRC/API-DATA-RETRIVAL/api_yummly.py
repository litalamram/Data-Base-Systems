# -*- coding: utf-8 -*-

import urllib, urllib2
import json
import MySQLdb as mdb
import os

SO_API_URL = "http://api.yummly.com/v1/api/"
# store API access key
cykey = '798ce71b'
app_key = 'bd5497426b5219277898b25c273700cd'

maxRes = 250


# query yummly api for recipes info
def get_res_json(start=0):
    try:
        params = urllib.urlencode(
            {"_app_id": cykey, "_app_key": app_key, "start": str(start), "maxResult": str(maxRes)})
        url = SO_API_URL + "recipes?" + params
    except Exception as e:
        print("failed encoding")
        print(str(e))
        return

    res = urllib2.urlopen(url).read();
    return json.loads(res)


# query yummly api for specific recipe
def get_recipe(id):
    try:
        params = urllib.urlencode({"_app_id": cykey, "_app_key": app_key})
        url = SO_API_URL + "recipe/" + id + "?" + params
    except Exception as e:
        print("failed encoding")
        print(str(e))
        return

    res = urllib2.urlopen(url).read();
    return json.loads(res)


# query the api for to get 10,000 recipes and save the results to files
def query_api():
    start = 0
    total = 10000 / maxRes + 1
    
    for i in range(total):
        res_full = []
        js = get_res_json(start)
        json.dump(js["matches"], open("data/recipes" + str(start) + ".p", "wb"))

        for r in js["matches"]:
            recipe = get_recipe(r["id"])
            res_full.extend([recipe])
        json.dump(res_full, open("data/recipes_full" + str(start) + ".p", "wb"))
        start += maxRes


# populate DB with recipes records
def populate_db():
    num = 0
    total = 10000 / maxRes + 1
    for i in range(total):
        f = open(r'/specific/scratch/litalamram1/django/data/recipes_full' + str(num) + '.p', "rb")
        l = json.load(f)
        for data in l:
            insert_recipe(data)
        num += maxRes

    num = 0
    for i in range(41):
        f = open(os.getcwd() + r'/data/recipes' + str(num) + '.p', "rb")
        l = json.load(f)
        for data in l:
            insert_ingredients(data)
        num += maxRes


def insert_recipe(arr):
    # connect to db
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15')
    cur = con.cursor()
    con.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    try:
        calories = None
        for nut in arr["nutritionEstimates"]:
            if nut['attribute'] == "ENERC_KCAL":
                calories = nut["value"]

        # insert to Recipe
        cur.execute("INSERT INTO Recipe (ID, name, ingredients_list, time_needed, rating, number_serving, url, "
                    "number_of_ingredients, calories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (arr["id"], arr["name"], ",".join(i for i in arr["ingredientLines"]), arr["totalTimeInSeconds"],
                     arr["rating"], arr["numberOfServings"], arr["source"]["sourceRecipeUrl"],
                     str(len(arr["ingredientLines"])), calories))

        # insert to Recipe_Holiday
        holidays = arr['attributes'].get('holiday', None)
        if holidays is not None:
            for holiday in holidays:
                cur.execute("INSERT INTO Recipe_Holiday (recipe_id, holiday) VALUES (%s, %s)", (arr["id"], holiday))

        # insert to Recipe_Cuisine
        cuisines = arr['attributes'].get('cuisine', None)
        if cuisines is not None:
            for cuisine in cuisines:
                cur.execute("INSERT INTO Recipe_Cuisine (recipe_id, cuisine) VALUES (%s, %s)", (arr["id"], cuisine))

        con.commit()
        con.close()
    except Exception as e:
        print(str(e))
        con.rollback()
        con.close()


def insert_ingredients(arr):
    # connect to db
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15')
    cur = con.cursor()
    con.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    try:
        # insert to Recipe_Ingredient
        for i in arr["ingredients"]:
            cur.execute("INSERT INTO Recipe_Ingredient (Recipe_ID, Ingredient) VALUES(%s, %s)", (arr["id"], i))
        con.commit()
        con.close()
    except Exception as e:
        print(str(e))
        con.rollback()
        con.close()


if __name__ == "__main__":
    query_api()
    populate_db()
