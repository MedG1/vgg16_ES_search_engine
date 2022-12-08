import streamlit as st
from PIL import Image
import requests

DATA_ABSOLUTE_PATH = "C:/Users/med_g/OneDrive/Desktop/SUPCOM/DB Indexing & geospacial applications/elasticsearch/bdimage/idb/Objects/"
def main():
    st.set_page_config(layout="wide")
    image_query()

def image_query():
    st.header("Image Search Engine Based on VGG16 Features")
    image_upload = st.file_uploader(
        "Upload an image",
        type = ["jpg","png"],
        help="Drag and drop your image here"
    )
    request_size = st.slider(
        "Result count",
        min_value=1,
        max_value=50,
        value=10,
        help="Select the number of resulted queries"
    )
    params = {"size":request_size}
    if st.button("Search") and image_upload != None:
        progressBar = st.progress(0) 
        st.info("➼ Query image")
        st.image(image_upload, width = 224)
        progressBar.progress(25)
        res = requests.post(
            "http://localhost:8080/vgg_query", 
            files = {"image": image_upload}, 
            params = params
        )
        print(res)
        response = res.json()
        progressBar.progress(50)
        hits = []
        for hit in response:
            hits.append(Image.open(DATA_ABSOLUTE_PATH + hit['_source']['source_folder'] + '/' + hit['_source']['image_name']))
        progressBar.progress(80)
        st.success("Search results:")
        fullColumns = len(hits)//4
        remainder = len(hits) % 4
        for i in range(0, fullColumns*4, 4):
            cols = st.columns(4)
            cols[0].image(hits[i]  , use_column_width="always")
            cols[1].image(hits[i+1], use_column_width="always")
            cols[2].image(hits[i+2], use_column_width="always")
            cols[3].image(hits[i+3], use_column_width="always")
        if(remainder):
            cols = st.columns(remainder)
            for i in range(0, remainder):
                cols[i].image(hits[fullColumns*4 + i], use_column_width="always")
        progressBar.progress(100)
    
if __name__ == '__main__':
    main()
