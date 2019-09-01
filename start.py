from flask import Flask, render_template, request, flash, url_for, redirect
import sqlite3

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        category_name = request.form['business'].replace(' ', '_')
        print('HI')
        return render_template('home.html', category_name=category_name)
    cate = []
    print('BYE')
    connection = sqlite3.connect('db/categories.db')
    cursor = connection.cursor()
    result = cursor.execute("Select * from categories")
    categories = cursor.fetchall()
    if result:
        for category in categories:
            cate.append(category[1])


    return render_template('home.html', cate=cate)

@app.route('/edit_category/<string:name>', methods=['GET', 'POST'])
def edit_category(name):
    if request.method == 'POST':
        cate_name = name.replace(' ', '_')
        paid = request.form['paid']
        connection = sqlite3.connect('db/{}.db'.format(cate_name))
        cursor = connection.cursor()
        _ = cursor.execute("Select * from {}".format(cate_name))
        category_details = cursor.fetchall()
        length = len(category_details)
        total_amnt = category_details[length-1][1]
        prev_balance = category_details[length-1][2]
        current_balance = int(prev_balance)-int(paid)
        cursor.execute("Insert into "+cate_name+"(total_amount, balance, paid) Values(?, ?, ?)",(total_amnt, current_balance, paid))
        connection.commit()
        return redirect(url_for('all_category'))
    return render_template('edit_category.html', name=name)
    
@app.route('/all_category')
def all_category():
    connection = sqlite3.connect('db/categories.db')
    cursor = connection.cursor()
    result = cursor.execute("Select * from categories")
    categories = cursor.fetchall()
    if result:
        return render_template('all_categories.html', category=categories)
    else:
        return render_template('all_categories.html', msg="No Data Found")

@app.route('/show_history/<string:name>')
def show_history(name):
    category_name = name.replace(' ', '_')
    connection = sqlite3.connect('db/{}.db'.format(category_name))
    cursor = connection.cursor()
    result = cursor.execute("Select * from {}".format(category_name))
    history = cursor.fetchall()
    if result:
        return render_template('category_history.html', history = history, category_name = name)
    else:
        return render_template('category_history.html', msg="No data to show")

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        total_amnt = request.form['total_amnt']
        ct_name = category_name.replace(' ', '_')
        connection = sqlite3.connect('db/'+ct_name+'.db')
        cursor = connection.cursor()
        try:
            sql = """Create table {} (id INTEGER PRIMARY KEY AUTOINCREMENT, total_amount INTEGER, 
            balance INTEGER, paid INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)""".format(ct_name)
            cursor.execute(sql)
            connection.commit()
            conn = sqlite3.connect('db/categories.db')
            cur = conn.cursor()
            cur.execute("Insert into categories(category_name, total_amount) Values(?, ?)",(category_name, total_amnt))
            conn.commit()
            cur.close()
            cursor.execute("Insert into "+ct_name+"(total_amount, balance, paid) Values(?, ?, ?)",(total_amnt, total_amnt, 0))
            connection.commit()
            flash("DB created successfully", 'success')
        except Exception as e:
            print(e)
        return redirect(url_for('all_category'))
    return render_template('add_category.html')

@app.route('/delete_category/<string:name>', methods=['GET', 'POST'])
def delete_category(name):
    connection = sqlite3.connect('db/categories.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM categories WHERE category_name=?',(name.replace(' ','_'),))
    connection.commit()
    flash('Category Deleted', 'success')
    return redirect(url_for('all_category'))

if __name__ == "__main__":
    app.secret_key='secret123'
    app.run(debug=True)