import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import json

# Load environment variables from .env file
load_dotenv()

db_host = "192.168.100.196"
db_name = "Superstore"
# Access environment variables
db_user = os.getenv('PGUSER')
db_pswd = os.getenv('PGPASSWORD')
db_port = os.getenv('PGPORT')

st.set_page_config(layout="wide")

# Create expander with default state not expanded
with st.expander("INFO: to connect with postgresql", expanded=False):
    info_text = f'''- Host: {db_host} // with docker container
- User: {db_user} 
- Password: {db_pswd}
- Port: {db_port}
- Database: {db_name}
'''
    st.info(info_text)

# Connect to the PostgreSQL database server
# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}')
sql = "SELECT id, district_city, alias_district_city, code, state_province, state FROM tablestatecity WHERE id != 'f2eb5673-0061-4269-816a-2d0459bbd14c' ORDER BY district_city ASC LIMIT 60;"
df = pd.read_sql(sql, engine, index_col='id')

# Convert district_city to title case in Python
df['district_city'] = df['district_city'].apply(lambda x: x.title())

# Tampilkan judul aplikasi
st.title("Pilih Kota")

# Dropdown untuk memilih kota
selected_city_id = st.selectbox("Pilih kota:", 
                                df.index, format_func=lambda id: f"{df.loc[id, 'district_city']}, {df.loc[id, 'state']}",
                                key="selectbox_city_id",
                                help="Pilih kota dengan ukuran font 25px.",
                    )


selected_data = df.loc[[selected_city_id]].to_dict(orient='records')

st.write("Data yang Anda pilih")

# Tampilkan data dalam format JSON
json_data = json.dumps(selected_data, indent=2)
st.json(json_data)