from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "chave_secreta"  # Necessário para usar sessão

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pythonteste939@gmail.com'
app.config['MAIL_PASSWORD'] = 'lyek bvqt veyq pvks'

mail = Mail(app)

def enviar_email(nome, filme, data, resposta):
    destinatario = "fernando.ct.prata@outlook.com"  # 📩 Seu e-mail
    assunto = "Confirmação de Filmes"

    corpo_email = f"""
    Olá Fernando,

    O usuário {nome} respondeu "{resposta}" para assistir:

    🎬 Filme: {filme}  
    📅 Data: {data}  

    Atenciosamente,  
    Seu Site de Escolha de Filmes
    """

    try:
        msg = Message(assunto, sender=app.config['MAIL_USERNAME'], recipients=[destinatario])
        msg.body = corpo_email
        mail.send(msg)
        print("📩 E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")


# Lista de filmes
filmes = [
    "O Homem do Saco", "Mufasa: O Rei Leão", "O Auto da Compadecida 2",
    "Sing Sing", "Chico Bento e a Goiabeira Maravilhosa", "Blindado",
    "Bridget Jones: Louca pelo Garoto", "Ainda Estou Aqui", "Acompanhante Perfeita",
    "Conclave", "Emilia Perez", "Capitão América: Admirável Novo Mundo"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        session["nome"] = nome
        return redirect(url_for("catalogo"))
    return render_template("index.html")

@app.route("/catalogo", methods=["GET", "POST"])
def catalogo():
    if request.method == "POST":
        session["filmes_escolhidos"] = request.form.getlist("filmes")
        return redirect(url_for("calendario"))  # Vai para o calendário após escolher os filmes
    return render_template("catalogo.html", filmes=filmes)

from datetime import datetime

@app.route("/calendario", methods=["GET", "POST"])
def calendario():
    if request.method == "POST":
        session["filmes_escolhidos"] = request.form.getlist("filmes")
        data_bruta = request.form.get("data")  # Pega a data do formulário

        # Formata a data para DD/MM/AAAA antes de salvar na sessão
        if data_bruta:
            data_formatada = datetime.strptime(data_bruta, "%Y-%m-%d").strftime("%d/%m/%Y")
            session["data_escolhida"] = data_formatada

        return redirect(url_for("confirmacao"))

    filmes_escolhidos = session.get("filmes_escolhidos", [])
    return render_template("calendario.html", filmes=filmes_escolhidos)

from datetime import datetime

@app.route("/confirmacao", methods=["GET", "POST"])
def confirmacao():
    if "filmes_escolhidos" not in session or len(session["filmes_escolhidos"]) == 0:
        return redirect(url_for("index"))  # Se não houver filmes, volta ao início

    filmes_escolhidos = session["filmes_escolhidos"]
    filme_atual = filmes_escolhidos[0]  # Pega o primeiro da lista
    data = session.get("data_escolhida", "Data não definida")

    # 🚀 Converte a data dentro da função para garantir o formato correto
    if data != "Data não definida":
        try:
            data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            pass  # Se a data já estiver no formato certo, não faz nada

    if request.method == "POST":
        resposta = request.form.get("resposta")

         # 📩 Agora o e-mail inclui a resposta do usuário
        enviar_email(session.get("nome", "Usuário"), [filme_atual], data, resposta)

        if resposta == "sim" or resposta == "nao":
            filmes_escolhidos.pop(0)  # Remove o filme confirmado

            # Se ainda houver filmes na lista, recarrega a página com o próximo
            if len(filmes_escolhidos) > 0:
                session["filmes_escolhidos"] = filmes_escolhidos
                return redirect(url_for("confirmacao"))

            # Se não houver mais filmes, finaliza e volta à página inicial
            session.pop("filmes_escolhidos")  # Remove da sessão
            return redirect(url_for("index"))

    return render_template("confirmacao.html", nome=session.get("nome", "Usuário"), filme=filme_atual, data=data)


if __name__ == "__main__":
    app.run(debug=True)

