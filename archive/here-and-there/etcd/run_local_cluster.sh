TOKEN=token-01
CLUSTER_STATE=new
NAME_1=machine-1
NAME_2=machine-2
NAME_3=machine-3
HOST_1=localhost
HOST_2=localhost
HOST_3=localhost
EXPORT_CLIENT_PORT_1=2379 # default
EXPORT_CLIENT_PORT_2=2479
EXPORT_CLIENT_PORT_3=2579
EXPORT_PEER_PORT_1=2380 # default
EXPORT_PEER_PORT_2=2480
EXPORT_PEER_PORT_3=2580
CLUSTER=${NAME_1}=http://${HOST_1}:${EXPORT_PEER_PORT_1},${NAME_2}=http://${HOST_2}:${EXPORT_PEER_PORT_2},${NAME_3}=http://${HOST_3}:${EXPORT_PEER_PORT_3}

rm -rf /tmp/etcd-data/${NAME_1} && mkdir -p /tmp/etcd-data/${NAME_1} && \
  docker rmi gcr.io/etcd-development/etcd:v3.3.9 || true && \
  docker run \
  -p ${EXPORT_CLIENT_PORT_1}:2379 \
  -p ${EXPORT_PEER_PORT_1}:2380 \
  --mount type=bind,source=/tmp/etcd-data/${NAME_1},destination=/etcd-data \
  --name ${NAME_1} \
  gcr.io/etcd-development/etcd:v3.3.9 \
  /usr/local/bin/etcd \
  --name ${NAME_1} \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-token ${TOKEN} \
  --initial-cluster-state ${CLUSTER_STATE}

rm -rf /tmp/etcd-data/${NAME_2} && mkdir -p /tmp/etcd-data/${NAME_2} && \
  docker run \
  -p ${EXPORT_PEER_PORT_2}:2379 \
  -p ${EXPORT_PEER_PORT_2}:2380 \
  --mount type=bind,source=/tmp/etcd-data/${NAME_2},destination=/etcd-data \
  --name ${NAME_2} \
  gcr.io/etcd-development/etcd:v3.3.9 \
  /usr/local/bin/etcd \
  --name ${NAME_2} \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-token ${TOKEN} \
  --initial-cluster-state ${CLUSTER_STATE}


rm -rf /tmp/etcd-data/${NAME_3} && mkdir -p /tmp/etcd-data/${NAME_3} && \
  docker run \
  -p ${EXPORT_PEER_PORT_3}:2379 \
  -p ${EXPORT_PEER_PORT_3}:2380 \
  --mount type=bind,source=/tmp/etcd-data/${NAME_3},destination=/etcd-data \
  --name ${NAME_3} \
  gcr.io/etcd-development/etcd:v3.3.9 \
  /usr/local/bin/etcd \
  --name ${NAME_3} \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-token ${TOKEN} \
  --initial-cluster-state ${CLUSTER_STATE}


docker exec ${NAME_1} /bin/sh -c "/usr/local/bin/etcd --version"
docker exec ${NAME_1} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl version"
docker exec ${NAME_1} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl endpoint health"
docker exec ${NAME_1} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl put foo bar"
docker exec ${NAME_1} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl get foo"

docker exec ${NAME_2} /bin/sh -c "/usr/local/bin/etcd --version"
docker exec ${NAME_2} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl version"
docker exec ${NAME_2} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl endpoint health"
docker exec ${NAME_2} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl put foo bar"
docker exec ${NAME_2} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl get foo"

docker exec ${NAME_3} /bin/sh -c "/usr/local/bin/etcd --version"
docker exec ${NAME_3} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl version"
docker exec ${NAME_3} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl endpoint health"
docker exec ${NAME_3} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl put foo bar"
docker exec ${NAME_3} /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl get foo"