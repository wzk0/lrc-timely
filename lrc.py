import time
import os
from threading import Thread

def main(player,lrc_name,lrc_path,music_path):
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
					print('\n\033[1;36m已找到同名的歌词文件!\033[0m')
					ls.append(l)
				else:
					print('\n\033[1;36m未找到同名的歌词文件,但找到可能相关的歌词文件!名称为: \033[1;32m'+str(l)+'\033[0m\033[1;36m 将使用该歌词文件!\033[0m')
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
		t=tm.split('.')[0].split(':')
		if t==['']:
			pass
		else:
			return 60*int(t[0])+int(t[1])

	def begin(name,w):
		data=read(name)
		ls=[]
		for i in data:
			tm=i.replace('[','').split(']')
			ls.append(tm)
		for t in ls:
			tm=t[0]
			me=ls.index(t)
			if me==0:
				needlose=0
			else:
				now=ls[me][0]
				pre=ls[me-1][0]
				if now=='':
					pass
				else:
					time.sleep(get(now)-get(pre))
					print(t[1])
					##可以搞彩色的皮肤!

	def play(player,file):
		os.system(player+' '+file)

	result=find(lrc_name,lrc_path,music_path)
	if result[-1]==0:
		return False
	if result[-1]==1:
		music_name=result[0]
		print('\n\033[1;36m没有找到歌词!\033[0m')
		play(player,music_path+music_name)
	if result[-1]==2:
		music_name=result[1]
		lrc_name=result[0]
		t1=Thread(target=begin,args=(lrc_path+lrc_name,''))
		t2=Thread(target=play,args=(player,music_path+get_good_name(music_name)))
		t1.start()
		t2.start()
		t1.join()
		t2.join()

'''
main(player,name,lrc_path,music_path)

player是播放器的名字,可以填cvlc或者play,注意需要末尾加空格;

如果是cvlc,建议加上参数cvlc --play-and-exit,在播放后后会自动结束线程,以保证接下来程序的正常运行;

name是待查询的文件名;

lrc_path是歌词文件所在路径;

music_path是音频文件所在路径.
'''