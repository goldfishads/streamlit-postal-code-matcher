import streamlit as st
import pandas as pd

# Made by: Goldfish Ads 

postal_code_df = pd.read_csv('Postcodedistrict_postcodesector.csv')

def find_postalcode_sectors(postalcode_district, df):
    matching_sectors = df[df['postcode_district'] == postalcode_district]['postcode_sector'].tolist()
    return matching_sectors

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

st.title("Find matching postal code sectors - Powered by Goldfish Ads")
st.write("This app allows you to find matching postal code sectors for a list of given districts.")
st.write("To get started, upload a csv file with a column named 'district' containing the districts you want to match.")
upload_districts_table = st.file_uploader(
        "Upload a csv with the header 'district'")
if upload_districts_table is not None:
    
    # check upload type
    if upload_districts_table.type != "text/csv":
        st.error("Unsupported file format. Please upload a .csv file.")
        error = True    
   
    # Load the CSV file with postal code districts to match
    districts_to_match_df = pd.read_csv(upload_districts_table)
    all_matching_sectors = []
    for district in districts_to_match_df['district']:
        matching_sectors = find_postalcode_sectors(district, postal_code_df)
        all_matching_sectors.extend(matching_sectors)
        print("Postal code sectors matching '{}': {}".format(district, matching_sectors))

    # Create a dataframe with the results
    matching_sectors_df = pd.DataFrame(all_matching_sectors, columns=['postal_code'])
    csv = convert_df(matching_sectors_df)

    # download
    st.download_button(
        "Press to Download postal code sectors",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )
