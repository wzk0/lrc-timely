import time
import os
from threading import Thread

def main(player,lrc_name,lrc_path,music_path,sleep_time):
	def get_good_name(name):
		name=name.replace('(','\(')
		name=name.replace(')','\)')
		name=name.replace(' ','\ ')
		return name

	def find(name,lrc_path,music_path):
		lrc=os.listdir(lrc_path)
		music=os.listdir(music_path)
		ls=[]
		for l in lrc:
			if name in l:
				if name==l.split('.')[0]:
					print('\n\033[1;36m已找到同名的歌词文件!\n\033[0m')
					ls.append(l)
				else:
					print('\n\033[1;36m未找到同名的歌词文件,但找到可能相关的歌词文件!名称为: \033[1;32m'+str(l)+'\033[0m\033[1;36m 将使用该歌词文件!\n\033[0m')
					ls.append(l)
		for m in music:
			mm=m.split('.')[0]
			if name==mm:
				ls.append(m)
		ls.append(len(ls))
		return ls

	##无模糊识别:
	'''
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
	'''

	def read(name):
		with open(name,'r')as f:
			return list(f.read().split('\n'))

	def get(tm):
		t=tm.split(':')
		if t==['']:
			pass
		else:
			return 60*int(t[0])+float(t[1])

	def begin(name,w):
		data=read(name)
		ls=[]
		for i in data:
			tm=i.replace('[','').split(']')
			ls.append(tm)
		def do(ls,sleep_time):
			for t in ls:
				tm=t[0]
				me=ls.index(t)
				if me==0:
					print(ls[0][1])
				else:
					now=ls[me][0]
					pre=ls[me-1][0]
					if now=='':
						pass
					else:
						time.sleep(get(now)-get(pre)-sleep_time)
						print(t[1])
						##可以搞彩色的皮肤!
		if '00:00.00' in ls[0][0]:
			ls=ls
		else:
			ls.insert(0,['00:00.000','\n不规范的歌词文件,已自动修复!\n'])
		do(ls,sleep_time)

	def play(player,file):
		os.system(player+' '+file)

	result=find(lrc_name,lrc_path,music_path)
	if result[-1]==0:
		return False
	if result[-1]==1:
		music_name=result[0]
		print('\n\033[1;36m没有找到歌词!\n\033[0m')
		play(player,music_path+music_name)
	if result[-1]==2:
		music_name=result[1]
		lrc_name=result[0]
		t1=Thread(target=begin,args=(lrc_path+lrc_name,''))
		t2=Thread(target=play,args=(player,music_path+get_good_name(music_name)))
		t1.daemon = True
		t2.daemon = True
		t1.start()
		t2.start()
		t2.join()
		if t2.is_alive()!=True:
			if t1.is_alive():
				try:
					t1._stop()
				except:
					print('\n\033[1;36m由于不规范的歌词或手动中断了歌曲,已中途退出!\n\033[0m')
			else:
				pass

'''
eg: 

main('cvlc --play-and-exit ','Maru-^Nyan_Cat^__Kawaii_Future_Bass_Remix','歌词/','./',0.01)

main(player,lrc_name,lrc_path,music_path,sleep_time)内,

player是播放器的名字,可以填cvlc或者play,注意需要末尾加空格;

如果是cvlc,建议加上参数cvlc --play-and-exit,在播放后后会自动结束线程,以保证接下来程序的正常运行;

name是待查询的文件名;

lrc_path是歌词文件所在路径;

music_path是音频文件所在路径;

sleep_time是歌词提前于时刻出现的时间长度.这个数请尽量小,因为会叠加效果;如果这个数大,说唱歌曲可能出词速度过快.

=======================================================

10.4更新:

* 五处输出添加了换行(19,22,83,94,116);

* 不规范的歌词的再次规范,例如:

[00:00.000] 作曲 : daniwell
[99:00.00]纯音乐，请欣赏

(太恐怖了...)

* 中断的相关处理;

* 线程属性的规范(daemon守护),这样一来只需要Ctrl C一次即可中途退出.
'''