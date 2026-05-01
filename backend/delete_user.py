from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()

# Supprimer par email
email_to_delete = "user@saplateforme.com"

user = db.query(User).filter(User.email == email_to_delete).first()

if user:
    db.delete(user)
    db.commit()
    print(f"✅ Utilisateur {email_to_delete} supprimé")
else:
    print(f"❌ Utilisateur {email_to_delete} non trouvé")

db.close()