# cognitive-science-society

A scraper to collect the blog posts from https://cognitivesciencesociety.org/blog/ and insert the results into a database.

## Project Setup

This project uses Poetry for dependency management. To set up the project:

1. Install Poetry if you haven't already (see https://python-poetry.org/docs/#installation for instructions).
2. Clone the repository and navigate into the project directory.
3. Run `poetry install` to install the project's dependencies.
4. Activate the Poetry shell with `poetry shell`.

## Database Setup

Before you can run the scraper, you'll need to set up the database:

1. Ensure you have MySQL installed and running.
2. Run the `database_setup.py` script with Python (`python database_setup.py`). Make sure to do this within the Poetry shell, so that the necessary dependencies are available.

With both of these steps completed, you should be ready to run the scraper.
