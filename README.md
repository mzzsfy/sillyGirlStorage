# 傻妞数据存储
[![](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fmzzsfy%2FsillyGirlStorage&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/mzzsfy)

备份了个人认为比较好用版本的傻妞,升级后仓库内插件可能不能兼容,不建议升级

二进制文件[点我](./bin)

web插件文件[点我](./webPlugin)

人形傻妞插件[点我](./pagermaid-modify)


## docker

docker版傻妞使用方法

安装
```bash
docker run -itd --name sillygirl -p 8080:8080 --restart always -v "$(pwd)"/sillyGirl:/etc/sillyGirl mzzsfy/sillygirl:latest
```
与傻妞控制台交互
```bash
docker attach sillygirl
```

详情:

https://hub.docker.com/r/mzzsfy/sillygirl


配套docker:  

node-onebot/oicq

https://hub.docker.com/r/mzzsfy/node-onebot

cqhttp:  

https://hub.docker.com/r/mzzsfy/go-cqhttp
