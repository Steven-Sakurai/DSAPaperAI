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

#### 目前效果
连续跑五次knockout

```bash
+----+------------------------+----------------+-----------+
Knockout Result: Crazy_Pig wins.
AI_normal_wanderer 3 : 11 Crazy_Pig
+----+------------------------+----------------+-----------+
|  # |     Endgame Winner     | Endgame Reason |    Rmk    |
+----+------------------------+----------------+-----------+
|  1 |     (B) Crazy_Pig      |  (1020, 1262)  | END, 4000 |
|  2 |     (A) Crazy_Pig      |  (1258, 1182)  | END, 4000 |
|  3 |     (B) Crazy_Pig      |  (1219, 1638)  | END, 4000 |
|  4 |     (A) Crazy_Pig      |  (1666, 845)   | END, 4000 |
|  5 |     (B) Crazy_Pig      |  (970, 1452)   | END, 4000 |
|  6 | (B) AI_normal_wanderer |       KO       | TAP, 1437 |
|  7 | (A) AI_normal_wanderer |  (1810, 1599)  | END, 4000 |
|  8 |     (A) Crazy_Pig      |       KO       | TAP, 3483 |
|  9 |     (B) Crazy_Pig      |  (837, 1884)   | END, 4000 |
| 10 |     (A) Crazy_Pig      |  (2373, 1274)  | END, 4000 |
| 11 |     (B) Crazy_Pig      |  (1343, 2191)  | END, 4000 |
| 12 | (B) AI_normal_wanderer |       KO       | TAP, 2675 |
| 13 |     (B) Crazy_Pig      |  (1145, 2439)  | END, 4000 |
| 14 |     (A) Crazy_Pig      |  (1554, 1367)  | END, 4000 |
|    |        Knockout        |   Ended Here   |           |
+----+------------------------+----------------+-----------+

+----+------------------------+----------------+-----------+
Knockout Result: Crazy_Pig wins.
AI_normal_wanderer 1 : 11 Crazy_Pig
+----+------------------------+----------------+-----------+
|  # |     Endgame Winner     | Endgame Reason |    Rmk    |
+----+------------------------+----------------+-----------+
|  1 |     (B) Crazy_Pig      |  (1106, 1991)  | END, 4000 |
|  2 |     (A) Crazy_Pig      |  (1807, 1088)  | END, 4000 |
|  3 |     (B) Crazy_Pig      |  (847, 2067)   | END, 4000 |
|  4 |     (A) Crazy_Pig      |  (1899, 1149)  | END, 4000 |
|  5 |     (B) Crazy_Pig      |       KO       | CIT, 2611 |
|  6 |     (A) Crazy_Pig      |  (1545, 1200)  | END, 4000 |
|  7 | (A) AI_normal_wanderer |       KO       | ERR, 3663 |
|  8 |     (A) Crazy_Pig      |       KO       | TAP, 2778 |
|  9 |     (B) Crazy_Pig      |  (892, 1393)   | END, 4000 |
| 10 |     (A) Crazy_Pig      |  (2075, 1139)  | END, 4000 |
| 11 |     (B) Crazy_Pig      |       KO       | TAP, 2407 |
| 12 |     (A) Crazy_Pig      |       KO       | TAP, 2980 |
|    |        Knockout        |   Ended Here   |           |
+----+------------------------+----------------+-----------+

+----+------------------------+----------------+-----------+
Knockout Result: Crazy_Pig wins.
AI_normal_wanderer 2 : 11 Crazy_Pig
+----+------------------------+----------------+-----------+
|  # |     Endgame Winner     | Endgame Reason |    Rmk    |
+----+------------------------+----------------+-----------+
|  1 |     (B) Crazy_Pig      |  (1017, 1468)  | END, 4000 |
|  2 |     (A) Crazy_Pig      |  (2021, 1194)  | END, 4000 |
|  3 |     (B) Crazy_Pig      |  (1354, 1454)  | END, 4000 |
|  4 | (B) AI_normal_wanderer |       KO       | TAP, 3440 |
|  5 |     (B) Crazy_Pig      |  (1141, 2293)  | END, 4000 |
|  6 |     (A) Crazy_Pig      |       KO       | TAP, 1944 |
|  7 |     (B) Crazy_Pig      |  (1189, 2012)  | END, 4000 |
|  8 | (B) AI_normal_wanderer |       KO       | CIT, 3970 |
|  9 |     (B) Crazy_Pig      |  (1111, 1260)  | END, 4000 |
| 10 |     (A) Crazy_Pig      |  (1418, 991)   | END, 4000 |
| 11 |     (B) Crazy_Pig      |  (935, 1283)   | END, 4000 |
| 12 |     (A) Crazy_Pig      |  (1483, 652)   | END, 4000 |
| 13 |     (B) Crazy_Pig      |  (745, 1746)   | END, 4000 |
|    |        Knockout        |   Ended Here   |           |
+----+------------------------+----------------+-----------+

+----+------------------------+----------------+-----------+
Knockout Result: Crazy_Pig wins.
AI_normal_wanderer 5 : 11 Crazy_Pig
+----+------------------------+----------------+-----------+
|  # |     Endgame Winner     | Endgame Reason |    Rmk    |
+----+------------------------+----------------+-----------+
|  1 | (A) AI_normal_wanderer |       KO       | TAP, 1045 |
|  2 |     (A) Crazy_Pig      |       KO       | TAP, 3580 |
|  3 |     (B) Crazy_Pig      |       KO       | TAP, 3129 |
|  4 |     (A) Crazy_Pig      |  (1657, 1227)  | END, 4000 |
|  5 |     (B) Crazy_Pig      |  (1069, 1638)  | END, 4000 |
|  6 |     (A) Crazy_Pig      |  (1381, 984)   | END, 4000 |
|  7 |     (B) Crazy_Pig      |  (1012, 1627)  | END, 4000 |
|  8 | (B) AI_normal_wanderer |       KO       | ERR, 2386 |
|  9 | (A) AI_normal_wanderer |       KO       | ERR, 3249 |
| 10 |     (A) Crazy_Pig      |  (1579, 1157)  | END, 4000 |
| 11 | (A) AI_normal_wanderer |  (1513, 1382)  | END, 4000 |
| 12 |     (A) Crazy_Pig      |  (1460, 1140)  | END, 4000 |
| 13 |     (B) Crazy_Pig      |       KO       | TAP, 2591 |
| 14 | (B) AI_normal_wanderer |       KO       | TAP, 2043 |
| 15 |     (B) Crazy_Pig      |  (990, 1636)   | END, 4000 |
| 16 |     (A) Crazy_Pig      |       KO       | TAP, 3482 |
|    |        Knockout        |   Ended Here   |           |
+----+------------------------+----------------+-----------+

+----+------------------------+----------------+-----------+
Knockout Result: Crazy_Pig wins.
AI_normal_wanderer 1 : 11 Crazy_Pig
+----+------------------------+----------------+-----------+
|  # |     Endgame Winner     | Endgame Reason |    Rmk    |
+----+------------------------+----------------+-----------+
|  1 |     (B) Crazy_Pig      |  (987, 1488)   | END, 4000 |
|  2 |     (A) Crazy_Pig      |  (1828, 1360)  | END, 4000 |
|  3 | (A) AI_normal_wanderer |       KO       | ERR, 2675 |
|  4 |     (A) Crazy_Pig      |  (1908, 992)   | END, 4000 |
|  5 |     (B) Crazy_Pig      |  (1079, 1663)  | END, 4000 |
|  6 |     (A) Crazy_Pig      |  (1933, 974)   | END, 4000 |
|  7 |     (B) Crazy_Pig      |       KO       | TAP, 1242 |
|  8 |     (A) Crazy_Pig      |  (2064, 1247)  | END, 4000 |
|  9 |     (B) Crazy_Pig      |  (1073, 1424)  | END, 4000 |
| 10 |     (A) Crazy_Pig      |       KO       | TAP, 1772 |
| 11 |     (B) Crazy_Pig      |  (966, 2084)   | END, 4000 |
| 12 |     (A) Crazy_Pig      |  (1813, 967)   | END, 4000 |
|    |        Knockout        |   Ended Here   |           |
+----+------------------------+----------------+-----------+
```
## Crazy Pig v2

