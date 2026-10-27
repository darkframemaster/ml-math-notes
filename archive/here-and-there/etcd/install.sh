# better run in a docker component
ETCD_VER=v3.3.9
DOWNLOAD_PATH=/home/tools
INSTALL_PATH=/tmp/etcd
PACKAGE_NAME=etcd-${ETCD_VER}-linux-amd64.tar.gz

# download url. here use github
GITHUB_URL=https://github.com/etcd-io/etcd/releases/download/v3.3.9/${PACKAGE_NAME}

rm -f ${DOWNLOAD_PATH}/${PACKAGE_NAME} && mkdir ${DOWNLOAD_PATH}
rm -rf ${INSTALL_PATH} && mkdir ${INSTALL_PATH}

curl -L ${GITHUB_URL} -o ${DOWNLOAD_PATH}/${PACKAGE_NAME}
tar xzvf ${DOWNLOAD_PATH}/${PACKAGE_NAME} -C ${INSTALL_PATH} --strip-components=1

# simply test
${INSTALL_PATH}/etcd --version
ETCDCTL_API=3 ${INSTALL_PATH}/etcdctl version
