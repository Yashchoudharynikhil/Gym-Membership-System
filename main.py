from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rajaram@123",
    database="membership_db"
)

cursor = db.cursor()

# 🏠 HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# ➕ ADD MEMBER
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        plan = request.form['plan']
        expiry = request.form['expiry']

        cursor.execute(
            "INSERT INTO members (name, plan, expiry_date) VALUES (%s, %s, %s)",
            (name, plan, expiry)
        )
        db.commit()

        return redirect('/members')

    return render_template('add.html')


# 📋 VIEW MEMBERS
@app.route('/members')
def members():
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()
    return render_template('members.html', members=data)


# 🗑 DELETE
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM members WHERE id=%s", (id,))
    db.commit()
    return redirect('/members')


# ✏️ EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        plan = request.form['plan']
        expiry = request.form['expiry']

        cursor.execute(
            "UPDATE members SET name=%s, plan=%s, expiry_date=%s WHERE id=%s",
            (name, plan, expiry, id)
        )
        db.commit()
        return redirect('/members')

    cursor.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cursor.fetchone()
    return render_template('edit.html', member=member)


if __name__ == '__main__':
    app.run(debug=True)