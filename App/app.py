from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'Reisita' 
app.config['MYSQL_PASSWORD'] = '1234'  
app.config['MYSQL_DB'] = 'database'  

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   nombre VARCHAR(100) NOT NULL,
                   password VARCHAR(100) NOT NULL
            )
                   ''')
    mysql.connection.commit()
    cur.close()

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            edad INT
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.route('/')
def administrador():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM admin')
    admin = cur.fetchall()
    cur.close()
    return render_template('sesion.html', admin=admin)
def validar():
    if request.method == 'GET':
        usuario = request.form['admin']
        password = request.form['pase_admin']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE nombre = %s AND password = %s', (usuario, password))
        cur.fetchall()
        cur.close()
        return redirect(url_for('index')) 
    return render_template('sesion.html')
    
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    cur.close()
    return render_template('index.html', usuarios=usuarios)

    
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        edad = request.form['edad']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (nombre, email, edad) VALUES (%s, %s, %s)', (nombre, email, edad))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        edad = request.form['edad']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuarios SET nombre = %s, email = %s, edad = %s WHERE id = %s', (nombre, email, edad, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = %s', (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)