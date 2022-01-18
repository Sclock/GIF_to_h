## 简介

这是一个搭配最新[SD$^3$](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay) 固件里 Animate 方法所用的动图头文件生成方法库，可以简单的使用 GIF 生成 Animate 方法可用的头文件，快速的更改 SD$^3$右下角的动态图像。

## 需要使用的库

- Python3.7+(开发环境为 Python3.8.8)
- pillow
  ```bash
  pip install pillow
  ```

### 使用方法

- ~~0.给本库点 Star~~
- 1.下载本库 or 复制 `init.py` 里的所有内容至本地某 .py 文件里。
- 2.把需要转换的 GIF 放在 py 文件同一目录内。
- 3.更改倒数第二行的 `"hutao.gif"` 为你的 GIF 名称，需带后缀。
- 4.运行。
- 5.复制生成的.h 文件到 Animate 库的 [\img](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/tree/main/src/Animate/img) 目录内，并更改 [Animate.cpp](<(https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/blob/main/src/Animate/Animate.cpp)>) 内的 `imgAnim` 函数。
- 6.将 [config.h](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/blob/main/src/config.h) 文件里的 `Animate_Choice` 后面的数更改为你的动画分支。

### imgAnim 函数的修改方法

- 什么！你说你没有 Animate 库！即刻更新[SD$^3$](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay)！抛弃 - - Arduino,加入光荣的进化吧！

- 如果你的版本里有 [Animate.cpp](<(https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/blob/main/src/Animate/Animate.cpp)>) ,但和链接里的不一样，可以复制全部内容到你的 `Animate.cpp` 里粗暴更新。

如果你有`imgAnim`函数且形如：

```c++
void imgAnim(const uint8_t **Animate_value, uint32_t *Animate_size)
{
#if Animate_Choice != 0
    Animate_key++;
#endif

//太空人起飞
#if Animate_Choice == 1
    *Animate_value = astronaut[Animate_key];
    *Animate_size = astronaut[Animate_key];
    if (Animate_key >= 9)
        Animate_key = -1;
//胡桃摇
#elif Animate_Choice == 2
    *Animate_value = hutao[Animate_key];
    *Animate_size = hutao_size[Animate_key];
    if (Animate_key >= 31)
        Animate_key = -1;
#endif
}
```

那你可以在下面加入你新生成的 .h 文件里最下面两行的数组名。

假设你的 GIF 名字为 `newGif.gif` 那你的两个数组名应该是 `newGif` 和 `newGif_size` 。
在胡桃摇下方， `#endif` 上方，添加新的 `#elif` 分支。

```c++
#elif Animate_Choice == 3
    *Animate_value = newGif[Animate_key];
    *Animate_size = newGif_size[Animate_key];
    if (Animate_key >= 10)
        Animate_key = -1;
```

这里第一个数组名称对应你的第一个数组，第二个对应第二个，不要修改括号里的值。
而 if 里的数字是你 .h 文件最下面 定义的时候 `括号里的数字-1`
形如：

```c++
const uint8_t *newGif[15] PROGMEM {}
```

那就写

```c++
    if (Animate_key >= 14)
        Animate_key = -1;
```

修改后形如：

```c++
void imgAnim(const uint8_t **Animate_value, uint32_t *Animate_size)
{
#if Animate_Choice != 0
    Animate_key++;
#endif

//太空人起飞
#if Animate_Choice == 1
    *Animate_value = astronaut[Animate_key];
    *Animate_size = astronaut[Animate_key];
    if (Animate_key >= 9)
        Animate_key = -1;
//胡桃摇
#elif Animate_Choice == 2
    *Animate_value = hutao[Animate_key];
    *Animate_size = hutao_size[Animate_key];
    if (Animate_key >= 31)
        Animate_key = -1;

// 添加区域开始
#elif Animate_Choice == 3
    *Animate_value = newGif[Animate_key];
    *Animate_size = newGif_size[Animate_key];
    if (Animate_key >= 14) // .h 文件最下方定义括号里的数字-1
        Animate_key = -1;
// 添加区域结束

#endif
}
```

