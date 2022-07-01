import sys

def pprint_dict(header, d):
    print("\n\n ---------------------------")
    print(f"****** {header} ******")
    for key, value in d.items():
        print(key, value)
    print("---------------------------\n\n ")


print(f"------------ Running {__name__} ------------")

pprint_dict("module1.globals", globals())

print(f"------------ End of {__name__} ------------")
