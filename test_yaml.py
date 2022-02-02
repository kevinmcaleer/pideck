from qd_yaml import YAML

y = YAML()

with open('keypad.yml') as file:
    my_yaml = y.load(file)

print(my_yaml)