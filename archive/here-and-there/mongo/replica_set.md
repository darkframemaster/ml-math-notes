# replica set
[replica set](https://docs.mongodb.com/manual/replication/#replication)

### what is replica set and what is it for
>A replica set in MongoDB is a group of mongod processes that maintain the same data set. Replica sets provide redundancy(冗余，备份) and high availability, and are the basis for all production deployments. 
>
>With multiple copies of data on different database servers, replication provides a level of fault tolerance(容错功能) against the loss of a single database server.
>
>In some cases, replication can provide increased read capacity as clients can send read operations to different servers.

### how it works
> A replica set contains several data bearing nodes(轴节点) and optionally one arbiter node(仲裁节点),Of the data bearing nodes, one and only one member is deemed(被视为) the primary node, while the other nodes are deemed secondary nodes.
> 
> The primary node receives all write operations. A replica set can have only one primary capable of confirming writes with { w: "majority" } write concern; although in some circumstances(情况), another mongod instance may transiently(暂时的) believe itself to also be primary. [1] The primary records all changes to its data sets in its operation log.

![](https://docs.mongodb.com/manual/_images/replica-set-read-write-operations-primary.png)

>The secondaries replicate the primary’s oplog and apply the operations to their data sets such that the secondaries’ data sets reflect the primary’s data set. If the primary is unavailable, an eligible(合适的) secondary will hold an election(选举) to elect(选择) itself the new primary.

![](https://docs.mongodb.com/manual/_images/replica-set-primary-with-two-secondaries.png)

>You may add an extra mongod instance to a replica set as an arbiter. Arbiters do not maintain a data set. The purpose of an arbiter is to maintain a quorum(仲裁) in a replica set by responding to heartbeat and election requests by other replica set members. 

![](https://docs.mongodb.com/manual/_images/replica-set-primary-with-secondary-and-arbiter.png)

>An arbiter will always be an arbiter whereas a primary may step down and become a secondary and a secondary may become the primary during an election.

## configuration
Build three mongod process.
```bash
# host=127.0.0.1 port=27018
$echo "replSet = rep_set_name" >> /etc/mongo/repset_one.conf
$mongod -f /etc/mongo/repset_one.conf

# host=127.0.0.1 port=27019
$echo "replSet = rep_set_name" >> /etc/mongo/repset_two.conf
$mongod -f /etc/mongo/repset_two.conf

# host=127.0.0.1 port=27020
$echo "replSet = rep_set_name" >> /etc/mongo/repset_three.conf
$mongod -f /etc/mongo/repset_three.conf
```

Connect to one of the mongod process, and config the repset.
```bash
$mongo 127.0.0.1:27018
# check repset status before config.
>rs.status()
 {  
	"startupStatus" : 3,	
	"info" : "run rs.initiate(...) if not yet done for the set",
	"errmsg" : "can't get local.system.replset config from self or any seed (EMPTYCONFIG)",
	"ok" : 0
 }
>cfg = {_id : "rep_set_name", members :[
... {_id: 0, host: '127.0.0.1:27018'},
... {_id: 1, host: '127.0.0.1:27019'},
... ]}
>rs.initiate(cfg)
 {	
	"info" : "Config now saved locally.  Should come online in about a minute.",  
	"ok" : 1
 }
>rs.status()
...
```

Make secondary node readable.
```bash
SECONDARY>db.foo.find()
error: { "$err" : "not master and slaveok=false", "code" : 13435}
# After last configuration, secondary node is not readable, run `rs.slaveOk()` to fix.
SECONDARY>rs.slaveOk()
```

Add a arbiter node.
```bash
PRIMARY>rs.addArb("127.0.0.1:27020")
{"ok" : 1 }
# connect to arbiter node.
# arbiter will not store a data copy.
ARBITER>rs.status()
ARBITER>show dbs

# check db's character in repset.
ARBITER>db.isMaster()
```

Turn down the Primary node.
```
# assume the primary node is 127.0.0.1:27018
PRIMARY>use admin
PRIMARY>db.shutdownServer()

# connect to secondary node, which will be the new primary node
PRIMARY>rs.status()
PRIMARY>use admin
PRIMARY>db.shutdownServer()
{err: '...'}

# restart the node 127.0.0.1:27018
$mongod -f /etc/mongo/repset_one.conf
$mongo localhost:127.0.0.1:27018
SECONDARY>rs.status()
SECONDARY>rs.slaveOk()
``` 





