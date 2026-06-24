from fastapi import FastAPI
from app.users.user_api import router as signup_router







app = FastAPI(
    title="COHORT",
    description="Cohort: the platform a learning program uses to run courses, not just host them"
    )

app.include_router(signup_router)

@app.get("/health")
def get_health():
    return {
        "message": "routes working"
    }