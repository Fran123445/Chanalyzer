from fastapi import FastAPI

app = FastAPI(title="Chanalyzer API")

@app.get("/")
def root():
    return {"message": "Welcome to the Chanalyzer API"}