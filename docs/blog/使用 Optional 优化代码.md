# Optional 优化之前
```java 

// 查询用户角色关联表
SysUserRoleRel userRoleRel = userRoleRelMapper.selectOne(new LambdaQueryWrapper<SysUserRoleRel>()
                    .eq(SysUserRoleRel::getUserId, userInfo.getId()));
// 获取用户角色名称
if (Objects.nonNull(userRoleRel)){
      // 查询角色信息
      SysRoleInfo roleInfo = roleInfoMapper.selectById(userRoleRel.getRoleId());
      if (Objects.nonNull(roleInfo)) {
          userResp.setRoleName(roleInfo.getRoleName());
          userResp.setRoleId(roleInfo.getId());
      }
}
```

# Optional 优化之后 :star_struck: 
```java
// 查询用户角色关联表
SysUserRoleRel userRoleRel = userRoleRelMapper.selectOne(new LambdaQueryWrapper<SysUserRoleRel>()
                    .eq(SysUserRoleRel::getUserId, userInfo.getId()));
// 获取用户角色名称
Optional.ofNullable(userRoleRel)
                    .map(SysUserRoleRel::getRoleId)
                    .map(roleId -> roleInfoMapper.selectById(roleId))
                    .ifPresent(sysRoleInfo -> {
                        userResp.setRoleName(sysRoleInfo.getRoleName());
                        userResp.setRoleId(sysRoleInfo.getId());
                    });

```

> [!NOTE]
> `Optional#map` 从 `SysUserRoleRel::getRoleId` -> `roleInfoMapper.selectById(roleId)` 最后获取到了`sysRoleInfo`，中间如果有空值就不会执行后面的方法。

