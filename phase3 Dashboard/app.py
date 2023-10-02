import streamlit as st
from streamlit_extras.let_it_rain import rain
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('attrs/logo.png')
st.image(image)
rain(
    emoji="📙",
    font_size=30,
    falling_speed=9,
    animation_length="infinite",
)

"""
### Project Structure

```
current_project
├── .gitignore
├── app.py
├── pages
│   ├── 1💻_table_filtering.py
│   ├── 2📊_static_chart.py
|   └── 3📈_interactive_chart.py
├── model
|    └── __init__.py
├── codes
|    ├── Scrap.ipynb
|    ├── get_links.ipynb
|    ├── writer_translator_info.ipynb
|    ├── Database.ipynb
|    ├── Streamlit
|    └── statistic.ipynb
└── csvFiles
     ├── award.csv
     ├── book_veneration.csv
     ├── bookData.csv
     ├── books_url.csv
     ├── BookSummaryData.csv 
     ├── bookTagsData.csv  
     ├── cover_type.csv   
     ├── data.csv   
     ├── format.csv     
     ├── price-history.csv       
     ├── publisher.csv
     ├── tag.csv
     ├── translator.csv
     ├── translator_info.csv
     ├── writer.csv
     ├── writer_info.csv
     ├── writer_page.csv
     └──   translator_page.csv 
```
"""

with st.sidebar.expander("About the App"):
    st.write(
        "Introducing our innovative app designed exclusively for bookshop owners! Our app streamlines the process of sourcing and purchasing books for your store. With a vast catalog of titles, easy search and filter options, you can effortlessly discover and acquire the perfect additions to your shelves. Say goodbye to the hassles of manual book procurement and hello to a more efficient, book-loving future with our app!"
    )
