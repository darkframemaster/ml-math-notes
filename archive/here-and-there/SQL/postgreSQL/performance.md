# Indexes and Performance
## Type of indexes in postgreSQL
### Partial Indexes
A partial index covers just a subset of a table’s data. It is an index with a WHERE clause. The idea is **to increase the efficiency of the index by reducing its size**. A smaller index takes less storage, is easier to maintain, and is faster to scan.

For example, suppose you allow users to flag comments on your site, which in turn sets the flagged boolean to true. You then process flagged comments in batches. You may want to create an index like so:

```sql
CREATE INDEX articles_flagged_created_at_index ON articles(created_at) WHERE flagged IS TRUE;
```

This index will remain fairly small, and can also be used along other indexes on the more complex queries that may require it.

### Expression Index
Expression indexes are useful for queries that match on some function or modification of your data. Postgres allows you **to index the result of that function** so that searches become as efficient as searching by raw data values. For example, you may require users to store their email addresses for signing in, but you want case insensitive authentication. In that case it’s possible to store the email address as is, but do searches on WHERE lower(email) = '<lowercased-email>'. The only way to use an index in such a query is with an expression index like so:

```sql
CREATE INDEX users_lower_email ON users(lower(email));
```

Another common example is for finding rows for a given date, where we’ve stored timestamps in a datetime field but want to find them by a date casted value. An index like:

```sql
CREATE INDEX articles_day ON articles ( date(published_at) );
```

can be used by a query containing filter like this:

```sql
WHERE date(articles.created_at) = date('2011-03-07');
```

### Unique Indexes
A unique index guarantees that the table won’t have more than one row with the same value. It’s advantageous to create unique indexes for two reasons: **data integrity** and **performance**. Lookups on a unique index are generally **very fast**.

In terms of data integrity, using a validates_uniqueness_of validation on an ActiveModel class does not really guarantee uniqueness because there can and will be concurrent users creating invalid records. Therefore you should **always create the constraint at the database level** - either with an index or a unique constraint.

There is little distinction between unique indexes and unique constraints. Unique indexes can be thought of as lower level, since expression indexes and partial indexes cannot be created as unique constraints. Even partial unique indexes on expressions are possible.

## Multi-column Indexes
While Postgres has the ability to create multi-column indexes, it’s important to understand when it makes sense to do so. The Postgres query planner has the ability to combine and use multiple single-column indexes in a multi-column query by performing a **bitmap index scan**. In general, you can create an index on every column that covers query conditions and in most cases Postgres will use them, so make sure to benchmark and justify the creation of a multi-column index before you create them. As always, indexes come with a cost, and multi-column indexes can only optimize the queries that reference the columns in the index in the **same order**, while multiple single column indexes provide performance improvements to a larger number of queries.

However there are cases where a multi-column index clearly makes sense. An index on columns (a, b) can be used by queries containing WHERE a = x AND b = y, or queries using WHERE a = x only, but will not be used by a query using WHERE b = y. So if this matches the query patterns of your application, the multi-column index approach is worth considering. Also note that in this case creating an index on a alone would be redundant.


### B-Tree and sorting
B-Tree index entries are sorted in ascending order by default. In some cases it makes sense to supply a different sort order for an index. Take the case when you’re showing a paginated list of articles, sorted by most recent published first. We may have a published_at column on our articles table. For unpublished articles, the published_at value is NULL.

In this case we can create an index like so:

```sql
CREATE INDEX articles_published_at_index ON articles(published_at DESC NULLS LAST);
```

>In Postgres 9.2 and above, it’s of note that indexes are not always required to go to the table, provided we can get everything needed from the index (i.e. no unindexed columns are of interest). This feature is called **“Index-only scans”**.

Since we will be querying the table in sorted order by published_at and limiting the result, we may get some benefit out of creating an index in the same order. Postgres will find the rows it needs from the index in the correct order, and then go to the data blocks to retrieve the data. If the index wasn’t sorted, there’s a good chance that Postgres would read the data blocks sequentially and sort the results.

This technique is mostly relevant with single column indexes when you require “nulls to sort last” behavior, because otherwise the order is already available since an index can be scanned in any direction. It becomes even more relevant when used against a multi-column index when a query requests a mixed sort order, like a ASC, b DESC.


### Why is my query not using an index?
There are many reasons why the Postgres planner may choose to not use an index. Most of the time, the planner chooses correctly, even if it isn’t obvious why. It’s okay if the same query uses an index scan on some occasions but not others. The **number of rows retrieved from the table** may vary based on the particular constant values the query retrieves. So, for example, it might be correct for the query planner to use an index for the query select * from foo where bar = 1, and yet not use one for the query select * from foo where bar = 2, if there happened to be far more rows with “bar” values of 2. When this happens, a sequential scan is actually most likely much faster than an index scan, so the query planner has in fact correctly judged that the cost of performing the query that way is lower.


###Managing and Maintaining indexes
Indexes in Postgres do **not** hold all row data. Even when an index is used in a query and matching rows where found, **Postgres will go to disk to fetch the row data**. Additionally, row visibility information (discussed in the MVCC article) is not stored on the index either, therefore Postgres must also go to disk to fetch that information.

Having that in mind, you can see how in some cases using an index doesn’t really make sense. **An index must be selective enough to reduce the number of disk lookups for it to be worth it**. For example, a primary key lookup with a big enough table makes good use of an index: instead of sequentially scanning the table matching the query conditions, Postgres is able to find the targeted rows in an index, and then fetch them from disk selectively. For very small tables, for example a cities lookup table, an index may be undesirable, even if you search by city name. In that case, Postgres may decide to ignore the index in favor of a sequential scan. Postgres will decide to perform a sequential scan on any query that will hit a significant portion of a table. If you do have an index on that column, it will be a dead index that’s never used - and **indexes are not free: they come at a cost in terms of storage and maintenance.**

