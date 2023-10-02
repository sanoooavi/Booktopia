import streamlit as st
from model import *
from matplotlib import pyplot as plt
import numpy as np
# from wordcloud import WordCloud

st.set_page_config(page_icon='💯',page_title='extera feature')
st.markdown("<h1 style='text-align: center;'>📢 publishers</h1>", unsafe_allow_html=True)
try:
    mysqldb = get_connection()
except:
    st.error("Make Sure Database is up & Running", icon="🚨")
    st.stop()

# @st.cache_data
# def prepare():
#     book_summary_df=get_book_summary(mysqldb)
#     book_title_list=book_summary_df['Persian_title'].drop_duplicates().to_list()
#     return book_summary_df,book_title_list



# book_summary_df,book_title_list=prepare()
# Create some sample text
# font_path = "C:\\Users\\Asus\\Downloads\\chocolatier_artisanal\\Chocolatier Artisanal.ttf"
# translator = Translator(from_lang="fa", to_lang="en")
# st.markdown("<h1 style='text-align: center;'>☁️📗Book's word cloud</h1>", unsafe_allow_html=True)
# book_title= st.selectbox("Select a book", book_title_list) 
# if book_title is None:
#     st.write('select')
# else:
#     book_summary=book_summary_df[book_summary_df['Persian_title']==book_title]['summary']
#     # st.write(book_summary.iloc[0])
#     # translation=translator.translate(book_summary.iloc[0])
#     # st.write(translation)
#     wordcloud = WordCloud(width=800, height=400, background_color='white'
#                           )\
#     .generate(book_summary.iloc[0])
#     # st.markdown(f'<div dir="rtl">{wordcloud.to_html()}</div>', unsafe_allow_html=True)
#     st.image(wordcloud.to_image())

st.markdown("<h5 style='text-align: center;'>publisher's same books network graph</h5>", unsafe_allow_html=True)
df=get_number_of_books_published_by_pubs(mysqldb)

from pyvis.network import Network
net = Network()
actors1=list(df['publisher1'])
nodes=set(list(df['publisher1'])+list(df['publisher2']))
net.add_nodes(nodes)
for index,row in df.iterrows():
    net.add_edge(row['publisher1'], row['publisher2'], value=row['book_count'],title=row['book_count'])
net.show('network.html')
with open("network.html", "r") as f:
    network_html = f.read()
st.components.v1.html(network_html, width=800, height=600)