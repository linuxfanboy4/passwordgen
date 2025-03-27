#!/usr/bin/env python3

import random
import string
import secrets
import math
import os
import json
from cryptography.fernet import Fernet
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import track

console = Console()

# Encryption key for storing passwords securely (generated once)
# This key should be kept secure, don't hardcode it in real applications.
# In this example, the key is generated when the application runs for the first time.
ENCRYPTION_KEY_FILE = "encryption.key"
PASSWORD_DB_FILE = "passwords.json"


def generate_key():
    """Generate and save an encryption key."""
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """Load the encryption key from file."""
    if os.path.exists(ENCRYPTION_KEY_FILE):
        with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        return generate_key()


key = load_key()
cipher = Fernet(key)


def save_password(service, password):
    """Store the password in an encrypted file."""
    if not os.path.exists(PASSWORD_DB_FILE):
        with open(PASSWORD_DB_FILE, "w") as f:
            json.dump({}, f)

    with open(PASSWORD_DB_FILE, "r+") as f:
        data = json.load(f)
        data[service] = cipher.encrypt(password.encode()).decode()
        f.seek(0)
        json.dump(data, f)


def retrieve_password(service):
    """Retrieve an encrypted password from the storage."""
    if os.path.exists(PASSWORD_DB_FILE):
        with open(PASSWORD_DB_FILE, "r") as f:
            data = json.load(f)
            encrypted_password = data.get(service)
            if encrypted_password:
                return cipher.decrypt(encrypted_password.encode()).decode()
    return None


def generate_password(length=23, complexity="high", exclude_chars=""):
    """Generate a password with specified rules."""
    available_chars = string.ascii_letters + string.digits + string.punctuation
    if complexity == "low":
        characters = string.ascii_letters + string.digits
    elif complexity == "medium":
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = available_chars

    characters = [c for c in characters if c not in exclude_chars]

    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password


def calculate_entropy(password):
    """Calculate the entropy of the password."""
    unique_characters = len(set(password))
    entropy = math.log2(unique_characters ** len(password))
    return round(entropy, 2)


def estimated_cracking_time(entropy):
    """Estimate the cracking time of the password based on entropy."""
    time_in_seconds = 2 ** entropy / 1000000000  # 1 billion guesses per second
    years = time_in_seconds / (60 * 60 * 24 * 365)
    return round(years, 2)


def rate_password_strength(password):
    """Rate password strength on a scale."""
    entropy = calculate_entropy(password)
    if entropy < 40:
        return "Weak"
    elif 40 <= entropy < 60:
        return "Moderate"
    elif 60 <= entropy < 80:
        return "Strong"
    else:
        return "Very Strong"


def display_password_info(password):
    """Display detailed password information."""
    entropy = calculate_entropy(password)
    cracking_time = estimated_cracking_time(entropy)

    table = Table(title="Password Information")
    table.add_column("Attribute", justify="center", style="bold cyan")
    table.add_column("Value", justify="center", style="bold green")

    table.add_row("Length", str(len(password)))
    table.add_row("Entropy", str(entropy) + " bits")
    table.add_row("Estimated Cracking Time", f"{cracking_time} years")
    table.add_row("Strength", rate_password_strength(password))

    console.print(table)


def main():
    console.print("[bold magenta]Welcome to the Terminal Password Manager![/bold magenta]\n")
    console.print("[bold blue]Generate strong, secure passwords with ease![/bold blue]\n")

    length = Prompt.ask("[bold yellow]Enter the desired password length (default is 23):", default=23, type=int)
    complexity = Prompt.ask("[bold yellow]Enter password complexity (low, medium, high):", default="high")
    exclude_chars = Prompt.ask("[bold yellow]Enter characters to exclude (comma separated, optional):", default="")
    exclude_chars = exclude_chars.replace(",", "")

    console.print("\n[bold green]Generating password...[/bold green]")
    password = generate_password(length, complexity, exclude_chars)

    console.print(f"\n[bold blue]Generated Password:[/bold blue] [bold red]{password}[/bold red]\n")

    display_password_info(password)

    save_option = Prompt.ask("[bold yellow]Do you want to save this password? (y/n):", default="n")
    if save_option.lower() == "y":
        service = Prompt.ask("[bold yellow]Enter the service name (e.g., 'Email', 'Facebook'):")
        save_password(service, password)
        console.print(f"[bold green]Password saved for {service}.[/bold green]\n")

    retrieve_option = Prompt.ask("[bold yellow]Do you want to retrieve a saved password? (y/n):", default="n")
    if retrieve_option.lower() == "y":
        service = Prompt.ask("[bold yellow]Enter the service name to retrieve password:")
        retrieved_password = retrieve_password(service)
        if retrieved_password:
            console.print(f"[bold blue]Password for {service}:[/bold blue] {retrieved_password}")
        else:
            console.print(f"[bold red]No password found for {service}.[/bold red]")

    console.print("\n[bold magenta]Password management complete![/bold magenta]\n")


if __name__ == "__main__":
    main()
