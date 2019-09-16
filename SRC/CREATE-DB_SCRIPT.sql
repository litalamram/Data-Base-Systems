CREATE TABLE Ingredient_tags (
	ingredient_name VARCHAR(100) NOT NULL,
	VEGAN TINYINT(4) NULL DEFAULT '0',
	VEGETARIAN TINYINT(4) NULL DEFAULT '0',
	PEANUT_FREE TINYINT(4) NULL DEFAULT '0',
	TREE_NUT_FREE TINYINT(4) NULL DEFAULT '0',
	ALCOHOL_FREE TINYINT(4) NULL DEFAULT '0',
	PRIMARY KEY (ingredient_name)
)
ENGINE=InnoDB
;

CREATE TABLE Product (
	ID VARCHAR(50) NOT NULL,
	product_name VARCHAR(100) NOT NULL,
	ingredient_name VARCHAR(50) NOT NULL,
	brand_name VARCHAR(50) NOT NULL,
	item_description TEXT NULL,
	water_grams FLOAT NULL DEFAULT NULL,
	calories FLOAT NULL DEFAULT NULL,
	total_fat FLOAT NULL DEFAULT NULL,
	saturated_fat FLOAT NULL DEFAULT NULL,
	trans_fatty_acid FLOAT NULL DEFAULT NULL,
	polyunsaturated_fat FLOAT NULL DEFAULT NULL,
	monounsaturated_fat FLOAT NULL DEFAULT NULL,
	cholesterol FLOAT NULL DEFAULT NULL,
	sodium FLOAT NULL DEFAULT NULL,
	total_carbohydrate FLOAT NULL DEFAULT NULL,
	dietary_fiber FLOAT NULL DEFAULT NULL,
	sugars FLOAT NULL DEFAULT NULL,
	protein FLOAT NULL DEFAULT NULL,
	vitamin_a_dv FLOAT NULL DEFAULT NULL,
	vitamin_c_dv FLOAT NULL DEFAULT NULL,
	calcium_dv FLOAT NULL DEFAULT NULL,
	iron_dv FLOAT NULL DEFAULT NULL,
	refuse_pct FLOAT NULL DEFAULT NULL,
	servings_per_container FLOAT NULL DEFAULT NULL,
	serving_size_qty FLOAT NULL DEFAULT NULL,
	serving_size_unit VARCHAR(50) NULL DEFAULT NULL,
	serving_weight_grams FLOAT NULL DEFAULT NULL,
	PRIMARY KEY (ID),
	INDEX ingredient_name (ingredient_name)
)
ENGINE=InnoDB
;

CREATE TABLE Recipe (
	ID VARCHAR(100) NOT NULL,
	name VARCHAR(100) NOT NULL,
	ingredients_list TEXT NOT NULL,
	time_needed FLOAT NULL DEFAULT NULL,
	rating INT(11) NOT NULL,
	number_serving INT(11) NOT NULL,
	url TINYTEXT NOT NULL,
	number_of_ingredients INT(11) NOT NULL,
	calories INT(11) NULL DEFAULT NULL,
	img TINYTEXT NULL,
	PRIMARY KEY (ID),
	FULLTEXT INDEX name (name)
)
ENGINE=InnoDB
;

CREATE TABLE Recipe_Cuisine (
	recipe_id VARCHAR(100) NOT NULL,
	cuisine VARCHAR(100) NOT NULL,
	PRIMARY KEY (recipe_id, cuisine),
	INDEX cuisine (cuisine),
	CONSTRAINT FK_Recipe_Cuisine_Recipe FOREIGN KEY (recipe_id) REFERENCES Recipe (id)
)
ENGINE=InnoDB
;

CREATE TABLE Recipe_Holiday (
	recipe_id VARCHAR(100) NOT NULL,
	holiday VARCHAR(50) NOT NULL,
	PRIMARY KEY (recipe_id, holiday),
	INDEX holiday (holiday),
	CONSTRAINT FK_Recipe_Holiday_Recipe FOREIGN KEY (recipe_id) REFERENCES Recipe (ID)
)
ENGINE=InnoDB
;

CREATE TABLE Recipe_Ingredient (
	recipe_id VARCHAR(100) NOT NULL,
	ingredient VARCHAR(100) NOT NULL,
	PRIMARY KEY (recipe_id, ingredient),
	INDEX recipe_id (recipe_id),
	INDEX ingredient (ingredient),
	CONSTRAINT FK_Part_of_recipe_Recipe FOREIGN KEY (recipe_id) REFERENCES Recipe (ID)
)
ENGINE=InnoDB
;
