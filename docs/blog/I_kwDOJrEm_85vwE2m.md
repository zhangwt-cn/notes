Mac os 环境下 安装好`rust`环境，使用`vscode`时`rust-analyzer`报错
```shell
Failed to spawn one or more proc-macro servers.

- cannot find proc-macro-srv, the workspace `/Users/xxxx/vscode/rust/guessing_game` is missing a sysroot

Failed to find sysroot for Cargo.toml file /Users/xxxx/vscode/rust/guessing_game/Cargo.toml. Is rust-src installed? can't load standard library from sysroot

/Users/xxxx/.rustup/toolchains/stable-x86_64-apple-darwin

(discovered via `rustc --print sysroot`)

try installing the Rust source the same way you installed rustc
``` 
解决方案
```shell
# 安装 rust-src
sudo rustup component add rust-src
``` 
在 `vscode` 中重启一下`rust-analyzer`插件之后就能解决。