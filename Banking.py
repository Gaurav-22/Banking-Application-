from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create a database connection and table for account information
conn = sqlite3.connect('accounts.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS accounts 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT, 
              password TEXT, 
              balance REAL DEFAULT 0.0)''')
conn.commit()
conn.close()

# Route to the account registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the registration form data
        username = request.form['username']
        password = request.form['password']
        
        # Create a new account in the database
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        
        # Redirect to the login page
        return redirect('/login')
    else:
        # Display the registration form
        return render_template('register.html')

# Route to the account login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the login form data
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match an account in the database
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE username=? AND password=?', (username, password))
        account = c.fetchone()
        conn.close()
        
        if account:
            # Create a session for the logged-in user
            session['user_id'] = account[0]
            session['username'] = account[1]
            
            # Redirect to the account dashboard
            return redirect('/dashboard')
        else:
            # Display an error message
            flash('Invalid username or password')
            return redirect('/login')
    else:
        # Display the login form
        return render_template('login.html')

# Route to the account dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Get the account information from the database
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute('SELECT balance FROM accounts WHERE id=?', (session['user_id'],))
        balance = c.fetchone()[0]
        c.execute('SELECT * FROM transactions WHERE account_id=?', (session['user_id'],))
        transactions = c.fetchall()
        conn.close()
        
        # Display the account dashboard with the account information and transaction history
        return render_template('dashboard.html', username=session['username'], balance=balance, transactions=transactions)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect('/login')
        
if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run(debug=True)
