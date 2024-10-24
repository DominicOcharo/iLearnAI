from groq import Groq
import os

# Initialize Groq client with the API key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Global variable to store dynamic course content
course_modules = []

def update_course_content(new_module: str):
    """Update global course content dynamically by adding new modules."""
    global course_modules
    course_modules.append(new_module)

def get_all_content():
    """Return all the course content."""
    return course_modules

def delete_course_content(module_title: str):
    """Delete a course module by title."""
    global course_modules
    course_modules = [module for module in course_modules if module['module_title'] != module_title]

def edit_course_content(module_title: str, new_content):
    """Edit a course module's content by title."""
    global course_modules
    for module in course_modules:
        if module['module_title'] == module_title:
            module['content_parts'] = new_content
            return module
    return None

def create_system_prompt():
    """Create a system prompt with the current course content."""
    if not course_modules:
        return "No course content available."
    
    # Combine all module contents
    combined_content = "\n\n".join([f"Module {i+1}: {module}" for i, module in enumerate(course_modules)])
    
    return f"You are a knowledgeable assistant. You can only answer questions based on the course content provided and take the whole content as correct. If the query is outside the content, respond with 'I cannot answer that as it is outside the scope of the provided content.' Here is the course content:\n\n{combined_content}"

def generate_response(user_query):
    # Ensure course content exists before generating responses
    if not course_modules:
        return "No course content available. Please update the content before asking questions."

    # Create a stream of completions based on the user's query and course content
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": create_system_prompt()
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=True,
    )

    response = ""
    # Output the response as it streams in
    for chunk in stream:
        delta_content = chunk.choices[0].delta.content
        if delta_content is not None:
            response += delta_content

    return response
