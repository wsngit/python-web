from typing import Annotated

from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload(
        file: Annotated[UploadFile, File(..., description="Загружаемый файл")]
):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("upload:app", reload=True)

