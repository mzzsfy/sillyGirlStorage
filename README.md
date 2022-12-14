# 傻妞数据存储

备份了个人认为比较好用版本的傻妞,升级后仓库内插件可能不能兼容,不建议升级

二进制文件[点我](./bin)

web插件文件[点我](./webPlugin)

人形傻妞插件[点我](./pagermaid-modify)


## docker

#docker #傻妞
```bash
docker run -itd --name sillygirl -p 8080:8080 --restart always -v "$(pwd)"/sillyGirl:/etc/sillyGirl mzzsfy/sillygirl:latest
```
交互:
```bash
docker attach sillygirl
```

详情:

https://hub.docker.com/r/mzzsfy/sillygirl

node-onebot/oicq:

https://hub.docker.com/r/mzzsfy/node-onebot

cqhttp:  

https://hub.docker.com/r/mzzsfy/go-cqhttp
