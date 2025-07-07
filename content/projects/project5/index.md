---
title: "MIT 6.S081"
date: 2021-07-01
draft: false
project_tags: ["Operating System"]
status: "growing"
summary: " "
weight: 1
---

## Lab1: Xv6 and Unix utilities
### Boot xv6
按照官网给的lab tools page配置一下环境
**Debian or Ubuntu**
```shell
sudo apt-get install git build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu 
```
检验安装是否成功
```shell
$ qemu-system-riscv64 --version
QEMU emulator version 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.7)
Copyright (c) 2003-2023 Fabrice Bellard and the QEMU Project developers
```
```shell
$ riscv64-linux-gnu-gcc --version
riscv64-linux-gnu-gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```
将项目下载下来
```shell
git clone git://g.csail.mit.edu/xv6-labs-2024
git clone --depth=1 git://g.csail.mit.edu/xv6-labs-2024 #外网速度比较慢，开启 Git 的断点续传
```

```shell
$ cd xv6-labs-2024
$ make qemu
... # 编译工具和选项
qemu-system-riscv64 -machine virt -bios none -kernel kernel/kernel -m 128M -smp 3 -nographic -global virtio-mmio.force-legacy=false -drive file=fs.img,if=none,format=raw,id=x0 -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0

xv6 kernel is booting

hart 2 starting
hart 1 starting
init: starting sh

$ ls
.              1 1 1024
..             1 1 1024
README         2 2 2403
xargstest.sh   2 3 93
cat            2 4 34280
echo           2 5 33208
forktest       2 6 16200
grep           2 7 37544
init           2 8 33672
kill           2 9 33120
ln             2 10 32944
ls             2 11 36312
mkdir          2 12 33184
rm             2 13 33168
sh             2 14 54744
stressfs       2 15 34064
usertests      2 16 179368
grind          2 17 49416
wc             2 18 35240
zombie         2 19 32544
console        3 20 0
```

#### vscode 添加clangd LSP
项目根目录运行
```shell
$ bear -- make
```
自动记录 make 的所有编译参数，生成 compile_commands.json，clangd 会自动识别

### sleep 
参考user/中的其他一些程序(例如 user/echo.c 、 user/grep.c 和 user/rm.c)了解命令行参数如何传递给程序。

命令行参数从```main(int argc, char *argv[]) ```传入

argc：Argument Count，参数个数（包含程序名本身）。

argv：Argument Vector，参数字符串数组，每个元素是一个 char*

**注意**：如果用户忘记传递参数，sleep 应该打印一条错误消息。

命令行参数以字符串形式传递；可以使用atoi将其转换为整数(在user/ulib.c实现)。

使用系统调用 sleep，查看xv6文档，找到sleep以及需要使用的write：

|System call|Description|
|----------------------------------|----------------------------------|
|int sleep(int n)|Pause for n clock ticks.|
|int write(int fd, char *buf, int n)|Write n bytes from buf to file descriptor fd; returns n.|

根据以上内容就可以完成代码
```C
//sleep.c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main(int argc, char* argv[])
{
    if (argc != 2) {
        write(1, "Usage: sleep <ticks>\n", 22);
        exit(1);
    }

    for (char* p = argv[1]; *p; p++) {
        if (*p < '0' || *p > '9') {
            write(1, "sleep: invalid time interval '", 30);
            write(1, argv[1], strlen(argv[1]));
            write(1, "'\n", 2);
            exit(1);
        }
    }

    sleep(atoi(argv[1]));
    exit(0);
}
```
之后在Makefile里找到第180行添加
```shell
180 UPROGS=\
181     $U/_cat\
182     $U/_echo\
183     $U/_forktest\
184     $U/_grep\
185     $U/_init\
186     $U/_kill\
187     $U/_ln\
188     $U/_ls\
189     $U/_mkdir\
190     $U/_rm\
191     $U/_sh\ 
192     $U/_sleep\
193     $U/_stressfs\
194     $U/_usertests\
195     $U/_grind\
196     $U/_wc\ 
197     $U/_zombie\
```
编译测试
```shell
$ ./grade-lab-util sleep
make: 'kernel/kernel' is up to date.
== Test sleep, no arguments == sleep, no arguments: OK (1.1s) 
== Test sleep, returns == sleep, returns: OK (0.7s) 
== Test sleep, makes syscall == sleep, makes syscall: OK (1.0s)
```
