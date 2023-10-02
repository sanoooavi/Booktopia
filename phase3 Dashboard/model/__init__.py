import mysql.connector
from mysql.connector import MySQLConnection
import pandas as pd

configs = {
    "host": "localhost",
    "user": "root",
    "database": "booktopia",
    "password": "123456",
}


def get_connection() -> MySQLConnection:
    return mysql.connector.connect(**configs)


def pandas_sql(mysql: MySQLConnection, query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, con=mysql)


def get_books_by_tags(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select t.name, count(distinct book_id) as number_of_books\
            from book_tag bt\
            inner join tags t on t.id = bt.tag_id\
            inner join book_detail on book_detail.site_id = bt.site_id\
            group by t.id\
            order by number_of_books desc'
    return pandas_sql(mysql, query)


def get_publisher_book_count(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select publisher.name as publisher, count(book_detail.book_id) as number_of_books\
         from book_detail\
         inner join publisher on publisher.id = book_detail.publisher_id\
         where publisher_id!=-1\
         group by publisher_id\
         order by number_of_books desc\
         limit 10'
    return pandas_sql(mysql, query)


def get_count_book_year_solar(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select solar_publication_year, count(book_id) as number_of_books\
            from book_detail\
            where solar_publication_year between 1320 and 1402\
            group by solar_publication_year ;'
    return pandas_sql(mysql, query)


def get_count_book_year_ad(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select ad_publication_year, count(book_id) as number_of_books\
           from book_detail\
           where ad_publication_year between 1900 and 2023\
           group by ad_publication_year;'
    return pandas_sql(mysql, query)


def get_top_10_writers(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select wp.name, count(distinct w.site_id) as number_of_books\
        from writer w\
        inner join writer_page wp on w.writer_id = wp.writer_id\
        inner join book_detail bd on w.site_id = bd.site_id\
        where wp.name != \"مجموعه ی نویسندگان\" \
        group by w.writer_id\
        order by number_of_books desc\
        limit 11'
    return pandas_sql(mysql, query)


def get_top_10_translators(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select tp.name, count( distinct book_detail.book_id) as number_of_books\
            from translator t\
            inner join translator_page tp on t.translator_id = tp.translator_id\
            inner join book_detail on book_detail.book_id=t.book_id\
            where tp.name != \'مجموعه ی نویسندگان\' and tp.name != \'مجموعه ی مترجمان\'\
            group by t.translator_id\
            order by number_of_books desc\
            limit 12'
    return pandas_sql(mysql, query)


def get_price_history(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select * from price_history'
    return pandas_sql(mysql, query)


def get_tags_df(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select * from tags'
    return pandas_sql(mysql, query)


def get_publishers_df(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select * from publisher where  name!=-1'
    return pandas_sql(mysql, query)


def get_writer_df(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select writer.writer_id,writer_page.name from writer inner join writer_page on writer.writer_id = writer_page.writer_id;'
    return pandas_sql(mysql, query)


def get_book_detail(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select * from book_detail'
    return pandas_sql(mysql, query)


def get_search_result(mysql: MySQLConnection, query: str) -> pd.DataFrame:
    return pandas_sql(mysql, query)


def get_page_num_rel_publication_year(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select solar_publication_year, page_number\
            from book_detail\
            where page_number between 1 and 10000\
            and (solar_publication_year between 1320 and 1402)'
    return pandas_sql(mysql, query)


def get_price_rel_publication_year(mysql: MySQLConnection) -> pd.DataFrame:
    query = "select book_detail.Persian_title,\
           book_detail.solar_publication_year,\
            max(price_history.date) as date,\
            price_history.price\
            from book_detail\
            inner join price_history on price_history.book_id = book_detail.book_id\
            where book_detail.stock_status=' موجود '\
            and (solar_publication_year between 1320 and 1402)\
            group by book_detail.book_id"
    return pandas_sql(mysql, query)


def get_price_rel_score(mysql: MySQLConnection) -> pd.DataFrame:
    query = "select book_detail.Persian_title,\
              book_detail.score,\
              max(price_history.date) as date,\
              price_history.price,\
              (price_history.price*(100-price_history.discount)/100) as after_discount\
          from book_detail\
          inner join price_history on price_history.book_id = book_detail.book_id\
          where book_detail.stock_status=' موجود '\
          and book_detail.score != 0\
          and price_history.price != -1\
          group by book_detail.book_id"
    return pandas_sql(mysql, query)


def get_num_book_based_format(mysql: MySQLConnection) -> pd.DataFrame:
    query = "select format.name as format, count(distinct book_detail.book_id) as number_of_books\
            from book_detail\
            inner join format on format.id = book_detail.format_id\
            where format.name!='null'\
            group by format_id\
            order by number_of_books desc"
    return pandas_sql(mysql, query)


def get_book_summary(mysql: MySQLConnection) -> pd.DataFrame:
    query = "select book_detail.Persian_title,book_summary.summary\
            from book_detail\
            inner join book_summary on book_detail.site_id = book_summary.site_id\
            where book_id!=-1 and book_summary.summary!='null'\
            group by book_detail.site_id"
    return pandas_sql(mysql, query)


def get_best_books_by_budget(mysql: MySQLConnection, budget) -> pd.DataFrame:
    query = f"select * from (\
            select book_detail.book_id,\
            book_detail.Persian_title,\
            max(price_history.date) as last_update,\
            score,\
            (price * (100 - price_history.discount) / 100) as after_discount,\
            sum((price * (100 - price_history.discount) / 100)) over (order by score\
            desc, price) as sumofprice\
            from book_detail\
            inner join price_history\
            on book_detail.book_id = price_history.book_id\
            where book_detail.stock_status = ' موجود '\
            and price_history.price<={budget}\
            group by book_detail.book_id\
            order by score desc, price) as t where sumofprice<={budget}"
    return pandas_sql(mysql, query)


def get_unique_books(mysql: MySQLConnection, number) -> pd.DataFrame:
    query = f"select book_id,Persian_title,English_title,count(distinct rewards.reward) as award\
         from rewards\
         inner join book_detail on book_detail.site_id = rewards.site_id\
         group by rewards.site_id\
         order by award desc\
         limit {number}"
    return pandas_sql(mysql, query)
# def get_movies_has_story(mysql:MySQLConnection)->list[str]:
#     query="select Title from  storyline inner join  movie on movie.id=storyline.Movie_id"
#     # query="select Title,Context from  storyline inner join  movie on movie.id=storyline.Movie_id"
#     return (pandas_sql(mysql,query).Title)

# def get_result_word_cloud(mysql:MySQLConnection,name:str)->str:
#     query=f"select Context from  storyline inner join  movie on movie.id=storyline.Movie_id where movie.Title='{name}'"
#     return pandas_sql(mysql,query).Context
