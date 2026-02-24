import pandas as pd

def email_campaign_reporting():
    """
    Calculates key email campaign metrics from a CSV file and outputs a tab-delimited table.
    """
    # 1. Get User Input
    sequence_name = input("Enter the Sequence Name: ")
    file_path = input("Enter the CSV file path: ")

    try:
        # 2. Read the CSV file
        df = pd.read_csv(file_path)

        # 3. Assume the first row contains aggregated data
        if not df.empty:
            first_row = df.iloc[0]
        else:
            print("Error: CSV file is empty.")
            return

        # 4. Extract and clean data from the first row
        total_sent = pd.to_numeric(first_row.get('Total Sent'), errors='coerce')
        total_sent = int(pd.Series(total_sent).fillna(0).iloc[0])

        delivered = pd.to_numeric(first_row.get('Delivered'), errors='coerce')
        delivered = int(pd.Series(delivered).fillna(0).iloc[0])

        opened = pd.to_numeric(first_row.get('Opened'), errors='coerce')
        opened = int(pd.Series(opened).fillna(0).iloc[0])

        replied = pd.to_numeric(first_row.get('Replied'), errors='coerce')
        replied = int(pd.Series(replied).fillna(0).iloc[0])

        bounced = pd.to_numeric(first_row.get('Bounced'), errors='coerce')
        bounced = int(pd.Series(bounced).fillna(0).iloc[0])

        opted_out = pd.to_numeric(first_row.get('Opted Out'), errors='coerce')
        opted_out = int(pd.Series(opted_out).fillna(0).iloc[0])


        # 5. Calculate metrics with division-by-zero handling
        delivery_rate = (delivered / total_sent) * 100 if total_sent > 0 else 0
        open_rate = (opened / delivered) * 100 if delivered > 0 else 0
        reply_rate = (replied / delivered) * 100 if delivered > 0 else 0
        opt_out_rate = (opted_out / delivered) * 100 if delivered > 0 else 0

        # 6. Format the output
        header = "Sequence\tDelivered\tDelivery Rate\tOpen Rate\tReply Rate\tBounced\tOpt Out Rate"
        
        data_row = (
            f"{sequence_name}\t"
            f"{delivered}\t"
            f"{delivery_rate:.2f}%\t"
            f"{open_rate:.2f}%\t"
            f"{reply_rate:.2f}%\t"
            f"{bounced}\t"
            f"{opt_out_rate:.2f}%"
        )

        # 7. Print the formatted output
        print("\n--- Copy the table below and paste it into Google Sheets ---")
        print(header)
        print(data_row)

    except FileNotFoundError:
        print(f"\nError: The file at '{file_path}' was not found.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    email_campaign_reporting()