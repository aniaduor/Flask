from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '852085208520'  # Change this to a secure secret key in production

# Mock user data (replace this with your actual user management system)
users = {
   '7ufw03zoo1l333g': {
        'username': 'Wattnow',
        'password': 'Wattnow123.',
        'id': '7ufw03zoo1l333g'
   }
}

@app.route('/')
@app.route('/home')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user_id'] = users[email]['id']
            return redirect(url_for('upload'))  # Redirect to upload page
        else:
            return 'Invalid email or password'
    return render_template('login.html')

@app.route('/upload')
def upload():
    if 'user_id' in session:
        # Fetch user data using the user_id if needed
        return render_template('upload.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
