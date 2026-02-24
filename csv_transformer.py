
import pandas as pd
from datetime import datetime
import sys

def transform_csv(file_path):
    """
    Reads a CSV file, transforms the data, and prints a tab-delimited table.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        transformed_data = []

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        for index, row in df.iterrows():
            # Handle phone number logic
            phone_number = row.get('Phone', '')
            if pd.isna(phone_number) or str(phone_number).strip() == '' :
                phone_number = row.get('Cell Phone', '')

            # Create the transformed row
            transformed_row = {
                'Date': current_date,
                'Recipient': f"{row.get('First Name', '')} {row.get('Last Name', '')}",
                'Company': row.get('Company', ''),
                'Title': row.get('Title', ''),
                'Phone Number': phone_number,
                'Email': row.get('Email', ''),
                'Engagement Number': f"Total Opens: {row.get('Opens', 0)}"
            }
            transformed_data.append(transformed_row)

        # Create a new DataFrame with the transformed data
        transformed_df = pd.DataFrame(transformed_data)

        # Print the output as a tab-separated string
        print("\n--- Copy the table below and paste it into Google Sheets ---")
        print(transformed_df.to_csv(sep='\t', index=False))

    except FileNotFoundError:
        print(f"\nError: The file at '{file_path}' was not found.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        transform_csv(file_path)
    else:
        print("Usage: python3 csv_transformer.py <path_to_your_csv_file>")
