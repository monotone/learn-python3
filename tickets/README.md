# 简易火车票查询
根据实验楼项目["Python3 实现火车票查询工具"](https://www.shiyanlou.com/courses/623/labs/2072/document)学习使用python的练手项目

写的时候火车票网站的数据格式已经发生了变化，自己进行了修正。
最后的测试日期是2017年06月10日。

## 用法
```python
Usage:
    tickets [-gdctkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -c          城际
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
```
