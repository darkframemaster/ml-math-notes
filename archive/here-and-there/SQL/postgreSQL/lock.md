## Locks in postgreSQL
[postgreSQL9.6 document](https://www.postgresql.org/docs/current/static/explicit-locking.html)

Lock is a very powerful and dangerous tool.

Lock can control current access to data in database, which is helpful for you to keep your data consistency(数据一致性), but it can also cause `DeadLock` which will cause all the access to the data be denied.

And there is a few mention when use lock:

* Lock is used within a `transaction`.

### table-level lock
```sql
BEGIN;
LOCK TABLE user IN SHARE ROW EXCLUSIVE MODE;
...
COMMIT;
-- or rollback if exception occur;
```

### row-level lock
```sql
SELECT * FROM user WHERE id = 1 FOR UPDATE NOWAIT;
```