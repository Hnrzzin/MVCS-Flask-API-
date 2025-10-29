-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS banco_cantores;
USE banco_cantores;

-- Remover tabelas se já existirem [[5](https://cursos.alura.com.br/forum/topico-tabela-ou-dado-ja-existente-428179)]
DROP TABLE IF EXISTS Cantor;
DROP TABLE IF EXISTS FeatFamoso;
DROP TABLE IF EXISTS Gravadora;
DROP TABLE IF EXISTS Usuario;

-- Tabela Usuario (NOVA - para autenticação)
CREATE TABLE Usuario (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

-- Tabela Gravadora (com AUTO_INCREMENT)
CREATE TABLE Gravadora (
    idGravadora INT PRIMARY KEY AUTO_INCREMENT,
    nomeGravadora VARCHAR(50),
    localizacao VARCHAR(50)
);

-- Tabela FeatFamoso (com AUTO_INCREMENT)
CREATE TABLE FeatFamoso (
    idFeat INT PRIMARY KEY AUTO_INCREMENT,
    nomeFeat VARCHAR(50),
    cantorFeat VARCHAR(50),
    streams VARCHAR(50)
);

-- Tabela Cantor (com AUTO_INCREMENT)
CREATE TABLE Cantor (
    idCantor INT PRIMARY KEY AUTO_INCREMENT,
    nomeCantor VARCHAR(50),
    nacionalidade VARCHAR(50),
    idade VARCHAR(3),
    sexo VARCHAR(15),
    Gravadora_idGravadora INT,
    FeatFamoso_idFeat INT,
    FOREIGN KEY (Gravadora_idGravadora) REFERENCES Gravadora(idGravadora),
    FOREIGN KEY (FeatFamoso_idFeat) REFERENCES FeatFamoso(idFeat)
);

-- Inserts para Gravadora (SEM especificar ID)
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('Capitol Records', 'Los Angeles');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('Cactus Jack Records', 'Houston');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('XO Records', 'Los Angeles');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('30praum', 'Fortaleza');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('RCA Records', 'Nova Iorque');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('Universal Music Group', 'Holanda');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('SALVE CRAZY REC', 'São Paulo');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('88rising', 'Nova Iorque');
INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES ('Labbel Records', 'São Paulo');

-- Inserts para FeatFamoso (SEM especificar ID)
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Fantasy', 'Don Toliver', '89.5 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Bus Stop', 'Brent Faiyaz', '63 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Stargirl Interlude', 'Lana Del Rey', '1.4 bi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Conexões de Máfia', 'Rich the Kid', '190 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('30 for 30', 'Kendrick Lamar', '220 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('FE!N', 'Playboi Carti', '1.3 bi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Rich Flex', '21 Savage', '900 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Vandame', 'Derek', '20 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('I Don''t Wanna Live Forever', 'Taylor Swift', '1.9 bi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('I Like It', 'Cardi B', '1.8 bi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Afterthought', 'Benee', '202 mi');
INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES ('Normal', 'Veigh', '10 mi');

-- Inserts para Cantor (SEM especificar ID)
INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Kali Uchis', 'Americana', '30', 'Feminino', 1, 1);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Don Toliver', 'Americano', '30', 'Masculino', 2, 2);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('The Weeknd', 'Canadense', '35', 'Masculino', 3, 3);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Matuê', 'Brasileiro', '31', 'Masculino', 4, 4);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('SZA', 'Americana', '35', 'Feminino', 5, 5);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Travis Scott', 'Americano', '34', 'Masculino', 2, 6);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Drake', 'Canadense', '38', 'Masculino', 6, 7);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Ryu The Runner', 'Brasileiro', '20', 'Masculino', 7, 8);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Zayn Malik', 'Britânico', '32', 'Masculino', 5, 9);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Bad Bunny', 'Porto-riquenho', '31', 'Masculino', 6, 10);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Joji', 'Japonês', '32', 'Masculino', 8, 11);

INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) 
VALUES ('Yunk Vino', 'Brasileiro', '27', 'Masculino', 9, 12);

-- Configuração de autenticação
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Henry45*1';
FLUSH PRIVILEGES;