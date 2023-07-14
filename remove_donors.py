from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FOLDER = os.getcwd()


def load_data():
    try:
        with open(os.path.join(DATA_FOLDER, 'funds.json'), 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


def save_data(data):
    with open(os.path.join(DATA_FOLDER, 'funds.json'), 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/remove_donors', methods=['POST'])
def remove_donors():
    donor_name = request.form['donor_name']

    data = load_data()

    updated_funds = [fund for fund in data.get("Funds", []) if fund['Name'] != donor_name]
    data["Funds"] = updated_funds

    save_data(data)

    return(render_template('display_donors.html'))


if __name__ == "__main__":
    app.run(debug=True)
