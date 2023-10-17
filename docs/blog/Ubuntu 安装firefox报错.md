在Ubuntu上安装firefox时提示
```shell
Running Firefox as *** in a regular user's session is not supported.  ($XDG_RUNTIME_DIR is /run/user/1001 which is owned by runner.)
```
需要修改目录权限
```shell
sudo chown -R root:root /run/user/1001
```