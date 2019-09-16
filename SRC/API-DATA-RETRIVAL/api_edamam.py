# -*- coding: utf-8 -*-

import urllib, urllib2
import json
import MySQLdb as mdb
import os

SO_API_URL = "https://api.edamam.com/api/nutrition-data"
# store API access key
app_id = '5a3cd645'
app_key = '024394cec4370e3b855879b4c4a63faa'


# create wrapper function
def get_res_json(phrase):
    try:
        params = urllib.urlencode({"app_key": app_key, "app_id": app_id, "ingr": phrase})
        url = SO_API_URL + "?" + params
    except Exception as e:
        print("failed encoding")
        print(str(e))
        return
    print(url)

    res = urllib2.urlopen(url).read()
    return json.loads(res)


def insert_ingredient_tags(healthLabels, ing_name):
    con = mdb.connect('mysqlsrv1.cs.tau.ac.il', 'DbMysql15', 'DbMysql15', 'DbMysql15')
    cur = con.cursor()
    con.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    tags_dict = {"VEGAN": 0, "VEGETARIAN": 1, "PEANUT_FREE": 2, "TREE_NUT_FREE": 3, "ALCOHOL_FREE": 4, "DAIRY_FREE": 5,
                 "LOW_SUGER": 6, "LOW_FAT_ABS": 7, "SUGER_CONSCIOUS": 8, "FAT_FREE": 9, "GLUTEN_FREE": 10,
                 "WHEAT_FREE": 11}
    tags_lst = [0 for i in range(12)]
    for tag in healthLabels:
        if tag in tags_dict:
            tags_lst[tags_dict[tag]] = 1
        else:
            print(tag + "not in dict")
    tags_lst.append(ing_name)

    try:
        sql = "INSERT INTO Ingredient_tags (VEGAN, VEGETARIAN, PEANUT_FREE, TREE_NUT_FREE, ALCOHOL_FREE, DAIRY_FREE, " \
              "LOW_SUGER, LOW_FAT_ABS, SUGER_CONSCIOUS, FAT_FREE, GLUTEN_FREE, WHEAT_FREE, ingredient_name) VALUES (" \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        cur.execute(sql, tags_lst)
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
        js = get_res_json(ingredient)

        insert_ingredient_tags(js["healthLabels"], ingredient)
        print(i)
        json.dump(js, open("data/products_" + str(ingredient) + ".json", "wb"))

    print("finished " + i)


if __name__ == "__main__":
    populate_db()

