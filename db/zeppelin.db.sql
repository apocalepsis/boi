CREATE DATABASE zeppelin;
USE zeppelin;

CREATE TABLE users (
    username TEXT,
    password TEXT,
    password_salt TEXT
);

CREATE TABLE user_roles (
    username TEXT,
    role_name TEXT
);

CREATE TABLE user_permissions(
    username TEXT,
    permission TEXT
);
