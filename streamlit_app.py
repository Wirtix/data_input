import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Vendor Management Portal")
st.markdown("Enter the details of the new vendor below.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Produ

AKTYWNY = [
    'Aktywny',
    'Blokada'
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    nazwisko_imie = st.text_input(label="Nazwisko Imie*")
    adres = st.text_input(label="Adres*")
    #business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    telefon = st.text_input(label="Telefon*")
    email = st.text_input(label="Email*")
    aktywny = st.selectbox("Aktywny_Blokada", options=AKTYWNY)
    #years_in_business = st.slider("Years in Business", 0, 50, 5)
    #onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Dodatkowe Notatki")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not nazwisko_imie or not adres:
            st.warning("Wprowadz dane mamo!")
            st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "Nazwisko_Imie": nazwisko_imie,
                        "Adres": adres,
                        "Telefon":telefon,
                        "Email":email,
                        "Aktywny_Blokada": ", ".join(aktywny),
                        #"YearsInBusiness": years_in_business,
                        #"OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "Dodatkowe_Info": additional_info,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Vendors", data=updated_df)

            st.success("Poprawnie przesłane Dane!")

