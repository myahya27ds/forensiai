from fastapi import FastAPI

app = FastAPI(
    title="ForensiAI",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "ForensiAI API Running"
    }