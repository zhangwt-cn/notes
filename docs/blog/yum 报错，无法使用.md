### 背景
在中标麒麟`Linux master01 4.19.90-17.5.ky10.aarch64`服务器上升级安装`python` #12 之后发现`yum`无法使用了，报错信息如下
```log
[root@master01 yum-src]# yum
Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
ModuleNotFoundError: No module named 'dnf'
```
大多数博客都是让修改`/usr/bin/yum`中第一行，将`#!/usr/bin/python3` 改为重新安装之后的`python`环境路径，请先尝试这个方法能不能解决，如不能解决请继续看下去
## 报错原因
在重新安装`python`环境的时候执行了`rpm -qa|grep python3|xargs rpm -ev --allmatches --nodeps` 和 `whereis python3 |xargs rm -frv` 将`yum`依赖的`python`环境全部删除了，导致`yum`执行报错

## 解决步骤
[中标麒麟rpm](https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/)
### rpm 包准备
- [python3-3.7.4-8.se.01.ky10.x86_64.rpm](https://update.cs2c.com.cn/NS/V10/V10SP1/os/adv/lic/appstore/x86_64/Packages/python3-3.7.4-8.se.01.ky10.x86_64.rpm)
- [python3-libdnf-0.37.2-2.ky10.aarch64.rpm](https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-libdnf-0.37.2-2.ky10.aarch64.rpm)
- [python3-setuptools-40.4.3-4.ky10.noarch.rpm](https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-setuptools-40.4.3-4.ky10.noarch.rpm)
- [python3-rpm-generators-9-1.ky10.noarch.rpm](https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-rpm-generators-9-1.ky10.noarch.rpm)
- [python3-rpm-4.15.1-12.ky10.aarch64.rpm](https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-rpm-4.15.1-12.ky10.aarch64.rpm)
- [python3-libcomps-0.1.8-20.ky10.aarch64.rpm](https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-libcomps-0.1.8-20.ky10.aarch64.rpm)
- python3-gpgme-1.13.1-5.ky10.aarch64  无法找到
- [python3-gpg-1.13.1-6.p01.ky10.aarch64](https://update.cs2c.com.cn/NS/V10/V10SP1/os/adv/lic/updates/aarch64/Packages/python3-gpg-1.13.1-6.ky10.ky10.aarch64.rpm)
- python3-hawkey-0.37.2-2.ky10.aarch64 无法找到

> 在线下载，也可以先下载到本地再上传到服务器
```
wget https://update.cs2c.com.cn/NS/V10/V10SP1/os/adv/lic/appstore/x86_64/Packages/python3-3.7.4-8.se.01.ky10.x86_64.rpm
wget https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-libdnf-0.37.2-2.ky10.aarch64.rpm
wget https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-setuptools-40.4.3-4.ky10.noarch.rpm
wget https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-rpm-generators-9-1.ky10.noarch.rpm
wget https://update.cs2c.com.cn/NS/V10/V10SP1.1/os/adv/lic/base/aarch64/Packages/python3-rpm-4.15.1-12.ky10.aarch64.rpm
wget https://update.cs2c.com.cn/NS/V10/V10SP1/os/adv/lic/updates/aarch64/Packages/python3-gpg-1.13.1-6.ky10.ky10.aarch64.rpm
```

### 安装依赖
1. 安装`python rpm`
```
rpm -ivh python3-3.7.4-8.se.01.ky10.x86_64.rpm
```
2. 拷贝`dnf`、`gpg ` 和 `hawkey`
找一台相同环境yum正常的服务器，查询对应包位置拷贝过去
```
# 查找dnf 、gpg  和 hawkey 位置
find / -name gpg
```
> 正常情况下`dnf` 包在`/usr/lib/python3.7/site-packages/`下，`gpg` 和 `hawkey`都在`/usr/lib64/python3.7/site-packages/` 路径下，将这三个包拷贝到yum 有问题的服务器`/usr/lib/python3.7/site-packages/`目录下

**依赖包路径可能会有所不同，主要区别于`python`的版本，例如如果`yum`使用的是`python2.7`的话，依赖包路径应该是`/usr/lib/python2.7/site-packages/`**

3. 安装其他依赖
> 必须按照顺序安装
```
rpm -ivh python3-libdnf-0.37.2-2.ky10.aarch64.rpm
rpm -ivh python3-setuptools-40.4.3-4.ky10.noarch.rpm
rpm -ivh python3-rpm-generators-9-1.ky10.noarch.rpm
rpm -ivh python3-rpm-4.15.1-12.ky10.aarch64.rpm
rpm -ivh python3-libcomps-0.1.8-20.ky10.aarch64.rpm
```
4. 执行`yum` 检查是否正常

### 依赖缺失错误输出
```
# 缺少 dnf
[root@master01 yum-src]# yum
Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
ModuleNotFoundError: No module named 'dnf'

# 缺少 python3-libdnf
Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
  File "/usr/local/python3/lib/python3.7/site-packages/dnf/__init__.py", line 30, in <module>
    import dnf.base
  File "/usr/local/python3/lib/python3.7/site-packages/dnf/base.py", line 29, in <module>
    import libdnf.transaction
ModuleNotFoundError: No module named 'libdnf'

# 缺少 python3-rpm
[root@master01 yum-src]# yum
Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
  File "/usr/lib/python3.7/site-packages/dnf/__init__.py", line 30, in <module>
    import dnf.base
  File "/usr/lib/python3.7/site-packages/dnf/base.py", line 31, in <module>
    from dnf.comps import CompsQuery
  File "/usr/lib/python3.7/site-packages/dnf/comps.py", line 27, in <module>
    from dnf.exceptions import CompsError
  File "/usr/lib/python3.7/site-packages/dnf/exceptions.py", line 22, in <module>
    import dnf.util
  File "/usr/lib/python3.7/site-packages/dnf/util.py", line 30, in <module>
    import dnf.callback
  File "/usr/lib/python3.7/site-packages/dnf/callback.py", line 22, in <module>
    import dnf.yum.rpmtrans
  File "/usr/lib/python3.7/site-packages/dnf/yum/rpmtrans.py", line 26, in <module>
    import rpm
ModuleNotFoundError: No module named 'rpm'


# 缺少python3-libcomps
[root@master01 yum-src]# yum
Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
  File "/usr/lib/python3.7/site-packages/dnf/__init__.py", line 30, in <module>
    import dnf.base
  File "/usr/lib/python3.7/site-packages/dnf/base.py", line 31, in <module>
    from dnf.comps import CompsQuery
  File "/usr/lib/python3.7/site-packages/dnf/comps.py", line 36, in <module>
    import libcomps
ModuleNotFoundError: No module named 'libcomps'

# 缺少 gpg
[root@master01 yum-src]# yum
Traceback (most recent call last):
  File "/usr/lib/python3.7/site-packages/dnf/crypto.py", line 35, in <module>
    from gpg import Context
ModuleNotFoundError: No module named 'gpg'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
  File "/usr/lib/python3.7/site-packages/dnf/__init__.py", line 30, in <module>
    import dnf.base
  File "/usr/lib/python3.7/site-packages/dnf/base.py", line 34, in <module>
    from dnf.db.history import SwdbInterface
  File "/usr/lib/python3.7/site-packages/dnf/db/history.py", line 28, in <module>
    from dnf.yum import misc
  File "/usr/lib/python3.7/site-packages/dnf/yum/misc.py", line 30, in <module>
    import dnf.crypto
  File "/usr/lib/python3.7/site-packages/dnf/crypto.py", line 38, in <module>
    import gpgme
ModuleNotFoundError: No module named 'gpgme'

# 缺少hawkey
[root@master01 yum-src]# yum
Traceback (most recent call last):
  File "/usr/bin/yum", line 57, in <module>
    from dnf.cli import main
  File "/usr/lib/python3.7/site-packages/dnf/__init__.py", line 30, in <module>
    import dnf.base
  File "/usr/lib/python3.7/site-packages/dnf/base.py", line 44, in <module>
    import dnf.conf
  File "/usr/lib/python3.7/site-packages/dnf/conf/__init__.py", line 40, in <module>
    from dnf.conf.config import PRIO_DEFAULT, PRIO_MAINCONFIG, PRIO_AUTOMATICCONFIG
  File "/usr/lib/python3.7/site-packages/dnf/conf/config.py", line 33, in <module>
    import hawkey
ModuleNotFoundError: No module named 'hawkey'
```
> 检查`/usr/lib/python3.7/site-packages/`(不同版本可能有所差异，具体要看`yum`使用的`python`版本)下是否存在对应包，如果不存在，请按照上述方式安装相关依赖。





