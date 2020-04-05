import re
a = ['35']
print(
    re.findall(r'\d+',str(a))
)