from fastapi import FastAPI, Header

app = FastAPI()

# Параметры в заголовках
@app.get("/hello")
def hello(name: str =  Header()):
    return f"Hello {name}!!!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("header:app", reload=True)

