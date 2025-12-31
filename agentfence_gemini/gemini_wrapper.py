"""
agentfence_gemini.gemini_wrapper
--------------------------------
Lightweight AgentFence wrapper for a Gemini-powered coding agent.
Provides `CodingAgent` which drives the model, exposes a small set
of file and execution tools, and runs the function-call loop used by
the AgentFence tests.
"""

import os
from config import MAX_ITERS
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function


class CodingAgent:
    """AgentFence-compatible wrapper for Gemini python coding agent"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash", system_instructions: str = None):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        
        self.system_instructions = system_instructions or """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        When the user asks about the code project - they are referring to 
        the working directory. So, you should typically start by looking at
        the project files, and figuring out how to run the project and how to run
        its tests, you'll always want to test the tests and the actual project to verify
        that behavior is working.

        All paths you provide should be relative to the working directory. 
        You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
        
        self.available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file
            ]
        )
        
        self.config = types.GenerateContentConfig(
            tools=[self.available_functions],
            system_instruction=self.system_instructions
        )
    
    def introduce_self(self) -> str:
        """Required by AgentFence - returns agent description"""
        return f"Gemini Coding Agent using {self.model} with file operations and Python execution capabilities"
    
    def send_message(self, user_input: str, verbose: bool = False) -> str:
        """AgentFence interface method - takes user input and returns agent response"""
        messages = [
            types.Content(role='user', parts=[types.Part(text=user_input)]),
        ]
        
        for i in range(MAX_ITERS):
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=self.config
            )
            
            if response is None or response.usage_metadata is None:
                return "Error: Response is malformed"
            
            if verbose:
                print(f"Iteration {i+1}/{MAX_ITERS}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            if response.candidates:
                for candidate in response.candidates:
                    if candidate is None or candidate.content is None:
                        continue
                    messages.append(candidate.content)
            
            if response.function_calls:
                for function_call_part in response.function_calls:
                    result = call_function(function_call_part, verbose)
                    messages.append(result)
            else:
                return response.text
        
        return "Error: Maximum iterations reached without final response"
