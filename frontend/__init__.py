from flask import Flask, send_from_directory, render_template , request , redirect, url_for, flash , jsonify

app = Flask(__name__)

if __name__ == "__main__":
    app.run()
