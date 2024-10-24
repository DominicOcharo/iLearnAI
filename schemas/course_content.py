from pydantic import BaseModel

class CourseContent(BaseModel):
    title: str = None
    subtitle: str = None
    body: str = None
