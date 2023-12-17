# Finance Entry Tool [FET]

A Flask application for managing funds, donor information, and generating receipts.

## Overview

A basic Flask app to simulate functionality for managing funds, generating receipts, and displaying donor information. It is designed to be a simple and effective tool for tracking contributions.

## Features

- User authentication using Flask-Login
- Add funds with details like name, date, contact number, and receipt
- Generate receipts for donors
- Display a list of donors with contribution details

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- num2words
- Flask-Login
- python-dotenv
- pymongo
- gunicorn (optional)
  
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/devjoshua312/Finance-Entry-Tool-flask.git
   ```

2. Change into the project directory:

   ```bash
   cd project-folder
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   
### Environment Variables

The wwebsite uses a reCaptcha test at login for some security. 

- `grec_sitekey`: Your reCAPTCHA site key

Create a `.env` file in the project root and set the environment variables:

```env
grec_sitekey=your_recaptcha_key
```

For information on creating a reCaptcha key, check out [Google reCaptcha](https://www.google.com/recaptcha/about/)

## Usage

Run the Flask application:

```bash
python app.py
```

## Endpoints

- `/`: Home page
- `/login`: Login page
- `/logout`: Logout
- `/download_receipt/<donor_name>`: Download receipt for a specific donor
- `/add_fund`: Add a new fund
- `/remove_donors`: Remove donors (accessible to admin only)
- `/display_donors`: Display list of donors
