import sqlite3

conn = sqlite3.connect("my_database.db")

cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE Cor (
    pk_cor INTEGER PRIMARY KEY,
    cor VARCHAR(20) NOT NULL
);

CREATE TABLE Cores (
    ID_cores INTEGER PRIMARY KEY,
    ID_cor INTEGER NOT NULL,
    FOREIGN KEY (ID_cor) REFERENCES Cor (pk_cor)
);

CREATE TABLE Veiculo (
    PK_Veiculo INTEGER PRIMARY KEY,
    Marca_fabricante VARCHAR(20) NOT NULL,
    Nome_modelo VARCHAR(30) NOT NULL,
    Carroceria VARCHAR(20) NOT NULL,
    Quilometragem INTEGER NOT NULL,
    ID_Cores INTEGER NOT NULL,
    FOREIGN KEY (ID_Cores) REFERENCES Cores (ID_cores)
);

CREATE TABLE Localizacao (
    PK_Localizacao INTEGER PRIMARY KEY,
    Estado VARCHAR(20) NOT NULL,
    Cidade VARCHAR(30) NOT NULL,
    Rua VARCHAR(30) NOT NULL,
    Numero INTEGER NOT NULL
);

CREATE TABLE Negociante (
    PK_Negociante INTEGER PRIMARY KEY,
    Nome VARCHAR(40) NOT NULL,
    FK_Localizacao INTEGER NOT NULL,
    Buy_from_home BOOLEAN NOT NULL,
    FOREIGN KEY (FK_Localizacao) REFERENCES Localizacao (PK_Localizacao)
);

CREATE TABLE Venda (
    PK_Veiculo INTEGER NOT NULL,
    PK_Localizacao INTEGER NOT NULL,
    PK_Negociante INTEGER NOT NULL,
    Status_da_venda BOOLEAN NOT NULL,
    Valor INTEGER NOT NULL,
    PRIMARY KEY (PK_Veiculo, PK_Localizacao, PK_Negociante),
    FOREIGN KEY (PK_Veiculo) REFERENCES Veiculo (PK_Veiculo),
    FOREIGN KEY (PK_Localizacao) REFERENCES Localizacao (PK_Localizacao),
    FOREIGN KEY (PK_Negociante) REFERENCES Negociante (PK_Negociante)
);
""")

#cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)

conn.commit()
conn.close()