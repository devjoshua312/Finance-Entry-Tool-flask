from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import json
import os
from num2words import num2words
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

LoginManager.session_protection = "strong"


# find out where users.json and funds.json files are located
# and set the DATA_FOLDER variable to that location
DATA_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', 'data')


app = Flask(__name__)
app.secret_key = f"{os.environ.get('SECRET_KEY')}"

login_manager = LoginManager()
login_manager.init_app(app)

DATA_FOLDER = os.getcwd()

uri = os.environ.get("mongo_uri")

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


users = {
    os.environ.get('USER1'): {
        'password': os.environ.get('PASSWORD1')
    },
    os.environ.get('USER2'): {
        'password': os.environ.get('PASSWORD2')
    },
    os.environ.get('DEV'): {
        'password': os.environ.get('DEV_PASSWORD')
    },
    os.environ.get('ADMIN1'): {
        'password': os.environ.get('ADMIN1_PASSWORD')
    },
    os.environ.get('ADMIN2'): {
        'password': os.environ.get('ADMIN2_PASSWORD')
    },
    "dev": {
        'password':  "dev"
    }
}


print(os.environ.get('USER1'))
print(os.environ.get('PASSWORD1'))


def load_data():
    try:
        with open(os.path.join(DATA_FOLDER, 'funds.json'), 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


def save_data(data):
    try:
        with open(os.path.join(DATA_FOLDER, 'funds.json'), 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
            return({})

@app.route('/')
def home():
    return render_template('index.html')

@login_required
@app.route('/debug')
def debug():
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        return render_template("debug.html", message="Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        return render_template('debug.html', message=e)
    finally:
        return render_template('debug.html', message=f"Travelled far and wide, but i could not achieve this task. Your mongo uri is {uri}")

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


@app.route('/download_receipt/<donor_name>', methods=['GET'])
@login_required
def download_receipt(donor_name):
    try:
        for filename in os.listdir('receipts'):
            if current_user.id != 'dev':
                return send_file('receipts\\511.txt', as_attachment=True)
            elif current_user.id == 'dev' and filename.__contains__(donor_name):
                    return send_file(f'receipts/{filename}', as_attachment=True)
            else:
                return "No receipt found"
    except Exception as e:
        return(f"Error. Either the reciepts cannot be found or the folder could not be accessed. {e}")

@app.route('/add_fund', methods=['POST'])
@login_required
def add_fund():
    try:
        
    # Retrieve form data
        name = request.form['name']
        date = request.form['date']
        contact_number = request.form['contact_number']
        amount_words = num2words(
              float(request.form['amount_number']), lang='en_IN')
        amount_number = request.form['amount_number']
        address = request.form['address']
        try:
            if request.files != None:
                receipt = request.files['receipt']
                receipt.save(f'receipts/{name.strip()}')
            else:
                pass
        except:
            pass

        if not name or not date or not contact_number or not amount_words or not amount_number:
             return jsonify({'error': 'Please enter all fund details.'})

        data = load_data()

        duplicate_fund = next((fund for fund in data.get(
             "Funds", []) if fund['Name'] == name), None)

        if duplicate_fund:
             existing_amount_number = float(duplicate_fund['AmountNumber'])
             new_amount_number = existing_amount_number + float(amount_number)
             duplicate_fund['AmountNumber'] = str(new_amount_number)

             new_amount_words = num2words(new_amount_number, lang='en_IN')
             duplicate_fund['AmountWords'] = new_amount_words

        else:
             new_fund = {
                   "Name": name,
                   "Date": date,
                   "ContactNumber": contact_number,
                   "AmountWords": amount_words,
                   "AmountNumber": amount_number,
                   "Address": address,
                   "type": 'completed transaction'
                 }

             data.setdefault("Funds", []).append(new_fund)

             save_data(data)

             return render_template('index.html')
    except Exception as e:
        return(f"The system encountered an error. Either the files were not created or they could not be accessed.Here's the info {e}")
    # finally:
    #     return(f"Aight. looks like you got an error. heres what i know: the data folder is {DATA_FOLDER}. your current dir is {os.getcwd()}. the current user is {current_user.id}. The program couldnt find the json files specified. The files in this directory are: {os.listdir()}")

     

@app.route('/remove_donors', methods=['POST'])
@login_required
def remove_donors():
    if current_user.id != 'dev':
        return send_file('receipts/511', as_attachment=True)
    else:
        donor_name = request.form['donor_name']

        data = load_data()

        updated_funds = [fund for fund in data.get(
            "Funds", []) if fund['Name'] != donor_name]
        data["Funds"] = updated_funds

        save_data(data)

    return (render_template('display_donors.html'))


@app.route('/display_donors')
@login_required
def display_donors():
    try:
        data = load_data()
        funds = data.get("Funds", [])

        # Find the highest donor
        highest_donor = ""
        highest_amount = 0
        for fund in funds:
            if float(fund['AmountNumber']) > highest_amount:
                highest_amount = float(fund['AmountNumber'])
                highest_donor = fund['Name']

        with open(os.path.join(DATA_FOLDER, 'users.json')) as file:
            user_data = json.load(file)
        users = user_data.get("users")

        return render_template('display_donors.html', funds=funds, users=users, username=current_user.id, highest_donor=highest_donor)
    except Exception as e:
        return(f"error: {e}")
    # finally:
    #      return(f"Aight. looks like you got an error. heres what i know: the data folder is {DATA_FOLDER}. your current dir is {os.getcwd()}. the current user is {current_user.id}. The program couldnt find the json files specified. The files in this directory are: {os.listdir()}")


if __name__ == '__main__':
    app.run(debug=True)
