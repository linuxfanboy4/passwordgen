# PasswordGen - Terminal Password Manager

## Overview

PasswordGen is a secure terminal-based password manager that generates strong, cryptographically secure passwords with configurable complexity. It provides detailed security analysis of generated passwords, including entropy calculations and estimated cracking time. Passwords are stored locally with strong encryption.

## Features

- Generate cryptographically secure passwords with customizable length and complexity
- Exclude specific characters from password generation
- Calculate password entropy and estimate cracking time
- Rate password strength based on mathematical analysis
- Secure encrypted storage for generated passwords
- Retrieve saved passwords by service name
- Clean terminal interface with rich text formatting
- MIT licensed open source project

## Installation

Install PasswordGen directly from GitHub using pip:

```bash
pip install git+https://github.com/linuxfanboy4/passwordgen.git
```

After installation, run the application with:

```bash
python -m passwordgen
```

## Dependencies

PasswordGen requires the following Python packages which will be installed automatically:

- cryptography
- rich
- secrets (Python standard library)
- math (Python standard library)
- os (Python standard library)
- json (Python standard library)

## Usage Example

Below is a typical PasswordGen session:

```
Welcome to the Terminal Password Manager!

Generate strong, secure passwords with ease!

Enter the desired password length (default is 23): 24
Enter password complexity (low, medium, high): high
Enter characters to exclude (comma separated, optional): <,>,&

Generating password...

Generated Password: 7K$9pL@2mQv6#sF1%jX4*zY8

+-----------------------------------------+
|           Password Information          |
+-----------------+-----------------------+
| Attribute       | Value                 |
+-----------------+-----------------------+
| Length          | 24                    |
| Entropy         | 132.21 bits           |
| Estimated       | 6.84e+28 years        |
| Cracking Time   |                       |
| Strength        | Very Strong           |
+-----------------+-----------------------+

Do you want to save this password? (y/n): y
Enter the service name (e.g., 'Email', 'Facebook'): GitHub
Password saved for GitHub.

Do you want to retrieve a saved password? (y/n): y
Enter the service name to retrieve password: GitHub
Password for GitHub: 7K$9pL@2mQv6#sF1%jX4*zY8

Password management complete!
```

## Security Considerations

- Passwords are generated using Python's `secrets` module which is cryptographically secure
- All stored passwords are encrypted using Fernet symmetric encryption
- The encryption key is stored locally in `encryption.key`
- For maximum security, consider storing the encryption key separately from the password database
- The password database is stored in `passwords.json` in encrypted form

## Password Generation Algorithm

PasswordGen uses the following approach to generate secure passwords:

1. Creates a character set based on selected complexity level
2. Removes any user-specified excluded characters
3. Uses `secrets.choice()` for cryptographically secure random selection
4. Generates a string of the specified length from the filtered character set

## Password Strength Analysis

The application calculates password strength using:

- **Entropy**: Measured in bits, calculated as log2(N^L) where N is the number of possible characters and L is the password length
- **Cracking Time**: Estimated based on entropy assuming 1 billion guesses per second
- **Strength Rating**: Classified as Weak, Moderate, Strong, or Very Strong based on entropy thresholds

## License

PasswordGen is released under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. Please fork the repository and submit pull requests for any enhancements or bug fixes.

## Support

For support, issues, or feature requests, please open an issue on the GitHub repository.
