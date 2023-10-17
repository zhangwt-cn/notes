```conf
# 匹配路径
location /websocket {
    proxy_set_header  Host $host;
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header  X-Forwarded-Proto   $scheme;
    # 代理地址
    proxy_pass        http://127.0.0.1:8040/websocket;
    
    # 关键配置 start
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    # 关键配置 end
} 

``` 