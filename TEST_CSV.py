Update_status = False
fp = open('portfolio.csv','r')
header = fp.readline().strip().split(',')
d = []
for u in fp:
    if u:
        print(u.strip()+'sdasdas')
        print (u)
    if not u:
        print('not u')
fp.close()