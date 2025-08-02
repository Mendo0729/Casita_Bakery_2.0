# run.py
from app import create_app
from app.routes.main import main  # Asegúrate de que este archivo y blueprint existan

app = create_app()
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
