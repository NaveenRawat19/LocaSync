from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/upload")
async def upload_file(request: Request):
    async for chunk in request.stream():
        # Process each chunk of the uploaded file
        print(f"Received chunk of size: {len(chunk)} bytes")

@app.get("/get-video")
async def stream_video():
    video_path = "C:/Users/NAVEEN/Downloads/video23.mp4"
    def iterfile():
        with open(video_path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # Read in 1MB chunks
                print(f"Sending chunk of size: {len(chunk)} bytes")
                yield chunk
    
    return StreamingResponse(iterfile(), media_type="video/mp4")
