# Paper.io
Group work

## 如何增强normal wanderer  
- 在领地内wander时，尽量靠边    
- 尽量圈别人地  
- 如果领先很多，贴防

## Crazy Pig      
#### 思路    
- 离敌人远时，往他身上靠    
- 离敌人近时，躲着跑    
- 离敌人绝对距离远时，圈地激进一点（就是改成除4或除3） 
 
#### 代码改动  
- storage['myField'] is a np matrix: {0: nothing, 1: my field, 2: my band, 3: his field, 4: his band}  
- directions相关都改成np.array，转向用矩阵乘法    

#### 调参  
- 主要是118行那个20可以调下  
- 还有202-218  

## git 使用说明  
先下载git  
设置邮箱：git config --global user.email "xxx@pku.edu.cn"  
然后  
git clone https://github.com/Steven-Sakurai/Paper.io  
cd Paper.io  
git pull origin master  
添加文件  
touch xxx.py  
git add -A  
git commit -m "一些信息"  
git push origin master  
