# run.py
from app import create_app # Asegúrate de que este archivo y blueprint existan

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
