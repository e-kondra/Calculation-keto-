PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS category;
CREATE TABLE category(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (64)
);

INSERT INTO category (id, name) VALUES (1, 'мясо и субпродукты');
INSERT INTO category (id, name) VALUES (2, 'молочные продукты');
INSERT INTO category (id, name) VALUES (3, 'рыба и морепродукты');

DROP TABLE IF EXISTS product;
CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL,
    name VARCHAR (128) NOT NULL,
    is_active INTEGER DEFAULT 1,
    kkal INTEGER NOT NULL,
    water INTEGER,
    proteins REAL NOT NULL,
    fats REAL NOT NULL,
    carbs REAL NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

INSERT INTO product (id, category_id, is_active, name, kkal, water, proteins, fats, carbs)
VALUES (1, 2, 1, 'сыр Чеддер', 404, 0, 22.9, 33.31, 3.1);
INSERT INTO product (id, category_id, is_active, name, kkal, water, proteins, fats, carbs)
VALUES (2, 1, 1, 'говяжья печень', 134, 0, 21.39, 1.23, 0);
INSERT INTO product (id, category_id, is_active, name, kkal, water, proteins, fats, carbs)
VALUES (3, 1, 1, 'свиная печень', 134, 0, 21.34, 3.7, 0);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;