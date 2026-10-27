# introduction to etcd
## what is etcd
ETCD是一个一致的分布式密钥值存储。在分布式系统中主要用作单独的协调服务。

>etcd is pronounced /ˈɛtsiːdiː/, and means distributed etc directory.

etcd是一个提供一致性的分布式服务，但是对于客户端而言，并不需要知道服务的leader，对于具有强一致性要求的请求，etcd会讲请求发至leader节点，对于不需要强一致性需求的请求，etcd的任意节点都可以进行处理。

- [etcd in github](https://github.com/etcd-io/etcd)
- [read the doc of etcd](https://etcd.readthedocs.io/en/latest/index.html)

## install
### install use docker
这里将讲解如何使用docker部署etcd服务，这也是推荐的使用etcd的方法，如果你只是想在本地尝试一下，你可以直接查看`install directly`部分的内容。

这里的使用配置文件的方式进行配置，更多的配置方法请查看：[configuration](https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/configuration.md)


### install directly
你也可以直接运行当前目录下的`install.sh`的文件进行安装测试，该脚本在ubuntu系统中测试通过，请注意修改对应的package.

你也可以在这里找到更多的版本和下载的方式：[etcd releases](https://github.com/etcd-io/etcd/releases)

```bash
$uname -a
Linux f5aa234bec36 4.9.93-linuxkit-aufs #1 SMP Wed Jun 6 16:55:56 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
```

```bash
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
```

## runtime reconfiguration