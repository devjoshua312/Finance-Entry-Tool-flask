# Finance Entry Tool [FET]

A Flask application for managing funds, donor information, and generating receipts.

## Overview

A basic Flask app to simulate functionality for managing funds, generating receipts, and displaying donor information. It is designed to be a simple and effective tool for tracking contributions.

## Features

- User authentication using Flask-Login
- Add funds with details like name, date, contact number, and receipt
- Generate receipts for donors
- Display a list of donors with contribution details
- Scan the reciept given by donor to see if the names match


## Prerequisites

Before running the application, ensure you have all the required packages by running;

```
pip install -r requirements.txt
```

To use the reciept scanning feature, you need the Tesseract engine. Check out [how to install](https://tesseract-oc.r.github.io/tessdoc/Installation.html).

  
## Installation

1. Clone the repository:

   ```
   git clone https://github.com/devjoshua312/Finance-Entry-Tool-flask.git
   ```

2. Change into the project directory:

   ```
   cd project-folder
   ```

### Environment Variables

The website uses a reCaptcha test at login for some security. 

- `grec_sitekey`: Your reCAPTCHA site key

Create a `.env` file in the project root and set the environment variables:

```
grec_sitekey=your_recaptcha_key
```

For information on creating a reCaptcha key, check out [Google reCaptcha](https://www.google.com/recaptcha/about/)

## Usage

Run the Flask application:

There are two ways to do this. One is with the Python Flask service:
```
python app.py
```

And the other is by using Gunicorn

```
gunicorn app:app.py
```

## Endpoints

- `/`: Home page
- `/login`: Login page
- `/logout`: Logout
- `/download_receipt/<donor_name>`: Download receipt for a specific donor
- `/add_fund`: Add a new fund
- `/remove_donors`: Remove donors (accessible to admin only)
- `/display_donors`: Display list of donors