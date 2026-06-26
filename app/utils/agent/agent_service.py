from pydantic import BaseModel
from langchain.agents import create_agent
from app.assignments.assignment_service import AssignmentService
from app.core.config.config import settings
import os
from langchain_community.utilities import SQLDatabase
from app.core.database import database


SQLDatabase(
    engine=database.engine,
    metadata=database.Base.metadata
)

os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

func = AssignmentService.get_all_my_grades_for_course

agent = create_agent(model="google_genai:gemini-3.5-flash", tools=[func])