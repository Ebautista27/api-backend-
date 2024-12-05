from flaskr import create_app
from flaskr.modelos import db, Rol  # Importa el modelo Rol

# Función para inicializar roles
def seed_roles():
    with app.app_context():  # Asegúrate de estar en el contexto de la aplicación
        # Crea las tablas en la base de datos si no existen
        db.create_all()

        # Verifica si ya existen roles para evitar duplicados
        if not Rol.query.first():  # Si no hay ningún rol, los crea
            roles = [
                Rol(id=1, nombre="Administrador"),
                Rol(id=2, nombre="Usuario")
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()
            print("Roles inicializados correctamente.")
        else:
            print("Los roles ya están inicializados.")

# Crear la aplicación
app = create_app()

# Inicializar la app y roles
if __name__ == '__main__':
    seed_roles()  # Inicializa los roles si no existen
    app.run(debug=True)
