from flaskr import create_app
from flaskr.modelos import db, Rol

def seed_roles():
    app = create_app()
    with app.app_context():
        db.create_all()
        if not Rol.query.first():
            roles = [
                Rol(id=1, nombre="Administrador"),
                Rol(id=2, nombre="Usuario")
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()
            print("Roles inicializados correctamente.")
        else:
            print("Los roles ya están inicializados.")

if __name__ == "__main__":
    seed_roles()
