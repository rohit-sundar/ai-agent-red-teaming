from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test_get_files_info():
    working_dir = "calculator"
    root_contents = get_files_info(working_dir, ".")
    print (root_contents)

    pkg_contents = get_files_info(working_dir, "pkg")
    print(pkg_contents)

    outside_contents = get_files_info(working_dir, "/bin")
    print(outside_contents)

    parent_contents = get_files_info(working_dir, '../')
    print(parent_contents)

def test_get_file_content():
    working_dir = "calculator"

    print(get_file_content(working_dir, "lorem.txt"))
    print(get_file_content(working_dir, "main.py"))
    print(get_file_content(working_dir, "pkg/calculator.py"))
    print(get_file_content(working_dir, "/bin/cat"))
    print(get_file_content(working_dir, "pkg/does_not_exist.py"))

def test_write_file():
    working_dir = "calculator"
    
    print(write_file(working_dir, "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file(working_dir, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file(working_dir, "/tmp/temp.txt", "this should not be allowed"))
    print(write_file(working_dir, "pkg2/temp.txt", "this should be allowed"))

def test_run_python_file():
    working_dir = "calculator"

    print(run_python_file(working_dir, "main.py"))
    print(run_python_file(working_dir, "main.py", ["3 + 5"]))
    print(run_python_file(working_dir, "tests.py"))
    print(run_python_file(working_dir, "../main.py"))
    print(run_python_file(working_dir, "nonexistent.py"))

if __name__ == "__main__":
    #test_get_files_info()
    #test_get_file_content()
    #test_write_file()
    #test_run_python_file()
    print("all tests over!")