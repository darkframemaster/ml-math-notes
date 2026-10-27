# master and slave
## configuration
**master**

```
port = 27017
dbpath = /path/to/data
logpath = /logfile/path
logappend = true/false
master = true
```

**slave**

```
port = 27017
dbpath = /path/to/data
logpath = /logfile/path
logappend = true/false
slave = true
source = hostname:host_mongo_port
```

### test
save data in master

```
$mongo masterip:port
>db.test.save({name: "xuehao"})
```

get data from slave

```
$mongo slaveip:port
>db.test.find({name: "xuehao"})
```

try to insert from slave

```
$mongo slaveip:port
>db.test.save({name: "Max+"})
not master
>db.test.insert({name: "Max+"})
not master
```
