import time
import os
from threading import Thread
from mutagen.mp3 import MP3

def main(player,lrc_name,lrc_path,music_path,sleep_time,preview):
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

	def red(name):
		with open(name,'r')as f:
			return list(f.read().split('\n'))

	def get(tm):
		t=tm.split(':')
		if t==['']:
			pass
		else:
			return 60*int(t[0])+float(t[1])

	def pla(player,file):
		os.system("%s '%s'"%(player,file))

	def show(dic,ttt,sleep_time,preview):
		ttt.start()
		for l in dic:
			t=float(sum(l.keys()))
			if ttt.is_alive():
				time.sleep(t-sleep_time)
				print(str(l[t]))
				if preview:
					try:
						nxt=dic.index(l)+1
						nxt=dic[nxt]
						nxt_t=float(sum(nxt.keys()))
						nxt_d=nxt[nxt_t]
						print('\033[1;30;40m'+str(nxt_t)+'秒后: '+nxt_d+'\033[0m')
					except IndexError:
						print('\033[1;30;40m歌词到底啦!\033[0m')
			else:
				print('\n你似乎手动终止了音乐...')
				return
		ttt.join()
			
	def analysis(name,ttt):
		data=red(name)
		ls=[]
		for i in data:
			tm=i.replace('[','').split(']')
			ls.append(tm)
		def do(ls,sleep_time):
			dic=[]
			for t in ls:
				tm=t[0]
				me=ls.index(t)
				if me==0:
					dic.append({0:t[1]})
				else:
					now=ls[me][0]
					pre=ls[me-1][0]
					if now=='':
						pass
					else:
						lls=[]
						slt=get(now)-get(pre)-sleep_time-sleep_time
						lls.append(slt)
						llls=[]
						llls.append(t[1])
						dic.append(dict(zip(lls,llls)))
			return dic
		if '00:00.00' in ls[0][0]:
			ls=ls
		else:
			ls.insert(0,['00:00.000','\n不规范的歌词文件,已自动修复!'])
		return do(ls,sleep_time)

	def get_at(dic):
		ls=[]
		for d in dic:
			ls.append(sum(d.keys()))
		return sum(ls)

	result=find(lrc_name,lrc_path,music_path)
	if result[-1]==0:
		return False
	if result[-1]==1:
		music_name=result[0]
		print('\n\033[1;36m没有找到歌词!\n\033[0m')
		MP3(music_path+get_good_name(music_name)).info.length
		pla(player,music_path+get_good_name(music_name))
	if result[-1]==2:
		music_name=result[1]
		lrc_name=result[0]
		ttt=Thread(target=pla,args=(player,music_path+get_good_name(music_name)))
		ttt.daemon=True
		length=MP3(music_path+get_good_name(music_name)).info.length
		res=analysis(lrc_path+lrc_name,ttt)
		if get_at(res)>length:
			print('\033[1;36m此歌词文件中写明的时长与歌曲实际时长不符,请将此歌曲文件\033[1;32m'+lrc_path+lrc_name+'\033[0m\033[1;36m的最后一行进行修改后再重新播放.已自动跳过该首歌!\n\033[0m')
			return 1
		else:
			show(res,ttt,sleep_time,preview)

'''
eg: 

main('cvlc --play-and-exit ','近藤真彦-夕焼けの歌','歌词/','./',0,True)

=========================================================

10.4更新:

* 五处输出添加了换行(19,22,83,94,116);

* 不规范的歌词的再次规范,例如:

[00:00.000] 作曲 : daniwell
[99:00.00]纯音乐，请欣赏

(太恐怖了...)

* 中断的相关处理;

* 线程属性的规范(daemon守护),这样一来只需要Ctrl C一次即可中途退出.

=========================================================

10.6更新:

* 添加了新参数:preview,决定是否要预览;

* 完全重构了歌词显示的函数(也不是完全);

* 考虑了更多情况(歌词结束,强制中断,歌词时长大于实际时长...)

'''