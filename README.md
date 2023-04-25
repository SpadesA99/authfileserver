# authfileserver

### python 文件下载服务,随机生成auth账号,下载完成删除文件


使用说明
```
git clone https://github.com/SpadesA99/authfileserver.git
cd authfileserver
python3 main.py -l "服务器ip" -p 8080 -d "文件目录" -e 1
```

DOCKER
```
docker run -dit --name authfileserver --restart always -p 8080:8080 -v /home/bin:/data python bash -c "git clone https://github.com/SpadesA99/authfileserver.git && cd authfileserver && python3 main.py -l '服务器ip' -p 8080 -d '/data' -e 1"
```
