from facelock import app
from flask import render_template,redirect
from flask_login import current_user,login_required


@app.route("/")
@login_required
def index():
    nome = current_user.nome
    return render_template('index.html', nome=nome)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
