import os

for obj in os.listdir("data/objs/"):
    if "-" in obj and "scan" not in obj:
        os.remove(os.path.join("data", "objs", obj))


