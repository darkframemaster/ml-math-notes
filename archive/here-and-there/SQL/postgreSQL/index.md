# index in PostgreSQL
Index is a very powerful weapon to speed up your query, and today's topic is index in PostgreSQL.

Assume we have a table store posts from users named as `bbs_linking` and here is the structure of the table:

```
=#\d bbs_linking
                                     Table "public.bbs_linking"
    Column    |           Type           |                        Modifiers
--------------+--------------------------+----------------------------------------------------------
 id           | integer                  | not null default nextval('bbs_linking_id_seq'::regclass)
 title        | character varying(100)   | not null
 description  | character varying(140)   | not null
 userid       | integer                  | not null
 create_at    | timestamp with time zone | not null
 modify_at    | timestamp with time zone | not null
 text         | text                     | not null
 up           | integer                  | not null
 topic_id     | integer                  |
 link_type    | integer                  | not null
 board_id     | integer                  | not null
 ip           | character varying(20)    | not null
 comment_num  | integer                  | not null
 is_web       | integer                  | not null
 has_video    | integer                  | not null
 has_imgs     | integer                  | not null
 award_num    | integer                  | not null default 0
 special_type | integer                  | not null default 0
Indexes:
    "bbs_linking_pkey" PRIMARY KEY, btree (id)
    "bbs_linking_board_id" btree (board_id)
    "bbs_linking_topic_id_link_type_modify_at" btree (topic_id, link_type, modify_at)
    "bbs_linking_board_id_link_type_modify_at" btree (board_id, link_type, modify_at)
    "bbs_linking_board_id_link_type_modify_at_topic_id_idx" btree (board_id, link_type, modify_at, topic_id)
    "bbs_linking_modify_at_where_link_type_eq_1_idx" btree (modify_at) WHERE link_type = 1
    "bbs_linking_topic_id" btree (topic_id)
    "bbs_linking_userid" btree (userid)ql
Foreign-key constraints:
    "bbs_linking_board_id_fkey" FOREIGN KEY (board_id) REFERENCES bbs_board(id) DEFERRABLE INITIALLY DEFERRED

-- here is the table size
=# select count(*) from bbs_linking;
2728537
```

As you can see, we've got some indexes here, now we want to get some data from the table. 

We just want those post with `board_id` = 1 and `topic_id` 2 and `link_type` = 1, the data will be ordered by field `modify_at`,  and here is the performance of our query:

```sql
=# explain select id from bbs_linking where board_id = 1 and topic_id = 2 and link_type = 1 order by modify_at limit 10;

					QUERY PLAN
------------------------------------------------------------------------------------------------------
 Limit  (cost=0.56..45.46 rows=10 width=12)
   ->  Index Scan using bbs_linking_board_id_link_type_modify_at_topic_id_idx on bbs_linking  (cost=0.56..135834.13 rows=30249 width=12)
         Index Cond: ((board_id = 1) AND (link_type = 1) AND (topic_id = 2))
(3 rows)
```

Not bad, this query hit the index `bbs_linking_board_id_link_type_modify_at_topic_id_idx` and using just a index scan to finish the query.

And now, we changed our mind, we want those post with `board_id` = 1 and `topic_id` in one of the value in list `1, 2, 3, 4, 5` and `link_type` = 1 and order the result by field `modify_at`, guess what will happen...

```sql
=# explain select id from bbs_linking where board_id = 1 and (topic_id=1 or topic_id=2 or topic_id=3 or topic_id = 4 or topic_id = 5) and link_type = 1 order by modify_at limit 10;  

					QUERY PLAN
------------------------------------------------------------------------------------------------------
 Limit  (cost=0.43..20.33 rows=10 width=12)
   ->  Index Scan using bbs_linking_modify_at_where_link_type_eq_1_idx on bbs_linking  (cost=0.43..173265.85 rows=87070 width=12)
         Filter: ((board_id = 1) AND ((topic_id = 1) OR (topic_id = 2) OR (topic_id = 3) OR (topic_id= 4) OR (topic_id = 5)))
(3 rows)
```

