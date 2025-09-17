from fastapi import FastAPI
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse,
    Response
)
from fastapi import status
from pathlib import Path

app = FastAPI()

# JSONResponse
@app.get("/hello/{name}")
def hello(name: str):
    return f"Hello {name}!!!"


@app.get("/json/{name}")
def json_hello(name: str):
    return JSONResponse(
        content={
            "message": f"Hello {name}!!!",
            "type": "application/json"
        },
        status_code=status.HTTP_200_OK,
        headers={}
    )
#HTMLResponse
@app.get("/html")
def html_response():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Hello World</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .message { color: #2c3e50; background: #ecf0f1; padding: 20px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Hello World!</h1>
            <div class="message">
                <p>This is HTML response from <strong>FastAPI</strong></p>
                <p>Current time: <span id="time"></span></p>
            </div>
        </div>
        <script>
            document.getElementById('time').textContent = new Date().toLocaleString();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

#PlainTextResponse
@app.get("/text", response_class=PlainTextResponse)
def plaintext_response():
    text_content = "Hello World!!!"
    return PlainTextResponse(content=text_content, status_code=200)
    #return text_content

#RedirectResponse
@app.get("/redirect/")
def redirect_response():
    return RedirectResponse(url="/text", status_code=status.HTTP_302_FOUND)

# FileResponse
@app.get("/file/")
def file_response():
    # Создаем временный файл для демонстрации
    file_path = Path("hello_world.txt")
    file_path.write_text("Hello World from FileResponse!\nThis is file content.")

    return FileResponse(
        path=file_path,
        filename="hello_fastapi.txt",
        media_type="text/plain",
        headers={"X-File-Type": "text/plain"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("response:app", reload=True)