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
            book_detail.English_title,\
            publisher_id,score,\
            (prices_tbl.price * (100 - prices_tbl.discount) / 100) as after_discount,\
            prices_tbl.date\
            from book_detail\
                     inner join (SELECT book_id, date, price, discount\
                                 FROM price_history\
                                 WHERE (book_id, date) IN (SELECT book_id, MAX(date)\
                                                           FROM price_history\
                                                           GROUP BY book_id)) as prices_tbl\
                                on prices_tbl.book_id = book_detail.book_id\
            where book_detail.stock_status = ' موجود '\
            and (prices_tbl.price * (100 - prices_tbl.discount) / 100) <= {budget}\
            order by score desc, after_discount) as inner_tbl) as outer_tbl\
            where sumofprice <= {budget}"
    return pandas_sql(mysql, query)


def get_most_profitable_books_by_budget(mysql: MySQLConnection, budget) -> pd.DataFrame:
    query = f"select * from (\
            select book_detail.book_id,\
            book_detail.Persian_title,\
            book_detail.English_title,\
            publisher_id,edition,\
            (prices_tbl.price * (100 - prices_tbl.discount) / 100) as after_discount,\
            prices_tbl.date\
            from book_detail\
                     inner join (SELECT book_id, date, price, discount\
                                 FROM price_history\
                                 WHERE (book_id, date) IN (SELECT book_id, MAX(date)\
                                                           FROM price_history\
                                                           GROUP BY book_id)) as prices_tbl\
                                on prices_tbl.book_id = book_detail.book_id\
            where book_detail.stock_status = ' موجود '\
            and (prices_tbl.price * (100 - prices_tbl.discount) / 100) <= {budget}\
            order by edition desc, after_discount) as inner_tbl) as outer_tbl\
            where sumofprice <= {budget}"
    return pandas_sql(mysql, query)


def get_most_books_by_budget(mysql: MySQLConnection, budget) -> pd.DataFrame:
    query = f"select * from (\
            select book_detail.book_id,\
            book_detail.Persian_title,\
            book_detail.English_title,\
            publisher_id,\
            (prices_tbl.price * (100 - prices_tbl.discount) / 100) as after_discount,\
            prices_tbl.date\
            from book_detail\
                     inner join (SELECT book_id, date, price, discount\
                                 FROM price_history\
                                 WHERE (book_id, date) IN (SELECT book_id, MAX(date)\
                                                           FROM price_history\
                                                           GROUP BY book_id)) as prices_tbl\
                                on prices_tbl.book_id = book_detail.book_id\
            where book_detail.stock_status = ' موجود '\
            and (prices_tbl.price * (100 - prices_tbl.discount) / 100) <= {budget}\
            order by after_discount) as inner_tbl) as outer_tbl\
            where sumofprice <= {budget}"
    return pandas_sql(mysql, query)


def get_unique_books(mysql: MySQLConnection, number) -> pd.DataFrame:
    query = f"select book_id,Persian_title,English_title,count(distinct rewards.reward) as award\
         from rewards\
         inner join book_detail on book_detail.site_id = rewards.site_id\
         group by rewards.site_id\
         order by award desc\
         limit {number}"
    return pandas_sql(mysql, query)


def get_most_veneration_book(mysql: MySQLConnection, num) -> pd.DataFrame:
    query = f'select book_detail.Persian_title,book_detail.English_title,\
            count(distinct  veneration.prise_writer) as count_comment\
            from book_detail\
            inner join veneration on veneration.site_id = book_detail.site_id\
            group by veneration.site_id\
            order by count_comment desc\
            limit {num}'
    return pandas_sql(mysql, query)


