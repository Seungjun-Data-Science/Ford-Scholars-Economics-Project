import pandas as pd 
import os
count=2
flag=1


# file="/Users/Sal/Desktop/scrape/firms.csv"
# f=pd.read_csv(file)
# f['Total Earnings Abroad']=pd.Series([NaN])

while (flag==1):
	filename="/Users/Sal/Desktop/scrape/"+str(count)+".txt"
	print(filename)
	with open(filename,'r') as f:
		lines=f.readlines()
		string=str(lines)
		a=string.split('. ')
		len_a=len(a)
		for i in range(0,len_a):
			if 'indefinitely reinvested'  in a[i]:
				sentence=a[i]
				print(sentence)
				words=sentence.split(" ")
				len_words=len(words)
				for j in range(0, len_words):
					if '$' in words[j]:
						print(words[j])
						try:
							print(words[j+1])
							if words[j+1]=="million" or "billion":
								value=words[j]+words[j+1]
								print(words[j]+" "+words[j+1])
						except IndexError:
							pass
							continue

		f.close()
	count=count+1
	break
	if count==100:
		flag=0

