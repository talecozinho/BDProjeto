import sqlite3
import hashlib
import random

# Connect to the database
connection = sqlite3.connect("vtt.db")
cursor = connection.cursor()

# Load the database schema
with open("vtt_sqlite_schema.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# INSERT
def create_user(password, email, username):
    try:
        # Verifica se email já existe
        cursor.execute("SELECT 1 FROM User WHERE email = ?", (email,))
        if cursor.fetchone():
            print("[ERRO] Este e-mail já está em uso. Por favor, use outro.")
            return False
        # Gera ID único e randômico
        id_user = random.randint(-10**10, 10**10)
        while True:
            cursor.execute("SELECT 1 FROM User WHERE idUser = ?", (id_user,))
            if not cursor.fetchone():
                break
            id_user = random.randint(-10**10, 10**10)
        # Insere usuário
        cursor.execute(
            "INSERT INTO User (idUser, password, email, username) VALUES (?, ?, ?, ?)",
            (id_user, hash_password(password), email, username)
        )
        connection.commit()
        print("[SUCESSO] Usuário criado com sucesso!")
        return True
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao criar usuário: {e}")
        return False

def create_gametable(gametablename, gm_userid):

    #Geração de um ID único e randômico
    id_gametable = random.randint(-10**10, 10**10)

    while True:
        cursor.execute("SELECT 1 FROM Gametable WHERE idGametable = ?", (id_gametable,))
        if not cursor.fetchone():
            break
        id_gametable = random.randint(-10**10, 10**10)

    #Insere Mesa
    cursor.execute(
        "INSERT INTO Gametable (idGametable, gametablename, gm_userid) VALUES (?, ?, ?)",
        (id_gametable, gametablename, gm_userid)
    )
    connection.commit()

# SELECT
def list_gametables(gm_userid):
    cursor.execute(
        "SELECT Gametable.idGametable, Gametable.gametablename, User.username FROM Gametable INNER JOIN User ON Gametable.gm_userid = User.idUser  WHERE Gametable.gm_userid = ?",
        (gm_userid,)
    )
    for data in cursor.fetchall():
        print(f"ID: {data[0]}\nNome: {data[1]}\nGM: {data[2]}\n")

def login(email, password):
    try:
        # Verifica credenciais comparando com o hash armazenado
        cursor.execute(
            "SELECT idUser, username FROM User WHERE email = ? AND password = ?",
            (email, hash_password(password))
        )
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"\n[SUCESSO] Login bem-sucedido! Bem-vindo, {resultado[1]}!")
            return resultado[0]  # Retorna idUser
        else:
            print("\n[ERRO] Email ou senha incorretos.")
            return None
    except sqlite3.Error as e:
        print(f"[ERRO] Falha no login: {e}")
        return None

# UPDATE
def update_user(id_user, email=None, username=None, password=None):
    updates = []
    params = []

    if email:
        updates.append("email = ?")
        params.append(email)
        
    if username:
        updates.append("username = ?")
        params.append(username)
        
    if password:
        updates.append("password = ?")
        params.append(hash_password(password))

    if updates:
        params.append(id_user)
        query = f"UPDATE User SET {', '.join(updates)} WHERE idUser  = ?"
        cursor.execute(query, params)
        connection.commit()
    else:
        print("No fields to update.")

# DELETE
def delete_gametable(gm_userid, id_gametable):
    cursor.execute("DELETE FROM Gametable WHERE gm_userid = ? AND idGametable = ?", (gm_userid, id_gametable))
    connection.commit()

def delete_user(id_user):
    cursor.execute("DELETE FROM User WHERE idUser  = ?", (id_user,))
    connection.commit()

# Main loop
while True:
    print("\n1 - Criar usuário\n2 - Login\n0 - Sair\n")
    opcao = input("Escolha: ")

    if opcao == "1":
        username = input("Nome de usuário: ")
        email = input("Email: ")
        password = input("Senha: ")
        create_user(password, email, username)

    elif opcao == "2":
        email = input("Email: ")
        senha = input("Senha: ")
        session = login(email, senha)
        if session:
            while True:
                print("1 - Criar Mesa\n2 - Ver minhas mesas\n3 - Atualizar meus dados\n4 - Deletar Mesa\n5 - Deletar Conta\n0 - Sair")
                opcao = input("Escolha: ")
                if opcao == "1":
                    gametablename = input("Nome da mesa: ")
                    create_gametable(gametablename, session)
                elif opcao == "2":
                    list_gametables(session)
                elif opcao == "3":
                    username = input("Novo nome de usuário (deixe em branco para não alterar): ")
                    email = input("Novo email (deixe em branco para não alterar): ")
                    password = input("Nova senha (deixe em branco para não alterar): ")
                    update_user(session, email if email else None, username if username else None, password if password else None)
                elif opcao == "4":
                    id_gametable = input("Gametable ID: ")
                    delete_gametable(session, id_gametable)
                elif opcao == "5":
                    delete_user(session)
                    break
                elif opcao == "0":
                    break

    elif opcao == "0":
        break

    else:
        print("Opção inválida.")

# Close the cursor and connection
cursor.close()
connection.close()
