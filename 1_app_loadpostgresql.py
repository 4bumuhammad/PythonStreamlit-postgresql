import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, ColumnsAutoSizeMode

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
sql = 'select * from tabledata;'
df = pd.read_sql(sql, engine, index_col=None)

# Use st.spinner to indicate processing state
with st.spinner("Processing..."):

    # Display the result after processing
    st.success("Done")
    # st.dataframe(df)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True)

    sel_mode=st.radio('Selection Type',options=['single','multiple'])
    gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
    gd.configure_side_bar()
    gridoptions=gd.build()

    grid_table=AgGrid(df, gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            allow_unsafe_jscode=True,
            height=400,
            ## Pagination
            custom_css={
                    "#gridToolBar": {
                        "padding-bottom": "0px !important",
                    }
                },
            theme='balham', # streamlit | alpine | balham | material
    )
    st.info("Total Rows :" + str(len(grid_table['data'])))   

    sel_row = grid_table["selected_rows"]
    st.subheader("Output")
    st.write(sel_row)