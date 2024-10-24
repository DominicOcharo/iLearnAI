from fastapi import APIRouter, Form, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from detectors.groq_client import (
    update_course_content, 
    generate_response, 
    get_all_content, 
    delete_course_content, 
    edit_course_content
)

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
)

# Pydantic model for adding or editing course content
class ModuleContent(BaseModel):
    module_title: str
    content_parts: Optional[List[str]] = None

@router.post("/update-content")
async def update_content(
    module_title: str = Form(...),
    content_parts: Optional[List[str]] = Form(None),
):
    """API to add a new module and update its content dynamically."""
    
    if not module_title.strip():
        raise HTTPException(status_code=400, detail="Module title must be provided.")
    
    # Build the module content from the provided content parts
    new_module = {
        "module_title": module_title,
        "content_parts": []
    }

    if content_parts:
        for part in content_parts:
            new_module["content_parts"].append(part)

    # Update the course content dynamically with the new module
    update_course_content(new_module)
    return {"status": True, "message": "Module and content added successfully", "data": {"module": new_module}}

@router.get("/get-content")
async def get_content():
    """API to get all the added course content."""
    content = get_all_content()
    return {"status": True, "message": "Content fetched successfully", "data": content}

@router.delete("/delete-content/{module_title}")
async def delete_content(module_title: str):
    """API to delete a module by its title."""
    delete_course_content(module_title)
    return {"status": True, "message": f"Module '{module_title}' deleted successfully"}

@router.put("/edit-content")
async def edit_content(module_title: str = Form(...), content_parts: Optional[List[str]] = Form(None)):
    """API to edit an existing module's content."""
    if not content_parts:
        raise HTTPException(status_code=400, detail="Content parts must be provided.")
    
    edited_module = edit_course_content(module_title, content_parts)
    if edited_module:
        return {"status": True, "message": "Module content updated successfully", "data": edited_module}
    
    raise HTTPException(status_code=404, detail="Module not found")

@router.post("/ask-question")
async def ask_question(
    query: str = Form(...)
):
    """API to ask a question based on the course content."""
    
    # Ensure the query is not empty
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    response = generate_response(query)
    if response:
        return {"status": True, "message": "Query answered", "data": {"response": response}}
    
    raise HTTPException(status_code=500, detail="Error generating response.")
