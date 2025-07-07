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