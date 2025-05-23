CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name VARCHAR(255),
  age INTEGER,
  phone_number VARCHAR(20)
);


insert into users(name, age, phone_number) VALUES
('John', 21, '099999395');