import streamlit as st
from model import *

st.title('💻Table Filtering')
try:
    mysqldb = get_connection()
except:
    st.error("Make Sure Database is up & Running", icon="🚨")
    st.stop()

def set_font():
    st.markdown(
            """
            <style>
            * {
                font-family: 'Tahoma', 'Times New Romans', sans-serif !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
def show_stars(rating):
    num_stars = int(rating)
    star_display = '⭐' * num_stars
    remaining_stars = 5 - num_stars
    star_display += '☆' * remaining_stars
    return star_display


@st.cache_data
def prepare_df():
    #price filtering
    price_history_df=get_price_history(mysqldb)
    price_list=price_history_df['price']*((100-price_history_df['discount'])/100).to_list()
    #tag filtering
    tags_df=get_tags_df(mysqldb)
    tags_list=tags_df['name'].to_list()
    #publisher filtering
    publishers_df=get_publishers_df(mysqldb)
    publishers_list=publishers_df['name'].drop_duplicates().to_list()
    #writer filtering
    writers_df=get_writer_df(mysqldb)
    writers_list=writers_df['name'].drop_duplicates().to_list()
    #book data filtering
    book_data_df=get_book_detail(mysqldb)
    edition_list=book_data_df[book_data_df['edition']!=-1]['edition'].drop_duplicates().to_list()
    language_list=book_data_df['book_language'].drop_duplicates().to_list()
    persian_title_list= book_data_df['Persian_title'].to_list()
    english_title_list= book_data_df['English_title'].to_list()
    stock_status_list=book_data_df['stock_status'].drop_duplicates().to_list()
    score_list=book_data_df['score'].drop_duplicates().to_list()
    return [price_list,tags_list,publishers_list,\
           writers_list,edition_list,language_list,persian_title_list,\
           english_title_list,stock_status_list,score_list]

    
set_font()
price_list,tags_list,publishers_list,writers_list\
,edition_list,language_list,persian_title_list,\
english_title_list,stock_status_list,score_list=prepare_df()
st.sidebar.markdown("Choose your filter: ")
persian_title_box=st.sidebar.multiselect('نام کتاب',options=persian_title_list,default=None)
tags_box=st.sidebar.multiselect('book_tags',options=tags_list,default=tags_list[0])
on=st.sidebar.toggle('discount')
price_range=st.sidebar.slider("price range: ",value=(price_list.min(),price_list.max()))
score_range=st.sidebar.slider("Score: ", value=(min(score_list),max(score_list) ))
edition_range=st.sidebar.slider(" edition: ", value=(min(edition_list),max(edition_list)))
language_box=st.sidebar.multiselect('language',options=language_list,default=language_list[0])
stock_status_box=st.sidebar.multiselect('stock status',options=stock_status_list,default=stock_status_list[0])
publishers_box=st.sidebar.multiselect('publisher',options=publishers_list,default=publishers_list[0])
writers_box=st.sidebar.multiselect('writer',options=writers_list,default=writers_list[0])
search_button=st.sidebar.button('filter')

if search_button:
    
    query='select book_detail.site_id,book_detail.book_id,Persian_title,English_title,score,edition,solar_publication_year,ad_publication_year,book_language,stock_status,price,discount,publisher.name as publisher,writer_page.name as writer\
            from book_detail \
            inner join price_history on price_history.book_id=book_detail.book_id\
            inner join publisher on publisher.id=book_detail.publisher_id\
            inner join writer on writer.site_id=book_detail.site_id \
            inner join writer_page on writer.writer_id = writer_page.writer_id\
            where price_history.price between '+str(price_range[0]) +' and '+str(price_range[1])
 
    if len(tags_box)!=0:
        book_tags_query='select book_tag.site_id, tags.name\
                    from (select site_id\
                    from book_tag\
                    inner join tags on tags.id = book_tag.tag_id\
                    where tags.name in('+str(tags_box).replace('[','').replace(']','')+')) as tbl\
                    inner join book_tag on tbl.site_id = book_tag.site_id\
                    inner join tags on book_tag.tag_id = tags.id'
        book_tags_df=get_search_result(mysqldb,book_tags_query) 
        book_tags_df.rename(columns={'name':'tag_name'},inplace=True)

    if len(persian_title_box)!=0:
        query+=' where Persian_title in ('+str(persian_title_box).replace('[','').replace(']','')+')'
    if on:
        query+=' and price_history.discount!=0'
    query+=' and score between '+str(score_range[0])+' and '+str(score_range[1])+' and edition between '+str(edition_range[0])+' and '+str(edition_range[1])
    if len(language_box)!=0:
        query+=' and book_language in('+str(language_box).replace('[','').replace(']','')+')'
    if len(stock_status_box)!=0:
        query+=' and stock_status in('+str(stock_status_box).replace('[','').replace(']','')+')'
    if len(publishers_box)!=0:
        query+=' and publisher.name in('+str(publishers_box).replace('[','').replace(']','')+')'
    if len(writers_box)!=0:
        query+=' and writer_page.name in('+str(writers_box).replace('[','').replace(']','')+')'

    searched_df=get_search_result(mysqldb,query)
    if len(book_tags_query)!=0:
            searched_df=pd.merge(book_tags_df,searched_df,how='inner')
   
    grouped=searched_df.groupby('book_id')
    
    all_book_list=[]
    book_dict={}
    for book_id, group in grouped:
        this_book_tag=[]
        this_book_writer=[]
        this_book_publisher=[]
        book_dict['book_id']=book_id
        book_dict['site_id']=group['site_id'].iloc[0]
        book_dict['persian_title']=group['Persian_title'].iloc[0]
        book_dict['english_title']=group['English_title'].iloc[0]
        book_dict['score']=group['score'].iloc[0]
        book_dict['edition']=group['edition'].iloc[0]
        book_dict['language']=group['book_language'].iloc[0]
        book_dict['status']=group['stock_status'].iloc[0]
        book_dict['price']=group['price'].iloc[0]
        book_dict['discount']=group['discount'].iloc[0]
        book_dict['solar_publication_year']=group['solar_publication_year'].iloc[0]
        book_dict['ad_publication_year']=group['ad_publication_year'].iloc[0]
        book_dict['publisher']=group['publisher'].iloc[0]
        # Loop through each row in the group
        for index, row in group.iterrows():
            this_book_tag.append(row['tag_name'])
            this_book_writer.append(row['writer'])
        book_dict['tags']=this_book_tag
        book_dict['writer']=list(set(this_book_writer))  
        all_book_list.append(book_dict.copy())
        # st.write(book_dict)
        # st.write("---")  
    # st.write(all_book_list)

    # cl1,cl2,cl3= st.columns(3)
    # for row in all_book_list:
    #         with cl1:
    #             st.markdown('نام کتاب: '+row['persian_title'])
    #             st.markdown('title: '+row['english_title'])
    #             st.markdown("writer: ")
    #             st.markdown(row['writer'])
    #             st.markdown("publisher: ")
    #             st.markdown(row['publisher'])
    #         with cl2:
    #             st.markdown("Average Rating:")
    #             st.markdown(f"{show_stars(row['score'])}")
    #             st.markdown('publication year :')
    #             st.markdown('solar: '+str(row['solar_publication_year']))
    #             st.markdown('ad: '+str(row['ad_publication_year']))
    #         with cl3:
    #             st.markdown("status: ")
    #             st.markdown(row['status'])
    #             st.markdown('Price: ')
    #             st.markdown(str(row['price'])+' toman ')
    #             st.markdown('Discount: ')
    #             st.markdown(str(row['discount'])+'%')
    #         st.markdown('tags: '+str(row['tags']))
    #         st.markdown(20*'-')
    for row in all_book_list:
            st.markdown('نام کتاب: '+row['persian_title'])
            st.markdown('title: '+row['english_title'])
            st.markdown("writer: ")
            st.markdown(row['writer'])
            st.markdown("publisher: ")
            st.markdown(row['publisher'])
            st.markdown("Average Rating:")
            st.markdown(f"{show_stars(row['score'])}")
            st.markdown('publication year :')
            st.markdown('solar: '+str(row['solar_publication_year']))
            st.markdown('ad: '+str(row['ad_publication_year']))
            st.markdown("status: ")
            st.markdown(row['status'])
            st.markdown('Price: ')
            st.markdown(str(row['price'])+' toman ')
            st.markdown('Discount: ')
            st.markdown(str(row['discount'])+'%')
            st.markdown('tags: '+str(row['tags']))
            st.markdown(20*'-')

        
else:
    st.write('look for your books here ...')