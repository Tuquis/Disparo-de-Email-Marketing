CREATE DATABASE base_email_marketing;
USE base_email_marketing;
 
CREATE TABLE clientes (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR (100),
    sobrenome VARCHAR (100),
    email VARCHAR (255) UNIQUE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);