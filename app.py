from flask import Flask, render_template, request, redirect
import gspread
import bcrypt
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

def webserver(host, port, google_sheet, credentials_file):
    app = Flask(__name__, template_folder='templates')
    @app.route('/')
    def login_page():
        return render_template('login_page.html')

    @app.route('/', methods=['POST'])
    def login_page_form_data():
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)      
        username = request.form['username']
        password = str(request.form['password']).encode("utf8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
        sheet = client.open(google_sheet).sheet1
        sheet.insert_row([username, hashed.decode("utf8")], index=2)
        return redirect('/main')
        return username

    @app.route('/main')
    def main_page():
        return render_template('your_page.html')

    app.run(debug=True, host=host, port=port)