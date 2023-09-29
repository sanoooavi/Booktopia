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
    "In this project, our goal is to learn how to use [`streamlit`](streamlit.io) by creating the ultimate data dashboard."
)