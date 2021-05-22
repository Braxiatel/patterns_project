
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32) UNIQUE, email VARCHAR (32));

DROP TABLE IF EXISTS category;
CREATE TABLE category (category_id INTEGER PRIMARY KEY NOT NULL UNIQUE, category VARCHAR (32), name VARCHAR (32) UNIQUE, courses VARCHAR (128));

DROP TABLE IF EXISTS course;
CREATE TABLE course (course_id INTEGER PRIMARY KEY NOT NULL UNIQUE, name VARCHAR (32) UNIQUE, category INTEGER REFERENCES category(category_id), location VARCHAR (32), start_date VARCHAR (32));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
