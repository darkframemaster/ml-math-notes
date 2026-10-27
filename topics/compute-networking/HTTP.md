
### 2.2 HTTP
#### 2.2.2 非持续链接和持续链接
- **非持续链接**：
    - 每个请求/响应对是经一个单独的TCP链接发送。每个TCP链接在服务器发送一个对象后关闭，每个TCP链接只传输一个请求报文和一个响应报文（即只能传输一个对象），T总=T（建立连接）+T（请求文件并响应）+T（传输文件）= **2RTT**（往返时间）+文件传输时间。
	- 缺点：Web服务器负担大  时间消耗大
- **持续链接**：
  - 所有的请求及其相应经相同的TCP链接发送。

### 2.2.3 HTTP报文格式
#### HTTP请求报文（1请求  4首部  最后跟个实体主体）
`GET /somedir/page.html HTTP/1.1`  //**请求行** （3个字段）：方法字段（**GET**，POST，HEAD，PUT，DELETE）    URL字段   HTTP版本字段。

`Host: www.someschool.edu`              //**首部行**：Web代理高速缓存需要

`Connection:close`                                  //**首部行**：是否是持续链接 close表示No

`User-agent:Mozilla/5.0`                        //**首部行** ：用户代理，服务器据此发送相应版本的对象。

`Accept-language:fr`                                //**首部行** ：用户希望得到的语言版本

####HTTP响应报文（1状态 6首部 最后跟个实体体）
`HTTP/1.1 200 OK`                                   //**状态行**（3个字段）：协议版本字段   状态码（200 301 400 404 505）   相应状态信息
   
`connection:close`                                   //**首部行**：链接类型

`Date:Tue, 09 Aug 2011 15:44:04 GMT`                //**首部行**：服务器产生并发送该响应报文的日期和时间。

`Server: Apache/2.2.3 (CentOS)`                 //**首部行**：服务器类型 Apache/2.2.3

`Last-Modified:Tue, 09 Aug 2011 15:11:03 GMT`               //**首部行**：对象创建或者最后修改的日期和时间

`Content-Length:6821`           //**首部行** ：被发送对象的字节数。

`Content-Type: text/html`           //**首部行**：被发送对象的类型

`(data data data data ...)`                          //**实体体**：报文的主要部分

*关于状态码 及其相应信息*

* 200 OK：请求成功
* 301 Moved：请求的对象已经被永久转移了，新的UPL定义在响应报文的Location：首部行中。客户软件将自动获取新的UPL
* 400 Bad Request：一个通用差错代码，指示该请求不能被服务器理解。
* 404 Not Found：被请求的文档不再服务器上。
* 505 HTTP Version Not Supported：服务器不支持请求报文使用的HTTP协议版本。

*用以下的命令查看响应报文*

`telnet cis.poly.edu 80`

`GET /~ross/ HTTP/1.1`

`Host: cis.poly.edu`
