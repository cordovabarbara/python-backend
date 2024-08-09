#Type Hints#

my_string_variable = "my first string"
print(type(my_string_variable))

my_typed_variable: str = "my second variable"
print(my_typed_variable.upper())

'''These "type hints" or annotations are a special syntax that allow declaring the type of a variable.'''

def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))