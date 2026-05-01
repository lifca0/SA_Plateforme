from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.auth import hash_password

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer une session
db = SessionLocal()

# Supprimer les utilisateurs existants si besoin
db.query(User).delete()

# Créer des utilisateurs prédéfinis
users = [
    {
        "email": "admin@saplateforme.com",
        "password": "admin123",
        "full_name": "Administrateur",
        "is_active": True
    },
    {
        "email": "user@saplateforme.com",
        "password": "user123",
        "full_name": "Utilisateur Standard",
        "is_active": True
    },
    {
        "email": "commercial@saplateforme.com",
        "password": "commercial123",
        "full_name": "Commercial",
        "is_active": True
    }
]

for user_data in users:
    user = User(
        email=user_data["email"],
        password=hash_password(user_data["password"]),
        full_name=user_data["full_name"],
        is_active=user_data["is_active"]
    )
    db.add(user)

db.commit()
db.close()

print("✅ Utilisateurs créés avec succès !")
print("📧 admin@saplateforme.com / admin123")
print("📧 user@saplateforme.com / user123")
print("📧 commercial@saplateforme.com / commercial123")