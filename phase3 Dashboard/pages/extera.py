import streamlit as st
from model import *
from matplotlib import pyplot as plt
import numpy as np
from wordcloud import WordCloud

st.set_page_config(page_icon='☁️',page_title='wordCloud')
# st.title('📈 interactive_chart')
try:
    mysqldb = get_connection()
except:
    st.error("Make Sure Database is up & Running", icon="🚨")
    st.stop()

@st.cache_data
def prepare():
    book_summary_df=get_book_summary(mysqldb)
    book_title_list=book_summary_df['Persian_title'].drop_duplicates().to_list()
    return book_summary_df,book_title_list



book_summary_df,book_title_list=prepare()
# Create some sample text
font_path = "C:\\Users\\Asus\\Downloads\\chocolatier_artisanal\\Chocolatier Artisanal.ttf"

st.markdown("<h1 style='text-align: center;'>☁️📗Book's word cloud</h1>", unsafe_allow_html=True)
book_title= st.selectbox("Select a book", book_title_list) 
if book_title is None:
    st.write('select')
else:
    book_summary=book_summary_df[book_summary_df['Persian_title']==book_title]['summary']
    wordcloud = WordCloud(width=800, height=400, background_color='white',font_path=font_path).generate(book_summary)
    st.image(wordcloud.to_image())


# st.markdown("<h1 style='text-align: center;'>🎭actors netwrok graph</h1>", unsafe_allow_html=True)
# df= worked_actors_togethar(mysqldb)

# from pyvis.network import Network
# net = Network()
# actors1=list(df['actor1'])
# nodes=set(list(df['actor1'])+list(df['actor2']))
# net.add_nodes(nodes)
# for index,row in df.iterrows():
#     net.add_edge(row['actor1'], row['actor2'], value=row['count'],title=row['count'])
# # net.show('network.html')
# with open("network.html", "r") as f:
#     network_html = f.read()

# # Display the network in Streamlit
# st.components.v1.html(network_html, width=800, height=600)