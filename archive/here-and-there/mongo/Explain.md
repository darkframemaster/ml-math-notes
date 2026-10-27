# explain
>MongoDB provides the db.collection.explain() method, the cursor.explain() method, and the explain command to return information on query plans and execution statistics of the query plans.

查看查询方案及其执行数据

## explain result
>The explain results present the query plans as a tree of stages. Each stage passes its results (i.e. documents or index keys) to the parent node. The leaf nodes access(访问) the collection or the indices. The internal(内部) nodes manipulate(操作) the documents or the index keys that result from the child nodes. The root node is the final stage from which MongoDB derives(获得) the result set.