from fastapi import FastAPI

app = FastAPI(title="Remind Servcie API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

