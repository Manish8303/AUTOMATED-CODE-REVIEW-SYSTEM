"""
A simple Python program to demonstrate clean and error-free code.
This program defines a few basic functions and uses them correctly.
"""

def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b


def multiply_numbers(a, b):
    """Return the product of two numbers."""
    return a * b


def greet_user(name):
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to Python coding."


def main():
    """Main function to test other functions."""
    x = 10
    y = 5

    print("Addition:", add_numbers(x, y))
    print("Multiplication:", multiply_numbers(x, y))
    print(greet_user("Manish"))


if __name__ == "__main__":
    main()