之后，在上方的 include 区域引入你的动画头文件，形如：

```c++
#if Animate_Choice == 1
#include "img/astronaut.h"
#elif Animate_Choice == 2
#include "img/hutao.h"
// 添加区域开始
#elif Animate_Choice == 3
#include "img/newGif.h"
// 添加区域结束
#endif
```

到这里，关于 [Animate.cpp](<(https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/blob/main/src/Animate/Animate.cpp)>) 文件的修改工作就结束了。修改后完整的 [Animate.cpp](<(https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/blob/main/src/Animate/Animate.cpp)>) 文件形如：

```c++
#include "Animate.h"
#include "config.h"

#if Animate_Choice != 0
int Animate_key = -1; //初始化图标显示帧数
#endif

#if Animate_Choice == 1
#include "img/astronaut.h"
#elif Animate_Choice == 2
#include "img/hutao.h"

// 添加区域开始
#elif Animate_Choice == 3
#include "img/newGif.h"
// 添加区域结束

#endif

void imgAnim(const uint8_t **Animate_value, uint32_t *Animate_size)
{
#if Animate_Choice != 0
    Animate_key++;
#endif

//太空人起飞
#if Animate_Choice == 1
    *Animate_value = astronaut[Animate_key];
    *Animate_size = astronaut[Animate_key];
    if (Animate_key >= 9)
        Animate_key = -1;
//胡桃摇
#elif Animate_Choice == 2
    *Animate_value = hutao[Animate_key];
    *Animate_size = hutao_size[Animate_key];
    if (Animate_key >= 31)
        Animate_key = -1;

// 添加区域开始
#elif Animate_Choice == 3
    *Animate_value = newGif[Animate_key];
    *Animate_size = newGif_size[Animate_key];
    if (Animate_key >= 14) // .h 文件最下方定义括号里的数字-1
        Animate_key = -1;
// 添加区域结束

#endif
}

```

只需要到 [config.h](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay/blob/main/src/config.h) 文件里 `Animate_Choice` 后面的数更改为你的动画分支，形如：

```c++
#define Animate_Choice 3
```

并重新烧录，即刻看到你修改的结果了！

## 进阶

### init.py 里各个参数的意义

首先来看 init 函数的定义：

```python
def init(file_name_all, key=1, image_size=(70, 70)):
```

由此我们可知 init 函数需要三个参数(file_name_all, key, image_size)

#### 第一个参数

`file_name_all` ,是 GIF 文件的名字。传入名字后会在 init.py 运行目录里查找这个文件并打开。

#### 第二个参数

`key` 关键帧参数。众所周知，电影的帧率是 24 帧，也就是一秒刷新 24 张图像。可 [SD$^3$](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay) 由于性能的限制在一秒内并不能稳定的刷新 24 张（大约为稳定刷新 12 张，为防止占用性能过多，故默认一秒刷新 10 张），由于 flash 大小的限制，并不能传入超过 70 张 70\*70 的 jpg 文件。所以如果传入的 GIF 帧率过高，在保持动画速度不变的情况下就需要抽帧。

假设你有一个 每秒 60 帧的 GIF，在你刷新率为 60Hz 的电脑上，播放速度为 1x。

可如果你原原本本的传入[SD$^3$](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay)这个 GIF，由于[SD$^3$](https://github.com/SmallDesktopDisplay-team/SmallDesktopDisplay)的刷新率为 10Hz，在第一秒只能显示出这张 GIF 前 10 帧的图像，而完整的显示则需要六秒，播放速度为 1/6 x。

所以，如果你的 GIF 帧率高于 10，则需要按照一定的比率抽帧以保证播放速度不变。

具体的公式为

$ key = \frac{GIF 帧率}{10} $

如果没看懂，那就用默认的吧

### 第三个参数

`image_size` 输出文件尺寸参数，默认的宇航员，胡桃都是正方形的 GIF，如果你导入的也是正方形的 GIF,可以忽视掉此参数。如果不是正方形的，暂时建议你换个 GIF，当然如果你有足够的耐心，可以尝试调整此参数以适配你的 GIF。
