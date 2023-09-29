import mysql.connector
from mysql.connector import MySQLConnection
import pandas as pd

configs = { 
    "host": "localhost",
    "user": "root",
    "database": "bookutopia",
    "password": "san.mousavi30nr3ii3",
}


def get_connection() -> MySQLConnection:
    return mysql.connector.connect(**configs)

def pandas_sql(mysql: MySQLConnection,query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, con=mysql)

def get_books_by_tags(mysql: MySQLConnection) -> pd.DataFrame:
    query='select  t.name, count(site_id) as count\
          from book_tag bt\
          inner join tags t on t.id = bt.tag_id\
          group by t.id\
          order by count desc'
    return pandas_sql(mysql,query)

def get_publisher_book_count(mysql:MySQLConnection) -> pd.DataFrame:
    query='select publisher.name, count(book_detail.book_id) as books_count\
         from book_detail\
         inner join publisher on publisher.id = book_detail.publisher_id\
         group by publisher_id\
         order by books_count desc\
         limit 10'
    return pandas_sql(mysql,query)

def get_count_book_year_solar(mysql:MySQLConnection) -> pd.DataFrame:
    query='select solar_publication_year, count(book_id) as books_count\
            from book_detail\
            where solar_publication_year between 1333 and 1402\
            group by solar_publication_year ;'
    return pandas_sql(mysql,query)

def get_count_book_year_ad(mysql:MySQLConnection) -> pd.DataFrame:
    query='select ad_publication_year, count(book_id) as books_count\
           from book_detail\
           where ad_publication_year between 1600 and 2023\
           group by ad_publication_year;'
    return pandas_sql(mysql,query)

def get_top_10_writers(mysql:MySQLConnection) ->pd.DataFrame:
    query='select wp.name, count(distinct w.site_id) as count_book\
        from writer w\
        inner join writer_page wp on w.writer_id = wp.writer_id\
        inner join book_detail bd on w.site_id = bd.site_id\
        group by w.writer_id\
        order by count_book desc\
        limit 11'
    return pandas_sql(mysql,query)

def get_top_10_translators(mysql:MySQLConnection)->pd.DataFrame:
    query='select tp.name, count( distinct book_detail.site_id) as count_book\
            from translator t\
            inner join translator_page tp on t.translator_id = tp.translator_id\
            inner join book_detail on book_detail.book_id=t.book_id\
            group by t.translator_id\
            order by count_book desc\
            limit 12'
    return pandas_sql(mysql,query)

def get_price_history(mysql:MySQLConnection) -> pd.DataFrame:
    query='select * from price_history'
    return pandas_sql(mysql,query)

def get_tags_df(mysql:MySQLConnection)->pd.DataFrame:
    query='select * from tags'
    return pandas_sql(mysql,query)

def get_publishers_df(mysql:MySQLConnection)->pd.DataFrame:
    query='select * from publisher where  name!=-1'
    return pandas_sql(mysql,query)

def get_writer_df(mysql:MySQLConnection)->pd.DataFrame:
    query='select writer.writer_id,writer_page.name from writer inner join writer_page on writer.writer_id = writer_page.writer_id;'
    return pandas_sql(mysql,query)

def get_book_detail(mysql:MySQLConnection)->pd.DataFrame:
    query='select * from book_detail'
    return pandas_sql(mysql,query)

def get_search_result(mysql:MySQLConnection,query:str) ->pd.DataFrame:
    return pandas_sql(mysql,query)
# def get_movies_has_story(mysql:MySQLConnection)->list[str]:
#     query="select Title from  storyline inner join  movie on movie.id=storyline.Movie_id"
#     # query="select Title,Context from  storyline inner join  movie on movie.id=storyline.Movie_id"
#     return (pandas_sql(mysql,query).Title)

# def get_result_word_cloud(mysql:MySQLConnection,name:str)->str:
#     query=f"select Context from  storyline inner join  movie on movie.id=storyline.Movie_id where movie.Title='{name}'"
#     return pandas_sql(mysql,query).Context
