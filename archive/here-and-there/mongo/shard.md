# sharding
>Sharding is a method for distributing data across multiple machines. MongoDB uses sharding to support deployments with **very large data sets** and **high throughput operations**.

>MongoDB supports horizontal scaling through sharding.

>MongoDB shards data at the **collection level**, distributing the collection data across the shards in the cluster.



## Components of a sharded cluster
A MongoDB sharded cluster consists of the following components:

* **shard**: Each shard contains a subset of the sharded **data**. Each shard can be deployed as a replica set.
* **mongos**: The mongos acts as a **query router**, providing an interface between client applications and the sharded cluster.
* **config servers**: Config servers store **metadata and configuration settings** for the cluster. As of MongoDB 3.4, config servers must be deployed as a replica set (CSRS).

### shards
Users, clients, or applications should only directly connect to a shard to perform local administrative and maintenance operations.

Performing queries on a single shard only returns a **subset of data**. Connect to the mongos to perform cluster level operations, including read or write operations.

#### Primary Shard¶
Each database in a sharded cluster has a primary shard that **holds all the un-sharded** collections for that database.The primary shard has no relation to the primary in a replica set.
 
The mongos **selects** the primary shard when creating a new database by picking the shard in the cluster that has the **least amount of data**. mongos uses the `totalSize` field returned by the `listDatabase` command as a part of the selection criteria.

To change the primary shard for a database, use the `movePrimary` command. 

The process of migrating the primary shard may take significant time to complete, and you **should not access** the collections associated to the database until it completes.

Depending on the amount of data being migrated, the migration may affect overall cluster operations. Consider the impact to cluster operations and network load before attempting to change the primary shard.

>**WARNING**
If you use the movePrimary command to move un-sharded collections, you must either restart all mongos instances, or use the flushRouterConfig command on all mongos instances before reading or writing any data to any unsharded collections that were moved. This action ensures that the mongos is aware of the new shard for these collections.
If you do not update the mongos instances’ metadata cache after using movePrimary, the mongos may miss data on reads, and may not write data to the correct shard. To recover, you must manually intervene.

