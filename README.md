# Expense Tracking Project
==========================

A simple web application for personal or small-scale expense tracking, built using Python and Flask.

## Table of Contents
-----------------

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Overview
------------

This project provides a basic expense tracking system, allowing users to manage their expenses with ease. It includes user authentication, expense CRUD operations, categorization, and simple filtering.

## Features
------------

* **User Authentication**: Secure registration and login functionality
* **Expense Management**: Create, Read, Update, and Delete expenses
* **Categorization**: Predefined categories for organizing expenses (e.g., Food, Transportation, Entertainment)
* **Filtering**: View expenses by category

## Technologies Used
--------------------

* **Backend**: Python, Flask, Flask-Login, Flask-SQLAlchemy
* **Database**: SQLite (using Flask-SQLAlchemy for ORM)
* **Frontend**: Basic HTML, CSS
* **Templates**: Jinja2 (for HTML templating, comes bundled with Flask)

## Getting Started
-------------------

1. **Clone the repository**: `git clone https://github.com/N3tup/Expense-Tracking-project.git`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Initialize the database**: `flask db init` (then apply migrations if any)
4. **Run the application**: `flask run`

## Usage
---------

1. **Register** a new user: `/register`
2. **Login** to the platform: `/login`
3. **Create** a new expense: `/expenses/new`
4. **View** all expenses: `/expenses`
5. **Filter** expenses by category: `/expenses?category=<category_name>`

## Contributing
------------

Contributions are welcome! If you'd like to report an issue or suggest a feature, please:

1. **Open an issue** on this repository's issue tracker
2. **Fork the repository** and submit a pull request with your changes

## License
-------

Romain BOUCHEZ, ESIEA
