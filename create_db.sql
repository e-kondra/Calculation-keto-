PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS category;
CREATE TABLE category(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (64)
);
INSERT INTO category (id, name) VALUES (1, 'мясо');
INSERT INTO category (id, name) VALUES (2, 'субпродукты');
INSERT INTO category (id, name) VALUES (3, 'молочные продукты');
INSERT INTO category (id, name) VALUES (4, 'рыба и морепродукты');

DROP TABLE IF EXISTS product;
CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL,
    name VARCHAR (128) NOT NULL UNIQUE,
    is_active INTEGER DEFAULT 1,
    kkal INTEGER NOT NULL,
    water INTEGER,
    ash REAL,
    proteins REAL,
    tryptophan REAL,
    threonine REAL,
    isoleucine REAL,
    leucine REAL,
    lysine REAL,
    methionine REAL,
    cystine REAL,
    phenylalanine REAL,
    tyrosine REAL,
    valine REAL,
    arginine REAL,
    histidine REAL,
    alanine REAL,
    aspartic REAL,
    glutamic REAL,
    glycine REAL,
    proline REAL,
    serine REAL,
    fats REAL NOT NULL,
    saturated REAL,
    butyric REAL,
    caproic REAL,
    caprylic REAL,
    capric REAL,
    lauric REAL,
    myristic REAL,
    palmitic REAL,
    stearic REAL,
    arachinoic REAL,
    behenic REAL,
    lignoceric REAL,
    monounsaturated REAL,
    palmitoleic REAL,
    oleic REAL,
    gadolin REAL,
    erucic REAL,
    nervonic REAL,
    polyunsaturated REAL,
    linoleic REAL,
    linolenic REAL,
    alpha_linolenic REAL,
    gamma_linolenic REAL,
    eicosadiene REAL,
    arachidonic REAL,
    eicosapentaenoic REAL,
    docosapentaenoic REAL,
    sterol REAL,
    cholesterol REAL,
    phytosterols REAL,
    stigmasterol REAL,
    campesterol REAL,
    beta_sitosterol REAL,
    trans REAL,
    mono_trans REAL,
    poly_trans REAL,
    carbs REAL NOT NULL,
    glucose REAL,
    fructose REAL,
    galactose REAL,
    sucrose REAL,
    lactose REAL,
    maltose REAL,
    sum_sugar REAL,
    fiber REAL,
    starch REAL,
    vitA REAL,
    beta_carotene REAL,
    alpha_carotene REAL,
    vitD REAL,
    vitD2 REAL,
    vitD3 REAL,
    vitE REAL,
    vitC REAL,
    vitB1 REAL,
    vitB2 REAL,
    vitB3 REAL,
    vitB4 REAL,
    vitB5 REAL,
    vitB6 REAL,
    vitB9 REAL,
    vitB12 REAL,
    Ca REAL,
    Fe REAL,
    Mg REAL,
    Phos REAL,
    Kalis REAL,
    Na REAL,
    Zn REAL,
    Cu REAL,
    Mn REAL,
    Se REAL,
    Fluor REAL,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

INSERT INTO product (id, category_id, is_active, name, kkal, water, proteins, fats, carbs)
VALUES (1, 3, 1, 'сыр Чеддер', 404, 0, 22.9, 33.31, 3.1);
INSERT INTO product (id, category_id, is_active, name, kkal, water, proteins, fats, carbs)
VALUES (2, 2, 1, 'говяжья печень', 134, 0, 21.39, 1.23, 0);
INSERT INTO product (id, category_id, is_active, name, kkal, water, proteins, fats, carbs)
VALUES (3, 2, 1, 'свиная печень', 134, 0, 21.34, 3.7, 0);

--
DROP TABLE IF EXISTS user;
CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (64) UNIQUE ,
    password VARCHAR (256),
    isadmin INTEGER DEFAULT 0
);

INSERT INTO user (id, name, password, isadmin) VALUES (1, 'admin', 'd7c5ec9572423b16c3d142d2b703b524f66e4d7d24e443bb7486837ab23d88db', 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;