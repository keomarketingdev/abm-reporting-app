import streamlit as st
import pandas as pd
from datetime import datetime
import phonenumbers
import re

# --- 1. Custom CSS for Styling ---
def inject_custom_css():
    """Injects custom CSS for a blue sidebar, metric cards with hover, and typography."""
    
    PRIMARY_BLUE = "#1A73E8"
    LIGHT_BLUE_ACCENT = "#E6F0FF"

    st.markdown(f"""
    <style>
        /* 1. Overall Page Style and Font */
        .main-header {{
            color: #333;
            font-size: 2.5em;
            border-bottom: 2px solid {PRIMARY_BLUE};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        /* 2. Custom Metric Card Style (The "Box") */
        .metric-card {{
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid {LIGHT_BLUE_ACCENT};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
            height: 100%; /* Ensures cards in the same row are the same height */
        }}
        
        /* 3. Hover Effect */
        .metric-card:hover {{
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            border-left: 5px solid {PRIMARY_BLUE};
            cursor: pointer;
            transform: translateY(-2px);
        }}
        
        /* 4. Large Value Font Size (3em or 3x larger) */
        .big-number {{
            font-size: 3em !important; 
            font-weight: 700;
            color: #333; /* Black or dark gray for contrast */
            margin-top: 0.1em;
            margin-bottom: 0.1em;
        }}
        
        /* 5. Custom Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {PRIMARY_BLUE};
            color: white;
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        [data-testid="stSidebar"] h2 {{
            color: white;
            text-transform: uppercase;
        }}

        [data-testid="stSidebar"] button {{
            width: 180px;
            height: 40px;
            background-color: #1E90FF !important; /* Dodger Blue */
        }}
        
        /* 6. Main Header Styling */
        h1, h2, h3, h4 {{
            color: #333;
        }}
        
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Display Logic ---
def display_custom_metric(container, label, value):
    """
    Displays a custom metric card using markdown for precise styling.
    
    :param container: The Streamlit container (e.g., st.columns[0]) to draw in.
    :param label: The descriptive text (e.g., "Total Deliveries").
    :param value: The numerical value.
    """
    formatted_value = f"{float(value):,.0f}" # Format with comma separator
    
    with container:
        # Wrap in a div with the custom CSS class for the box and hover effect
        st.markdown(f"""
            <div class="metric-card">
                <p style="font-size: 1.1em; font-weight: 600; color: #555;">{label}</p>
                <p class="big-number">{formatted_value}</p>
            </div>
        """, unsafe_allow_html=True)

# --- Existing Page Functions ---
def format_phone_number(phone_number_str):
    if not phone_number_str or pd.isna(phone_number_str):
        return ""
    if isinstance(phone_number_str, float):
        phone_number_str = int(phone_number_str)
    try:
        parsed_number = phonenumbers.parse(str(phone_number_str), "US")
        if phonenumbers.is_valid_number(parsed_number):
            national_number_str = str(parsed_number.national_number)
            if parsed_number.country_code == 1 and len(national_number_str) == 10:
                return f"({national_number_str[:3]}) {national_number_str[3:6]}-{national_number_str[6:]}"
            else:
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.phonenumberutil.NumberParseException:
        try:
            parsed_number = phonenumbers.parse(str(phone_number_str), None)
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.phonenumberutil.NumberParseException:
            pass
    return str(phone_number_str)

def page_merge_and_deduplicate():
    st.header("Merge & Deduplicate CSVs")
    uploaded_files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True)
    if uploaded_files:
        try:
            dfs = [pd.read_csv(file) for file in uploaded_files]
            merged_df = pd.concat(dfs, ignore_index=True)
            st.write("Original number of rows:", len(merged_df))
            deduplicated_df = merged_df.drop_duplicates(subset=['Email'])
            st.write("Number of rows after deduplication:", len(deduplicated_df))
            st.session_state['deduplicated_df'] = deduplicated_df
            st.session_state['total_items'] = len(merged_df)
            st.session_state['removed_items'] = len(merged_df) - len(deduplicated_df)
            st.subheader("Merged and Deduplicated Data")
            st.dataframe(deduplicated_df)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def page_utn_reply_io_contacts_merger():
    st.header("UTN Reply.io Contacts Merger")
    uploaded_files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True, key="utn_merger_uploader")
    if uploaded_files:
        try:
            dfs = [pd.read_csv(file) for file in uploaded_files]
            merged_df = pd.concat(dfs, ignore_index=True)
            st.write("Original number of rows:", len(merged_df))
            deduplicated_df = merged_df.drop_duplicates(subset=['Email'])
            st.write("Number of rows after deduplication:", len(deduplicated_df))
            st.session_state['utn_deduplicated_df'] = deduplicated_df
            st.session_state['utn_total_items'] = len(merged_df)
            st.session_state['utn_removed_items'] = len(merged_df) - len(deduplicated_df)
            st.subheader("Merged and Deduplicated Data")
            st.dataframe(deduplicated_df)
        except Exception as e:
            st.error(f"An error occurred: {e}")



def page_process_and_transform():
    st.header("Cold: Lead Contacts")
    if 'deduplicated_df' not in st.session_state:
        st.warning("Please merge and deduplicate your CSV files on the 'Merge & Deduplicate' page first.")
        return
    df = st.session_state['deduplicated_df']
    transformed_data = []
    current_date = datetime.now().strftime("%m/%d/%Y")
    for index, row in df.iterrows():
        phone_number_raw = row.get('Phone', '')
        if pd.isna(phone_number_raw) or str(phone_number_raw).strip() == '' :
            phone_number_raw = row.get('Cell Phone', '')
        formatted_phone = format_phone_number(phone_number_raw)
        opens = row.get('Opens', 0)
        try:
            engagement_number = f"Total Opens: {int(opens)}"
        except (ValueError, TypeError):
            engagement_number = "Total Opens: 0"
        transformed_row = {
            'Date': current_date,
            'Recipient': f"{row.get('First Name', '')} {row.get('Last Name', '')}",
            'Company': row.get('Company', ''),
            'Title': row.get('Title', ''),
            'Phone Number': formatted_phone,
            'Email': row.get('Email', ''),
            'Engagement Number': engagement_number
        }
        transformed_data.append(transformed_row)
    transformed_df = pd.DataFrame(transformed_data)
    column_order = ['Date', 'Recipient', 'Company', 'Title', 'Phone Number', 'Email', 'Engagement Number']
    transformed_df = transformed_df[column_order]
    st.subheader("Final Transformed Data")
    st.dataframe(transformed_df)
    csv = transformed_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='transformed_data.csv',
        mime='text/csv',
    )

def page_utn_cold_contacts():
    st.header("UTN Cold Contacts")
    if 'utn_deduplicated_df' not in st.session_state:
        st.warning("Please merge and deduplicate your CSV files on the 'UTN Reply.io Contacts Merger' page first.")
        return
    df = st.session_state['utn_deduplicated_df']
    transformed_data = []
    current_date = datetime.now().strftime("%m/%d/%Y")
    for index, row in df.iterrows():
        phone_number_raw = row.get('Phone', '')
        if pd.isna(phone_number_raw) or str(phone_number_raw).strip() == '' :
            phone_number_raw = row.get('Cell Phone', '')
        formatted_phone = format_phone_number(phone_number_raw)
        opens = row.get('Opens', 0)
        try:
            engagement_number = f"Total Opens: {int(opens)}"
        except (ValueError, TypeError):
            engagement_number = "Total Opens: 0"
        transformed_row = {
            'Date': current_date,
            'Recipient': f"{row.get('First Name', '')} {row.get('Last Name', '')}",
            'Company': row.get('Company', ''),
            'Title': row.get('Title', ''),
            'Campaign': row.get('Sequence', ''),
            'Phone Number': formatted_phone,
            'Email': row.get('Email', ''),
            'Engagement Number': engagement_number
        }
        transformed_data.append(transformed_row)
    transformed_df = pd.DataFrame(transformed_data)
    column_order = ['Date', 'Recipient', 'Company', 'Title', 'Campaign', 'Phone Number', 'Email', 'Engagement Number']
    transformed_df = transformed_df[column_order]
    st.subheader("Final Transformed Data")
    st.dataframe(transformed_df)
    csv = transformed_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='transformed_data.csv',
        mime='text/csv',
    )






def page_abm_email_outreach_overview():
    st.header("Cold Email Overview")
    data_to_paste = st.text_area("Paste your data here", height=400)
    if st.button("Process Data"):
        if data_to_paste:
            try:
                columns = ["Sequence", "Delivery Rate", "Delivered", "Open Rate", "Opens", "Reply Rate", "Replies", "Click Rate", "Clicks", "Opt Out Rate", "Opt Outs", "not reached Rate", "Not reached", "Interested Rate", "Interested", "Meeting booked rate", "meetings booked", "bounced rate", "bounced"]
                lines = [line for line in data_to_paste.strip().split('\n') if line.strip()]
                blocks = [lines[i:i + 19] for i in range(0, len(lines), 19)]
                all_rows = []
                for block in blocks:
                    if len(block) == 19:
                        row_data = dict(zip(columns, block))
                        all_rows.append(row_data)
                if all_rows:
                    df = pd.DataFrame(all_rows)
                    df = df[columns]
                    st.subheader("Processed Data")
                    st.dataframe(df)
                    st.subheader("Summary")
                    summary_data = {
                        'Email Campaign Name': df['Sequence'],
                        'Subject': '',
                        'Deliveries': df['Delivered'],
                        'Delivery Rate': df['Delivery Rate'],
                        'Open Rate': df['Open Rate'],
                        'Reply Rate': df['Reply Rate'],
                        'Bounces': df['Not reached'],
                        'Opt-Outs': df['Opt Out Rate']
                    }
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df)
                    st.session_state['cold_total_deliveries'] = pd.to_numeric(df['Delivered'], errors='coerce').sum()
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name='processed_data.csv',
                        mime='text/csv',
                    )
                else:
                    st.warning("No data was extracted. Please check the format of your pasted data. Each record should have 19 lines.")
            except Exception as e:
                st.error(f"An error occurred while parsing the data: {e}")
        else:
            st.warning("Please paste some data to process.")

def page_campaign_performance():
    st.header("Warm: Email Overview")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("Detailed Campaign Performance")
            transformed_data = []
            current_date = datetime.now().strftime("%m/%d/%Y")
            for index, row in df.iterrows():
                transformed_row = {
                    'Date': current_date,
                    'Email Name': row.get('Email Name', ''),
                    'Subject': row.get('Subject', ''),
                    'Campaign': row.get('Campaign', ''),
                    'Internal HubSpot ID': row.get('All Internal HubSpot IDs', ''),
                    'Sent': row.get('Sent', 0),
                    'Delivered': row.get('Delivered', 0),
                    'Delivery Rate': f"{round(row.get('Delivery Rate', 0))}%" if pd.notna(row.get('Delivery Rate')) else "0%",
                    'Opened': row.get('Opened', 0),
                    'Open Rate': f"{round(row.get('Open Rate', 0))}%" if pd.notna(row.get('Open Rate')) else "0%",
                    'Clicked': row.get('Clicked', 0),
                    'Click Rate': f"{round(row.get('Click Rate', 0))}%" if pd.notna(row.get('Click Rate')) else "0%",
                    'Click Through Rate': f"{round(row.get('Click Through Rate', 0))}%" if pd.notna(row.get('Click Through Rate')) else "0%",
                    'Replied': row.get('Replied', 0),
                    'Reply Rate': f"{round(row.get('Reply Rate', 0))}%" if pd.notna(row.get('Reply Rate')) else "0%",
                    'Not Sent': row.get('Not Sent', 0),
                    'Hard Bounced': row.get('Hard Bounced', 0),
                    'Soft Bounced': row.get('Soft Bounced', 0),
                    'Spam Reports': row.get('Spam reports', 0),
                    'Spam Rate': f"{round(row.get('Spam rate', 0))}%" if pd.notna(row.get('Spam rate')) else "0%",
                    'Unsubscribed': row.get('Unsubscribed', 0),
                    'Send Date (Your time zone)': row.get('Send Date (Your time zone)', ''),
                    'Simple Campaign Name': row.get('Email Name', '')
                }
                transformed_data.append(transformed_row)
            transformed_df = pd.DataFrame(transformed_data)
            st.dataframe(transformed_df)
            st.subheader("Summary")
            summary_data = []
            for index, row in df.iterrows():
                sent = row.get('Sent', 0)
                unsubscribed = row.get('Unsubscribed', 0)
                if sent > 0:
                    opt_out_rate = (unsubscribed / sent) * 100
                else:
                    opt_out_rate = 0
                summary_row = {
                    'Email Campaign Name': row.get('Email Name', ''),
                    'Subject': '',
                    'Deliveries': sent,
                    'Delivery Rate': f"{round(row.get('Delivery Rate', 0))}%" if pd.notna(row.get('Delivery Rate')) else "0%",
                    'Open Rate': f"{round(row.get('Open Rate', 0))}%" if pd.notna(row.get('Open Rate')) else "0%",
                    'Reply Rate': f"{round(row.get('Reply Rate', 0))}%" if pd.notna(row.get('Reply Rate')) else "0%",
                    'Bounces': row.get('Hard Bounced', 0) + row.get('Soft Bounced', 0),
                    'Opt-Outs': f"{round(opt_out_rate, 2)}%"
                }
                summary_data.append(summary_row)
            summary_df = pd.DataFrame(summary_data)
            summary_df = summary_df.sort_values(by='Email Campaign Name')
            st.dataframe(summary_df)
            st.session_state['warm_total_sent'] = df['Sent'].sum()
            if st.button("Copy Table"):
                st.text_area("Copied!", transformed_df.to_csv(sep='\t', index=False), height=200)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- 3. Main Streamlit App ---
def main():
    # 3a. Configuration and CSS Injection
    st.set_page_config(
        page_title="ABM Report Generator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    inject_custom_css()
    
    # 3b. UI Structure
    
    # Sidebar content (now blue)
    with st.sidebar:
        st.header("Navigation")
        st.divider()
        
        if 'page' not in st.session_state:
            st.session_state.page = 'Home'

        if st.button("Home"):
            st.session_state.page = 'Home'
        st.markdown("COLD Campaign (KEO, Oneness)")
        if st.button("Merge & Deduplicate"):
            st.session_state.page = 'Merge & Deduplicate'
        if st.button("Cold: Lead Contacts"):
            st.session_state.page = 'Cold: Lead Contacts'
        if st.button("UTN Reply.io Contacts Merger"):
            st.session_state.page = 'UTN Reply.io Contacts Merger'
        if st.button("UTN Cold Contacts"):
            st.session_state.page = 'UTN Cold Contacts'
        if st.button("Cold Email Overview"):
            st.session_state.page = 'Cold Email Overview'
        if st.button("Warm: Email Overview"):
            st.session_state.page = 'Warm: Email Overview'

    page = st.session_state.page

    if page == "Home":
        st.markdown('<h1 class="main-header">Account Based Marketing Analytics</h1>', unsafe_allow_html=True)
        st.header("Summary Report Overview")
        st.caption("A high-level view of key metrics from ABM and Email Campaigns.")
        st.divider()

        # ABM Report Generator Summary
        st.subheader("ABM Report Generator Summary")
        abm_col1, abm_col2 = st.columns(2)
        
        display_custom_metric(
            abm_col1, 
            "Total Items Listed", 
            st.session_state.get('total_items', 0)
        )
        
        display_custom_metric(
            abm_col2, 
            "Deduplicated Items Removed", 
            st.session_state.get('removed_items', 0)
        )

        st.divider()

        # Email Campaign Overview Summary
        st.subheader("Email Campaign Overview Summary")
        email_col1, email_col2 = st.columns(2)
        
        display_custom_metric(
            email_col1, 
            "Total Cold Deliveries", 
            st.session_state.get('cold_total_deliveries', 0)
        )
        
        display_custom_metric(
            email_col2, 
            "Total Warm Emails Sent", 
            st.session_state.get('warm_total_sent', 0)
        )

        st.divider()

    elif page == "Merge & Deduplicate":
        page_merge_and_deduplicate()
    elif page == "UTN Reply.io Contacts Merger":
        page_utn_reply_io_contacts_merger()
    elif page == "Cold: Lead Contacts":
        page_process_and_transform()
    elif page == "UTN Cold Contacts":
        page_utn_cold_contacts()
    elif page == "Cold Email Overview":
        page_abm_email_outreach_overview()
    elif page == "Warm: Email Overview":
        page_campaign_performance()

if __name__ == "__main__":
    main()