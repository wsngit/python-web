from fastapi import FastAPI, Query, Form
from typing import List, Annotated
from pydantic import BaseModel

app = FastAPI()

# Парамерты в пути
@app.get("/hello/{name}")
def hello(name: str):
    return f"Hello {name}!!!"

# Query параметр
@app.get("/hello")
def hello(name: str):
    return f"Hello {name}!!!"

# Query параметр список
@app.get("/helloall")
def helloall(names:  Annotated[List[str], Query()] = []):
    allnames = ','.join(names)
    return f"Hello {allnames}!!!"

# Body параметры - json
class User(BaseModel):
    username: str
    email: str
    age: int

@app.post("/hellouser")
def hellouser(user: User):
    return f"Hello {user.username}!!!"

# Body параметры - Form
@app.post("/login")
async def login(
        username: Annotated[str, Form(..., min_length=3)],
        password: Annotated[str, Form(..., min_length=8)]
):
    return {"username": username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("parameters:app", reload=True)