import os

print(os.path.abspath("a.txt") + "\\ezyZip")

with open("C:\\gdg website\\backend\\ezyZip\\a.txt", "r") as file:
    print(file.read())
    file.close()