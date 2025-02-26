import sqlite3

conn = sqlite3.connect("my_database.db")

cursor = conn.cursor()

#Consulta 1
cursor.executescript("""
    SELECT DISTINCT N.Nome AS Negociante
    FROM Venda V
    JOIN Veiculo L ON V.PK_Veiculo = L.PK_Veiculo
    JOIN Negociante N ON V.PK_Negociante = N.PK_Negociante
    WHERE L.Marca_fabricante = 'Mazda' AND L.Nome_modelo = 'Miata MX5';
""")

resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado[0])
print("----------------------------")

#Consulta 2
cursor.executescript("""
    SELECT L.Nome_modelo, C.cor, COUNT(*) AS Numero_de_vendas
    FROM Venda V
    JOIN Veiculo L ON V.PK_Veiculo = L.PK_Veiculo
    JOIN Cores Co ON L.ID_Cores = Co.ID_cores
    JOIN Cor C ON Co.ID_cor = C.pk_cor
    GROUP BY L.Nome_modelo, C.cor
    ORDER BY L.Nome_modelo, Numero_de_vendas DESC;
""")

resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado[0])
print("----------------------------")

#Consulta 4
cursor.executescript("""
    SELECT L.Marca_fabricante, L.Nome_modelo, L.Carroceria, V.Valor
    FROM Venda V
    JOIN Veiculo L ON V.PK_Veiculo = L.PK_Veiculo
    JOIN Negociante N ON V.PK_Negociante = N.PK_Negociante
    WHERE L.Carroceria = 'SUV' AND N.Nome = 'ABCMotors';
""")

resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado[0])
print("----------------------------")

#Consulta 7
cursor.executescript("""
    SELECT SUM(V.Valor) AS Total_Vendas
    FROM Venda V
    JOIN Veiculo L ON V.PK_Veiculo = L.PK_Veiculo
    WHERE L.Quilometragem < 100000 AND V.Status_da_venda = 1;
""")

resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado[0])
print("----------------------------")

conn.close