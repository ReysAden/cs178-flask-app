# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
# it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')
# Displaying Items in the inventory
@app.route('/display-inventory-items')
def display_users():
    # load inventory from database
    try:
        inventory_list = execute_query('SELECT * FROM Inventory')
    except Exception as e:
        flash(f'Error loading inventory: {e}', 'danger')
        inventory_list = []

    return render_template('display_inventory.html', users=inventory_list)

# Adding an item to the inventory
@app.route('/add-inventory-item', methods=['GET', 'POST'])
def add_inventory_item():
    if request.method == 'POST':
        # grab form data from the request
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['categoryID']
        try:
            # insert new item into the database
            execute_insert('INSERT INTO Inventory (description, price, categoryID) VALUES (%s, %s, %s)',
                           (description, price, category_id))
            flash('Item added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding item: {e}', 'danger')
        return redirect(url_for('home'))
    # load the add inventory form
    return render_template('add_inventory_item.html')

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)