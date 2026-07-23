import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Crew Check-In & Check-Out", layout="centered")

st.title("⭐ Secret Island Festival — Crew Check-In App")

# -----------------------------
# GOOGLE SHEETS SETUP
# -----------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["google"],
    scopes=scope
)

client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Secret Island Crew Log").sheet1

# -----------------------------
# CHECK-IN / CHECK-OUT FORM
# -----------------------------
st.header("Crew Check-In / Check-Out")

name = st.text_input("Crew Name")
role = st.selectbox(
    "Role",
    ["Security", "Bar", "Welfare", "Medics", "Gate", "Production", "Artist Liaison", "Other"]
)

# Check In
if st.button("Check In"):
    if name.strip() == "":
        st.error("Please enter a name before checking in.")
    else:
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, role, check_in_time, ""])
        st.success(f"{name} checked in at {check_in_time}")

# Check Out
if st.button("Check Out"):
    if name.strip() == "":
        st.error("Please enter a name before checking out.")
    else:
        check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records = sheet.get_all_records()

        updated = False
        for i, row in enumerate(records, start=2):  # row 2 = first data row
            if row["Name"] == name and row["Check Out"] == "":
                sheet.update_cell(i, 4, check_out_time)
                updated = True
                st.success(f"{name} checked out at {check_out_time}")
                break

        if not updated:
            st.error("This person has not checked in yet or is already checked out.")



