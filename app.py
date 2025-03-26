from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, Callable
import logging
from datetime import datetime
from ai_engine import AIEngine


logging.basicConfig(
    filename='automation_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="AI-Powered Automation API",
             description="REST API for executing automation functions using LLM and RAG")


ai_engine = AIEngine()

class ExecuteRequest(BaseModel):
    prompt: str

class ExecuteResponse(BaseModel):
    success: bool
    action: str
    result: Optional[Any]
    error: Optional[str] = None

class CustomFunctionRequest(BaseModel):
    name: str
    code: str
    description: str

@app.post("/register-function")
async def register_custom_function(request: CustomFunctionRequest):
    """
    Register a custom user-defined function using LLM and RAG.
    
    Args:
        request (CustomFunctionRequest): Contains function name, code, and description
    """
    try:
        
        ai_engine.add_custom_function(
            name=request.name,
            description=request.description,
            code=request.code
        )
        
        logging.info(f"Registered custom function: {request.name}")
        return {"success": True, "message": f"Function '{request.name}' registered successfully"}
        
    except Exception as e:
        logging.error(f"Error registering function {request.name}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/list-functions")
async def list_available_functions():
    """List all available functions including built-in and custom functions."""
    try:
        
        functions = ai_engine.function_store.similarity_search(
            "List all available functions",
            k=100  
        )
        
        return {
            "functions": [
                {
                    "name": doc.metadata["name"],
                    "type": doc.metadata["type"],
                    "description": doc.page_content
                }
                for doc in functions
            ]
        }
    except Exception as e:
        logging.error(f"Error listing functions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute", response_model=ExecuteResponse)
async def execute_automation(request: ExecuteRequest):
    """
    Execute automation functions based on natural language prompt using LLM and RAG.
    
    Args:
        request (ExecuteRequest): Contains the natural language prompt
    """
    start_time = datetime.now()
    prompt = request.prompt.lower()
    
    try:
        logging.info(f"Processing prompt: {prompt}")
        
       
        result = await ai_engine.process_prompt(prompt)
        
        if not result["success"]:
            raise ValueError(result["error"])
            
        return ExecuteResponse(
            success=True,
            action=result["action"],
            result=result["result"]
        )
            
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error executing prompt '{prompt}': {error_msg}")
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "action": "unknown",
                "error": error_msg
            }
        )
    finally:
        execution_time = (datetime.now() - start_time).total_seconds()
        logging.info(f"Request completed in {execution_time:.2f} seconds")

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting AI-Powered Automation API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)