## 使用说明

将三个.csv文件放置于当前目录下

运行data_loader.py得到处理后的json文件

运行requester提交到elastic，之后可通过http请求进行查询

注意：此提交是持久的，不必重复提交，elastic关闭重启后也不需要再提交。