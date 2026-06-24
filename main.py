from fastapi import FastAPI

app = FastAPI(
    title="COHORT",
    description="Cohort: the platform a learning program uses to run courses, not just host them"
    )

@app.get("/health")
def get_health():
    return {
        "message": "routes working"
    }