Even quicker than the first query, but it used the `bbs_linking_modify_at_where_link_type_eq_1_idx`, why? Maybe the reason is not so clear, so let'us take another example:

```sql
-- drop the index first
=# drop index bbs_linking_modify_at_where_link_type_eq_1_idx;

=# explain analyze select id from bbs_linking where (topic_id=4 or topic_id=1 or topic_id = 2) and link_type = 1 order by modify_at desc limit 10;

					QUERY PLAN
-------------------------------------------------------------------------------------------------------
 Limit  (cost=135053.16..135053.18 rows=10 width=12)
   ->  Sort  (cost=135053.16..135553.26 rows=200041 width=12)
         Sort Key: modify_at
         ->  Bitmap Heap Scan on bbs_linking  (cost=5379.82..130730.35 rows=200041 width=12)
               Recheck Cond: (((link_type = 1) AND (topic_id = 4)) OR ((link_type = 1) AND (topic_id = 1)) OR ((link_type = 1) AND (topic_id = 2)))
               ->  BitmapOr  (cost=5379.82..5379.82 rows=205650 width=0)
                     ->  Bitmap Index Scan on bbs_linking_topic_id_link_type_modify_at_idx  (cost=0.00..250.58 rows=9815 width=0)
                           Index Cond: ((link_type = 1) AND (topic_id = 4))
                     ->  Bitmap Index Scan on bbs_linking_topic_id_link_type_modify_at_idx  (cost=0.00..2887.97 rows=113554 width=0)
                           Index Cond: ((link_type = 1) AND (topic_id = 1))
                     ->  Bitmap Index Scan on bbs_linking_topic_id_link_type_modify_at_idx  (cost=0.00..2091.24 rows=82281 width=0)
                           Index Cond: ((link_type = 1) AND (topic_id = 2))
 Planning time: 0.195 ms
 Execution time: 616.273 ms
(14 rows)
```

In this query, we just use `topic_id` and `link_type` as the query condition and our query do hit the index `bbs_linking_topic_id_link_type_modify_at_idx`, but it cast a lot of time using `Bitmap Heap Scan` and it also cast a lot of time in sorting 200041 rows.

Let us rebuild the index `bbs_linking_modify_at_where_link_type_eq_1_idx` and try the same query:

```sql
=# explain analyze select id from bbs_linking where (topic_id=4 or topic_id=1 or topic_id = 2)   and link_type = 1 order by modify_at desc limit 10;

					QUERY PLAN
----------------------------------------------------------------------------------------------------------
 Limit  (cost=0.43..8.34 rows=10 width=12) (actual time=0.028..0.072 rows=10 loops=1)
   ->  Index Scan Backward using bbs_linking_modify_at_where_link_type_eq_1_idx on bbs_linking  (cost=0.43..158219.63 rows=200035 width=12) (actual time=0.027..0.071 rows=10 loops=1)
         Filter: ((topic_id = 4) OR (topic_id = 1) OR (topic_id = 2))
         Rows Removed by Filter: 18
 Planning time: 0.477 ms
 Execution time: 0.100 ms
(6 rows)
```

Here we go, same query but the spead is 1000 times faster, so actually the PostgreSQL has choosed `bbs_linking_modify_at_where_link_type_eq_1_idx` as the query index but not `bbs_linking_topic_id_link_type_modify_at_idx` because of the much better performance.

> PostgreSQL dose not support **force index** in a query, so in normal condition, PostgreSQL choose the best way to perform the query.

Finially, we has this query give to you, think about what will happen when you run this query.

```sql
=# explain select id from bbs_linking where board_id = 1 and topic_id in (1,2,3,4,5,6,7) and link_type = 1 order by modify_at limit 10;

					QUERY PLAN
------------------------------------------------------------------------------------------------------
 Limit  (cost=0.43..17.36 rows=10 width=12)
   ->  Index Scan using bbs_linking_modify_at_where_link_type_eq_1_idx on bbs_linking  (cost=0.43..165762.40 rows=97907 width=12)
         Filter: ((board_id = 1) AND (topic_id = ANY ('{1,2,3,4,5,6,7}'::integer[])))
(3 rows)
```
