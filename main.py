from fastapi import FastAPI
from app.users.user_api import router as signup_router
from app.auth.login_api import router as login_router
from app.courses.courses_api import router as course_router
from app.cohort.cohort_api import router as cohort_router
from app.course_onboarding.course_onboarding_api import router as onboarding_router
from app.assignments.assignment_api import router as assignment_router
from app.notifications.notification_api import router as notification_router


app = FastAPI(
    title="COHORT",
    description="Cohort: the platform a learning program uses to run courses, not just host them"
    )

app.include_router(signup_router)
app.include_router(login_router)
app.include_router(cohort_router)
app.include_router(course_router)
app.include_router(onboarding_router)
app.include_router(assignment_router)
app.include_router(notification_router)


@app.get("/health")
def get_health():
    return {
        "message": "routes working"
    }