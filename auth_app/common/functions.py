import string
import secrets

def generate_password(length=12):
    # Define the characters to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        # Generate a random password using secrets.choice
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Check if the password meets the requirements
        if (
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in string.punctuation for char in password) and
            not any(char in "<>~`^;|\/'" for char in password)
        ):
            return password
