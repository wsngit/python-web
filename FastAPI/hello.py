from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return "Hello World!!!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("hello:app", reload=True)

