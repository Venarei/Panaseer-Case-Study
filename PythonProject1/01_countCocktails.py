import requests
import string


def count_cocktails_by_letter():
    # Store count of cocktails for each letter
    cocktail_counts = {}

    # Loop through all letters from A to Z
    for letter in string.ascii_lowercase:
        # API and bring back dictionary list
        url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}'

        # GET request to the API
        try:
            response = requests.get(url)

            # Check response is successful
            if response.status_code == 200:
                data = response.json()

                # Check if the response contains KEY 'drinks' and get the count of items
                if 'drinks' in data:
                    drinks = data['drinks']
                    cocktail_counts[letter] = len(drinks)  # Store the count for each letter
                else:
                    cocktail_counts[letter] = 0  # No cocktails found for this letter
            else:
                print(f"Error: Failed to retrieve data for letter '{letter}'. Status Code: {response.status_code}")
                cocktail_counts[letter] = 0
        # Error Handling for Letter with no Count
        except Exception as e:
            print(f"Error: Could not make request for letter '{letter}'. Error: {e}")
            cocktail_counts[letter] = 0

    # Return counts of cocktails for each letter
    return cocktail_counts


# Get the count of cocktails for each letter A to Z
cocktail_counts = count_cocktails_by_letter()

# Print the result
for letter, count in cocktail_counts.items():
    print(f"Total cocktails starting with '{letter.upper()}': {count}")
