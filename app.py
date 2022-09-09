import streamlit as st
import requests
import pandas as pd

url = 'http://ec2-13-212-176-7.ap-southeast-1.compute.amazonaws.com/UrlConversion/UrlConversion/'
long_urls = ["www.mysite.com/marketing/going-live/how-to-tell-the-world-about-your-new-business"]
st.set_page_config(page_title="Govtech url shortener", page_icon ="favicon.png")

st.write(
        """
    # Govtech url shortener
    This simple app takes in the the url and output a shorter version using [pyshorteners](https://pypi.org/project/pyshorteners/):
    
    Features:
    > 1. Stores every request in a db
    > 2. If requested url exisits in db, will return the entry from db
    > 3. Delete all history from db
    > 4. Use on any device! This app is web responsive
    
    Created by [Wesley Ong](https://wesleyongs.com/).
    """
    )

st.header("Make new request")
with st.expander("Some test cases", expanded=False):
    st.markdown(f"""- {str(long_urls[0])}
                """)
input_url = st.text_input("Input long url here", placeholder=long_urls[0], help="If url exists in db, duplicate entry will not be created, the existing result will instead be returned")


if input_url:
    myobj = {"input_url": input_url}
    x = requests.post(url, params=myobj)
    
    if x.status_code==200:
        st.success(x.json()['output_url'])
    else:
        st.exception(x.text)
    
st.header("Request history")
x = requests.get(url)
df = pd.DataFrame(data=x.json())
if not df.empty:
    st.table(df)

st.header("Delete everything")
delete_all = st.button("Delete all history")
if delete_all:
    x = requests.delete(url)    
    if x.status_code==200:
        st.success("Done")
    else:
        st.exception(x.text)
