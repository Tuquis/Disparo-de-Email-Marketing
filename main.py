from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexão com o bd (banco de dados)
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="71208794",
        database="email_marketing"
    )

@app.route('/')
def home():
    return jsonify({"mensagem": "API funcionando! Use as rotas disponíveis."})

# Adicionar email (evita duplicados)
@app.route('/adicionar_email', methods=['POST'])
def adicionar_email():
    dados = request.json
    nome = dados.get("nome")
    sobrenome = dados.get("sobrenome")
    email = dados.get("email")

    db = conectar_bd()
    cursor = db.cursor()

    try:
        # Verifica se o email já existe
        cursor.execute("SELECT id FROM clientes WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"erro": "Email já cadastrado."}), 400
        
        cursor.execute("INSERT INTO clientes (nome, sobrenome, email) VALUES (%s, %s, %s)", 
                       (nome, sobrenome, email))
        db.commit()
        return jsonify({"mensagem": "Email adicionado com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        cursor.close()
        db.close()

# Listar emails
@app.route('/listar_emails', methods=['GET'])
def listar_emails():
    db = conectar_bd()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, sobrenome, email FROM clientes")
    emails = cursor.fetchall()
    cursor.close()
    db.close()

    return jsonify([{"id": e[0], "nome": e[1], "sobrenome": e[2], "email": e[3]} for e in emails])

# Atualizar email
@app.route('/atualizar_email/<int:id>', methods=['PUT'])
def atualizar_email(id):
    dados = request.json
    nome = dados.get("nome")
    sobrenome = dados.get("sobrenome")
    email = dados.get("email")

    db = conectar_bd()
    cursor = db.cursor()

    try:
        cursor.execute("UPDATE clientes SET nome = %s, sobrenome = %s, email = %s WHERE id = %s", 
                       (nome, sobrenome, email, id))
        db.commit()
        return jsonify({"mensagem": "Email atualizado com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        cursor.close()
        db.close()

# Remover email
@app.route('/remover_email/<int:id>', methods=['DELETE'])
def remover_email(id):
    db = conectar_bd()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
        db.commit()
        return jsonify({"mensagem": "Email removido com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
