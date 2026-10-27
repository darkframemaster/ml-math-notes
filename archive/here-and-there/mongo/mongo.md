## Mongo
>MongoDB is an open-source document database that provides high performance, high availability, and automatic scaling.

### install
```shell
sudo apt-get update
sudo apt-get install mongodb
```

```shell
# default config file
/etc/mongodb.conf

# start service
mongod -f [configfile]

# connect to mongo
mongo --host hostname --port port
>help()
```

### The advantages of using documents are:
* Documents (i.e. objects) correspond to native data types in many programming languages.
* Embedded documents and arrays reduce need for expensive joins.
* Dynamic schema supports fluent polymorphism.


* 大众化的数据类型支持
* 允许数据冗余，支持反范式化
* 子文档降低数据操作成本(`ex: join`)
* 动态的schema提供可扩展性

### key features
* **high performance**
	* Support for embedded data models reduces I/O activity on database system.
	* Indexes support faster queries and can include keys from **embedded documents and arrays**.
* **rich query language**
	* data aggregation
	* **text search :** 提供了中文支持(然而要付费)
* **high availability**
	* MongoDB’s replication facility, called replica set, provides:
		* automatic failover
		* data redundancy.

### doc
* max(size) == 16 Mb
	* 避免查询占用太多RAM或频繁访问文件系统
* 写入操作在 `doc` 级是原子性的
* 文档增大
	* `Mongo` 为 `doc` 提供了一些留白，以支持更新导致的数据增大，如果更新导致 `doc` 增大到超过分配的留白，`doc` 将被迁移，这可能导致系统性能下降
	* 对于可能频繁增长的属型，将其设计为范式化对象
* 对 `col` 设置 `MongoDB TTL` 指定文档的生命周期

### special search
* [text search](https://docs.mongodb.com/manual/text-search/)
* [Geospatial Queries](https://docs.mongodb.com/manual/tutorial/geospatial-tutorial/)

### version 3.4
* [MongoDB 3.4 功能改进一览](http://www.mongoing.com/archives/3586)
* [Release Notes for MongoDB 3.4](https://docs.mongodb.com/manual/release-notes/3.4/)