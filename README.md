# libmanager

## Overview

This is a small library management application designed for home usage. It allows users to manage a collection of books, track users, rent out books, and check which users have borrowed which books. The application is written in Python using the PySide6 library for the graphical user interface, and it uses an SQLite database for data storage.

## Features

- **Add Books**: Easily add new books to your library collection.
- **Add Users**: Manage users who can borrow books from the library.
- **Rent Books and return**: Keep track of which books are rented out and to whom.
- **Check Rentals**: View the current status of all rented books and see who has borrowed them.

## Technologies Used

- **Python**: The core programming language used for developing the application.
- **PySide6**: A Python binding for the Qt framework, used to create the graphical user interface (GUI).
- **SQLite**: A lightweight, disk-based database used for storing all data related to books, users, and rentals.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- `pip` (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AdamJakubczak/libmanager.git
   cd libmanager

2. Install requirements:

   ```bash
   pip install -r requirements.txt

3. Run the application

   ```bash
   python run.py

