from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def get_hello():
    return "Hello World!!!"

@app.post("/hello")
def post_hello():
    return "Hello World!!!"

@app.head("/hello")
def head_hello():
    return "Hello World!!!"

@app.put("/hello")
def put_hello():
    return "Hello World!!!"

@app.options("/hello")
def options_hello():
    return {"Allow": "GET, POST, PUT, DELETE, OPTIONS, HEAD"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("methods:app", reload=True)

