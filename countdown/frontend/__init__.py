from countdown.frontend.endpoints import app

app.config.from_pyfile('config/__init__.py')

app.run(debug=True)
