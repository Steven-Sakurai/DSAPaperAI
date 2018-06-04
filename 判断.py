
def point_dis(x1,y1,x2,y2):
	'''
	求两点(x1,y1)到(x2,y2)之间的距离
	距离定义为：|x1-x2| + |y1-y2|
	'''
	return (abs(x1-x2)+abs(y1-y2))
	
def fields_dis(x,y,fields,id):
	'''
	求点(x,y)到玩家id的领地的距离
	定义为(x,y)到属于id的领地内的点的最短距离
	输入：
	    x - 点的横坐标
		y - 点的纵坐标
		fields - 当店场地内领地的情况
		id - 玩家的id
	输出：一个整数，点(x,y)到玩家id的领地的距离
	'''
	width = len(fields)
	height = len(fields[0])
	dis = None
	
	for i in range(width):
		for j in range(height):
			if (fields[i][j] == id) and ((dis = None) or (point_dis(i,j,x,y)<dis)):
				dis = point_dis(i,j,x,y)
	return dis
			
def ave(alist):
	'''
	求一个列表alist中所有数字的平均数
	'''
	return sum(alist)/len(alist)
	
def enemytype(stat):
	'''
	主函数：判断对手的风格
	判断标准：
		基本原则是对方离自己的领地越远，风格越激进。以自己目前到对方的距离作为参照pivot，判断远近
		如果过去30步的最远距离大于pivot，或者平均距离大于pivot/2，很激进；
		如果过去30步的最远距离大于pivot/2，或者平均距离大于pivot/4，偏激进；
		如果过去30步的最远距离大于pivot/3，或者平均距离大于pivot/6，偏保守；
		如果过去30步的最远距离小于pivot/3，而且平均距离小于pivot/6，很保守。		
	
	输入：
		游戏数据stat
	输出：一个整数，代表对手风格
		1：很保守
		2：偏保守
		3：遍激进
		4：很激进
	'''
	length = len(stat['log'])
	l = len(stat['log'])
	if l > 30:   # 取之前30步对手纸卷头到对手领地的距离；如果还不到30步，就取当前已经走过的步数
		l = 30
		
	dislist = []
	for i in range(l):
		time = length - i - 1
		x = stat['log'][time]['enemy']['x']
		y = stat['log'][time]['enemy']['y']
		id = stat['log'][time]['enemy']['id']
		dislist.append(fields_dis(x,y,stat['log'][time]['fields'],id))
	
	enemyx, enemyy = stat['log'][-1]['enemy']['x'], stat['log'][-1]['enemy']['y']
	selfx, selfy = stat['log'][-1]['me']['x'], stat['log'][-1]['me']['y']
	pivot = point_dis(enemyx, enemyy, selfx, selfy)
	
	if (max(dislist) >= pivot) or (ave(dislist) >= pivot/2): 
		return 4
	elif (max(dislist) >= pivot/2) or (ave(dislist) >= pivot/4):
		return 3
	elif (max(dislist) >= pivot/3) or (ave(dislist) >= pivot/6):
		return 2
	else:
		return 1