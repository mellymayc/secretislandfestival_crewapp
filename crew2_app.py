import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Crew Check-In & Check-Out", layout="centered")

st.title("⭐ Secret Island Festival — Crew Check-In App")

# Storage for crew data
if "crew_data" not in st.session_state:
    st.session_state.crew_data = []

crew_data = st.session_state.crew_data

st.header("Crew Check-In / Check-Out")

name = st.text_input("Crew Name")
role = st.selectbox("Role", ["Security", "Bar", "Welfare", "Medics", "Gate", "Production", "Artist Liaison", "Other"])

# Check In Button
if st.button("Check In"):
    if name.strip() == "":
        st.error("Please enter a name before checking in.")
    else:
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        crew_data.append({
            "Name": name,
            "Role": role,
            "Check In": check_in_time,
            "Check Out": ""
        })
        st.success(f"{name} checked in at {check_in_time}")

# Check Out Button
if st.button("Check Out"):
    if name.strip() == "":
        st.error("Please enter a name before checking out.")
    else:
        check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        found = False
        for person in crew_data:
            if person["Name"] == name and person["Check Out"] == "":
                person["Check Out"] = check_out_time
                found = True
                st.success(f"{name} checked out at {check_out_time}")
                break
        if not found:
            st.error("This person has not checked in yet or is already checked out.")

st.header("Current Crew Log")
st.table(crew_data)
