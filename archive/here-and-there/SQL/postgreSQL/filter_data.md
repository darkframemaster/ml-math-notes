```sql
with exclude as (select * from bbs_linking as a left join bbs_dislikelink as b on a.id = b.linking_id where a.link_type!=0 and b.userid = 4553539)
select bbs_linking.id from bbs_linking where link_type!=0 and (topic_id = 1 or topic_id = 2 or topic_id = 3 or topic_id = 4 or topic_id = 5 or topic_id = 6 or topic_id = 7 or topic_id = 9) and not exists(select 1 from exclude where bbs_linking.id = exclude.linking_id) order by modify_at desc limit 20;
```

```sql
select bbs_linking.id from bbs_linking where link_type!=0 and (topic_id = 1 or topic_id = 2 or topic_id = 3 or topic_id = 4 or topic_id = 5 or topic_id = 6 or topic_id = 7 or topic_id = 9) and id not in (1,2,3,4,5,6,7) order by modify_at desc limit 20;
```
