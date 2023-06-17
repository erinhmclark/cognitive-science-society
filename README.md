# cognitive-science-society

A scraper to collect the blog posts from https://cognitivesciencesociety.org/blog/ and insert the results into a database.

# Cognitive Science Society Blog Scraper

This project is a web scraper for the Cognitive Science Society blog. 
It extracts blog details such as the title, date published, link, tags, and full text, and stores them in a MySQL database.

## Features

- Scrapes the Cognitive Science Society blog
- Extracts blog details including the title, date of publication, link, tags, and full text
- Stores the data in a MySQL database
- Uses Beautiful Soup for HTML parsing

## Getting Started

These instructions will guide you through setting up the project and running the scraper on your local machine.

### Prerequisites

This project requires:

- Python 3.8+
- Poetry for Python dependency management
- MySQL 5.7+ 

### Project Setup

1. **Clone the Repository:** Clone this repository to your local machine:

    ```
    git clone https://github.com/erinhmclark/cognitive-science-society.git
    cd projectname
    ```

2. **Install Poetry:** If you don't already have Poetry installed, you can install it with:

    ```
    curl -sSL https://install.python-poetry.org | python -
    ```

    For more detailed installation instructions, see the [Poetry documentation](https://python-poetry.org/docs/#installation).

3. **Install Dependencies:** Install the project's dependencies with:

    ```
    poetry install
    ```

4. **Activate the Virtual Environment:** Start the Poetry shell with:

    ```
    poetry shell
    ```

### Database Setup

1. **Install MySQL:** If you don't already have MySQL installed, you can download it from the [official website](https://dev.mysql.com/downloads/installer/).

2. **Configure MySQL:** Make sure your MySQL server is running and correctly configured. You'll need to know your MySQL user name, password, host, and database name to connect to the database.
3. **Setting up Environment Variables:** Open the .env.template file and modify it with your secret variables. Save the modified .env.template file as .env. **NOTE:** This file must be named '.env' or the file name used must be added to the file '.gitignore' to ensure security of your credentials.
4. **Run Database Setup Script:** Run the `database_setup.py` script with Python to set up the necessary database tables:

    ```
    python database_setup.py
    ```

### Running the Scraper

With the setup complete, you can now run the scraper:
```
python cognitive_science_society_scraper.py 
```
