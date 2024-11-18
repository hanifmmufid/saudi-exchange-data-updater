# Saudi Exchange Data Updater

This project updates data for Saudi Exchange by pulling information from an external API and inserting it into a Google Sheet. The script fetches data from the latest available date and updates it until the current date.

## Requirements

### Software Requirements:
- **Python 3.7+**
- **pip (Python Package Installer)**

### Install Python:

1. Download Python from [python.org](https://www.python.org/downloads/).
2. Follow the installation instructions for your operating system.
   - **Windows**: Make sure to check the box `Add Python to PATH` during installation.
   - **Mac/Linux**: Python is often pre-installed, but you may want to update it using `brew` (Mac) or package managers like `apt` (Linux).

### Install Dependencies:

1. Ensure you have a `requirements.txt` file with all the necessary packages in the project directory.
2. To install the required packages, run the following command in the terminal:

   ```bash
   pip install -r requirements.txt
   ```
## Running the Script

1. Open a terminal in the project directory.

2. (Optional but recommended) Create and activate a **virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```
3. Ensure that you have a Google Sheet set up for the script to update. You need to update the sheet_id variable in the Python script with your Google Sheet ID (found in the URL of your Google Sheet).

4. Run the Python script:
   ```bash
   python main.py
   ```
   - The script will fetch data from the API and insert it into your Google Sheet.
   - It will update data from the latest available date to the current date.

5. How the script works:
   - The script checks the most recent date in the Google Sheet and only fetches new data since that date.
   - The data will be added to the sheet, with the most recent data at the top.

6. To update the sheet with the latest data, simply re-run the script as needed.
