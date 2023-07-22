from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Cambiar esto con la dirección de tu servidor MySQL
app.config['MYSQL_USER'] = 'mizzu'  # Cambiar esto con tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = '1234'  # Cambiar esto con tu contraseña de MySQL
app.config['MYSQL_DB'] = 'myflaskdb'  # Cambiar esto con el nombre de la base de datos creada


mysql = MySQL(app)

# Crear la tabla de usuarios en la base de datos
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