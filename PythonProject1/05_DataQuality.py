import csv
import string

#  special characters
special_characters = string.punctuation


def find_fields_with_special_chars_csv(file_path):
    fields_with_special_chars = {}  # Store fields and counts with special chars

    # Open the CSV file created from 04_Extract
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Rows in CSV
        for row in reader:
            for field, value in row.items():
                # Count special characters in field
                count = sum(1 for char in value if char in special_characters)

                if count > 0:
                    if field not in fields_with_special_chars:
                        fields_with_special_chars[field] = count
                    else:
                        fields_with_special_chars[field] += count

    return fields_with_special_chars


# My Raw CSV File
file_path = r'C:\Users\Bosto\PycharmProjects\PythonProject1\RawFiles\cocktails.csv'
fields_with_counts = find_fields_with_special_chars_csv(file_path)

# Print the result
if fields_with_counts:
    print("Fields with Special Characters and Their Counts:")
    for field, count in fields_with_counts.items():
        print(f"Field: {field}, Special Characters Count: {count}")
else:
    print("No fields with special characters were found.")