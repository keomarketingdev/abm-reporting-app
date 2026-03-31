import streamlit as st
import pandas as pd
from datetime import datetime
import phonenumbers
import re

# --- 1. Custom CSS for Styling ---
def inject_custom_css(theme="light"):
    """Injects custom CSS matching KEO Marketing website branding."""

    PRIMARY_BLUE = "#163b70"
    DEEP_BLUE = "#0e2a52"
    ACCENT_ORANGE = "#e78627"
    DARK_ORANGE = "#d47220"
    LIGHT_BG = "#f4f6f9"
    WHITE = "#ffffff"
    DARK_BG = "#111827"
    DARK_CARD = "#1e293b"
    DARK_TEXT = "#e2e8f0"
    LIGHT_BORDER = "#e2e8f0"

    # Determine colors based on theme
    if theme == "dark":
        bg_color = DARK_BG
        card_color = DARK_CARD
        text_color = DARK_TEXT
        text_secondary = "#94a3b8"
        header_color = WHITE
        border_color = "#163b70"
        input_bg = "#1e293b"
        input_border = "#475569"
        section_alt_bg = "#0f172a"
    else:
        bg_color = LIGHT_BG
        card_color = WHITE
        text_color = "#163b70"
        text_secondary = "#64748b"
        header_color = PRIMARY_BLUE
        border_color = LIGHT_BORDER
        input_bg = WHITE
        input_border = "#cbd5e1"
        section_alt_bg = WHITE

    st.markdown(f"""
    <style>
        /* ===== GOOGLE FONTS IMPORT ===== */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

        /* ===== 0. RESET & BASE ===== */
        *:not([data-testid="stIconMaterial"]), *::before, *::after {{
            font-family: 'Outfit', sans-serif !important;
        }}

        /* Preserve Streamlit Material icon font */
        [data-testid="stIconMaterial"] {{
            font-family: 'Material Symbols Rounded' !important;
        }}

        .main {{
            background-color: {bg_color} !important;
        }}

        html, body {{
            background-color: {bg_color} !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color} !important;
        }}

        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: transparent !important;
        }}

        /* Base text color */
        * {{
            color: {text_color} !important;
        }}

        /* Header bar text & icons - light color */
        [data-testid="stHeader"],
        [data-testid="stHeader"] *,
        [data-testid="stToolbar"] *,
        [data-testid="stAppDeployButton"] *,
        [data-testid="stMainMenu"] *,
        [data-testid="stBaseButton-header"] *,
        [data-testid="stBaseButton-headerNoPadding"] *,
        [data-testid="stMainMenuButton"] * {{
            color: {text_secondary} !important;
            fill: {text_secondary} !important;
        }}

        /* Replace hamburger menu icon with settings gear + blue color */
        [data-testid="stMainMenuButton"] svg {{
            display: none !important;
        }}

        [data-testid="stMainMenuButton"]::before {{
            content: '\\e8b8';
            font-family: 'Material Symbols Rounded' !important;
            font-size: 24px;
            color: {PRIMARY_BLUE} !important;
            -webkit-font-smoothing: antialiased;
        }}

        [data-testid="stMainMenuButton"] {{
            color: {PRIMARY_BLUE} !important;
        }}

        /* ===== 1. TYPOGRAPHY ===== */
        h1 {{
            color: {header_color} !important;
            font-weight: 800 !important;
            font-size: 40px !important;
            letter-spacing: -0.03em !important;
        }}

        h2 {{
            color: {header_color} !important;
            font-weight: 700 !important;
            font-size: 1.5em !important;
            letter-spacing: -0.02em !important;
        }}

        h3, h4, h5, h6 {{
            color: {header_color} !important;
            font-weight: 600 !important;
        }}

        p {{
            color: {text_color} !important;
            line-height: 1.7 !important;
            font-size: 0.9em !important;
        }}

        span {{
            color: {text_color} !important;
        }}

        small, caption {{
            color: {text_secondary} !important;
            font-size: 0.85em !important;
        }}

        /* ===== 2. MAIN HEADER (Home page hero) ===== */
        .main-header {{
            color: {header_color} !important;
            font-size: 2.6em !important;
            font-weight: 900 !important;
            letter-spacing: -0.03em;
            padding-bottom: 16px;
            margin-bottom: 8px;
            position: relative;
        }}

        .main-header::after {{
            content: '';
            display: block;
            width: 80px;
            height: 4px;
            background: {ACCENT_ORANGE};
            border-radius: 2px;
            margin-top: 16px;
        }}

        /* ===== 3. PAGE HEADER BAR ===== */
        .page-header-bar {{
            background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, {DEEP_BLUE} 100%);
            padding: 32px 40px;
            border-radius: 16px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }}

        .page-header-bar::before {{
            content: '';
            position: absolute;
            top: -30px;
            right: -30px;
            width: 120px;
            height: 120px;
            background: rgba(231, 134, 39, 0.15);
            border-radius: 50%;
        }}

        .page-header-bar::after {{
            content: '';
            position: absolute;
            bottom: -20px;
            right: 60px;
            width: 80px;
            height: 80px;
            background: rgba(231, 134, 39, 0.1);
            border-radius: 50%;
        }}

        div.page-header-bar h2,
        div.page-header-bar h2 span,
        .page-header-bar h2 {{
            color: white !important;
            font-size: 40px !important;
            font-weight: 800 !important;
            margin: 0 !important;
            letter-spacing: -0.02em;
        }}

        div.page-header-bar p,
        div.page-header-bar p span,
        .page-header-bar p {{
            color: rgba(255,255,255,0.8) !important;
            font-size: 0.95em !important;
            margin-top: 6px !important;
        }}

        .page-header-bar .orange-accent {{
            color: {ACCENT_ORANGE} !important;
            font-weight: 700;
        }}

        /* ===== 4. METRIC CARDS ===== */
        .metric-card {{
            background: {card_color};
            padding: 28px 24px;
            border-radius: 16px;
            border: 1px solid {border_color};
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, {ACCENT_ORANGE}, {DARK_ORANGE});
            border-radius: 4px 0 0 4px;
        }}

        .metric-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 12px 28px rgba(22, 59, 112, 0.08);
            transform: translateY(-4px);
        }}

        .metric-label {{
            font-size: 0.8em !important;
            font-weight: 700 !important;
            color: {text_secondary} !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }}

        .big-number {{
            font-size: 2.8em !important;
            font-weight: 900 !important;
            color: {ACCENT_ORANGE} !important;
            margin: 0 !important;
            letter-spacing: -0.03em;
            line-height: 1.1 !important;
        }}

        /* ===== 5. SECTION CARD WRAPPER ===== */
        .section-card {{
            background: {card_color};
            border-radius: 16px;
            padding: 32px;
            border: 1px solid {border_color};
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            margin-bottom: 24px;
        }}

        .section-card h3 {{
            font-size: 1.15em !important;
            font-weight: 700 !important;
            margin-bottom: 20px !important;
            padding-bottom: 12px;
            border-bottom: 2px solid {border_color};
        }}

        /* ===== 6. SIDEBAR ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_BLUE} 0%, {DEEP_BLUE} 100%) !important;
        }}

        [data-testid="stSidebar"] * {{
            color: white !important;
        }}

        [data-testid="stSidebar"] [role="region"] {{
            padding: 0px !important;
        }}

        /* Hide sidebar collapse icon above logo */
        [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        /* Sidebar logo */
        [data-testid="stSidebar"] .stImage {{
            margin-bottom: 8px !important;
            padding: 12px 16px 0 16px !important;
        }}

        [data-testid="stSidebar"] .stImage img {{
            border-radius: 0 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stImageToolbar"] {{
            display: none !important;
        }}

        .sidebar-logo img {{
            border-radius: 0 !important;
            width: 250px;
        }}

        /* Navigation header */
        [data-testid="stSidebar"] h2 {{
            color: rgba(255,255,255,0.5) !important;
            text-transform: uppercase;
            font-size: 0.75em !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            padding: 0 16px !important;
        }}

        /* Sidebar nav buttons */
        [data-testid="stSidebar"] button {{
            width: 100%;
            min-height: 44px !important;
            height: auto !important;
            background-color: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            font-size: 0.9em !important;
            color: rgba(255, 255, 255, 0.9) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 4px !important;
            text-align: left !important;
            padding: 10px 16px !important;
            box-sizing: border-box !important;
        }}

        [data-testid="stSidebar"] button:hover {{
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            transform: translateX(3px) !important;
        }}

        [data-testid="stSidebar"] button p {{
            text-align: left !important;
            width: 100% !important;
            color: rgba(255, 255, 255, 0.9) !important;
        }}

        /* Active nav button */
        [data-testid="stSidebar"] button[kind="primary"] {{
            background: linear-gradient(135deg, {ACCENT_ORANGE}, {DARK_ORANGE}) !important;
            border: none !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(231, 134, 39, 0.3) !important;
        }}

        [data-testid="stSidebar"] button[kind="primary"] p,
        [data-testid="stSidebar"] button[kind="primary"] span,
        [data-testid="stSidebar"] button[kind="primary"] {{
            color: white !important;
        }}

        [data-testid="stSidebar"] button[kind="primary"]:hover {{
            background: linear-gradient(135deg, {DARK_ORANGE}, #c4611a) !important;
            transform: none !important;
        }}

        /* Nav section headers */
        .nav-section-header {{
            color: rgba(255, 255, 255, 0.45) !important;
            font-size: 0.7em !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            margin-top: 24px !important;
            margin-bottom: 8px !important;
            padding-left: 16px !important;
            padding-bottom: 0 !important;
            border-bottom: none !important;
            display: block !important;
        }}

        .nav-section-divider {{
            margin: 0 16px 8px 16px !important;
            border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
        }}

        /* ===== 7. MAIN CONTENT BUTTONS ===== */
        [data-testid="stMainBlockContainer"] button {{
            background: linear-gradient(135deg, {ACCENT_ORANGE}, {DARK_ORANGE}) !important;
            color: {WHITE} !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.9em !important;
            padding: 10px 24px !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(231, 134, 39, 0.2) !important;
            letter-spacing: 0.01em !important;
        }}

        [data-testid="stMainBlockContainer"] button:hover {{
            background: linear-gradient(135deg, {DARK_ORANGE}, #c4611a) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(231, 134, 39, 0.3) !important;
        }}

        [data-testid="stMainBlockContainer"] button p {{
            color: {WHITE} !important;
        }}

        /* ===== 8. DIVIDERS ===== */
        hr {{
            border: none !important;
            height: 1px !important;
            background: {border_color} !important;
            margin: 28px 0 !important;
        }}

        /* ===== 9. INPUT & FORM ELEMENTS ===== */
        input, select {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 1.5px solid {input_border} !important;
            border-radius: 10px !important;
            padding: 10px 14px !important;
            font-size: 0.9em !important;
            transition: border-color 0.2s ease !important;
        }}

        input:focus, select:focus {{
            border-color: {ACCENT_ORANGE} !important;
            box-shadow: 0 0 0 3px rgba(231, 134, 39, 0.1) !important;
        }}

        textarea {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 1.5px solid {input_border} !important;
            border-radius: 12px !important;
            font-size: 0.9em !important;
        }}

        textarea:focus {{
            border-color: {ACCENT_ORANGE} !important;
            box-shadow: 0 0 0 3px rgba(231, 134, 39, 0.1) !important;
        }}

        /* ===== 10. FILE UPLOADER ===== */
        [data-testid="stFileUploaderDropzone"] {{
            background-color: {input_bg} !important;
            border: 2px dashed {input_border} !important;
            border-radius: 14px !important;
            padding: 28px !important;
            transition: all 0.25s ease !important;
        }}

        [data-testid="stFileUploaderDropzone"]:hover {{
            border-color: {ACCENT_ORANGE} !important;
            background-color: {"rgba(231, 134, 39, 0.03)" if theme == "light" else "rgba(231, 134, 39, 0.05)"} !important;
        }}

        [data-testid="stFileUploaderDropzone"] div {{
            background-color: transparent !important;
        }}

        [data-testid="stFileUploaderDropzone"] span {{
            color: {text_secondary} !important;
        }}

        [data-testid="stFileUploaderDropzone"] button {{
            background: {card_color} !important;
            color: {PRIMARY_BLUE} !important;
            border: 1.5px solid {input_border} !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            padding: 6px 16px !important;
        }}

        [data-testid="stFileUploaderDropzone"] button:hover {{
            background: {LIGHT_BG if theme == "light" else "#163b70"} !important;
            border-color: {ACCENT_ORANGE} !important;
            transform: none !important;
            box-shadow: none !important;
        }}

        [data-testid="stFileUploaderDropzone"] button p {{
            color: {PRIMARY_BLUE if theme == "light" else DARK_TEXT} !important;
        }}

        /* ===== 11. DATAFRAME ===== */
        [data-testid="dataframe"] {{
            background-color: {card_color} !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid {border_color} !important;
        }}

        /* ===== 12. TABS ===== */
        [data-testid="stTabs"] {{
            background-color: transparent !important;
        }}

        /* ===== 13. ALERT BOXES ===== */
        [data-testid="stAlert"] {{
            border-radius: 12px !important;
            border-left-width: 4px !important;
            font-size: 0.9em !important;
        }}

        /* ===== 14. THEME TOGGLE ===== */
        .st-key-theme_toggle_wrap {{
            background-color: transparent !important;
        }}

        .st-key-theme_toggle_wrap button {{
            background: {PRIMARY_BLUE} !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 38px !important;
            height: 38px !important;
            min-width: 38px !important;
            max-width: 38px !important;
            padding: 0 !important;
            font-size: 1.1em !important;
            box-shadow: 0 2px 8px rgba(22, 59, 112, 0.2) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.25s ease !important;
        }}

        .st-key-theme_toggle_wrap button:hover {{
            background: {ACCENT_ORANGE} !important;
            transform: scale(1.1) !important;
            box-shadow: 0 4px 12px rgba(231, 134, 39, 0.3) !important;
        }}

        .st-key-theme_toggle_wrap button p {{
            color: white !important;
        }}

        /* ===== 15. DOWNLOAD BUTTON ===== */
        [data-testid="stDownloadButton"] button {{
            background: linear-gradient(135deg, {PRIMARY_BLUE}, {DEEP_BLUE}) !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(22, 59, 112, 0.2) !important;
        }}

        [data-testid="stDownloadButton"] button:hover {{
            background: linear-gradient(135deg, {DEEP_BLUE}, #091d3e) !important;
            box-shadow: 0 6px 16px rgba(22, 59, 112, 0.3) !important;
        }}

        [data-testid="stDownloadButton"] button p {{
            color: white !important;
        }}

        /* ===== 16. RESPONSIVE ===== */
        @media (max-width: 768px) {{
            [data-testid="stSidebar"] button {{
                height: 40px !important;
                font-size: 0.85em !important;
                margin-bottom: 3px !important;
            }}

            .nav-section-header {{
                font-size: 0.65em !important;
                margin-top: 16px !important;
            }}

            .page-header-bar {{
                padding: 24px !important;
                border-radius: 12px !important;
            }}

            .page-header-bar h2 {{
                font-size: 1.4em !important;
            }}

            .metric-card {{
                padding: 20px !important;
                border-radius: 12px !important;
            }}

            .big-number {{
                font-size: 2.2em !important;
            }}
        }}

        /* ===== 17. SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}

        ::-webkit-scrollbar-track {{
            background: {bg_color};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {border_color};
            border-radius: 3px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {text_secondary};
        }}

    </style>
    """, unsafe_allow_html=True)


