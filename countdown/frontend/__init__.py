from countdown.frontend.endpoints import app

app.config.from_pyfile('config/__init__.py')

if __name__ == "__main__":
    app.run(debug=True)
