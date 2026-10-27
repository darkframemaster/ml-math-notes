# Operations in  mongo
## db operation
* `db.runCommand({cloneCollection: "maxnews.hsnews", from: "10.10.10.8:37017", query: {'show': 1})` [learn more](https://docs.mongodb.com/manual/reference/command/cloneCollection)

## col operation
* `insert(document)`
* `save(document)`
* `update(query, document)`
* `find(query)`
    * `findOne(query)`
    * `limit(int)`
    * `skip(int)`
    * `sort()`
    * `count()`
    * `distinct(key)`
    * `ensureIndex(key)`
    * `getIndexes()`
    * `dropIndex({name: 'index name'})`
    * `group()`
    * `mapReduce()`
* `remove(query)`

## query
### update
* `$inc`
    * `{"$inc":{"age":1}}`
* `$set`
    * `{"$set":{"age":30}}`
* `$unset` 删除字段
    * `{"$unset":{"age"}}`
* `$push` 添加数组元素
    * `{"$push":{"user":{"name": "xuehao"}}}`
* `$pull` 删除数组元素
    * `{"$pull":{"user":{"name": "xuehao"}}}`
* `addToSet` 添加数组元素，重复不添加
    * `{"addToSet":{"user":{"name":"xuehao"}}}`

### filter
* `$ne`
* `$or`
    * `{"$or": [{"name":xuehao}, {"company":"max+"}]}`
* `$not`
    * `{"age": {"$not": {"$gt":40}}}`
* `$lt $gt $lte $gte`
    * `{"age":{"$gt":20, "$lte": 30}}`
* `$in $nin`
    * `{"age": {$in: [10,20,30]}}`
* `$all`
    * `{"age": {$all: [10,20]}}`
    * all是包含整个list， in是包含list中的某个或者多个
* `regex`
    * `{"name": {"$regex": "ueharere"}}`

## text search
Enable text search:
```bash
#several options for enabling the beta text search feature in MongoDB 2.4:

#in your MongoDB configuration file with:
setParameter=textSearchEnabled=true

#via the command-line when you start mongod:
mongod --setParameter textSearchEnabled=true

#via the mongo shell:
db.adminCommand( { setParameter: true, textSearchEnabled : true})
```
Getting start:
```bash
db.COL.createIndex({title: "text", content: "text"})

# 按关键字 key 和 word 检索
db.COL.find({$text: {$search: "key word"}})
# 排除关键字
db.COL.find({$text: {$search: "key -word"}})
# 按关键字 key 和 key word 检索
db.COL.find({$text: {$search: "key \"key word\""}})
# 按匹配值排序
db.COL.find({$text: {$search: "key word"}}, {score:{$meta: "textScore"}}).sort({score: {$meta: "textScore"}})
```

## group
group不支持分片运算

```
# Example
db.COLNAME.group(
    {
        key: {}, # SELECT 
        cond: {}, # WHERE or HAVING
        reduce: function(curr, result) {}, # 
        initial: {} # 
    }
)

db.goods.group(
    {
        key: {good_id}, # SELECT
        cond: {}, # WHERE or HAVING
        reduce: function(curr, result) {
            if(curr.shop_price > result.max){
                result.max = curr.shop_price;
            }
        },
        initial: {max:0}
    }
)
```

## aggregation
[learn more about operator](https://docs.mongodb.com/manual/reference/operator/aggregation/)
![](https://docs.mongodb.com/manual/_images/aggregation-pipeline.png)

* `{$match: {key: "value"}}` filter
* `{$group: {'_id': "required", new_key: {$ope: "$old_key"}}}` define a new table structure