"""
This Python file intentionally includes syntax errors,
logical mistakes, bad formatting, and style violations
for testing the analyzer UI.
"""

def add_numbers(a, b)
    # Missing colon above, indentation issue below
    result = a + b
     print("Sum is:", result)
    return result


def divide_numbers(a, b):
    # Division by zero risk, no proper error handling
    return a / b

def greetUser(name)
    print("Hello " + name)
    if name == "Manish"
        print("Welcome Back!")  # Missing colon above
     else
        print("Nice to meet you!") # Indentation error


def main():
  # Mixed indentation and poor variable naming
    X = 10
    y=0
    add_numbers(X,y)
    print("Division:", divide_numbers(X, y))
    greetUser("Manish")


main()
