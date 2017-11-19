import psycopg2

DBNAME = "news"

query_1 = (
    "select articles.title, count(*) as num "
    "from articles inner join log  "
    "on log.path like concat('%', articles.slug, '%') "
    "group by articles.title, log.path "
    "order by num desc limit 3"
    )

query_2 = (
    "select authors.name, count(*) as num "
    "from articles inner join authors "
    "on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug, '%') "
    "group by authors.name "
    "order by num desc"
    )

# query uses SQL View error_rate
query_3 = (
    "select * from error_rate "
    "where error_rate.percentage > 1 "
    "order by error_rate.percentage desc; "
    )


def top_articles():

    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(query_1)
    results = cursor.fetchall()

    print('Top Three Articles')

    for i in results:
        print('"' + i[0] + '" — ' + str(i[1]) + ' views')
    # insert space for visual clarity
    print('')

    conn.close()


def top_authors():

    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(query_2)
    results = cursor.fetchall()

    print('Top Three Authors')

    for i in results:
        print(i[0] + ' — ' + str(i[1]) + ' views')
    print('')

    conn.close()


def top_error_days():

    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(query_3)
    results = cursor.fetchall()

    print('Days With High Errors')

    for i in results:
        print(i[0].strftime('%B %d, %Y') + " - " +
              str(round((i[1]), 1)) + "%" + " errors")
    print('')

    conn.close()

top_articles()
top_authors()
top_error_days()
