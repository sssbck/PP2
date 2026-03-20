import shutil
import os

os.makedirs("target", exist_ok=True)

if os.path.exists("example.txt"):
    shutil.move("example.txt", "target/example.txt")
    print("File moved")
else:
    print("example.txt not found")