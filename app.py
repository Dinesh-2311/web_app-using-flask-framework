from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Sabiha@231101',  # Replace with your MySQL password
    'database': 'personal_data',
    'cursorclass': pymysql.cursors.DictCursor  # Return results as dictionaries
}

def get_db_connection():
    """Create and return a MySQL database connection."""
    return pymysql.connect(**db_config)

def create_table():
    """Create the 'persons' table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            telephone VARCHAR(15) NOT NULL,
            address VARCHAR(100) NOT NULL,
            age INT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Create the table when the application starts
create_table()

@app.route('/')
def index():
    """Render the homepage with the form and display all stored data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, surname, telephone, address, age FROM persons')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission and insert data into the database."""
    name = request.form['name']
    surname = request.form['surname']
    telephone = request.form['telephone']
    address = request.form['address']
    age = request.form['age']

    # Validate data
    errors = []
    if not name:
        errors.append("Name is required.")
    if not surname:
        errors.append("Surname is required.")
    if not telephone or not telephone.isdigit() or len(telephone) != 8:
        errors.append("Telephone must be 8 digits.")
    if not address:
        errors.append("Address is required.")
    if not age or not age.isdigit():
        errors.append("Age must be a number.")

    if not errors:
        # Insert data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO persons (name, surname, telephone, address, age)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, surname, telephone, address, age))
        conn.commit()
        cursor.close()
        conn.close()

    # Redirect to the homepage to display updated data
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)