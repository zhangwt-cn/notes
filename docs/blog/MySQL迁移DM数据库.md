## 项目基本情况
 现有技术框架SpringBoot、Mybatis-plus、MySQL等，需要将MySQL替换成DM数据库。

## 达梦数据初始化配置
  1. 设置大小写不敏感，最大程度兼容Mybatis-plus代码(可以减少很多适配工作量和莫名其妙的报错)
  2. DM数据库没有库的概念，只有模式，一般来说默认创建表结构都是关联到以数据库用户名下的表结构中。

## 数据库连接客户端
  1. Mac 
      Mac 没有DM数据库连接的客户端，可以使用idea去连接
  3. WIndows
      可以在官网下载DM客户端，或者[这里下载](https://pan.baidu.com/share/init?surl=Q9aIfJLIdmK4J5oafyQNDw) 提取码：dy3a, [客户端使用说明](https://eco.dameng.com/document/dm/zh-cn/start/tool-dm-manager.html)，**在DM客户端执行SQL执行之后需要手动点击提交数据才会写入数据**（手动执行SQL写入数据未生效，这个问题排查了一上午）。

## DM数据库表结构初始化
**从MySQL中导出所有表结构，转换成DM数据库支持表结构和字段，Windows DM客户端安装之后提供了一个数据迁移工具，表比较多的情况下可以使用它来转换，也可以使用chatgpt来转换。**

### 表结构转换的坑
  1. id自增，MySQL 中id自增语法与DM中不一样
```sql
# MySQL 主键自增，使用AUTO_INCREMENT
`id` int(14) PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT 'id'

# DM 主键自增，使用  IDENTITY (1, 1) 
"id" INT PRIMARY KEY IDENTITY (1, 1) COMMENT 'id',
```
   2. \`\` 和 “” 符号问题，在DM数据库中不支持\`\`，“”在达梦数据库中能够保证不会转换成大写，因为DM数据库默认会把字段转换成大写。
   3. longtext不支持，需要转换成DM中的CLOD，但是使用CLOD后在测试中查询CLOD字段会报错，提示`Data type mismatch`。    
```java
// 报错代码，排查之后将value 字段改为varchar(2048)，测试正常
Param p = new LambdaQueryChainWrapper<>(baseMappingMapper)
             .eq(Param::getValue, 1)
             .one();
``` 
4. 更新时间问题，DM不支持根据数据更新时触发更新时间字段更新，有两种方案处理：

- 设置触发器，数据更新时触发更新时间更新。

- Mybatis-plus 字段设置使用`@TableField(fill = FieldFill.INSERT_UPDATE)` 和 `@TableField(fill = FieldFill.INSERT)`实现。
5. double不支持，可以考虑转换成Number类型

## 项目数据库配置
1. SpringBoot 配置
 - 配置文件
```yml
# 这里使用Druid不是因为迁移DM才使用的
spring:
  datasource:
    url: jdbc:dm://ip:port?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=utf-8
    username: 用户名
    password: 密码
    platform: DM
    type: com.alibaba.druid.pool.DruidDataSource
    driver-class-name: dm.jdbc.driver.DmDriver
``` 
- pom 依赖
``` xml
<dependency>
   <groupId>com.dameng</groupId>
   <artifactId>DmJdbcDriver18</artifactId>
   <version>8.1.1.193</version>
</dependency>
```      
2. MyBatis-plus 配置
 将DbType设置成DbType.DM，如果DbType没有DM枚举，需要升级Mybatis-plus版本
```java
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();

        // 添加分页插件
        PaginationInnerInterceptor pageInterceptor = new PaginationInnerInterceptor();
        // 设置请求的页面大于最大页后操作，true调回到首页，false继续请求。默认false
        pageInterceptor.setOverflow(false);
        // 单页分页条数限制，默认无限制
        pageInterceptor.setMaxLimit(500L);
        // 设置数据库类型
        pageInterceptor.setDbType(DbType.DM);

        interceptor.addInnerInterceptor(pageInterceptor);
        return interceptor;
    }
``` 
## 测试过程中发现的问题

1. Fail to cast string 报错

```sql
# 报错SQL
# age 是 int 类型，但是传入不能转成int类型的字符串会报错，提示Fail to cast string
select * from tb where age = "十八"；
``` 
 2. 自增列插入报错
```sql
# 打开自增列插入
SET IDENTITY_INSERT ON

# 插入sql

# 关闭自增列插入
SET IDENTITY_INSERT OFF
```