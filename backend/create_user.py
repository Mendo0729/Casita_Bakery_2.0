import mysql.connector
from mysql.connector import errorcode
import sys
from werkzeug.security import generate_password_hash

def crear_usuario_mysql(username, password):
    try:
        # Carga variables de entorno si usas dotenv
        import os
        from dotenv import load_dotenv
        load_dotenv()

        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "")
        )

        cursor = conexion.cursor()

        # Hashea la contraseña
        password_hash = generate_password_hash(password)

        # Verificar si usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (username,))
        if cursor.fetchone():
            print(f"El usuario '{username}' ya existe.")
            return

        # Insertar nuevo usuario
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        conexion.commit()
        print(f"Usuario '{username}' creado exitosamente.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Usuario o contraseña de MySQL incorrectos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Base de datos no existe.")
        else:
            print(f"Error MySQL: {err}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python create_user_mysql.py <username> <password>")
        sys.exit(1)
    crear_usuario_mysql(sys.argv[1], sys.argv[2])
