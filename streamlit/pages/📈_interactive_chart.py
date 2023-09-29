import streamlit as st
from model import *
from matplotlib import pyplot as plt
import numpy as np
from wordcloud import WordCloud

st.title('📈 interactive_chart')

try:
    mysqldb = get_connection()
except:
    st.error("Make Sure Database is up & Running", icon="🚨")
    st.stop()


st.markdown("<h1 style='text-align: center;'>The most sold movies in a genre</h1>", unsafe_allow_html=True)
genre = st.selectbox("Select a genre", get_genres(mysql=mysqldb)) 
movies_in_genre=get_movies_genres(mysql=mysqldb,genre=genre)
st.bar_chart(movies_in_genre,x='Title',y='Gross_Us_Canada')




st.markdown("<h1 style='text-align: center;'>Movies based on your interest</h1>", unsafe_allow_html=True)
movie_name= st.selectbox("Select a movie you like", get_movies(mysql=mysqldb)) 
result=recommend_base_genre(mysql=mysqldb,movie_name=movie_name)
st.dataframe(result,hide_index=True)


# Create some sample text
font_path = "C:\\Users\\Asus\\Downloads\\chocolatier_artisanal\\Chocolatier Artisanal.ttf"

st.markdown("<h1 style='text-align: center;'>☁️🎬movie's word cloud</h1>", unsafe_allow_html=True)
movies_list=get_movies_has_story(mysql=mysqldb)
movie_name= st.selectbox("Select a movie", movies_list) 
if movie_name is None:
    st.write('select')
else:
    slm=get_result_word_cloud(mysqldb,movie_name)[0]
    wordcloud = WordCloud(width=800, height=400, background_color='white',font_path=font_path).generate(slm)
    st.image(wordcloud.to_image())


st.markdown("<h1 style='text-align: center;'>🎭actors netwrok graph</h1>", unsafe_allow_html=True)
df= worked_actors_togethar(mysqldb)
# G=nx.Graph()
# G=nx.from_pandas_edgelist(df,source='actor1',target='actor2',edge_attr='count')
# # nx.draw(G)
# pos = nx.circular_layout(G)
# edge_labels = {(source, target): count['count'] for source, target, count in G.edges(data=True)}
# nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black',width=2)
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
# st.pyplot()
from pyvis.network import Network
net = Network()
actors1=list(df['actor1'])
nodes=set(list(df['actor1'])+list(df['actor2']))
net.add_nodes(nodes)
for index,row in df.iterrows():
    net.add_edge(row['actor1'], row['actor2'], value=row['count'],title=row['count'])
# net.show('network.html')
with open("network.html", "r") as f:
    network_html = f.read()

# Display the network in Streamlit
st.components.v1.html(network_html, width=800, height=600)