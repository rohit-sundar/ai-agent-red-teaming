"""
main
----
Simple CLI wrapper exposing a `CodingAgent` backed by Gemini. The
agent accepts a single prompt and uses the function-call tools in
`functions/` to inspect and manipulate the workspace during generation.
"""

import os
import sys
from dotenv import load_dotenv
from config import MAX_ITERS
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

class CodingAgent:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        system_prompt: str = None
    ):
        
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt or """
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
            system_instruction=self.system_prompt
        )

    def query(
        self,
        user_prompt: str,
        verbose: bool = False,
    ) -> str:

        messages = [
            types.Content(role='user', parts=[types.Part(text=user_prompt)]),
        ]

        for i in range(MAX_ITERS):
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=self.config
            )

            if response is None or response.usage_metadata is None:
                print("response is malformed")
                return    
            if verbose:
                print(f"User prompt: {user_prompt}")
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
                # final agent text message
                return response.text

def main():

    load_dotenv()
    API_KEY = os.environ.get("GEMINI_API_KEY")
    agent = CodingAgent(api_key=API_KEY)

    if len(sys.argv) < 2:
        print("give me a prompt")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    response = agent.query(user_prompt=prompt, verbose=verbose_flag)

if __name__ == "__main__":
    main()