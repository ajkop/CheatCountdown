from .endpoints import app

app.config.from_pyfile('config.py')

app.run(debug=True)
