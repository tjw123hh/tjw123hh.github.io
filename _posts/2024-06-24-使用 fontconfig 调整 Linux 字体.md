---
title: 使用 fontconfig 调整 Linux 字体
tags:
    - Linux
    - 字体
---

## 前言

之前一些 emoji 总是显示成方框，输入法（fcitx5）中的字体甚至也模糊了。而之前一直使用 KDE 的“字体”调整字体，但这样只能设定一个字体而不能设定替代字体（像是之前调成思源黑体后 emoji 部分就全部不能显示）。所以就去网上查到以下几篇关于 fontconfig 的文章。然后写篇简明点的文章（顺便巩固学习成果）。

## Fontconfig 是什么

[官网介绍](https://www.freedesktop.org/wiki/Software/fontconfig/)

Linux 上**几乎所有程序**获取字体都需要经过 fontconfig，因为它有发现、查找字体的功能。而 fontconfig 是高度可定制的，意味着我们可以通过修改 fontconfig 的配置来控制**几乎所有程序**的字体显示（比直接使用 KDE/GNOME 的字体程序还广泛）。

程序通过 fontconfig 查找到字体信息后，调用渲染器（如 FreeType）渲染字体。

它不仅可以指定替代字体，还能为每个语言、每个程序单独设定字体，从而避免合成字体、在每个程序设定字体（通常只能设定一个）的麻烦。

但 fontconfig 的支持视程序而定，大部分 Linux 程序对 fontconfig 有较好的支持，但 Chrome（以及其他使用 Chromium 的程序）完全不传语言给 fontconfig 且只使用结果中的首个字体。

## 前置知识（关于字体）

此部分内容可以选择性阅读（了解的部分可以跳过）。

### 字体的字族

字族（family）就是字体的名称，一个字体可以有多个字族（但一般程序选择字体时只显示一个）。

一个字体文件，可以提供多个字族。比如在 Arch Linux 安装 `wqy-microhei` 包后，增加了 `wqy-microhei.ttc` 这个字体文件，分别提供“WenQuanYi Micro Hei”“文泉驛微米黑”“文泉驿微米黑”三个字体族名。我们可以运行 fontconfig 提供的命令行工具 `fc-list` 去查看系统上已安装的字体已经它们对应的字体族名。

字族称为“族”是因为一个字族可以有多个字型，如 `Noto Sans CJK SC Regular` 等，这不应在指定字族时使用，但大多数程序支持将此作为字族（大多数浏览器支持）。

### 印刷字体的分类

- 衬线体（serif）与无衬线体（sans-serif）：衬线是印刷文字的装饰部分，也称为“字脚”。衬线体就是有衬线的字体，无衬线体就是没有衬线的字体。中文的衬线体一般就只指宋体（港台称明体）、非衬线体就指黑体或由黑体衍生的幼圆等字体。

- 等宽字体（monospace）：就是写代码时经常用到的英文字符（半角字符）宽度一致、中文字符（全角字符）宽度是英文字符（半角字符）两倍的字体。因为一些程序（如终端）只能使用这种字体，以及显示代码的需求，所以在此处独立出来。

示例：
> <span style="font-family: serif;">这是衬线体。This is serif.</span><br />
> <span style="font-family: sans-serif;">这是无衬线体。This is sans-serif.</span><br />
> <span style="font-family: monospace;">这是等宽字体。This is monospace.</span>

### 通用字族

大部分时候，由于程序并不知道用户电脑里装了什么字体，指定具体的字体难以实现。人们发明了通用字族，让程序能够通过字体的类型制定使用的字体，而无需关注各种语言所需字体等细节。常用的包括 `system-ui`、`serif`、`sans-serif`（`sans`、`sans serif`）、`monospace`（`mono`），其中 `system-ui` 指的是系统界面字体，可以指定为任意类型，其它的三个与[印刷字体的分类](#印刷字体的分类)中的三种类型相对应。极少数程序支持指定手写体（`cursive`）。

通用字族可以在任何调用字族的地方使用，例如上面和下面的示例都是用内联样式 `font-family` 中使用通用字族名得到的。但如果你的 fontconfig 或浏览器设置不正确，就无法正确显示。

示例：

> <span style="font-family: system-ui;">这是系统界面字体。This is system-ui.</span><br />
> <span style="font-family: serif;">这是衬线体。This is serif.</span><br />
> <span style="font-family: sans-serif;">这是无衬线体。This is sans-serif.</span><br />
> <span style="font-family: monospace;">这是等宽字体。This is monospace.</span>

### 合成字体

一些系统（Windows、未“ROOT”的安卓等）没有类似 fontconfig 的字体管理工具，很多时候只能使用一种字体显示电脑上全部的字符。但一般中文字体西文显示不好（特别是连字），甚至等宽；一些西文字体不能显示中文。加上更多其他文字的字体独立开来，这些系统的用户只能使用合成字体来解决这些问题。在 Linux 下，没有必要使用合成字体，它们通常更新慢或者需要自己合成。只需要合理地配置 fontconfig 就能实现比合成字体更加灵活的字体设置（毕竟一个 TTF 字体只能包含 65535 个字）。

## 常见字体配置问题

### 异体字不正确显示

每个地区，汉字的规范写法都不一样，而 Unicode 将许多同源的字形整合到一个编码上，而一些简体字在其他国家当作部件处理。如果只使用一种字体，无法正确显示不同语言的内容。因此，中文字体有大陆（SC/CN/GB）、香港（HK）、台湾（TW/*TC\**）、日本（JP/JA）、韩国（KR/KO）和朝鲜（KP）等地区变种，但一些变体鲜有字体支持。它们对应的语言代号分别为 `zh-CN`、`zh-HK`、`zh-TW`、`ja`、`ko`（`ko-KR`）、`ko-KP`。各字型的差异可以参照《[了解各个地区的汉字字形差异！](https://www.bilibili.com/video/BV1kK421t7jc)》（⸺[派对大魔王](https://space.bilibili.com/316576469)）。

*\* TC 全称 Traditional Chinese，即繁体中文，与简体中文（SC）对应。不一定符合台湾教育部规定字形（即“台教标”）。但大多数此变体针对台湾制作。*

但许多软件没有针对各个语言的独立字体设置，我们需要正确根据语言选择不同字体变体显示文字（见[#根据语言环境选择不同字体](#根据语言环境选择不同字体)）。

示例（仅在字体正确配置时可用，使用简体字）：

> 遍角次亮采之关复门 默认<br />
> <span lang="zh-CN">遍角次亮采之关复门 中文（中国） lang=zh-CN</span><br />
> <span lang="zh-TW">遍角次亮采之关复门 中文（台湾） lang=zh-TW</span><br />
> <span lang="zh-HK">遍角次亮采之关复门 中文（香港） lang=zh-HK</span><br />
> <span lang="ja">遍角次亮采之关复门 日文 lang=ja</span><br />
> <span lang="ko">遍角次亮采之关复门 韩文 lang=ko</span><br />
> <span lang="ko-KP">遍角次亮采之关复门 朝鲜文 lang=ko-KP</span>

### 引号的全半角问题

用输入法打出来的引号是“`“”‘’`”，关闭输入法，打出来的是“`""''`”。有许多人以为这是中英文引号的区别，但其实外文中也主要用“`“”‘’`”这种弯引号，“`""''`”只用于代码与模拟打字机时，被称为“傻瓜引号”。在大部分排版引擎（例如 Microsoft Word 或 LibreOffice Writer）中会被自动替换成弯引号（Jekyll 也是⸺所以我只能用代码块展示）。“`’`”更是缩写中常用的撇号。

然而，Unicode 没有将中文引号和英文引号与撇号区分开来。在大部分中文字体中，引号是全角的（占两个英文字符位置）；但在英文字体中，引号是半角的（占一个英文字符位置）。而全角引号在用作撇号时导致一个极大的空格，严重影响美观。

因此，我们也需要通过识别语言的方式切换字体来改变引号的全半角（见[#根据语言环境选择不同字体](#根据语言环境选择不同字体)）。

示例（仅在字体正确配置时可用）：
> ‘’“” 默认<br />
> <span lang="zh-CN">‘’“” 中文（中国） lang=zh-CN</span><br />
> <span lang="en">‘’“” 英文 lang=en</span>

## 使用

### Fontconfig 的运作方式

Fontconfig 通过**按顺序**利用各种配置文件对传入的 `pattern`（一个或多个字体，包括字体的大小、粗细等样式）进行修改，并最后将系统中存在的字体从得到的 `pattern` 中找出来最终以一个列表的形式传递出去。列表由最先尝试使用的字体开始，程序应在前面字体不能使用时调用后面的字体渲染。

Fontconfig 读取配置文件，这些配置文件识别传入的 `pattern` 后加上自己的修改（例如，在前面插入 `Noto Sans CJK SC` 字体），最终 fontconfig 挑出能够在系统里找到的字体组成列表传出（此时传入的 `sans-serif` 等通用字族名被剔除）。

**注**（也是 fontconfig **按顺序**读取配置文件的体现）：`sans`、`mono` 可以在最初传入的 `pattern` 中使用，但在 fontconfig 修改开始时便会被首先加载的配置文件分别替换为 `sans-serif` 和 `monospace`。由于 fontconfig 按顺序执行各个配置文件，当扫描到我们的配置文件时，`sans`（`sans serif`）和 `mono` 不会被我们检测到（因为它们已经不存在了）。因此，在我们自己的配置中，不能通过识别 `sans` 和 `mono` 来修改 `pattern`。

#### 强绑定与弱绑定

配置文件插入字体时，有强弱绑定之分，一般系统默认的配置使用弱绑定，用户的配置使用强绑定。在传出最终 `pattern` 之前，fontconfig 会将强绑定移到前面，弱绑定移到后面弱绑定字体的顺序还会被 fontconfig 调整，这样用户使用强绑定就不必担心自己配置文件的加载顺序了。

在我们添加自己的配置前，系统中已经有了许多默认配置（`/etc/fonts/conf.d/` 目录下）和可选配置［`/usr/share/fontconfig/conf.avail/`（旧为 `/etc/fonts/conf.avail/`）目录下］，用来自动选择字体来显示出更多的文字。

### 调试

#### `FC_DEBUG`
通过向**任何**使用 fontconfig 的程序传入环境变量 `FC_DEBUG` 来调试，设定为 `4` 显示 `pattern` 的替换流程，设置为 `1024` 显示读取的配置文件。其它值详见[官方用户文档](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)。

##### 示例
输入（可根据元素多少调整 `-A` 后面的行数）：
```bash
FC_DEBUG=4 fc-match -a sans:lang=zh | grep 'donePattern' -A 10 --max-count=1
```
输出：
```
FcConfigSubstitute donePattern has 7 elts (size 16)
        family: "Noto Sans CJK SC"(s) "Noto Sans"(s) "Noto Sans CJK SC"(s) "Noto Color Emoji"(s) "Symbols Nerd Font"(s) "Noto Sans"(w) "DejaVu Sans"(w) "Verdana"(w) "Arial"(w) "Albany AMT"(w) "Luxi Sans"(w) "Nimbus Sans L"(w) "Nimbus Sans"(w) "Nimbus Sans"(w) "Helvetica"(w) "Nimbus Sans"(w) "Nimbus Sans L"(w) "Lucida Sans Unicode"(w) "BPG Glaho International"(w) "Tahoma"(w) "Nachlieli"(w) "Lucida Sans Unicode"(w) "Yudit Unicode"(w) "Kerkis"(w) "ArmNet Helvetica"(w) "Artsounk"(w) "BPG UTF8 M"(w) "Waree"(w) "Loma"(w) "Garuda"(w) "Umpush"(w) "Saysettha Unicode"(w) "JG Lao Old Arial"(w) "GF Zemen Unicode"(w) "Pigiarniq"(w) "B Davat"(w) "B Compset"(w) "Kacst-Qr"(w) "Urdu Nastaliq Unicode"(w) "Raghindi"(w) "Mukti Narrow"(w) "malayalam"(w) "Sampige"(w) "padmaa"(w) "Hapax Berbère"(w) "MS Gothic"(w) "UmePlus P Gothic"(w) "Microsoft YaHei"(w) "Microsoft JhengHei"(w) "WenQuanYi Zen Hei"(w) "WenQuanYi Bitmap Song"(w) "AR PL ShanHeiSun Uni"(w) "AR PL New Sung"(w) "Hiragino Sans"(w) "PingFang SC"(w) "PingFang TC"(w) "PingFang HK"(w) "Hiragino Sans CNS"(w) "Hiragino Sans GB"(w) "MgOpen Modata"(w) "VL Gothic"(w) "IPAMonaGothic"(w) "IPAGothic"(w) "Sazanami Gothic"(w) "Kochi Gothic"(w) "AR PL KaitiM GB"(w) "AR PL KaitiM Big5"(w) "AR PL ShanHeiSun Uni"(w) "AR PL SungtiL GB"(w) "AR PL Mingti2L Big5"(w) "ＭＳ ゴシック"(w) "ZYSong18030"(w) "TSCu_Paranar"(w) "NanumGothic"(w) "UnDotum"(w) "Baekmuk Dotum"(w) "Baekmuk Gulim"(w) "Apple SD Gothic Neo"(w) "KacstQura"(w) "Lohit Bengali"(w) "Lohit Gujarati"(w) "Lohit Hindi"(w) "Lohit Marathi"(w) "Lohit Maithili"(w) "Lohit Kashmiri"(w) "Lohit Konkani"(w) "Lohit Nepali"(w) "Lohit Sindhi"(w) "Lohit Punjabi"(w) "Lohit Tamil"(w) "Meera"(w) "Lohit Malayalam"(w) "Lohit Kannada"(w) "Lohit Telugu"(w) "Lohit Oriya"(w) "LKLUG"(w) "Noto Sans"(w) "FreeSans"(w) "Arial Unicode MS"(w) "Arial Unicode"(w) "Code2000"(w) "Code2001"(w) "URW Gothic"(w) "Nimbus Sans"(w) "Nimbus Sans Narrow"(w) "sans-serif"(s) "Roya"(w) "Koodak"(w) "Terafik"(w) "Helvetica"(w) "sans-serif"(w) "ITC Avant Garde Gothic"(w) "URW Gothic"(w) "sans-serif"(w) "sans-serif"(w) "Helvetica"(w) "Helvetica Narrow"(w) "Nimbus Sans Narrow"(w)
        antialias: True(w)
        hintstyle: 1(i)(w)
        rgba: 1(i)(w)
        lang: zh(s)
        lcdfilter: 1(i)(w)
        prgname: "fc-match"(s)
...
```

此处可以看到第一个 `donePattern` 有 7 个元素（elt），这个 `pattern` 包括所有待选字体（后面的 `donePattern` 是单个字体的设置），每个元素都是一个属性（property），这包括字体信息、系统信息和程序信息，而在执行中的 `pattern` 也有许多元素，这些元素在配置文件中都可以检测得到，使得 fontconfig 的可自定义性非常强。属性的描述元素值后面的 `(i)`、`(f)` 分别指整型与浮点型，`(s)` 与 `(w)` 分别指强绑定与弱绑定。一些通用的元素在[官方用户文档](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)有详细描述。

#### `fc-match [-a] [pattern]`
传入 `pattern` 经过一系列操作后输出最终结果。使用 `-a` 不对最终列表进行任何修剪。（即使不传入 `pattern` 也会根据语言环境进行输出。）使用 `:<元素名称>=<元素值>` 指定 `pattern` 中特定元素的值，表示字体样式的可以直接省略前面的 `<元素名称>‌=`<!--为了避免`>=`连字，两者之间插入了零宽不连字符（HTML 中使用`&zwnj;`即可，但这里属于代码部分，只能直接粘贴）-->，如 `:bold`、`italic` 等。还可以用 `-XX` 指定字体大小，如 `Times-12` 指 12 点（或作“磅”）大小的 Times 字体。

##### 示例
输入：
```bash
fc-match -a sans:lang=en:weight=bold
```
输出：
```
NotoSans-Bold.ttf: "Noto Sans" "Bold"
NotoSans-SemiCondensedBold.ttf: "Noto Sans" "SemiCondensed Bold"
NotoSans-CondensedBold.ttf: "Noto Sans" "Condensed Bold"
NotoSans-ExtraCondensedBold.ttf: "Noto Sans" "ExtraCondensed Bold"
...
SourceCodeVF-Italic.otf: "SourceCodeVF" "<unknown style>"
```

输入：
```bash
FC_DEBUG=1024 fc-match
```
输出：
```
FC_DEBUG=1024
        Loading config file from /etc/fonts/fonts.conf
        Scanning config dir /etc/fonts/conf.d
        Loading config file from /etc/fonts/conf.d/00kde.conf
        ...
        Scanning config file from /usr/share/fontconfig/conf.avail/90-synthetic.conf
        Scanning config file from /usr/share/fontconfig/conf.avail/90-synthetic.conf done
NotoSansCJK-Regular.ttc: "Noto Sans CJK SC" "Regular"
```

#### `fc-list [[:<元素名称>=<元素值>]]`

前文已经提到，该命令可以用来查看系统上已安装的字体已经它们对应的字体族名。而它同样也可以过滤具有特定语言、样式的字体。

##### 示例

输入：
```bash
fc-list :medium:lang=zh-CN
```

输出：
```
/usr/share/fonts/noto-cjk/NotoSerifCJK-Medium.ttc: Noto Serif CJK TC,Noto Serif CJK TC Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSerifCJK-Medium.ttc: Noto Serif CJK HK,Noto Serif CJK HK Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSerifCJK-Medium.ttc: Noto Serif CJK SC,Noto Serif CJK SC Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSansCJK-Medium.ttc: Noto Sans CJK KR,Noto Sans CJK KR Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSerifCJK-Medium.ttc: Noto Serif CJK JP,Noto Serif CJK JP Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSerifCJK-Medium.ttc: Noto Serif CJK KR,Noto Serif CJK KR Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSansCJK-Medium.ttc: Noto Sans CJK HK,Noto Sans CJK HK Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSansCJK-Medium.ttc: Noto Sans CJK SC,Noto Sans CJK SC Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSansCJK-Medium.ttc: Noto Sans CJK JP,Noto Sans CJK JP Medium:style=Medium,Regular
/usr/share/fonts/noto-cjk/NotoSansCJK-Medium.ttc: Noto Sans CJK TC,Noto Sans CJK TC Medium:style=Medium,Regular
```

### 添加自己的配置

自己的字体配置最好添加在自己的用户目录下，配置文件在 `~/.config/fontconfig/fonts.conf`，也可以在 `~/.config/fontconfig/conf.d/` 目录下自行创建文件（文件名应为 `XX-Something.conf`，`XX` 为数字，按文件名字典序读取，故数字小于 10 时需加上前导 0 才能按数字顺序读取）。

#### 配置文件的语法

多个配置文件是按顺序执行的，每个配置文件内的语句也是按顺序执行的。每个配置文件都是 XML 格式。

示例：
```xml
<?xml version='1.0'?>
<!DOCTYPE fontconfig SYSTEM 'urn:fontconfig:fonts.dtd'>
<fontconfig>
    <!-- 主体部分 -->
</fontconfig>
```

主体部分由如下几个部分依次拼接而成：

- 目录设置（`<dir>`、`<cachedir>`、`<include>`）
- 杂项设置（`<config>`）
- 扫描阶段（`<match target="scan">`）
- 匹配阶段（`<alias>`、`<match target="pattern">`）
- 渲染阶段（`<match target="font">`）

在本文章中，只涉及匹配阶段与渲染阶段的语法（不完整），其它部分及完整内容请见[官方用户文档](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)，但这样已经可以满足调整字体的大部分需求。

##### 匹配阶段

`<alias>` 只能用于弱绑定，且用于弱绑定时和 `<match target="pattern">` 只是写法不同，实际作用相同，故此处只介绍 `<match target="pattern">` 的写法。

示例：
```xml
<match target="pattern">
  <test name="family">
    <string>sans-serif</string>
  </test>
  <edit name="family" mode="prepend" binding="strong">
    <string>Noto Sans CJK SC</string>
    <string>Noto Sans</string>
    <string>Noto Color Emoji</string>
  </edit>
</match>
```

`<match target="pattern">` 的内容由 `<test>` 和 `<edit>` 两部分组成，可以有多个。[前文](#fc_debug)讲到使用 `FC_DEBUG` 环境变量可以查看 `pattern` 中的所有属性。这里主要涉及的属性有：
- `family`*(string)*：字族。
- `lang`*(string)*：需要的语言，遵循 IETF 的 BCP 47 标准，即以`en`或`zh-CN`之类的语言代码表示。
- `prgname`*(string)*：调用程序的名称，可以通过在环境变量`FC_DEBUG`为`4`的情况下运行程序查看。

你也可以在[官方用户文档](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)查看其他属性的描述并使用它们。

语法：

- `<test>`：检测需要的属性。只有所有 `<test>` 都满足，才会进行修改。即多个 `<test>` 之间为“与”的关系。要实现“或”的关系，需要多个 `<match>` 元素。如果不需要检测，也可以不设置 `<test>`。
  - 元素属性
    - `name`：需要检测的属性。
    - `qual`：检测的品质。
      - `"any"`（默认）：检测到任意一项。
      - `"all"`：检测到全部。
      - `"first"`：检测到第一项。
      - `"not-first"`：第一项检测失败而后面的任意项被检测到。
    - `compare`：比较方法。
      - `"eq"`（默认）和 `"not_eq"`：用于任何值，完全匹配与非完全匹配（即等于与不等于）。
      - `"less"`、`"less_eq"`、`"more"` 和 `"more_eq"`：用于数值比较，小于、小于等于、大于和大于等于。
      - `“contains"` 和 `"not_contains"`：用于字符串，包含和不包含。
  - 元素内容：根据属性类型指定类型（使用 `<int>`、`<double>`、`<string>`、`<bool>`、`<charset>` 和 `<langset>`）包裹属性值或使用 `<const>` 包裹常量名。是需要检测（可能修改）的值。
- `<edit>`：修改。
  - 元素属性
    - `name`：需要修改的属性。
    - `mode`：修改模式，默认修改相应 `<test>`（相同 `name` 属性）检测到的值。没有相应检测项或者使用括号中的变种时，执行“**//**”后面的操作。为了获得最高的优先级，用户配置中一般需要使用强引用配合 `prepend`。
      - `"assign"`（`"assign_replace"`）：替换相应 `<test>` 检测到的值 **//** 替换整个列表。
      - `"prepend"`（`"prepend_first"`）和 `"append"`（`"append_last"`）：分别在相应 `<test>` 检测到的值前面、后面插入值 **//** 在列表最前、最后插入值。
      - `"delete"`（`"delete_all"`）：删除相应 `<test>` 检测到的值 **//** 删除整个列表。
    - `binding`：绑定模式。
      - `"strong"` 和 `"weak"`：指定强绑定和弱绑定。
      - `"same"`：与相应 `<test>` 检测到的值的绑定模式相同。
  - 元素内容：根据属性类型指定类型（使用 `<int>`、`<double>`、`<string>`、`<bool>`、`<charset>` 和 `<langset>`）包裹属性值或使用 `<const>` 包裹常量名，用来指定修改后的值。

匹配阶段结束，渲染阶段开始前的 `donePattern` 可以通过 `FC_DEBUG=4 fc-match -a sans:lang=zh | grep 'donePattern' -A 10 --max-count=1` 查看。

##### 渲染阶段

渲染阶段主要操控渲染器渲染字体的方式，可以提高性能、改善观感。

根据 `<match target="font">` 可以看出来此处针对的是字体，也就是说此处的 `pattern` 已经过滤完毕，只剩下那些存于系统中的字体了。可以操控的属性值可以查看最后一个 `donePattern`（上面查看的是第一个）。

同样使用 `<match>` 元素，语法与匹配阶段完全相同，只是操控的属性不同。这个阶段我们主要操控渲染相关的属性：

- `hinting`*(bool)*：启用或禁用字体微调。字体微调指使用数学指令来调整轮廓字体的显示，使其与像素对齐，让字看起来更加清晰，建议设置为 `true`（否则字体就会非常模糊）。
- `autohint`*(bool)*：使用自动微调代替内嵌微调。内嵌微调是指根据字体自带的算法微调；自动微调是指使用渲染器的自动微调功能进行字体微调。由于字体自带的微调通常比自动微调好（如果字体带有），建议设置为 `false`。［可参照 [Lcdfilter test](https://spasche.net/files/lcdfiltering/)（[截图存档 2024-04-28](/assets/4.png){:target="_blank"}）进行对比］
- `hintstyle`*(int)*：微调的程度，可设置为：`hintnone`*&lt;const&gt;* 或 `0`（关闭）、`hintslight`*&lt;const&gt;* 或 `1`（轻度）、`hintmedium`*&lt;const&gt;* 或 `2`（中度）、`hintfull`*&lt;const&gt;* 或 `3`（完全）。过度的字体微调会使字体失去字体特点，但显示得更加清晰。
- `antialias`*(bool)*：抗锯齿。建议设置为 `true`。
- `lcdfilter`*(int)*：LCD filter 用来消除文字的彩色边纹，此属性设定它的风格［可参照 [Lcdfilter test](https://spasche.net/files/lcdfiltering/)（[截图存档 2024-04-28](/assets/4.png){:target="_blank"}）进行对比］，可设置为：
  - `lcdnone`*&lt;const&gt;* 或 `0`：彻底关闭 LCD filter，不推荐，它会导致笔画边缘出现彩色边纹。
  - `lcddefault`*&lt;const&gt;* 或 `1`：最大限度地消除彩色边纹，但是可能会增加笔画的模糊程度。多数场合这是最佳选择。
  - `lcdlight`*&lt;const&gt;* 或 `2`：减轻笔画的模糊程度，但不能最大限度的消除彩色边纹。少数场合也许效果更好。
  - `lcdlegacy`*&lt;const&gt;* 或 `3`：为了与传统的 `"libXft color filter"` 兼容而设置，未来会被删除。
- `rgba`：指定 LCD 子像素的排列顺序，为了次像素渲染。分为：`unknown`*&lt;const&gt;* 或 `0`（未知）、`rgb`*&lt;const&gt;* 或 `1`、`bgr`*&lt;const&gt;* 或 `2`、`vrgb`*&lt;const&gt;* 或 `3`、`vbgr`*&lt;const&gt;* 或 `4`、`none`*&lt;const&gt;* 或 `5`（无子像素）。在 [Subpixel layout - Legom LCD Test](http://www.lagom.nl/lcd-test/subpixel.php) 中有区分。
![各种排列方式](/assets/3.png)
- `embeddedbitmap`*(bool)*：是否启用字体内嵌的点阵字形。视个人需要开关。点阵字形即位图字形，相对于一般的向量字形可能渲染更快，但没有次像素渲染，会丢失字体的许多细节。

这些属性对每个字体都独立，且每个字体只有一个值而不是值的列表，因此不需要考虑排序问题，可以弱绑定也可以强绑定。

#### 设置默认字体

知道了配置文件的语法，学会设置默认字体就非常简单了。

示例（不包括文件头和 `<fontconfig>`）：
```xml
<!-- Default system-ui fonts -->
<match target="pattern">
    <test name="family">
        <string>system-ui</string>
    </test>
    <edit binding="strong" mode="prepend" name="family">
        <string>sans-serif</string>
    </edit>
</match>
<!-- Default sans-serif fonts-->
<match target="pattern">
    <test name="family">
        <string>sans-serif</string>
    </test>
    <edit binding="strong" mode="prepend" name="family">
        <string>Noto Sans CJK SC</string>
        <string>Noto Sans</string>
        <string>Noto Color Emoji</string>
        <string>Symbols Nerd Font</string>
    </edit>
</match>
<!-- Default serif fonts-->
<match target="pattern">
    <test name="family">
        <string>serif</string>
    </test>
    <edit binding="strong" mode="prepend" name="family">
        <string>Noto Serif CJK SC</string>
        <string>Noto Serif</string>
        <string>Noto Color Emoji</string>
        <string>Symbols Nerd Font</string>
    </edit>
</match>
<!-- Default monospace fonts-->
<match target="pattern">
    <test name="family">
        <string>monospace</string>
    </test>
    <edit binding="strong" mode="prepend" name="family">
        <string>JetBrainsMono Nerd Font</string>
        <string>Noto Sans Mono CJK SC</string>
        <string>Noto Color Emoji</string>
        <string>Symbols Nerd Font</string>
    </edit>
</match>
```

**注**：如果要替换掉西文字体，应该把用来替换的放在前，中文字体作为备用字体。

#### 替换原有字体

有些应用或网页的字体无法更改，可以通过替换的方式直接换成自己想要的字体

示例（不包括文件头和 `<fontconfig>`）：
```xml
<match target="pattern">
    <test compare="contains" name="family">
        <string>Source Code</string>
    </test>
    <edit binding="strong" name="family">
        <string>JetBrainsMono Nerd Font</string>
    </edit>
</match>
```

#### 根据语言环境选择不同字体

这可以解决[#常见字体配置问题](#常见字体配置问题)中的[#异体字不正确显示](#异体字不正确显示)与[#引号的全半角问题](#引号的全半角问题)。

这里使用的 `Noto Sans CJK` 支持 `SC`（对应 `zh-CN`）、`HK`（对应 `zh-HK`）、`TC`（对应 `zh-TW`）、`JP`（对应 `ja`）、`KR`（对应 `ko`）五种变体。

示例一（不包括文件头和 `<fontconfig>`）：
```xml
<!-- Replace fonts for Chinese (Hong Kong) -->
<match target="pattern">
    <test name="lang">
        <string>zh-HK</string>
    </test>
    <test name="family">
        <string>Noto Sans CJK SC</string>
    </test>
    <edit binding="strong" name="family">
        <string>Noto Sans CJK HK</string>
    </edit>
</match>
<match target="pattern">
    <test name="lang">
        <string>zh-HK</string>
    </test>
    <test name="family">
        <string>Noto Sans Mono CJK SC</string>
    </test>
    <edit binding="strong" name="family">
        <string>Noto Sans Mono CJK HK</string>
    </edit>
</match>
```

此处替换了香港字体，其他地区切换类似。

示例二（不包括文件头和 `<fontconfig>`）：
```xml
<match target="pattern">
    <test compare="not_contains" name="lang" qual="first">
        <string>zh</string>
    </test>
    <test compare="not_contains" name="lang" qual="first">
        <string>ja</string>
    </test>
    <test compare="not_contains" name="lang" qual="first">
        <string>ko</string>
    </test>
    <test compare="contains" name="family">
        <string>Noto Sans CJK SC</string>
    </test>
    <edit binding="strong" mode="prepend" name="family">
        <string>Noto Sans</string>
</match>
<match target="pattern">
    <test compare="not_contains" name="lang" qual="first">
        <string>zh</string>
    </test>
    <test compare="not_contains" name="lang" qual="first">
        <string>ja</string>
    </test>
    <test compare="not_contains" name="lang" qual="first">
        <string>ko</string>
    </test>
    <test compare="contains" name="family">
        <string>Noto Serif CJK SC</string>
    </test>
    <edit binding="strong" mode="prepend" name="family">
        <string>Noto Serif</string>
</match>
```

**注**：Chrome 及 Chromium 只会取结果中的第一个字体，如果替换了将会使中文字符不能显示，此时需要通过属性 `prgname` 过滤掉这些程序，这些程序无法实现全半角切换。

#### 优化字体渲染

示例（也可以不指定强绑定，不包括文件头和 `<fontconfig>`）：
```xml
<!--rendering options-->
<match target="font">
    <edit mode="assign" name="autohint" binding="strong">
        <bool>false</bool>
    </edit>
    <edit mode="assign" name="hinting" binding="strong">
        <bool>true</bool>
    </edit>
    <edit mode="assign" name="hintstyle" binding="strong">
        <const>hintmedium</const>
    </edit>
    <edit mode="assign" name="antialias" binding="strong">
        <bool>true</bool>
    </edit>
    <edit mode="assign" name="lcdfilter" binding="strong">
        <const>lcddefault</const>
    </edit>
    <edit mode="assign" name="rgba" binding="strong">
        <const>rgb</const>
    </edit>
</match>
```

#### 其他程序的字体设定

许多程序自己有字体设定，或者使用 KDE 或 GNOME 等桌面环境的字体设定。但我们设置好了 fontconfig 不需要再设置这些软件。我们只需要在软件（或桌面环境提供的设置程序）中选择通用字族（可能为英文，也可能为中文 `等宽`、`衬线`、`无衬线`）为字体就行了。

## 局限性

除了一些程序不使用 fontconfig 外，fontconfig 作为十分底层的程序，可以满足大部分自定义字体的要求，但一些涉及到单字的字体设置（标点挤压、不依赖语言设置自动检测全半角引号等）只能通过更改字体本身实现，可以看我的[下一篇文章](https://tjw123hh.github.io/2024/07/28/Linux-%E5%9C%A8%E5%AD%97%E4%BD%93%E5%B1%82%E9%9D%A2%E5%AE%9E%E7%8E%B0%E6%A0%87%E7%82%B9%E6%8C%A4%E5%8E%8B/)。

## 另请参阅

- [Linux fontconfig 的字体匹配机制](https://catcat.cc/post/2020-10-31/) ⸺ [rydesun](https://catcat.cc/)（包含更多技术细节）
- [用 fontconfig 治理 Linux 中的字体](https://catcat.cc/post/2021-03-07/) ⸺ [rydesun](https://catcat.cc/)
- [fontconfig：Linux下的字体配置](https://www.lbqaq.top/p/linux-font/) ⸺ [luoboQAQ](https://www.lbqaq.top/)
- [Linux 上的字体配置与故障排除](https://blog.lilydjwg.me/2023/3/5/linux-fonts.216591.html) ⸺ [依云](https://blog.lilydjwg.me/)
- [官方用户文档（字体配置文件）](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [fonts.conf 中文手册](https://www.jinbuguo.com/gui/fonts.conf.html) ⸺ [金步国](https://www.jinbuguo.com/)

## 版权声明

本作品的原始版本及截至 2024 年 8 月 1 日 0:00 UTC 之前的所有版本均遵循 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1) 许可证。从 2024 年 8 月 1 日 0:00 UTC 开始的所有更新版本遵循 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1) 许可证。文章开头仅标注创作开始日期。
