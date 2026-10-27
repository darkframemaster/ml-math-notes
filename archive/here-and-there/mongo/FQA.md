### FQA
#### Different between nscanned and nscannedObjects
before we dive into this problem let see what is coverd index. here is a explain of coverd index in [StackOverFlow: what is a coverd index](http://stackoverflow.com/questions/62137/what-is-a-covered-index)

**What is covered index**

>A covering index is an index that contains all, and possibly more, the columns you need for your query.
>
>For instance, this:

```SQL
-- This is not a coverd index
-- if your index not contained the whole table's columns
SELECT *
FROM tablename
WHERE criteria
```

>will typically use indexes to speed up the resolution of which rows to retrieve using criteria, but then it will go to the full table to retrieve the rows.
>
>However, if the index contained the columns column1, column2 and column3, then this sql:

```SQL
-- This is a coverd index
-- while your indexes contained column1 and column2
SELECT column1, column2
FROM tablename
WHERE criteria
```

>and, provided that particular index could be used to speed up the resolution of which rows to retrieve, the index already contains the values of the columns you're interested in, so it won't have to go to the table to retrieve the rows, but can produce the results directly from the index.
>
>This can also be used if you see that a typical query uses 1-2 columns to resolve which rows, and then typically adds another 1-2 columns, it could be beneficial to append those extra columns (if they're the same all over) to the index, so that the query processor can get everything from the index itself.

Thus, covered indexes will have a better performance.

Let's go back to mongo, here is a query's explain result:
```js
{
    "cursor" : "BtreeCursor a_1_b_1",
    "isMultiKey" : false,
    "n" : 5,
    "nscannedObjects" : 5,
    "nscanned" : 9, 
    (...)
}
```

* `"nscanned" : 9` means query scanned 9 documents from the index
* `"nscannedObjects" : 5` means query then read 5 full documents from the collection

so there chould be two results:

if the index is a coverd index in your query result should be: 
* `nscannedObjects == nscanned` 
* `indexOnly == true`

otherwise:
* `nscannedObjects < nscanned`
* `indexOnly == false`


#### Does MongoDB support SQL?

>No. However, MongoDB does support a rich query language of its own.

#### Does MongoDB support transactions?

>MongoDB does not support multi-document transactions. However, MongoDB does provide atomic operations on a single document.

#### Does MongoDB handle caching?

>Yes. MongoDB keeps most recently used data in RAM. If you have created indexes for your queries and your working data set fits in RAM, MongoDB serves all queries from memory.
>
>MongoDB does not cache the query results in order to return the cached results for identical queries.

