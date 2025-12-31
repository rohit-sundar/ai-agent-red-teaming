"""
functions.get_file_content
--------------------------
Utility to read a file (bounded by `MAX_CHARS`) from a provided
working directory. Ensures reads are constrained to the working
directory for safety and returns errors as strings on failure.
"""

import os

from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
    
    file_content_string = ""
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f' [...File "{file_path}" truncated at 10000 characters]\n'

        return file_content_string
    
    except Exception as e:
        return f'Exception reading file "{e}"'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of the given file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)