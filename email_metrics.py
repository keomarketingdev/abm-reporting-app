
import pandas as pd

def calculate_metrics(file_path, sequence_name):
    """
    Reads a CSV file, calculates email campaign metrics, and returns a tab-delimited string.

    Args:
        file_path (str): The path to the CSV file.
        sequence_name (str): The name of the email sequence.

    Returns:
        str: A tab-delimited string of the calculated metrics.
    """
    try:
        df = pd.read_csv(file_path)

        # Assuming the first row contains aggregated data
        first_row = df.iloc[0]

        total_sent = int(first_row.get('Total Sent', 0))
        delivered = int(first_row.get('Delivered', 0))
        opened = int(first_row.get('Opened', 0))
        replied = int(first_row.get('Replied', 0))
        bounced = int(first_row.get('Bounced', 0))
        opted_out = int(first_row.get('Opted Out', 0))

        delivery_rate = (delivered / total_sent) * 100 if total_sent > 0 else 0
        open_rate = (opened / delivered) * 100 if delivered > 0 else 0
        reply_rate = (replied / delivered) * 100 if delivered > 0 else 0
        opt_out_rate = (opted_out / delivered) * 100 if delivered > 0 else 0

        # Format the output string
        output = f"{sequence_name}\t"
        output += f"{delivered}\t"
        output += f"{delivery_rate:.2f}%\t"
        output += f"{open_rate:.2f}%\t"
        output += f"{reply_rate:.2f}%\t"
        output += f"{bounced}\t"
        output += f"{opt_out_rate:.2f}%"

        return output

    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    sequence_name = input("Enter the Sequence Name: ")
    file_path = input("Enter the CSV file path: ")
    
    # Create a dummy CSV for testing if it doesn't exist
    try:
        pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Creating a dummy CSV file at: {file_path}")
        dummy_data = {
            'Total Sent': [1000],
            'Delivered': [950],
            'Opened': [350],
            'Replied': [50],
            'Bounced': [50],
            'Opted Out': [20]
        }
        dummy_df = pd.DataFrame(dummy_data)
        dummy_df.to_csv(file_path, index=False)


    metrics_output = calculate_metrics(file_path, sequence_name)

    # Print the header
    header = "Sequence\tDelivered\tDelivery Rate\tOpen Rate\tReply Rate\tBounced\tOpt Out Rate"
    print(header)
    print(metrics_output)
