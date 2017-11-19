# Logs Analysis Project

#### About
**The project scope involves building an internal reporting tool that will use information from a database to answer the following questions:**
1. What are the most popular three articles of all time? 
2. Who are the most popular authors of all time?
3. On which days did more than 1% of requests lead to errors?


- Requires Python3
- [Install VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- [Install Vagrant](https://www.vagrantup.com/downloads.html)

Download SQL Data and add to Vagrant directory
- [Download Data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Launch Vagrant using:
- `vagrant up`

Log in using:
- `vagrant ssh`

load data onto database using:
- `psql -d news -f newsdata.sql`

connect to database using:
- `psql -d news`

**Create view total_view using:**

```sql
CREATE VIEW total_view AS
SELECT date(time), COUNT(*) AS views
FROM log 
GROUP BY date(time)
ORDER BY date(time);
```

**Create view error_view using:**

```sql
CREATE VIEW error_view AS
SELECT date(time), COUNT(*) AS errors
FROM log WHERE status = '404 NOT FOUND' 
GROUP BY date(time) 
ORDER BY date(time);
```

**Create view error_rate using:**

```sql
CREATE VIEW error_rate AS
SELECT total_view.date, (100.0*error_view.errors/total_view.views) AS percentage
FROM total_view, error_view
WHERE total_view.date = error_view.date
ORDER BY total_view.date;
```

Execute Program using:
- `python3 logsanalysis.py`


