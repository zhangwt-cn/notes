# 起因
在接口接收url参数的时候出现中文乱码
```shell
// 乱码
url?name=测试   ->  url?name=娴嬭瘯
```
前端接口传入的name是测试，但是服务端接收到的是娴嬭瘯

# 转换正常中文方案
1. 找到在的编码和原来编码，在[这里](http://www.mytju.com/classcode/tools/messycoderecover.asp)输入乱码内容
   
   <img width="1179" alt="image" src="https://github.com/zhangwt-cn/notes/assets/52098594/207e6806-fd6c-4803-a6aa-635107b122ee">
   
   找到转换正常的编码，`UTF-8` 就是原来的编码，`GBK` 就是现在的编码
2. 将乱码从现在的编码转换成原来的编码
    ```java
     // 需要找到现在的编码和原来编码 才能转换成正常中文
     String newName = new String(name.getBytes("GBK"), StandardCharsets.UTF_8)
   ```



