import os

def create_hi_txt():
    try:
        # Get the path to the desktop directory
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Construct the full path to the hi.txt file
        hi_txt_path = os.path.join(desktop_path, "hi.txt")
        
        # Open the file in write mode and write the content "jonas was here"
        with open(hi_txt_path, "w") as file:
            file.write("jonas was here")
        
        print(f"File 'hi.txt' created successfully on the desktop with content 'jonas was here'.")
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    create_hi_txt()
