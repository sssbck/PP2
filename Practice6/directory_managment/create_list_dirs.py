import os

os.makedirs("test_dir/subdir", exist_ok=True)

print("Current dir:", os.getcwd())

print("Files and folders:")
print(os.listdir("."))

if os.path.exists("test_dir"):
    print("Directory exists")