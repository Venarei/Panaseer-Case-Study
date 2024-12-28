import requests


def get_random_cocktail_sample(n):
    # List to store the random cocktails
    random_cocktails = []

    # Loop to get random cocktails
    for _ in range(n):
        # API for getting a random cocktail
        url = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'

        # GET request to the API
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()

            # Ensure the API returned a drink
            if 'drinks' in data and data['drinks']:
                random_drink = data['drinks'][0]

                # Append the cocktail data to the list
                random_cocktails.append(random_drink)
            else:
                print("No drink found.")
        else:
            print("Failed to retrieve data from the Cocktail DB API.")

    # Return the list of random cocktails
    return random_cocktails


#  Get a random sample of 5 cocktails
sample_size = 5
cocktails = get_random_cocktail_sample(sample_size)

# Display the random cocktails, fields just for display
for i, cocktail in enumerate(cocktails, 1):
    print(f"\nRandom Cocktail {i}:")
    print(f"Name: {cocktail['strDrink']}")
    print(f"Category: {cocktail['strCategory']}")
    print(f"Alcoholic: {cocktail['strAlcoholic']}")
    print(f"Instructions: {cocktail['strInstructions']}")
    print(f"Ingredients:")

    # Print out the ingredients
    for j in range(1, 16):
        ingredient = cocktail.get(f'strIngredient{j}')
        measure = cocktail.get(f'strMeasure{j}')
        if ingredient:
            print(f"- {measure if measure else ''} {ingredient}")