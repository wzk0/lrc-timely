# 终端实时歌词!

通过sleep实现的终端lrc歌词文件解析和实时展示.

## 功能

1. 秒数级的实时歌词显示;

2. 自动寻词和模糊识别功能;

3. 多情况判断与参数返回;

4. ...

## 效果

> 使用`sox`播放时:

[录屏 2022年10月01日 19时56分54秒.webm](https://user-images.githubusercontent.com/89891126/193408480-e7f01c53-131d-4672-9347-b27ae3492a4b.webm)


> 使用`cvlc`播放时:

[录屏 2022年10月01日 19时59分37秒.webm](https://user-images.githubusercontent.com/89891126/193408574-83f2b972-bf1c-406f-a2c8-5141abad5d86.webm)

## 原理

我们可以拿一个lrc文件的一部分做演示:

```txt
[03:00.43]天生爱你 想回到你的怀里
[03:03.19]对你的爱意 像那无边的海域
[03:06.49]天生爱你 想回到你的怀里
[03:09.15]对你的爱意 像那无边的海域
```

首先需要把前面方括号里的时间提取出来,这个用`split`函数就行;

接着需要对前面这段时间进行处理.

例如:

`03:09.15`中,`03`是分钟数,`09`则是秒数,最后两位是毫秒数.

于是我就把分钟数乘60转换为秒数,然后忽略毫秒数,最后就转换成了`03:09.15`这个时刻相对于音乐播放开始时的时间长度(单位:秒).

之后需要对上一句歌词做同样的处理,然后用这一句的减上一句的,得到两句之间的时间差.

这个`时间差`就是需要`sleep`的时长.

再然后,用一个简单的双线程就能实现一边播放一边显示歌词啦!

## 用法

将`lrc.py`这个文件移动到你的项目里,使用函数`lrc.main()`调用.

参数:

`main(player,name,lrc_path,music_path)`,

其中:

`player`填写播放器名称(`play `或`cvlc `或其他),**注意:需要在末尾加空格!**

`name`填写待播放的文件名或文件的部分名,**注意:不需要加后缀名!**

`lrc_path`填写歌词文件所在文件夹的路径,

同理,`music_path`是音频文件所在文件夹的路径.

会根据`name`自动匹配两个文件夹中的歌词和音频;如果连音频都匹配不到,则会返回`False`;

有音频无歌词的情况下,会直接在终端打印`没有找到歌词!`

## 其他

可以在代码第54行的地方修改输出样式,例如`彩虹皮肤`:

![](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210021556347.png)

将此行修改为:

```python3
i=random.randint(30,37)
z=random.randint(40,47)
print('\033[1;'+str(i)+';'+str(z)+'m'+t[1]+'\033[0m')
```

开头加上`import random`就OK啦!

若取消模糊识别功能(文件夹内有重复度较高的音频文件时),请修改`find()`函数的内容为:

```python3
def find(name,lrc_path,music_path):
		lrc=os.listdir(lrc_path)
		music=os.listdir(music_path)
		ls=[]
		for l in lrc:
			if name==l:
				ls.append(l)
		for m in music:
			mm=m.split('.')[0]
			if name==mm:
				ls.append(m)
		ls.append(len(ls))
		return ls
```