# --- 2. Data Display Logic ---
def display_custom_metric(container, label, value):
    """Displays a styled metric card matching KEO website card design."""
    formatted_value = f"{float(value):,.0f}"
    theme = st.session_state.get('theme', 'light')
    label_color = "#64748b" if theme == 'light' else "#94a3b8"

    with container:
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label" style="color: {label_color} !important;">{label}</p>
                <p class="big-number">{formatted_value}</p>
            </div>
        """, unsafe_allow_html=True)


def render_page_header(title, subtitle=""):
    """Renders a branded page header bar matching KEO website style."""
    subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
    st.markdown(f"""
        <div class="page-header-bar">
            <h2>{title}</h2>
            {subtitle_html}
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

def _merge_and_deduplicate_logic(header_title, uploader_key, prefix=""):
    render_page_header(header_title, "Upload and merge CSV files, then remove duplicate entries by email.")
    uploaded_files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True, key=uploader_key)
    if uploaded_files:
        try:
            dfs = [pd.read_csv(file) for file in uploaded_files]
            merged_df = pd.concat(dfs, ignore_index=True)
            # Show stats in metric cards
            col1, col2 = st.columns(2)
            deduplicated_df = merged_df.drop_duplicates(subset=['Email'])
            removed = len(merged_df) - len(deduplicated_df)
            display_custom_metric(col1, "Original Rows", len(merged_df))
            display_custom_metric(col2, "After Deduplication", len(deduplicated_df))
            st.session_state[f'{prefix}deduplicated_df'] = deduplicated_df
            st.session_state[f'{prefix}total_items'] = len(merged_df)
            st.session_state[f'{prefix}removed_items'] = removed
            st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
            st.subheader("Merged and Deduplicated Data")
            st.dataframe(deduplicated_df, use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def page_merge_and_deduplicate():
    _merge_and_deduplicate_logic("Merge & Deduplicate CSVs", "standard_merger_uploader")

def page_utn_reply_io_contacts_merger():
    _merge_and_deduplicate_logic("UTN Reply.io Contacts Merger", "utn_merger_uploader", "utn_")


def page_process_and_transform():
    render_page_header("Cold: Lead Contacts", "Transform deduplicated data into formatted lead contact lists.")
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
    st.dataframe(transformed_df, use_container_width=True)
    csv = transformed_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='transformed_data.csv',
        mime='text/csv',
    )