```bash
# useages of related commands
# see an overview of the cluster.
>sh.status()

# movePrimary first changes the primary shard in the cluster metadata, and then migrates all un-sharded collections to the specified shard. 
>db.runCommand( { movePrimary: <databaseName>, to: <newPrimaryShard> } )

# removeShard: removes a shard from a sharded cluster.
# This command can also be used to check the remove progress's status
# MongoDB drains the shard by using the balancer to move the shard’s chunks to other shards in the cluster. Once the shard is drained, MongoDB removes the shard from the cluster.
>use admin
>db.runCommand( { removeShard : "bristol01" } )
```
#### Sharded Cluster Security (topic for next share)
[doc](https://docs.mongodb.com/manual/core/sharded-cluster-shards/#sharded-cluster-security)

### Config server
Config servers store the metadata for a sharded cluster. The metadata **reflects state and organization for all data and components** within the sharded cluster. The metadata includes the list of chunks on every shard and the ranges that define the chunks.

* The **mongos** instances **cache** this data and use it to route read and write operations to the correct shards. mongos updates the cache when there are metadata changes for the cluster, such as **Chunk Splits** or **adding a shard**. Shards also read chunk metadata from the config servers.
* The config servers also store Authentication configuration information such as Role-Based Access Control or internal authentication settings for the cluster.
* MongoDB also uses the config servers to manage distributed locks.
* The admin database and the config database exist on the config servers.

Each sharded cluster must have its own config servers. Do not use the same config servers for different sharded clusters.

>**WARNING**
Administrative(行政) operations conducted on config servers may have significant impact on sharded cluster performance and availability. Depending on the number of config servers impacted, the cluster may be read-only or offline for a period of time.

Config servers store metadata in the **Config Database.**

>**IMPORTANT**
Always back up the config database before doing any maintenance on the config server.

MongoDB writes data to the config database when the metadata changes, such as after a chunk migration or a chunk split.

Users should avoid writing directly to the config database in the course of normal operation or maintenance.

To access the config database, issue the following command from the mongo shell:

```bash
use config
```
In general, you should **never edit** the content of the config database directly. 

### Mongos
MongoDB mongos instances **route queries and write operations** to shards in a sharded cluster. mongos provide the only interface to a sharded cluster from the perspective of applications. Applications never connect or communicate directly with the shards.

[doc](https://docs.mongodb.com/manual/core/sharded-cluster-query-router/)
#### Routing And Results Process¶
A mongos instance routes a query to a cluster by:

1. Determining the list of shards that must receive the query.
2. Establishing(构造) a **cursor on all targeted shards**.

The mongos then merges the data from each of the targeted shards and returns the result document. Certain query modifiers, such as sorting, are performed on a shard such as the primary shard before mongos retrieves the results.

#### Sorting:
如果查询结果没有排序, mongos 会打开一个结果游标,对所有分片的游标依次轮询取得数据.
如果查询通过 sort() 指明要排序, mongos 会将 $orderby 选项发送给所有分片,当 mongos 接收到结果之后,会先进行 合并排序 再返回给应用程序.

#### Limits
如果查询通过 limit() 限制了返回文档的数量, mongos 会将这个限制发送到所有分片,并且在返回给应用程序之前再次使用这个限制对结果进行过滤.

#### Skips
If the query specifies a number of records to skip using the skip() cursor method, the mongos **cannot** pass the skip to the shards, but rather retrieves unskipped results from the shards and **skips the appropriate number of documents when assembling the complete result**.

When used in conjunction with a limit(), the mongos will pass the limit plus the value of the skip() to the shards to improve the efficiency of these operations.

#### Confirm Connection to mongos Instances
To detect if the MongoDB instance that your client is connected to is mongos, use the `isMaster` command. When a client connects to a mongos, isMaster returns a document with a msg field that holds the string `isdbgrid`. For example:

```json
{
   "ismaster" : true,
   "msg" : "isdbgrid",
   "maxBsonObjectSize" : 16777216,
   "ok" : 1
}
```


### Sharding Cluster Availability
#### Config Server Availability
If the config server replica set loses its primary and cannot elect a primary, the cluster’s metadata becomes read only. You can still read and write data from the shards, but no chunk migration or chunk splits will occur until the replica set can elect a primary. If all config databases become unavailable, the cluster can become inoperable.

The mongos instances cache the metadata from the config servers. As such, if all config server members become unavailable, you can still use the cluster if you do not restart the mongos instances until after the config servers are accessible again. If you restart the mongos instances before the config servers are available, the mongos cannot route reads and writes.



## Considerations Before Sharding
* Careful consideration in choosing the shard key is necessary for ensuring cluster performance and efficiency. You **cannot** change the shard key after sharding, nor can you unshard a sharded collection. 
* Sharding has certain **operational requirements and restrictions**.
* If queries do not include the shard key or the prefix of a compound shard key, mongos performs a **broadcast operation**, querying all shards in the sharded cluster. These scatter/gather queries can be long running operations.



## Sharded and Non-Sharded Collections
A database can have a **mixture of sharded and unsharded collections**. Sharded collections are partitioned and distributed across the shards in the cluster. Unsharded collections are stored on a primary shard. Each database has its own **primary shard**.

![](https://docs.mongodb.com/manual/_images/sharded-cluster-primary-shard.bakedsvg.svg)



## Connecting to a Sharded Cluster
You must connect to a **mongos router** to interact with any collection in the sharded cluster. This includes sharded and unsharded collections. Clients should never connect to a single shard in order to perform read or write operations.

Users, clients, or applications should only directly connect to a shard to perform local administrative and maintenance operations.

![](https://docs.mongodb.com/manual/_images/sharded-cluster-mixed.bakedsvg.svg)



## Shard keys
The shard key determines the distribution of the collection’s documents among the cluster’s shards. The shard key is either **an indexed field or indexed compound fields** that exists in **every document** in the collection.

MongoDB partitions data in the collection using ranges of shard key values. Each range defines a **non-overlapping**(不重叠的) range of shard key values and is associated with a chunk.

MongoDB attempts to distribute chunks evenly among the shards in the cluster. The shard key has a **direct relationship to the effectiveness of chunk distribution**.

>**IMPORTANT**
Once you shard a collection, the shard key and the shard key values are immutable; i.e.
	•	You **cannot** select a different shard key for that collection.
	•	You **cannot** update the values of the shard key fields.
	
### shard key index
All sharded collections **must have an index that supports the shard key**; i.e. the index can be an index on the shard key or a compound index where the shard key is a prefix of the index.

* If the collection is empty, `sh.shardCollection()` creates the index on the shard key if such an index does not already exists.
* If the collection is not empty, you must create the index first before using `sh.shardCollection()`.

```bash
# Shards a collection using the key as a the shard key.
> sh.shardCollection(namespace, key, unique, options)

>sh.shardCollection("dbname.colname", {fieldname: 1 } )
>sh.shardCollection(
..."dbname.colname",
...{ fieldname: 1 },
...false,
...{ numInitialChunks: 5, collation: { locale: "simple" } }
...)
```

### Unique Indexes
For a sharded collection, **only the _id field index and the index on the shard key or a compound index where the shard key is a prefix can be unique**:

* You **cannot** shard a collection that has unique indexes on other fields.
* You **cannot** create unique indexes on other fields for a sharded collection.

Through the use of the unique index on the shard key, MongoDB can enforce uniqueness on the shard key values.

To enforce uniqueness on the shard key values, pass the `unique` parameter as `true` to the `sh.shardCollection()` method:

* If the collection is **empty**, `sh.shardCollection()` creates the unique index on the shard key if such an index does not already exists.
* If the collection is not empty, you must create the index first before using `sh.shardCollection()`.

A unique shard key value can exist on no more than a single chunk at any given time. This is why **A chunk that only contains documents with a single shard key value cannot be split.**



## choose a shard key
At minimum, consider the consequences of the **cardinality, frequency, and rate of change of a potential shard key**.

### cardinality(基数)
The **cardinality (chunk num)** of a shard key determines the *maximum number of chunks* the balancer can create. If a shard key has a cardinality of 4, then there can be no more than 4 chunks within the sharded cluster, each storing one unique shard key value. 

The following image illustrates a sharded cluster using the field X as the shard key. If X has low cardinality(3), the distribution of inserts may look similar to the following:

![](https://docs.mongodb.com/manual/_images/sharded-cluster-ranged-distribution-low-cardinal.bakedsvg.svg)

The cluster in this example would **not scale horizontally**, as incoming writes would only route to a subset of shards.

如果这个字段基数比较低(即没有足够的选择性),你需要添加第二个字段,构成复合字段片键,在使用复合片键时,数据可以被更好地分离.

### frequency
the frequency of the shard key represents **how often a given value occurs in the data**. If the majority of documents contain only a subset of those values, then the chunks storing those documents become a bottleneck within the cluster. Furthermore, as those chunks grow, they may become indivisible chunks as they cannot be split any further. This *reduces or removes the effectiveness of horizontal scaling within the cluster.*

![](http://docs.mongoing.com/manual-zh/_images/sharded-cluster-ranged-distribution-frequency.png)

不要让数据非常集中到某一部分的chunk中。也可以使用复合字段。

### Monotonically Changing Shard Keys
A shard key on a value that increases or decreases monotonically(单调变化) is **more likely** to distribute inserts to a **single shard within the cluster**.

![](http://docs.mongoing.com/manual-zh/_images/sharded-cluster-monotonic-distribution.png)

If the shard key value is always increasing, all new inserts are routed to the chunk with maxKey as the upper bound. If the shard key value is always decreasing, all new inserts are routed to the chunk with minKey as the lower bound. The shard containing that chunk becomes the bottleneck for write operations.

If your data model requires sharding on a key that changes monotonically, consider using **Hashed Sharding**.
	


## A balance cluster
MongoDB ensures a balanced cluster using two processes: **chunk splitting** and the **balancer**.

### Data Partitioning with Chunks
MongoDB uses the shard key associated to the collection to partition the data into **chunks**. A chunk consists of a subset of sharded data. Each chunk has a **inclusive lower and exclusive upper range based on the shard key [lower, upper	)**.

The mongos routes writes to the appropriate chunk based on the **shard key value**.  MongoDB splits chunks when:
	
* They grows beyond the configured **chunk size**
* The number of documents in the chunk exceeds `Maximum Number of Documents Per Chunk to Migrate`. Both inserts and updates can trigger a chunk split.

The smallest range a chunk can represent is a single unique shard key value. **A chunk that only contains documents with a single shard key value cannot be split.**

To create splits, MongoDB does **not** migrate any data or affect the shards. Splits may lead to an uneven distribution of the chunks for a collection across the shards. In such cases, the balancer redistributes chunks across shards.

The balancer is a background process that manages chunk migrations. If **the difference in number of chunks between the largest and smallest shard exceed the** `migration thresholds`, the balancer begins migrating chunks across the cluster to ensure an even distribution of data.

`moveChunk directory`. If some error occurs during a migration, these files may be helpful in recovering documents affected during the migration.

#### Modify Chunk Size in a Sharded Cluster
The default chunk size for a sharded cluster is **64 megabytes**. This default chunk size works well for most deployments; however, if you notice that automatic migrations have more **I/O** than your hardware can handle, you may want to **reduce?** the chunk size. For automatic splits and migrations, a small chunk size leads to more rapid and frequent migrations. The allowed range of the chunk size is between **1 and 1024 megabytes ([1 M, 1024 M])**, inclusive.

```bash
# modify chunk size
# 1.Connect to any mongos in the cluster using the mongo shell.

# 2.Issue the following command to switch to the Config Database:
>use config

# 3.Issue the following save() operation to store the global chunk size configuration value:
>db.settings.save( { _id:"chunksize", value: <sizeInMB> } ) 
```

Modifying the chunk size has several **limitations**:

*	Automatic splitting only occurs on insert or update.
* If you lower the chunk size, it may take time for all chunks to split to the new size.
* Splits cannot be **undone(打开)**. Which means if you increase the chunk size, existing chunks grow only through insertion or updates until they reach the new size.
* The allowed range of the chunk size is between 1 and 1024 megabytes, inclusive.


### Sharded Cluster Balancer
The MongoDB balancer is a **background process** that monitors the number of chunks on each shard. When the number of chunks on a given shard reaches specific migration thresholds, the balancer attempts to **automatically(even when adding or deleting a shard)** migrate chunks **between shards** and reach an equal number of chunks per shard.

The balancing procedure for sharded clusters is entirely transparent(透明) to the user and application layer, though there may be some performance impact while the procedure takes place.

Chunk migrations carry some **overhead in terms of bandwidth and workload**, both of which can impact database performance.The balancer attempts to minimize the impact by:

* Restricting(限制) a shard to at most one migration at any given time; *From version `3.4` for a sharded cluster with n shards, MongoDB can perform at most n/2 (rounded down) simultaneous(并发的) chunk migrations.*
* Starting a balancing round **only** when the difference in the number of chunks between the shard with the greatest number of chunks for a sharded collection and the shard with the lowest number of chunks for that collection reaches the `migration threshold`s.


Changed in 3.4: The balancer runs on the **primary** of the **config server** replica set.

#### How
>The balancer migrates chunks from shards with more chunks to shards with a fewer number of chunks. The balancer migrates the chunks until there is an even distribution of chunks for the collection across the shards. 

从多到少，直到平衡。

#### why
* make read/write operations more efficient.

#### Adding and Removing Shards from the Cluster¶
Adding a shard to a cluster creates an imbalance, since the new shard has no chunks. While MongoDB begins migrating data to the new shard immediately, it can take some time before the cluster balances.

Removing a shard from a cluster creates a similar imbalance, since chunks residing on that shard must be redistributed throughout the cluster. While MongoDB begins **draining a removed shard immediately**, it can take some time before the cluster balances. Do not shutdown the servers associated to the removed shard during this process.



## Sharding Strategy
MongoDB supports two sharding strategies for distributing data across sharded clusters.

### Hashed Sharding
Hashed Sharding involves **computing a hash** of the shard key field’s value. Each chunk is then assigned a range based on the hashed shard key values.

>**TIP**
MongoDB **automatically** computes the hashes when resolving queries using hashed indexes. Applications do not need to compute hashes.

Advantages: While a range of shard keys may be “close”, their hashed values are unlikely to be on the same chunk. Data distribution based on hashed values facilitates **more even data distribution**, especially in data sets where the shard key changes monotonically(单调的).

Disadvantages: However, hashed distribution means that ranged-based queries on the shard key are less likely to target a single shard, resulting in **more cluster wide broadcast** operations.

>**WARNING**
MongoDB hashed indexes truncate floating point numbers to 64-bit integers before hashing. For example, a hashed index would store the same value for a field that held a value of 2.3, 2.2, and 2.9. To prevent collisions, do not use a hashed index for floating point numbers that cannot be reliably converted to 64-bit integers (and then back to floating point). MongoDB hashed indexes do not support floating point values larger than 253.

### Ranged Sharding
Ranged sharding involves **dividing data into ranges** based on the shard key values. Each chunk is then assigned a range based on the shard key values.

Advantages: A range of shard keys whose values are “close” are more likely to reside on the same chunk. This allows for targeted operations as a mongos can route the operations to only the shards that contain the required data.

Disadvantages: The efficiency of ranged sharding depends on the shard key chosen. Poorly considered shard keys can result in **uneven distribution** of data, which can negate(使无效) some benefits of sharding or can cause performance bottlenecks(平颈). See shard key selection for ranged sharding.



## Zones in Sharded Clusters
In sharded clusters, you can create zones of sharded data **based on the shard key**. You can associate each zone with **one or more** shards in the cluster. A shard can associate with any number of *non-conflicting* zones. In a balanced cluster, **MongoDB migrates chunks covered by a zone only to those shards associated with the zone**.

Each zone covers one or more ranges of shard key values. **Each range a zone covers is always inclusive of its lower boundary and exclusive of its upper boundary([lower, upper))**.

![](https://docs.mongodb.com/manual/_images/sharded-cluster-zones.bakedsvg.svg)

You must use fields contained in the shard key when defining a new range for a zone to cover. If using a compound shard key, the range must include the prefix of the shard key. 

When choosing a shard key, carefully consider the possibility of using zone sharding in the future, as you cannot change the shard key after sharding the collection.

Most commonly, zones serve to **improve the locality of data for sharded clusters** that span multiple data centers.

## Operational Restrictions in Sharded Clusters
[doc](https://docs.mongodb.com/manual/core/sharded-cluster-requirements/)



## Deployment
* [deploy sharded cluster ranged sharding](https://docs.mongodb.com/manual/tutorial/deploy-sharded-cluster-ranged-sharding/)
* [deploy sharded cluster hashed sharding](https://docs.mongodb.com/manual/tutorial/deploy-sharded-cluster-hashed-sharding/)

### Production configuration
![](https://docs.mongodb.com/manual/_images/sharded-cluster-production-architecture.bakedsvg.svg)

### Development configuration
![](https://docs.mongodb.com/manual/_images/sharded-cluster-test-architecture.bakedsvg.svg)

###Shard a Collection
To proceed, you must be connected to a **mongos** associated to the target sharded cluster.

To shard a collection, use the `sh.shardCollection()` method. You must specify the **full namespace** of the collection and a document containing the shard key. The database must have sharding enabled, To enable sharding for a database use the `sh.enableSharding("<database>")` method.

Your selection of shard key affects the efficiency of sharding, as well as your ability to take advantage of certain sharding features such as **zones**.

If the collection already contains data, you must create a Indexes on the shard key using the `db.collection.createIndex()` method before using `shardCollection()`.

* For **Hashed Sharding**: create a Hashed Indexes.
* For **Ranged Sharding**: create an index.

If the collection is empty, MongoDB creates the index as part of `sh.shardCollection()`.

The following operation shards the target collection using the **hashed sharding** strategy.

```bash
sh.shardCollection("<database>.<collection>", { <key> : "hashed" } )
```

The following operation shards the target collection using the **ranged sharding** strategy.

```bash
sh.shardCollection("<database>.<collection>", { <key> : <direction> } )
```

#### Remove Shards from an Existing Sharded Cluster
[doc](https://docs.mongodb.com/manual/tutorial/remove-shards-from-cluster/)
```bash
#Ensure the Balancer Process is Enabled
> sh.getBalancerState()
True

#Remove Chunks from the Shard
#From the admin database, run the removeShard command.
> use admin
> db.runCommand( { removeShard: "mongodb0" } )

#If the shard you remove is the primary shard of the sharded collection, run command like this.
> db.runCommand( { movePrimary: "<sharded_collection>", to: "anthor_shard" })

#To clean up all metadata information and finalize the removal, run removeShard again
> db.runCommand( { removeShard: "mongodb0" } )
```

#### Add Shards to a Cluster
[doc](https://docs.mongodb.com/manual/tutorial/add-shards-to-shard-cluster/)
```bash
> sh.addShard( "rs1/mongodb0.example.net:27017" )
```



# Everything you need to know about Sharding
## What is sharding
**Sharding** is a means of partitioning data across servers to enable:

* Scale
	* needed by modern applications to support massive work loads and data volume
* Geo-Locality
	* to support geographically distributed deployments to support optimal UX for customers across vast geographies.
* Hardware optimization
	* performance & cost
* Lower Recovery Times
	* to make RTO feasible

	

Sharding involves a **shard key** defined by a data modeler that describes the partition space of a data set.
	
Data is partitioned into data **chunks** by the shard key, and these chunks are distributed evenly across **shards** that reside across many physical servers.
	
MongoDB provides **3 Types** of Sharding Strategies:
	
* **Ranged**
* **Hashed**: A subset of Range Sharding. 
	* **Hash Shard Key(deviceId) = MD5(deviceId)**
	* Ensures data is distributed randomly within the range of MD5 values.
* **Tag-aware:**
	* Tag-aware sharding allows subset of **shards** to be tagged, and assigned to a sub-range of the shard-key.

### Applying Sharding
| usage | shard key |
|-------|:---------:|
| Scale |  Range or Hash |
| Geo-Locality | Tag-aware |
| Hardware Optimization | Tag-aware |
| Lower Recovery Times | Range or Hash |

## Hardware optimization
* High Memory Ratio Fast Cores HDD: Tag Cache
* Medium Memory Ratio High Compute SSDs: Tag Flash
* Low Memory Ratio Medium Compute HHD: Tag Archive

## Restoration Times
Scenario: Application bug causes logical corruption(污染) of the data, and the database needs to be rolled back to a previous PIT(Point-in-Time). What's RTO(Recovery time objective) does your business require in this event?

```
Total DB snapsize == 100TB

N = Shard number

N == 10:
10 * 10TB Snapshots generated and/or transferred in parallel(水平的).

N == 100:
100 * 1TB Snapshots generated and/or transferred in parallel.
```

## Life cycle of Sharding
1. Design & Development
2. Test/QA
3. Pre-Production
4. Production

### Do i need sharding
* **Throughput**: data from millions of sensors updated in real-time.
* **Latency**: The value of certain attributes need to be accesss with 95% < 10ms to support real-time decisions and automation.
* **Volume**: 1TB of data collected per day. Retained(保留) for 5 years.

### Select a Good Shard Key
* **Critical(关键) Step**
	* Sharding is only effective as the shard key.
	* Shard Key attributes are immutable.
	* Re-sharding is **non-trivial**. Requires re-partitioning data

* **Good Shard key**
	* **Cardinality(基数)**
	* **Write Distribution**
	* **Query Isolation**
	* Reliability
	* Index Locality

```python

# Consider you have five data center and use them to be the shard key.

Key = Data Center

# In this case, there will be only five chunks and may be some of them will grow quickly which can lower the performance of the whole cluster.
# So consider the Cardinality, it is better to use timestamp to be the shard key.

Key = timestamp

# But if we use timestamp, the recent coming data will be write to one shard.
# So consider the Write Distribution, it is better to use HASH(timestamp) to be the shard key

Key = Hash(timestamp)

# If will want to query something, Using Hash(timestamp) as shard key will cause "Scatter-gather query", which means you need to gather datas from many shards.
# So consider the Query Isolation, and assumes bulk of queries on collection are in context of a single deviceId, may be we can use Hash(DiviceId).

Key = Hash(DiviceId)

# And consider the Reliability, if we use hash(timestamp) to be the shard key and one of the shard is not working, may be the whole cluster will be unavailable, while Key hash(DiviceId) will just effect a subset of the data, because the distribution of the hash(timestamp) is evenly.

# But hash(DiviceId) is also a Random Access Index.

Key = DiviceId(random), Timestamp(sequences)

# DiviceId, Timestamp is a Right Balance Index, Right Balance Index may only need to be partially in RAM to be effective(In this case could be some recent data in some of the divices).
```

### Performance Testing

Sharding may results in massive(巨大的) performance degradation(衰退)!

* **Splits** happen on demand as chunks grow
* **Migrations** happen when an imbalance is detected, migrations is very expensive, because it moves data between server.

Best Practices:

* Pre-splits:
	* Hash Shard Key: specify numInitialChunks
		* [shard collection](https://docs.mongodb.com/manual/reference/command/shardCollection/)
	* Custom Shard Key: create a pre-split script
		* [create chunks in shared cluster](https://docs.mongodb.com/manual/tutorial/create-chunks-in-sharded-cluster/)

