from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Fake database
users = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"},
}


class User(BaseModel):
    name: str


@app.get("/")
def home():
    return {"message": "Hello FastAPI"}


@app.get("/users")
def get_users():
    return list(users.values())


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.post("/users", status_code=201)
def create_user(user: User):
    new_id = max(users.keys()) + 1
    new_user = {"id": new_id, "name": user.name}
    users[new_id] = new_user
    return new_user
