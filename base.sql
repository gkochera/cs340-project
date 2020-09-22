DROP TABLE IF EXISTS diagnostic;
CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);
INSERT INTO diagnostic (text) VALUES ("MySQL is working");
SELECT * FROM diagnostic;