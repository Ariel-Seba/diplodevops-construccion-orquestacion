from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    msg = '¡Hola gente! Soy una app simple y esta es mi ruta raiz.\n'
    print(msg)
    return msg

@app.route('/de')
def helloDe():
    msg = 'Hallo Leute!. Ich bin eine einfache App und das ist meine Route auf Deutsch.\n'
    print(msg)
    return msg

@app.route('/it')
def helloIt():
    msg = 'Ciao a tutti!. Sono una semplice app e questo è il mio percorso in italiano.\n'
    print(msg)
    return msg

@app.route('/en')
def helloEn():
    msg = os.environ.get("ENG_MSG")
    print(msg)
    return msg

@app.route('/secret')
def secret():
    secretsPath = os.environ.get("SECRETS_PATH", "/run/secrets/SECRET_MSG")
    f = open(secretsPath, "r")
    msg=f.read()
    print(f.read()) 
    return msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)