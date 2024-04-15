import os

def create_hello_txt():
    try:
        # Get the path to the desktop directory
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Construct the full path to the hello.txt file
        hello_txt_path = os.path.join(desktop_path, "hello.txt")
        
        # Open the file in write mode and close it immediately to create an empty file
        with open(hello_txt_path, "w"):
            pass
        
        print(f"File 'hello.txt' created successfully on the desktop.")
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    create_hello_txt()
