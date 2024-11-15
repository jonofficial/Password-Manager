# Password Manager

A secure, Tkinter-based password manager with login and registration functionality. This application allows users to securely store and manage their passwords using AES encryption, with features for password generation and strength analysis.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)

---

## Project Overview

This Password Manager project provides a user-friendly interface to manage passwords securely. Users can register, log in, and manage passwords in an encrypted format. The application is built with Python's Tkinter library for the GUI and uses AES encryption for secure password storage.

## Features

- User registration and login with SQLite database
- AES encryption for password storage
- Password generation and strength analysis
- CRUD (Create, Read, Update, Delete) operations for password records

## Technologies Used

- **Python**: Core programming language
- **Tkinter**: GUI library
- **SQLite**: Database for storing user information
- **PyCryptodome**: For AES encryption
- **zxcvbn**: For password strength analysis

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

Make sure you have **Python 3.7+** installed. You can download it from [python.org](https://www.python.org/).

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jonofficial/Password-Manager.git
   cd password-manager

# Password Manager

A secure, Tkinter-based password manager with login and registration functionality. This application allows users to securely store and manage their passwords using AES encryption, with features for password generation and strength analysis.

---

## Set up a virtual environment (recommended to avoid conflicts with other Python projects):

### On Windows:
```bash
python -m venv env
env\Scripts\activate
```

### On MacOS/Linux:
```bash
python -m venv env
env\Scripts\activate
```

## Install dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup:
No initial setup is required for the database, as it will be created automatically when you run the project.

## Usage:
```bash
python password_manager.py
```
