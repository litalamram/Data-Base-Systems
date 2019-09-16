# -*- coding: utf-8 -*-

import urllib, urllib2
import json
import MySQLdb as mdb
import os

SO_API_URL = "https://api.nutritionix.com/v1_1/search/"
# store API access key
app_id = '3d68d67a'
app_key = '1f6aac11dd01590a554af663ff64df10'

maxRes = 250


# query nutritionix api for products info
def get_res_json(range, phrase):
    try:
        params = urllib.urlencode({"appId": app_id, "appKey": app_key, "results": str(range), "fields": "*"})
        phrase = str.replace(phrase, '/', '')
        phrase = str.replace(phrase, '%', '')
        phrase = str.replace(phrase, ' ', '%20')
        url = SO_API_URL + phrase + "?" + params
    except Exception as e:
        print("failed encoding")
        print(str(e))
        return

    res = urllib2.urlopen(url).read()
    return json.loads(res)


def insert_product(arr, ing_name):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15')
    cur = con.cursor()
    con.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    try:
        cur.execute(
            "INSERT INTO Product (ID, product_name, ingredient_name, brand_name, item_description, water_grams, "
            "calories, total_fat, saturated_fat, trans_fatty_acid, polyunsaturated_fat, monounsaturated_fat, "
            "cholesterol, sodium, total_carbohydrate, dietary_fiber, sugars, protein, vitamin_a_dv, vitamin_c_dv, "
            "calcium_dv, iron_dv, refuse_pct, servings_per_container, serving_size_qty, serving_size_unit, "
            "serving_weight_grams) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (arr["item_id"], arr["item_name"], ing_name, arr["brand_name"], arr["item_description"],
             arr["nf_water_grams"], arr["nf_calories"], arr["nf_total_fat"], arr["nf_saturated_fat"],
             arr["nf_trans_fatty_acid"], arr["nf_polyunsaturated_fat"], arr["nf_monounsaturated_fat"],
             arr["nf_cholesterol"], arr["nf_sodium"], arr["nf_total_carbohydrate"], arr["nf_dietary_fiber"],
             arr["nf_sugars"], arr["nf_protein"], arr["nf_vitamin_a_dv"], arr["nf_vitamin_c_dv"], arr["nf_calcium_dv"],
             arr["nf_iron_dv"], arr["nf_refuse_pct"], arr["nf_servings_per_container"], arr["nf_serving_size_qty"],
             arr["nf_serving_size_unit"], arr["nf_serving_weight_grams"]))
        con.commit()
        con.close()
    except Exception as e:
        print(str(e))
        con.rollback()
        con.close()


def get_all_ingredients():
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15')
    cur = con.cursor()
    con.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    cur.execute("SELECT DISTINCT Ingredient FROM Recipe_Ingredient")
    ingredients = cur.fetchall()
    con.close()
    return ingredients


def populate_db():
    ingredients = get_all_ingredients()
    print("Amount of ingredients: " + str(len(ingredients)))
    i = 0
    for ingredient in ingredients:
        ingredient = ingredient[0]  # it's a tuple
        i += 1
        js = get_res_json("1:50", ingredient)
        for prod in js["hits"]:
            insert_product(prod["fields"], ingredient)
        json.dump(js["hits"], open("data/products_" + str(ingredient) + ".json", "wb"))

    print("finished")


if __name__ == "__main__":
    populate_db()
