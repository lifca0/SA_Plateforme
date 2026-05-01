from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.api.routes import router
from app.database import engine, Base
from app.models import user
import pandas as pd
from io import BytesIO

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SA Plateforme API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API SA Plateforme", "docs": "/docs"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    data = pd.read_excel(file.file, usecols="A:E,G:I,V:X,Z")
    output = BytesIO()
    data.to_excel(output, index=False)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=crm_ready.xlsx"
        }
    )