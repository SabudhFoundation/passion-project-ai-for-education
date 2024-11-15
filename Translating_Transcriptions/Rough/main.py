import ast


with open("data.txt") as file:
    data = file.readlines()


for key , value in ast.literal_eval(data).items():
    print(key)
    print()
    print(value)