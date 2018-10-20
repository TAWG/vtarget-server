# 微目标应用后台服务

服务使用python 3.6进行开发，使用flask作为web框架,gevent wsgi作为容器，Mysql作为数据存储。

## 1. 启动前准备工作

使用时请先安装python3.安装完成后安装pip。在使用pip安装相应组件。

然后依次安装
```python
    pip install flask
    pip install DBUtils
    pip install PyMySQL
    pip install gevent
```

debug运行时，在命令行使用（暂时使用flask默认端口5000）
```
    python app.py
```


生产环境使用gevent wsgi容器，启动时使用 startup.sh脚本进行拉起，此时默认的端口为80，端口信息可在config.json中进行配置
```
    chmod +x startup.sh
    ./startup.sh
```



## 2.一些说明

使用flask时，由于使用@app.route时，只能将被装饰的方法和app放在同一个文件中，而使用蓝图又有些重，所以进行了部分修改，通过route.json进行路由信息的配置，启动时会读取route.json的信息，通过app.add_url_rule方法将url和对应方法进行绑定。
