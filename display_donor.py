from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

DATA_FOLDER = os.getcwd()


# Load data from JSON file
def load_data():
    try:
        with open(os.path.join(DATA_FOLDER, 'funds.json'), 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


@app.route('/display_donors_by_name', methods=['POST'])
def display_donors_by_name():
    name = request.form['name'].strip()

    if not name:
        return render_template('display_donors.html', funds=[])

    # Load data
    data = load_data()
    funds = data.get("Funds", [])

    matching_donors = [fund for fund in funds if fund["Name"].lower().__contains__(name.lower())]

    return render_template('display_donors.html', funds=matching_donors)


@app.route('/display_all_donors')
def display_all_donors():
    # Load data
    data = load_data()
    funds = data.get("Funds", [])

    return render_template('display_donors.html', funds=funds)


if __name__ == "__main__":
    app.run(debug=True)