def page_utn_cold_contacts():
    render_page_header("UTN Cold Contacts", "Transform UTN data into formatted cold contact lists.")
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
    st.dataframe(transformed_df, use_container_width=True)
    csv = transformed_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='transformed_data.csv',
        mime='text/csv',
    )


def page_abm_email_outreach_overview():
    render_page_header("Cold Email Overview", "Paste campaign data from Reply.io to generate performance summaries.")
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
                    st.dataframe(df, use_container_width=True)
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
                    st.dataframe(summary_df, use_container_width=True)
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
    render_page_header("Warm: Email Overview", "Upload HubSpot campaign exports to analyze warm email performance.")
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
            st.dataframe(transformed_df, use_container_width=True)
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
            st.dataframe(summary_df, use_container_width=True)
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
        initial_sidebar_state="expanded",
        page_icon="fevicon.png"
    )

    # Initialize theme state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    # Apply theme-based CSS
    inject_custom_css(st.session_state.theme)

    # 3b. UI Structure

    # Theme toggle in top-right corner
    theme_emoji = "🌙" if st.session_state.theme == "light" else "☀️"
    next_theme = "dark" if st.session_state.theme == "light" else "light"
    _, toggle_col = st.columns([0.93, 0.07])
    with toggle_col:
        with st.container(key="theme_toggle_wrap"):
            if st.button(theme_emoji, key="theme_toggle", help=f"Switch to {next_theme} mode"):
                st.session_state.theme = next_theme
                st.rerun()

    # Sidebar
    with st.sidebar:
        import base64, pathlib
        _logo_b64 = base64.b64encode(pathlib.Path("keo-white-log.png").read_bytes()).decode()
        st.markdown(
            f'<div class="sidebar-logo"><a href="https://keomarketing.com/" target="_blank">'
            f'<img src="data:image/png;base64,{_logo_b64}" width="250"></a></div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div style="margin-bottom: 8px;"></div>', unsafe_allow_html=True)

        if 'page' not in st.session_state:
            st.session_state.page = 'Home'

        current_page = st.session_state.page

        if st.button("🏠  Home", key="nav_0", use_container_width=True, type="primary" if current_page == "Home" else "secondary"):
            if current_page != 'Home':
                st.session_state.page = 'Home'
                st.rerun()

        # Cold Campaign Section
        st.markdown('<p class="nav-section-header">Campaign Tools</p>', unsafe_allow_html=True)
        st.markdown('<div class="nav-section-divider"></div>', unsafe_allow_html=True)

        cold_pages = [
            ("Merge & Deduplicate", "🔀"),
            ("Cold: Lead Contacts", "📋"),
            ("UTN Reply.io Contacts Merger", "🔗"),
            ("UTN Cold Contacts", "❄️"),
            ("Cold Email Overview", "📧"),
            ("Warm: Email Overview", "🔥")
        ]

        for idx, (page_name, icon) in enumerate(cold_pages, start=1):
            is_active = current_page == page_name
            if st.button(f"{icon}  {page_name}", key=f"nav_{idx}", use_container_width=True, type="primary" if is_active else "secondary"):
                if not is_active:
                    st.session_state.page = page_name
                    st.rerun()

        # Sidebar footer
        st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size: 0.7em; color: rgba(255,255,255,0.3) !important; text-align: center; letter-spacing: 0.05em;">KEO Marketing &bull; ABM Analytics</p>',
            unsafe_allow_html=True
        )

    # --- PAGE CONTENT ---
    page = st.session_state.page

    if page == "Home":
        # Hero header
        st.markdown('<h1 class="main-header">Account Based Marketing Analytics</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size: 1.05em; margin-top: -4px; margin-bottom: 32px;">A high-level view of key metrics across your ABM and email campaigns.</p>',
            unsafe_allow_html=True
        )

        # ABM Summary Section
        st.markdown('<div class="section-card"><h3>ABM Report Summary</h3></div>', unsafe_allow_html=True)
        abm_col1, abm_col2 = st.columns(2)
        display_custom_metric(abm_col1, "Total Items Listed", st.session_state.get('total_items', 0))
        display_custom_metric(abm_col2, "Deduplicated Items Removed", st.session_state.get('removed_items', 0))

        st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

        # Email Campaign Section
        st.markdown('<div class="section-card"><h3>Email Campaign Overview</h3></div>', unsafe_allow_html=True)
        email_col1, email_col2 = st.columns(2)
        display_custom_metric(email_col1, "Total Cold Deliveries", st.session_state.get('cold_total_deliveries', 0))
        display_custom_metric(email_col2, "Total Warm Emails Sent", st.session_state.get('warm_total_sent', 0))

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
