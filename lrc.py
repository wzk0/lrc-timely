import time
import os
from threading import Thread

def main(player,lrc_name,music_name):
	def read(name):
		with open(name+'.lrc','r')as f:
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

	def play(player,file):
		os.system(player+' '+file)

	t1=Thread(target=begin,args=(lrc_name,''))
	t2=Thread(target=play,args=(player,music_name))
	t1.start()
	t2.start()
	t1.join()
	t2.join()

main(player,lrc_name,music_name)