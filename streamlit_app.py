import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator.login('main')


if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    #authenticator.logout()
    st.write(f'Cześć Śliczna/y *{st.session_state["name"]}*')
    # Display Title and Description
    st.title("Dane klientek mojej kochanej Mamusi <3")
    st.markdown("Śmiało wpisuj!")

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read(worksheet="Vendors", usecols=list(range(8)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    # List of Business Types and Produ

    AKTYWNY = [
        'Aktywny',
        'Blokada'
    ]

    # Onboarding New Vendor Form
    with st.form(key="vendor_form"):
        nazwisko_imie = st.text_input(label="Nazwisko Imie*")
        ulica = st.text_input(label="Ulica*")
        miasto = st.text_input(label="Miasto*")
        #business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
        telefon = st.text_input(label="Telefon*")
        email = st.text_input(label="Email*")
        aktywny = st.selectbox("Aktywny_Blokada", options=AKTYWNY)
        #years_in_business = st.slider("Years in Business", 0, 50, 5)
        #onboarding_date = st.date_input(label="Onboarding Date")
        additional_info = st.text_area(label="Dodatkowe Notatki")
        gotowe_do_druku = f'{nazwisko_imie}\n{ulica}\n{miasto}\n{email}\n{telefon}'
        # Mark mandatory fields
        st.markdown("**Obowiazkowe*")

        submit_button = st.form_submit_button(label="Zatwierdz dane")

        # If the submit button is pressed
        if submit_button:
            # Check if all mandatory fields are filled
            if not nazwisko_imie or not ulica:
                st.warning("Wprowadz dane mamo!")
                st.stop()
            else:
                # Create a new row of vendor data
                vendor_data = pd.DataFrame(
                    [
                        {
                            "Nazwisko_Imie": nazwisko_imie,
                            "Ulica": ulica,
                            "Miasto":miasto,
                            "Telefon":telefon,
                            "Email":email,
                            "Aktywny_Blokada": ", ".join(aktywny),
                            #"YearsInBusiness": years_in_business,
                            #"OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                            "Dodatkowe_Info": additional_info,
                            "Gotowe_Do_Durku": gotowe_do_druku
                        }
                    ]
                )

                # Add the new vendor data to the existing data
                updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                conn.update(worksheet="Vendors", data=updated_df)
                conn.update(worksheet="backup", data=updated_df)

                st.success("Poprawnie przesłane Dane!")