When tuning a query and understanding what indexes make the most sense, be sure to use a database as similar as possible to what exists, or will exist in production. Whether an index is used or not depends on a number of factors, including the Postgres server configuration, the data in the table, the index and the query. For instance, **trying to make a query use an index on your development machine with a small subset of “test data” will be frustrating**: Postgres will determine that the dataset is so small that it’s not worth the overhead of reading through the index and then fetching the data from disk. **Random I/O(the way index scan will use) is much slower than sequential(the way seq scan will use), so the cost of a sequential scan is lower than that of the random I/O introduced by reading the index and selectively finding the data on disk.** Performing index tuning should be done on production, or on a staging environment that is as close to production as possible. 

When you are ready to apply an index on your production database, keep in mind that creating an index locks the table against writes. For big tables that can mean your site is down for hours. Fortunately Postgres allows you to `CREATE INDEX CONCURRENTLY`, which will take much longer to build, but does not require a lock that blocks writes. Ordinary `CREATE INDEX` commands require a lock that blocks writes but not reads.

Finally, indexes will become fragmented and unoptimized after some time, especially if the rows in the table are often updated or deleted. In those cases it may be required to perform a `REINDEX` leaving you with a balanced and optimized index. However be cautious about reindexing big indexes as write locks are obtained on the parent table. One strategy to achieve the same result on a live site is to **build an index concurrently on the same table and columns but with a different name**, and then dropping the original index and renaming the new one. This procedure, while much longer, won’t require any long running locks on the live tables.

Postgres provides a lot of flexibility when it comes to creating B-tree indexes that are optimized to your specific use cases, as well as options for managing the ever-growing database behind your applications. These tips should help you keep your database healthy, and your queries snappy.

## Performance
### Cache and its Hit Rate
```sql
SELECT 
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit)  as heap_hit,
  100 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM 
  pg_statio_user_tables;
```

If you find yourself with a ratio significantly lower than 99% then you likely want to consider increasing the cache available to your database.


### Index Usage
```sql
SELECT 
  relname, 
  100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used, 
  n_live_tup rows_in_table
FROM 
  pg_stat_user_tables
WHERE 
    seq_scan + idx_scan > 0 
ORDER BY 
  n_live_tup DESC;
```

While there is no perfect answer, if you’re not somewhere around 99% on any table over 10,000 rows you may want to consider adding an index. When examining where to add an index you should look at what kind of queries you’re running. Generally you’ll want to add indexes where you’re looking up by some other id or on values that you’re commonly filtering on such as created_at fields.

Pro tip: If you’re adding an index on a production database use CREATE INDEX CONCURRENTLY to have it build your index in the background and not hold a lock on your table. The limitation to creating indexes concurrently is they can typically take 2-3 times longer to create and can’t be run within a transaction. Though for any large production site these trade-offs are worth the trade-off in experience to your end users.


### Query Analyze
```sql
-- Use key word EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM events WHERE app_info_id = 7559;                                                 

QUERY PLAN
-------------------------------------------------------------------
Seq Scan on events  (cost=0.00..63749.03 rows=38 width=688) (actual time=2.538..660.785 rows=89 loops=1)
  Filter: (app_info_id = 7559)
Total runtime: 660.885 ms
```


### Index Cache Hit Rate
```
SELECT 
  sum(idx_blks_read) as idx_read,
  sum(idx_blks_hit)  as idx_hit,
  (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) as ratio
FROM 
  pg_statio_user_indexes;
```
Generally, you should also expect this to be in the 99% similar to your regular cache hit rate.


### Optimizing
Take the query below as an example, this query on example data set does contain an index on user_id.

```sql
EXPLAIN ANALYZE
SELECT * 
FROM address 
WHERE user_id = 245 
  AND current = True


--This would yield results:

                                                                QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=4690.88..4690.88 rows=1 width=0) (actual time=519.288..519.289 rows=1 loops=1)
   ->  Nested Loop  (cost=0.00..4690.66 rows=433 width=0) (actual time=15.302..519.076 rows=213 loops=1)
         ->  Index Scan using idx_address_userid on address  (cost=0.00..232.52 rows=23 width=4) (actual time=10.143..62.822 rows=1 loops=8)
               Index Cond: (user_id = 245)
               Filter: current
               Rows Removed by Filter: 14
 Total runtime: 219.428 ms
(1 rows)

```

We can see that it is using an index as expected. The difference is its having to fetch 15 different rows from the index then discard the bulk of them. The number of rows discarded is showcased by the line:

```sql
Rows Removed by Filter: 14
```

This is just one more of the many improvements in Postgres 9.2 alongside pg_stat_statements.

To further optimize this we would great a conditional `OR composite index`. A conditional would be where only current = true, where as the composite would index both values. A conditional is commonly more valuable when you have a smaller set of what the values may be, meanwhile the composite is when you have a high variability of values. Creating the conditional index:

```sql
CREATE INDEX CONCURRENTLY idx_address_userid_current ON address(user_id) WHERE current = True;
```

We can then see the query plan is now even further improved as we’d hope:

```sql
EXPLAIN ANALYZE
SELECT * 
FROM address 
WHERE user_id = 245 
  AND current = True

                                                            QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=4690.88..4690.88 rows=1 width=0) (actual time=519.288..519.289 rows=1 loops=1)
     ->  Index Scan using idx_address_userid_current on address  (cost=0.00..232.52 rows=23 width=4) (actual time=10.143..62.822 rows=1 loops=8)
           Index Cond: ((user_id = 245) AND (current = True))
 Total runtime: .728 ms
(1 rows)
```
