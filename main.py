from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import json
import os
from num2words import num2words


app = Flask(__name__)
app.secret_key = "lkjghdfou;;'A'Fqpe7050&*%"  

login_manager = LoginManager()
login_manager.init_app(app)


DATA_FOLDER = os.getcwd()

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    # Load user from the database
    return User(user_id)


users = {
    os.environ.get('USER1'): {
        'password': os.environ.get('PASSWORD1')
        },
    os.environ.get('USER2'): {
        'password': os.environ.get('PASSWORD2')
    },
    "user3": {
        'password': "password3"
    }
}

# Load data from JSON file
def load_data():
    try:
        with open(os.path.join(DATA_FOLDER, 'funds.json'), 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


# Save data to JSON file
def save_data(data):
    with open(os.path.join(DATA_FOLDER, 'funds.json'), 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and password == users[username]['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))

        return 'Invalid username or password'

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/add_fund', methods=['POST'])
@login_required
def add_fund():
    # Extract fund details from the request form
    name = request.form['name']
    date = request.form['date']
    contact_number = request.form['contact_number']
    amount_words = num2words(float(request.form['amount_number']))
    amount_number = request.form['amount_number']

    if not name or not date or not contact_number or not amount_words or not amount_number:
        return jsonify({'error': 'Please enter all fund details.'})

    # Load existing data
    data = load_data()

    # Check if the donor is already present
    duplicate_fund = next((fund for fund in data.get("Funds", []) if fund['Name'] == name), None)

    if duplicate_fund:
        # Update the amount for duplicate donor
        existing_amount_number = float(duplicate_fund['AmountNumber'])
        new_amount_number = existing_amount_number + float(amount_number)
        duplicate_fund['AmountNumber'] = str(new_amount_number)

        existing_amount_words = duplicate_fund['AmountWords']
        new_amount_words = num2words(new_amount_number)
        duplicate_fund['AmountWords'] = new_amount_words
    else:
        # Create a new fund object
        new_fund = {
            "Name": name,
            "Date": date,
            "ContactNumber": contact_number,
            "AmountWords": amount_words,
            "AmountNumber": amount_number,
        }

        # Add the new fund to the existing data
        data.setdefault("Funds", []).append(new_fund)

    # Save the updated data
    save_data(data)

    # return a html popup
    return(render_template('index.html'))


@app.route('/remove_donors', methods=['POST'])
@login_required
def remove_donors():
    # Extract donor name from the request form
    donor_name = request.form['donor_name']

    # Load existing data
    data = load_data()

    # Remove the donor from the existing data
    updated_funds = [fund for fund in data.get("Funds", []) if fund['Name'] != donor_name]
    data["Funds"] = updated_funds

    # Save the updated data
    save_data(data)

    return(render_template('display_donors.html'))


@app.route('/display_donors')
@login_required
def display_donors():
    # Load data
    data = load_data()
    funds = data.get("Funds", [])
    return render_template('display_donors.html', funds=funds)

if __name__ == '__main__':
    app.run()