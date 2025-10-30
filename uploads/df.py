"""
Simple script with an intentional error.
"""

def greet(name: str) -> None:
    """
    Print a greeting message for the given person.
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    greet(user)  # ERROR: 'user' is not defined
