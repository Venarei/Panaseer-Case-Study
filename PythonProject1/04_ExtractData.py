import requests
import string
import logging
import pandas as pd
import csv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Create logs to a CSV file
class CSVLogHandler(logging.Handler):
    def __init__(self, csv_filename):
        super().__init__()
        self.csv_filename = csv_filename
        # Ensure the CSV file exists and create it if not
        with open(self.csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header row
            writer.writerow(['Timestamp', 'Log Level', 'Message'])

    def emit(self, record):
        """Override to write logs to the CSV file."""
        log_message = self.format(record)
        log_time = record.asctime
        log_level = record.levelname
        message = record.message

        # Write the log to the CSV file
        with open(self.csv_filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([log_time, log_level, message])


# CSV log handler
log_csv_file = 'Logs/info.csv'
csv_handler = CSVLogHandler(log_csv_file)
csv_handler.setLevel(logging.INFO)

# Logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
csv_handler.setFormatter(formatter)

# Add the CSV handler to the root logger
logging.getLogger().addHandler(csv_handler)


def fetch_drinks_by_letter(letter):
    """Drinks from API by Letter."""
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
    header = {"Content-Type": "application/json", "Accept-Encoding": "deflate"}

    try:
        # GET request to the API
        logging.info(f"Sending request for letter '{letter.upper()}'.")
        response = requests.get(url, headers=header)

        # response is successful?
        if response.status_code == 200:
            data = response.json()

            if 'drinks' in data:
                logging.info(f"Successfully fetched drinks starting with '{letter.upper()}'.")
                return data['drinks']
            else:
                logging.warning(f"No drinks found for letter '{letter.upper()}'.")
                return None
        else:
            logging.error(f"Error: Failed to retrieve data for letter '{letter}'. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: Could not make request for letter '{letter}'. Error: {e}")
        return None


def fetch_all_drinks():
    """Fetch all drinks from A to Z and return the results in a list."""
    all_drinks = []

    # Loop through all letters from A to Z
    for letter in string.ascii_lowercase:
        logging.info(f"Fetching drinks starting with '{letter.upper()}':")
        drinks = fetch_drinks_by_letter(letter)

        # If drinks are found, add them to the all_drinks list
        if drinks:
            all_drinks.extend(drinks)
        else:
            logging.warning(f"No drinks found for letter '{letter.upper()}'.")

    return all_drinks


def save_drinks_to_csv(drinks, filename="RawFiles/cocktails.csv"):
    """Save to a CSV file."""
    if drinks:
        # Normalize the nested JSON data into a flat table
        df = pd.json_normalize(drinks)

        # DataFrame to a CSV file with UTF-8 encoding
        df.to_csv(filename, index=False, encoding='utf-8')
        logging.info(f"Data successfully saved to {filename}.")
    else:
        logging.warning("No drinks data to save.")


# Main save to CSV
if __name__ == "__main__":
    logging.info("Starting to fetch drinks data...")

    # Get all drinks data
    all_drinks = fetch_all_drinks()

    # Save the drinks data to a CSV file
    save_drinks_to_csv(all_drinks)

    logging.info("Data fetching and saving complete.")
