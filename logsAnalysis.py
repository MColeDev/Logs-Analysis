#!/usr/bin/python3
import psycopg2

DBNAME = "news"

query_1 = ("""
    SELECT articles.title, count(*) AS num
    FROM articles INNER JOIN log
    ON log.path = concat('/article/' , articles.slug)
    GROUP BY articles.title, log.path
    ORDER BY num DESC
    LIMIT 3
    """)

query_2 = ("""
    SELECT authors.name, count(*) AS num
    FROM articles INNER JOIN authors
    ON articles.author = authors.id INNER JOIN log
    ON log.path = concat('/article/' , articles.slug)
    GROUP BY authors.name
    ORDER BY num DESC
    """)

# query uses SQL View error_rate
query_3 = ("""
    SELECT * FROM error_rate
    WHERE error_rate.percentage > 1
    ORDER BY error_rate.percentage desc;
    """)


def execute_query(query):
    """Connect to Database and return results of query"""

    try:
        conn = psycopg2.connect(database=DBNAME)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def main():
    """Print results of query request"""

    results = execute_query(query_1)

    print('Top Three Articles')

    for author, views in results:
        print('"{}" -- {} views'.format(author, views))
    # insert space for visual clarity
    print('')

    results = execute_query(query_2)

    print('Top Authors By Article View')

    for title, views in results:
        print('{} -- {} views'.format(title, views))
    # insert space for visual clarity
    print('')

    results = execute_query(query_3)

    print('Days With High Errors')

    for i in results:
        print('{0:%B %d, %Y} -- {1:.1f}% errors'.format(i[0], i[1]))

if __name__ == '__main__':
    main()
