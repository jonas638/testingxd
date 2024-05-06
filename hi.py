import os

def create_hi_txt():
    try:
        
        desktop_path = os.path.join(os.path.expanduser("~"), "Bureaublad")
        hi_txt_path = os.path.join(desktop_path, "hi.txt")
        with open(hi_txt_path, "w") as file:
            file.write("jonas was here")
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    create_hi_txt()
