
# main.py
from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from models import Gender, Role, User, UpdateUser

#Hard coded list of users in in-memory database
db: List[User] = [
    User(
     id=uuid4(),
     first_name="John",
     last_name="Doe",
     gender=Gender.male,
     roles=[Role.user],
    ),
    User(
     id=uuid4(),
     first_name="Jane",
     last_name="Doe",
     gender=Gender.female,
     roles=[Role.user],
    ),
    User(
     id=uuid4(),
     first_name="James",
     last_name="Gabriel",
     gender=Gender.male,
     roles=[Role.user],
    ),
    User(
     id=uuid4(),
     first_name="Eunit",
     last_name="Eunit",
     gender=Gender.male,
     roles=[Role.admin, Role.user],
    ),
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/users")
async def get_users():
    return db

@app.post("/api/v1/users")
async def create_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404, detail=f"Delete user failed, user \"{id}\" not found"
    )

@app.put("/api/v1/users/{id}")
async def update_user(user_update: UpdateUser, id: UUID):
    for user in db:
        if id == user.id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.gender is not None:
                user.gender = user_update.gender
            if user_update.roles is not None:
                user.roles = user_update.roles
        return user.id
    raise HTTPException(status_code=404, detail=f"Update user {id} failed - could not find user.")