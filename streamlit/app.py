import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
st.title("📚Booktopia")
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
|    ├── storyline.ipynb
|    ├── crawl.ipynb
|    ├── db.py
|    ├── apiws.py
|    └── crawl.py
└── csvFiles
    ├── cast.csv
    ├── cgenre.csv
    ├── story_line.csv
    ├── movie.csv
    ├── crew.csv
    └── person.csv
```
"""

with st.sidebar.expander("About the App"):
    st.write(
    "Introducing our innovative app designed exclusively for bookshop owners! Our app streamlines the process of sourcing and purchasing books for your store. With a vast catalog of titles, easy search and filter options, you can effortlessly discover and acquire the perfect additions to your shelves. Say goodbye to the hassles of manual book procurement and hello to a more efficient, book-loving future with our app!"
)