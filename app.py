from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'chave_secreta_123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost: 5433/crud'

db = SQLAlchemy(app)
app.app_context().push()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(150))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

db.create_all()

@app.route('/')
def index():
    users = Users.query.all()
    return render_template('index.html', users=users)

@app.route('/insert', methods= ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        data = Users(name, email, phone)
        db.session.add(data)
        db.session.commit()

        flash('Usuário adicionado com sucesso')

        return redirect(url_for('index')) 
    
    

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Users.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash('Usuário atualizado com sucesso')
        return redirect(url_for('index')) 
   


@app.route('/delete/<id>/', methods= ['GET', 'POST'])
def delete(id):
        my_data = Users.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash('Usuário removido com sucesso')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)