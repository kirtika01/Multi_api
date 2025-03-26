import os
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AIEngine:
    def __init__(self):
        """Initialize the AI engine with function store and embeddings."""
        self.embeddings = HuggingFaceEmbeddings() 
        self.function_store = None
        self.model = genai.GenerativeModel('gemini-pro')
        self.initialize_function_store()

    def initialize_function_store(self):
        """Initialize the vector store with function descriptions."""
        function_docs = [
            Document(
                page_content="Open Google Chrome web browser",
                metadata={"name": "open_chrome", "type": "app"}
            ),
            Document(
                page_content="Open Windows Calculator application",
                metadata={"name": "open_calculator", "type": "app"}
            ),
            Document(
                page_content="Open Windows Notepad text editor",
                metadata={"name": "open_notepad", "type": "app"}
            ),
            Document(
                page_content="Get current CPU usage percentage",
                metadata={"name": "get_cpu_usage", "type": "system"}
            ),
            Document(
                page_content="Get current RAM memory usage statistics",
                metadata={"name": "get_ram_usage", "type": "system"}
            ),
            Document(
                page_content="Execute a shell command in the system",
                metadata={"name": "execute_shell_command", "type": "system"}
            )
        ]
        self.function_store = FAISS.from_documents(function_docs, self.embeddings)

    def add_custom_function(self, name: str, description: str, code: str):
        """Add a custom function to the vector store."""
        new_doc = Document(
            page_content=description,
            metadata={"name": name, "type": "custom", "code": code}
        )
        if self.function_store is None:
            self.function_store = FAISS.from_documents([new_doc], self.embeddings)
        else:
            self.function_store.add_documents([new_doc])

    def get_relevant_function(self, prompt: str) -> Dict[str, Any]:
        """
        Retrieve the most relevant function based on the user's prompt.
        
        Args:
            prompt (str): User's natural language prompt
            
        Returns:
            Dict containing function name and metadata
        """
        if self.function_store is None:
            raise ValueError("Function store not initialized")

       
        docs = self.function_store.similarity_search(prompt, k=1)
        if not docs:
            raise ValueError("No relevant function found")

        return {
            "name": docs[0].metadata["name"],
            "type": docs[0].metadata["type"],
            "code": docs[0].metadata.get("code")
        }

    async def generate_code_with_gemini(self, prompt: str) -> str:
        """
        Generate code using Gemini API.
        
        Args:
            prompt (str): Code generation prompt
            
        Returns:
            str: Generated code
        """
        response = await self.model.generate_content_async(prompt)
        return response.text

    def generate_execution_code(self, function_info: Dict[str, Any], args: Dict[str, Any] = None) -> str:
        """
        Generate executable Python code for the function call.
        
        Args:
            function_info (Dict): Function information from get_relevant_function
            args (Dict): Optional arguments for the function
            
        Returns:
            str: Generated Python code
        """
        if function_info["type"] == "custom" and function_info.get("code"):
            return function_info["code"]

      
        function_name = function_info["name"]
        if args:
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in args.items())
            return f"import automation_functions as af\nresult = af.{function_name}({args_str})"
        else:
            return f"import automation_functions as af\nresult = af.{function_name}()"

    async def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Process a natural language prompt and execute the appropriate function.
        
        Args:
            prompt (str): User's natural language prompt
            
        Returns:
            Dict containing execution results
        """
        try:
          
            function_info = self.get_relevant_function(prompt)
            
           
            if "shell" in function_info["name"]:
                arg_prompt = f"Extract the shell command from this prompt: '{prompt}'. Return only the command, nothing else."
                command = await self.generate_code_with_gemini(arg_prompt)
                args = {"command": command.strip()}
            else:
                args = None

           
            exec_code = self.generate_execution_code(function_info, args)
            
            
            namespace = {}
            
           
            exec(exec_code, namespace)
            
            return {
                "success": True,
                "action": function_info["name"],
                "result": namespace.get("result"),
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "action": "unknown",
                "result": None,
                "error": str(e)
            }