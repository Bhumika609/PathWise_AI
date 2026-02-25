from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PathWise backend running"}

@app.get("/test")
def test():
    return {"status": "API working"}