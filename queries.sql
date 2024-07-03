CREATE DATABASE ruskiy;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id INT NOT NULL,
    username VARCHAR(255),
    isPrime BOOLEAN
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255) NOT NULL,
    translated_word VARCHAR(255) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);