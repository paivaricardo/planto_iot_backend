from fastapi import FastAPI

app = FastAPI()


@app.get("/health-check")
def health_check():
    """
    Realiza um health check da aplicação, indicando se está online ou não.
    """
    return {"status": "ok"}
