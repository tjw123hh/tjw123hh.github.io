---
title: 怎么用 Github 创一个自己的博客（使用 Jekyll 主题）
tags:
    - Web
---

## 前言

折腾了好久终于搞定了这个新主题
虽然我不知道建这个博客干什么
但我觉得还是讲一讲怎么创一个自己的博客吧
先讲讲前面的（最简单的）部分

## 你需要什么

- 基本 Git /会查资料
- 一台电脑~~（手机好像也行？）~~

## 前置

- 注册一个 [Github](https://github.com) 账号

## 如果你要使用 Jekyll 主题

### 找到你喜欢的主题

你可以去网上搜（），但是推荐到 [Jekyll Themes](http://jekyllthemes.org/) 这个网站上找。

~~网站长这样：~~<br />
![网站长这样](/assets/1.png)<br />
<center>^^^服务器没设置好：只能用 HTTP 不能用 HTTPS </center><br />

网站其实长这样： <br />
![网站其实长这样](/assets/2.png)<br />

接下来，你只需要按照官方教程就行了（）<br />

当然我用的 [jekyll-theme-WuK](https://jekyll-theme-wuk.wu-kan.cn/)（链接是官方教程）by [@wu-kan](https://wu-kan.cn) 我肯定会自己写教程的：

## 使用 [jekyll-theme-WuK](https://jekyll-theme-wuk.wu-kan.cn/)

### 关于

这是由 [@wu-kan](https://wu-kan.cn) 写的一个博客主题，比较简洁。但是功能非常多：包括 Live2D 看板娘、页面统计（浏览次数、人数等）、打赏界面、博客标签、评论、幻灯片、自动目录等等。总之十分方便。

### 使用

1. 首先，进入[作者给的示例站点](https://github.com/wu-kan/wu-kan.github.io)**（！！！不是[主题仓库](https://github.com/wu-kan/jekyll-theme-WuK)）**然后 Fork（官方教程）或者直接点击“Use this template”按钮<br />
![“Use this template”按钮](/assets/0.png)

2. 然后把库的名称改成`<你的 Github 用户名>.github.io`（如果你想在网站的根上建博客的话）或者你想要用的目录名称（网站会在`<你的 Github 用户名>.github.io/<库名>/`上）

3. 用 Git 克隆你的仓库到本地

    git clone https://github.com/<你的用户名>/<你的仓库名称>.git

4. 打开配置文件`_config.yml`按照注释改（大部分都需要自己改）

5. 保存之后先改一下`README.md`也就是主页，然后就可以把`_posts/`下的文件除了404、archive、comments、merger、tags几个页面都删除了，然后就可以用 Markdown 自己写博文了（文件名格式`yyyy-mm-dd-<标题>.md`）

### 文章前面的 YAML 头
这里讲一下文章前面的 YAML 头（其实看看原来`_posts/`下的文件就会了）<br />

#### 在文件开头加这种
（上下是三个以上连接符，就是 Markdown 中表格的格式）

    ---
    key1: value
    key2:
        - value1
        - value2
        ...
    ...
    ---

#### 几个可能的 key 及其 value

- `title`：博文的标题（覆盖文件名指定的标题，但路径不变）

- `tags`：就是文章的标签！（可以用上面`key2`的方法加多个。）标签页会自动统计。

- `layout`（根据作者的介绍）：

    - `default`：基于 [poole/lanyon](https://github.com/poole/lanyon) 的页面，提供一个侧边栏和可随侧边栏移动的 warp 。

    - `page`：基于`default`，提供了一个标题栏`.masthead`和文本框`.content`。

    - `archive`：基于`page`的归档页。<br />
    [我的归档页](/archive/)
        > 当前我对它不是很满意，可能会在以后的版本中修改。

    - `tags`：基于`page`的标签页。<br />
    [我的标签页](/tags/)
        > 当前我对它不是很满意，可能会在以后的版本中修改。

    - `comments`：基于`page`的留言页，留言插件使用了 Valine 。<br />
    [我的留言页](/comments/)

    - `post`：基于`comments`的博文页，为每篇博文增加描述信息。<br />
    这篇文章就是示例（

    - `page404`：基于[腾讯志愿者](http://e.t.qq.com/Tencent-Volunteers)的公益 404 页。<br />
    [我的 404 页](/404)

    - `merger`：基于 merger 的打赏页。<br />
    [我的捐赠页](/merger/)

    - `home`：就是主页的幻灯片（按`Esc`键有惊喜
    [我的主页](/)
        > 从 `v3.1.0` 版本开始，`layout: home` 被我重写，基于 [hakimel/reveal.js](https://github.com/hakimel/reveal.js) 实现了一个简洁的展示页面，既可以作为博客的封面，也可以用作 presentation！

    注：这些页面的设置全在`_config.yml`里

- `redirect_from`：从什么地方重定向来。
    - 也可以添加多个！例子就是你在`whataname.md`的 YAML 头里加上`redirect_from: /aspecialname`就可以通过`<你的博客的 Baseurl>/aspecialname`访问它（会显示几秒的`Redirecting...`）

## 你选择~~自力更生~~自己写样式

那么你只需要改你的`index.html`或`index.htm`就行了，这是你的主页，你需要自己添加导航到其他界面。