```bash
Knockout Result: Crazy_Pig_v2 wins.
Crazy_Pig 1 : 11 Crazy_Pig_v2
+----+------------------+----------------+-----------+
|  # |  Endgame Winner  | Endgame Reason |    Rmk    |
+----+------------------+----------------+-----------+
|  1 | (B) Crazy_Pig_v2 |       KO       | ERR, 2828 |
|  2 | (A) Crazy_Pig_v2 |       KO       | ERR, 1551 |
|  3 | (B) Crazy_Pig_v2 |       KO       | ERR, 1794 |
|  4 | (A) Crazy_Pig_v2 |       KO       | ERR, 1363 |
|  5 | (B) Crazy_Pig_v2 |       KO       | ERR, 1386 |
|  6 | (A) Crazy_Pig_v2 |       KO       | ERR, 1435 |
|  7 | (B) Crazy_Pig_v2 |       KO       | ERR, 1634 |
|  8 | (A) Crazy_Pig_v2 |       KO       | ERR, 1183 |
|  9 | (B) Crazy_Pig_v2 |       KO       | ERR, 1126 |
| 10 |  (B) Crazy_Pig   |       KO       | TAP, 2518 |
| 11 | (B) Crazy_Pig_v2 |       KO       | ERR, 3850 |
| 12 | (A) Crazy_Pig_v2 |       KO       | ERR, 2833 |
|    |     Knockout     |   Ended Here   |           |
+----+------------------+----------------+-----------+

Knockout Result: Crazy_Pig_v2 wins.
AI_normal_wanderer 3 : 11 Crazy_Pig_v2
+----+------------------------+----------------+-----------+
|  # |     Endgame Winner     | Endgame Reason |    Rmk    |
+----+------------------------+----------------+-----------+
|  1 |    (B) Crazy_Pig_v2    |       KO       | TAP, 1017 |
|  2 | (B) AI_normal_wanderer |       KO       | TAP, 2024 |
|  3 | (A) AI_normal_wanderer |       KO       | TAP,  697 |
|  4 | (B) AI_normal_wanderer |       KO       | TAP, 2078 |
|  5 |    (B) Crazy_Pig_v2    |       KO       | CIT, 2302 |
|  6 |    (A) Crazy_Pig_v2    |  (2051, 1293)  | END, 4000 |
|  7 |    (B) Crazy_Pig_v2    |  (1130, 1914)  | END, 4000 |
|  8 |    (A) Crazy_Pig_v2    |  (2259, 884)   | END, 4000 |
|  9 |    (B) Crazy_Pig_v2    |  (1203, 2471)  | END, 4000 |
| 10 |    (A) Crazy_Pig_v2    |       KO       | TAP, 3508 |
| 11 |    (B) Crazy_Pig_v2    |  (1016, 2014)  | END, 4000 |
| 12 |    (A) Crazy_Pig_v2    |  (1957, 1440)  | END, 4000 |
| 13 |    (B) Crazy_Pig_v2    |  (949, 2275)   | END, 4000 |
| 14 |    (A) Crazy_Pig_v2    |  (2264, 1636)  | END, 4000 |
|    |        Knockout        |   Ended Here   |           |
+----+------------------------+----------------+-----------+
```


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
