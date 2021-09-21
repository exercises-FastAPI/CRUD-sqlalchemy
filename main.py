from fastapi import FastAPI
from typing import List, Dict

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# #original function
# @app.get("/notes", response_model=List[schemas.Note])
# def read_notes(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     notes = crud.get_notes(db=db, skip=skip, limit=limit)
#     print(notes)
#     return notes
@app.get("/", response_class=HTMLResponse)
def read_notes(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db=db, skip=skip, limit=limit)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "notes": notes
    })

@app.post("/notes", response_model=schemas.Note, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)

@app.get("/notes/{note_id}", response_model=schemas.Note)
def read_user(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    return crud.delete_note(db=db, note_id=note_id)


@app.put("/notes/{note_id}", status_code=200)
async def put_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = schemas.Note(id = note_id, title= note.title, description=note.description)
    crud.update_note(db=db, note=db_note)

@app.patch("/notes/{note_id}", status_code=200)
async def patch_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    print(note_id)
    print(note.title)
    print(note.description)
    db_note = schemas.Note(id = note_id, title= note.title, description=note.description)
    crud.update_note(db=db, note=db_note)
