import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, ColumnsAutoSizeMode

import time

# Load environment variables from .env file
load_dotenv()

db_host = "localhost"
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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
progress_bar = st.empty()
button_info = st.empty()

if button_info.button("Mulai Progress"):
    # Reset progress dan status
    st.session_state.progress = 0
    st.session_state.status = "Proses: 0%"

    for i in range(10):
        time.sleep(0.5)
        st.session_state.progress = (i + 1) * 10
        st.session_state.status = f"Proses: {st.session_state.progress}%"

        progress_bar.progress(st.session_state.progress / 100.0)
        button_info.button(st.session_state.status)

    button_info.button("|| Ulangi ||")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Connect to the PostgreSQL database server
# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}')
sql = 'select * from tabledata;'
df = pd.read_sql(sql, engine, index_col=None)

# Use st.spinner to indicate processing state
with st.spinner("Processing..."):

    # Display the result after processing
    st.success("Done")

    # gd = GridOptionsBuilder.from_dataframe(df)
    gd = GridOptionsBuilder()

    gd.configure_default_column(
        resizable=True,
        filterable=True,
        sortable=True,
        editable=False,
    )

    df.rename(columns={'Order Date': 'orderDateAlias'}, inplace=True)    

    df["CheckboxColumn"] = '<input type="checkbox" />'
    # Configure the new checkbox column
    gd.configure_column(
        field="CheckboxColumn",
        header_name="",
        width=50,  # Adjust the width as needed
        checkboxSelection=True,
    )

    gd.configure_column(
        field="virtualYear",
        header_name="Order Year",
        valueGetter="new Date(data.orderDateAlias).getFullYear()",
        type=["numericColumn"],
        width=110,
        rowGroup=True,
        hide=True,
    )

    gd.configure_column(
        field="virtualMonth",
        header_name="Order Month",
        valueGetter="new Date(data.orderDateAlias).toLocaleDateString('id-ID',options={year:'numeric', month:'2-digit'})",
        width=120,
        rowGroup=True,
        hide=True,
    )

    gd.configure_column(field="state", header_name="State", width=100, 
        rowGroup=True,
        hide=True,
    )

    gd.configure_column(field="Order ID", header_name="Order ID", 
        width=120, 
        rowGroup=True,
        hide=True,
    )

    gd.configure_column(
        field="orderDateAlias",
        header_name="Order Date",
        width=110,
        valueFormatter="value != undefined ? new Date(value).toLocaleString('id-ID', {dateStyle:'medium'}): ''",
    )

    gd.configure_column(
        field="Customer Name", header_name="Customer Name", width=180, 
        tooltipField="Customer Name", 
        rowGroup=True,
    )

    gd.configure_column(
        field="segment", header_name="Segment", width=110, tooltipField="Segment"
    )

    gd.configure_column(
        field="city", header_name="City", width=130, tooltipField="City"
    )

    gd.configure_column(
        field="region", header_name="Region", width=90, tooltipField="Region"
    )

    gd.configure_column(
        field="category", header_name="Category", width=120, tooltipField="Category"
    )

    gd.configure_column(
        field="Sub-Category", header_name="Sub-Category", width=130, tooltipField="Sub-Category"
    )

    gd.configure_column(
        field="Product Name", header_name="Product Name", width=250, tooltipField="Product Name"
    )

    gd.configure_column(
        field="quantity",
        header_name="Qty",
        width=65,
        type=["numericColumn"],
    )

    gd.configure_column(
        field="profit",
        header_name="Profit",
        width=110,
        type=["numericColumn"],
        valueFormatter="value.toLocaleString()",
    )


    gd.configure_column(
        field="ColumnVirtualisation",
        header_name="Column Virtualisation",
        pinned="left",
        width=200,  # set width as per your requirement
    )

    gd.configure_grid_options(
        # groupDefaultExpanded=-1,
        suppressColumnVirtualisation=True,
        groupDisplayType="groupRows",
        autoGroupColumnDef=dict(
            minWidth=300, 
            pinned="left", 
            cellRendererParams=dict(suppressCount=True)
        ),
    )

    sel_mode=st.radio('Selection Type',options=['single','multiple'])
    gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
    gd.configure_pagination(enabled=True)
    gd.configure_side_bar()    
    gridoptions=gd.build()

    grid_table=AgGrid(df, gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            allow_unsafe_jscode=True,
            height=600,
            ## Pagination
            custom_css={
                    "#gridToolBar": {
                        "padding-bottom": "0px !important",
                    }
                },
            theme='balham', # streamlit | alpine | balham | material
    )

    # Display total rows information
    total_rows_info = "Total Rows: {}".format(len(grid_table['data']))
    # Display total rows with checkboxes selected
    selected_rows_count = len([row for row in grid_table["selected_rows"] if "CheckboxColumn" in row])
    selected_rows_info = "Total Rows with Checkboxes Selected: {}".format(selected_rows_count)
    # Combine the information into a single st.info message
    combined_info = "{}  |  {}".format(total_rows_info, selected_rows_info)
    st.info(combined_info)

    sel_row = grid_table["selected_rows"]
    st.subheader("Output")
    st.write(sel_row)