def get_all_books_with_tags(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'select book_tag.site_id, tags.name\
                    from (select site_id\
                    from book_tag\
                    inner join tags on tags.id = book_tag.tag_id) as tbl\
                    inner join book_tag on tbl.site_id = book_tag.site_id\
                    inner join tags on book_tag.tag_id = tags.id'
    return pandas_sql(mysql, query)


def get_translators_name(mysql: MySQLConnection) -> list[str]:
    query = 'select distinct name\
        from translator\
         inner join translator_page on translator.translator_id = translator_page.translator_id'
    return list(pandas_sql(mysql, query).name)


def get_all_books_translators(mysql: MySQLConnection) -> pd.DataFrame:
    query = "select book_detail.book_id, translator_page.name\
        from (select book_id\
            from translator\
                    inner join translator_page on translator_page.translator_id = translator.translator_id) as tbl\
         inner join book_detail on book_detail.book_id = tbl.book_id\
         inner join translator on book_detail.book_id = translator.book_id\
         inner join translator_page on translator_page.translator_id = translator.translator_id"
    return pandas_sql(mysql, query)


def get_number_of_books_published_by_pubs(mysql: MySQLConnection) -> pd.DataFrame:
    query = 'SELECT p1.name AS publisher1, p2.name AS publisher2,COUNT(*) AS book_count\
            FROM book_detail AS bd1\
            INNER JOIN book_detail AS bd2 ON bd1.English_title = bd2.English_title AND bd1.publisher_id < bd2.publisher_id\
            INNER JOIN publisher AS p1 ON bd1.publisher_id = p1.id\
            INNER JOIN publisher AS p2 ON bd2.publisher_id = p2.id\
            GROUP BY publisher1, publisher2\
            HAVING book_count >= 1\
            ORDER BY book_count DESC\
            limit 40;'
    return pandas_sql(mysql, query)


def get_all_books_writers(mysql: MySQLConnection) -> pd.DataFrame:
    query = "select book_detail.book_id, writer_page.name\
        from (select site_id\
            from writer\
                    inner join writer_page on writer_page.writer_id = writer.writer_id ) as tbl\
         inner join book_detail on book_detail.site_id = tbl.site_id\
         inner join writer on book_detail.site_id= writer.site_id\
         inner join writer_page on writer_page.writer_id = writer.writer_id"
    return pandas_sql(mysql, query)


def get_publisher_translator(mysql: MySQLConnection) -> pd.DataFrame:
    query = "SELECT p.name AS publisher_name, tp.name AS translator_name, MAX(translation_count) AS book_count\
             FROM publisher AS p\
                     JOIN book_detail AS bd ON p.id = bd.publisher_id\
                     JOIN translator AS t ON bd.book_id = t.book_id\
                     JOIN translator_page AS tp ON t.translator_id = tp.translator_id\
                     JOIN(SELECT p.id AS publisher_id, t.name AS translator_name, COUNT(*) AS translation_count\
                          FROM publisher AS p\
                                   JOIN book_detail AS bd ON p.id = bd.publisher_id\
                                   JOIN translator AS tr ON bd.book_id = tr.book_id\
                                   JOIN translator_page AS t ON tr.translator_id = t.translator_id\
                          GROUP BY p.id, t.name) AS translator_counts ON p.id = translator_counts.publisher_id\
                AND tp.name = translator_counts.translator_name\
             GROUP BY p.name\
             ORDER BY book_count desc"
    return pandas_sql(mysql, query)


def get_publisher_genres(mysql: MySQLConnection) -> pd.DataFrame:
    query = "SELECT t.name AS genre_name,p.name AS best_publisher_name,MAX(book_count) AS max_book_count\
                FROM tags AS t\
                JOIN book_tag AS bt ON t.id = bt.tag_id\
                JOIN book_summary AS bs ON bt.site_id = bs.site_id\
                JOIN book_detail AS bd ON bs.site_id = bd.site_id\
                JOIN publisher AS p ON bd.publisher_id = p.id\
                JOIN(SELECT t.id AS tag_id, p.id AS publisher_id,COUNT(*) AS book_count,ROW_NUMBER() OVER (PARTITION BY t.id ORDER BY COUNT(*) DESC) AS row_num\
                     FROM tags AS t\
                     JOIN book_tag AS bt ON t.id = bt.tag_id\
                     JOIN book_summary AS bs ON bt.site_id = bs.site_id\
                     JOIN book_detail AS bd ON bs.site_id = bd.site_id\
                     JOIN publisher AS p ON bd.publisher_id = p.id\
                     GROUP BY t.id, p.id\
                    ) AS max_counts ON t.id = max_counts.tag_id AND p.id = max_counts.publisher_id\
                GROUP BY t.name\
                limit 20;"
    return pandas_sql(mysql, query)
