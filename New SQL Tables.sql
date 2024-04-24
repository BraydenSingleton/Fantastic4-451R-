CREATE DATABASE bank_data;
USE bank_data;

CREATE TABLE user_info (
fName varchar(40),
lName varchar(40),
email varchar(40),
pword varchar(128),
a1 varchar(20),
a2 varchar(20),
a3 varchar(20)
);


CREATE TABLE user_transactions(
email VARCHAR(40),
category VARCHAR(20),
amount int(15),
date DATE 
);


