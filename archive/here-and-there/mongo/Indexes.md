# index in mongo
>Indexes are special data structures [1] that store a small portion of the collection’s data set in an easy to traverse form. The index stores the value of a specific field or set of fields, ordered by the value of the field. The ordering of the index entries supports efficient equality(等价的高效) matches and range-based query operations. In addition, MongoDB can return sorted results by using the ordering in the index.

## index types
* **single field**
	* sort order (i.e. ascending or descending) of the index key does not matter because MongoDB can traverse the index in either direction. 
* **compound index(multiple field)**
	* The order of fields listed in a compound index has significance. For instance, if a compound index consists of { userid: 1, score: -1 }, the index sorts first by userid and then, within each userid value, sorts by score.
	* ![](http://docs.mongoing.com/manual-zh/_images/index-compound-key.png)
	* **index prefix**
		* consider the following compound index:`{ "item": 1, "location": 1, "stock": 1 }`
* **multikey index**
	* MongoDB uses multikey indexes to index the content stored in arrays. If you index a field that holds an array value, MongoDB creates separate index entries for every element of the array. These multikey indexes allow queries to select documents that contain arrays by matching on element or elements of the arrays. MongoDB automatically determines whether to create a multikey index if the indexed field contains an array value; you do not need to explicitly specify the multikey type.
* **text index**
* **hash index**:Hashed indexes maintain entries with hashes of the values of the indexed field.

## index properties
* **Unique Index**:The unique property for an index causes MongoDB to reject duplicate values for the indexed field. 
* **Partial Indexes(3.2+)**:only index the documents in a collection that meet a specified filter expression.partial indexes have lower storage requirements and reduced performance costs for index creation and maintenance.
(在特殊情况时可以使用)
* **Sparse Index**:ensures that the index only contain entries for documents that have the indexed field. The index skips documents that **do not** have the indexed field.
	* combine the sparse index option with the unique index option to reject documents that have duplicate values for a field but ignore documents that do not have the indexed key.
* **TTL Index**:use to automatically remove documents from a collection after a certain amount of time.

 
## limitations in mongo's index
* **Extra memory**
	* indexes will slow down the performance of `CUD` operations, if the index is not needed any more, remember to remove the index.
* **Indexes stores in RAM**
	* If the size of the index is bigger then RAM, mongo will abandon some of the indexes witch will cause Performance Degradation(性能下降).
* **Query limitaions**, indexes will **not** be used in these conditions:
	* Regular expressions and non operators, such as `$nin`, `$not`, etc...
	* Arithmetic operators(算术运算符), such as `$mod`, etc...
	* `$where` clause
* 集合中索引不能超过64个
* 索引名的长度不能超过125个字符
* 一个复合索引最多可以有31个字段

## performance test
Useing `maxnews.data2news` from `host_ip:port` 

```bash
>db.runCommand({cloneCollection:'maxnews.dota2news', from:'host_ip:port'})
>db.dota2news.count()
5748

# without index
> db.dota2news.find({'title': {$regex: 'dota'}}).explain()
{
	"cursor" : "BasicCursor",
	"isMultiKey" : false,
	"n" : 32,
	"nscannedObjects" : 5748,
	"nscanned" : 5748,
	"nscannedObjectsAllPlans" : 5748,
	"nscannedAllPlans" : 5748,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 12,
	"indexBounds" : {
		
	},
}
> db.dota2news.find({'title': {$regex: 'dota|EHOME|IG|EG|LGD'}}).explain()
{
	"cursor" : "BasicCursor",
	"isMultiKey" : false,
	"n" : 235,
	"nscannedObjects" : 5748,
	"nscanned" : 5748,
	"nscannedObjectsAllPlans" : 5748,
	"nscannedAllPlans" : 5748,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 34,
	"indexBounds" : {
		
	},
}
> db.dota2news.find({'title': {$regex: 'dota|max|EHOME'}, 'content': {$regex: 'EHOME|IG|LGD|EG'}}).explain()
{
	"cursor" : "BasicCursor",
	"isMultiKey" : false,
	"n" : 199,
	"nscannedObjects" : 5748,
	"nscanned" : 5748,
	"nscannedObjectsAllPlans" : 5748,
	"nscannedAllPlans" : 5748,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 63,
	"indexBounds" : {
		
	},
}

# with title index
>db.dota2news.createIndex({title: 1})
>db.dota2news.find({'title': {$regex: 'dota2'}}).explain()
{
	"cursor" : "BtreeCursor title_1 multi",
	"isMultiKey" : false,
	"n" : 32,
	"nscannedObjects" : 32,
	"nscanned" : 5748,
	"nscannedObjectsAllPlans" : 32,
	"nscannedAllPlans" : 5748,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 10,
	"indexBounds" : {
		"title" : [
			[
				"",
				{
					
				}
			],
			[
				/dota/,
				/dota/
			]
		]
	},
}
>db.dota2news.find({title: {$regex: "dota|EHOME|IG|LGD|EG"}}).explain()
{
	"cursor" : "BtreeCursor title_1 multi",
	"isMultiKey" : false,
	"n" : 799,
	"nscannedObjects" : 799,
	"nscanned" : 5748,
	"nscannedObjectsAllPlans" : 799,
	"nscannedAllPlans" : 5748,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 34,
	"indexBounds" : {
		"title" : [
			[
				"",
				{
					
				}
			],
			[
				/dota|EHOME|IG|LGD|EG/,
				/dota|EHOME|IG|LGD|EG/
			]
		]
	},
}
>db.dota2news.find({'title': {$regex: 'dota|max|EHOME'}, 'content': {$regex: 'EHOME|IG|LGD|EG'}}).explain()
{
	"cursor" : "BtreeCursor title_1 multi",
	"isMultiKey" : false,
	"n" : 199,
	"nscannedObjects" : 235,
	"nscanned" : 5748,
	"nscannedObjectsAllPlans" : 2260,
	"nscannedAllPlans" : 7773,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 80,
	"indexBounds" : {
		"title" : [
			[
				"",
				{
					
				}
			],
			[
				/dota|max|EHOME/,
				/dota|max|EHOME/
			]
		]
	},
}

# with text-content combined index
>db.dota2news.createIndex({title:1, content:1})
>db.dota2news.find({'title': {$regex: 'dota2'}}, {'content': {$regex: 'EHOME'}}).explain()
{
	"cursor" : "BtreeCursor title_1_content_1 multi",
	"isMultiKey" : false,
	"n" : 0,
	"nscannedObjects" : 0,
	"nscanned" : 555,
	"nscannedObjectsAllPlans" : 556,
	"nscannedAllPlans" : 1666,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 5,
	"indexBounds" : {
		"title" : [
			[
				"",
				{
					
				}
			],
			[
				/dota/,
				/dota/
			]
		],
		"content" : [
			[
				"",
				{
					
				}
			],
			[
				/EHOME/,
				/EHOME/
			]
		]
	},
}
>db.dota2news.find({'title': {$regex: 'dota|max|EHOME'}, 'content': {$regex: 'EHOME|IG|LGD|EG'}}).explain()
{
	"cursor" : "BtreeCursor title_1_content_1 multi",
	"isMultiKey" : false,
	"n" : 53,
	"nscannedObjects" : 14,
	"nscanned" : 555,
	"nscannedObjectsAllPlans" : 584,
	"nscannedAllPlans" : 1666,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"millis" : 16,
	"indexBounds" : {
		"title" : [
			[
				"",
				{
					
				}
			],
			[
				/dota|max|EHOME/,
				/dota|max|EHOME/
			]
		],
		"content" : [
			[
				"",
				{
					
				}
			],
			[
				/EHOME|IG|LGD|EG/,
				/EHOME|IG|LGD|EG/
			]
		]
	},
}


>db.dota2news.status()
{
	"ns" : "maxnews.dota2news",
	"count" : 5748,
	"size" : 37038032,
	"avgObjSize" : 6443.63813500348,
	"storageSize" : 41570304,
	"numExtents" : 6,
	"nindexes" : 6,
	"lastExtentSize" : 20971520,
	"totalIndexSize" : 2125760,
	"indexSizes" : {
		"_id_" : 196224,
		"newsid_1" : 179872,
		"timestamp_-1_type_1_show_1" : 261632,
		"title_text" : 613200,
		"title_1" : 416976,
		"title_1_content_1" : 457856
	},
	"ok" : 1
}
```

