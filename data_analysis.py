import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np
from scipy import optimize

dist = {'doncheng': '东城', 'xicheng': '西城', 'haidian': '海淀', 'chaoyang': '朝阳',
        'fengtai': '丰台', 'shijingshan': '石景山', 'tongzhou': '通州', 'changping': '昌平'}

# 连接MySQL 并读取数据
# conn = pymysql.connect('127.0.0.1', 'root', '123456', 'lianjia', autocommit=True)
# sql = "select * from tbl_house_new"
# df_house = pd.read_sql(sql, conn)

# 从csv文件中读取
df_house = pd.read_csv('./house_data.csv')

# 面积=》小数
df_house['area'] = df_house['area'].apply(lambda x: float(x.strip()[:-2]))
df_house['district'] = df_house['district'].apply(lambda x: dist[x])

# points = []
# for idx, row in df_house.iterrows():
#     points.append({"lng": row['Longitude'], "lat": row['Latitude'], "count": row['average_price']})
# print(points)



price = df_house['average_price']
max_price = price.max()
min_price = price.min()
mean_price = price.mean()
median_price = price.median()

print("北京市二手房最高价格：%.2f元/平方米" % max_price)
print("北京市二手房最低价格：%.2f元/平方米" % min_price)
print("北京市二手房平均价格：%.2f元/平方米" % mean_price)
print("北京市二手房中位数价格：%.2f元/平方米" % median_price)

# 整体房价分布
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
plt.xlim(0, 200000)
plt.ylim(0, 1500)
plt.title("北京市二手房价格分析")
plt.xlabel("二手房均价（元/平米）")
plt.ylabel("数量（套）")
plt.hist(price, bins=60)
plt.vlines(mean_price, 0, 1500, color='red', label='平均价格', linewidth=1.5, linestyle='--')
plt.vlines(median_price, 0, 1500, color='red',label='中位数价格', linewidth=1.5)
plt.legend()
plt.show()

# 房屋总价分布
price = df_house['price']
max_price = price.max()
min_price = price.min()
mean_price = price.mean()
median_price = price.median()

print("北京市二手房最高总价：%.2f万元" % max_price)
print("北京市二手房最低总价：%.2f万元" % min_price)
print("北京市二手房平均总价：%.2f万元" % mean_price)
print("北京市二手房中位数总价：%.2f万元" % median_price)

plt.xlim(0, 4000)
plt.ylim(0, 5000)
plt.title("北京市二手房价格分析")
plt.xlabel("二手房总（万元）")
plt.ylabel("数量（套）")
plt.hist(price, bins=60)
plt.vlines(mean_price, 0, 5000, color='red', label='平均价格', linewidth=1.5, linestyle='--')
plt.vlines(median_price, 0, 5000, color='red',label='中位数价格', linewidth=1.5)
plt.legend()
plt.show()

# 各行政区房源数量
plt.figure(figsize=(12, 9))
#df_dist = pd.read_sql("select district, count(*) from tbl_house_new b group by b.district", conn)
df_dist = df_house.groupby('district', as_index=False)['price'].agg({'district_count': 'count'})
labels = df_dist['district']
values = df_dist['district_count']
explode = (0, 0, 0.03, 0, 0, 0, 0, 0)
patches,text1,text2 = plt.pie(values,
                      explode=explode,
                      labels=labels,
                      #colors=colors,
                      autopct = '%3.2f%%', #数值保留固定小数位
                      shadow = True, #无阴影设置
                      startangle =90, #逆时针起始角度设置
                      pctdistance = 0.6) #数值距圆心半径倍数的距离
#patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
# x，y轴刻度设置一致，保证饼图为圆形
plt.axis('equal')
for x in range(len(text1)):
    text1[x].set_fontsize(30)
    text2[x].set_fontsize(30)
plt.show()

# 各行政区平均房价分布
mean_price_district = df_house.groupby('district')['average_price'].mean().sort_values(ascending=False)
mean_price_district.plot(kind='bar',color='b')
print(mean_price_district)
plt.ylim(10000,120000,10000)
plt.title("北京市各行政区划二手房平均价格分析")
plt.xlabel("北京市行政区划")
plt.ylabel("二手房平均价格（元/平米）")
plt.show()

# 各行政区房屋价格箱形图
df_house.boxplot(column='average_price', by='district', whis=1.5)
plt.show()

# 房屋面积与价格分布
plt.scatter(df_house['area'], df_house['average_price'], s=2.5)
plt.xlabel("面积(平米)")
plt.ylabel("均价（元/平米）")
plt.title("房屋面积与房屋均价散点图")
plt.show()

# 各行政区内房屋面积对房价影响
plt.figure(figsize=(10, 8), dpi=256)
colors = ['red','red', 'blue', 'blue', 'green', 'green', 'gray', 'gray']
markers = ['o','x', 'o','x', 'o','x', 'o','x']
bj_districts = ['西城', '海淀', '朝阳', '东城', '丰台', '石景山', '通州', '昌平']
for i in range(len(bj_districts)):
    x = df_house.loc[df_house['district'] == bj_districts[i]]['area']
    y = df_house.loc[df_house['district'] == bj_districts[i]]['average_price']
    plt.scatter(x, y, c=colors[i], s=20, label=bj_districts[i], marker=markers[i])
plt.legend(loc=1, bbox_to_anchor=(1.138, 1.0), fontsize=12)
plt.xlim(0, 500)
plt.ylim(0,200000)
plt.title('北京市各行政区内房屋面积对房价的影响（散点图）',fontsize=20)
plt.xlabel('面积（平米）', fontsize=16)
plt.ylabel('均价（元/平米）')
plt.show()

# 线性拟合
def linear_fit(x, A, b):
    return A*x + b
plt.figure(figsize=(10,8), dpi=256)
for i in range(len(bj_districts)):
    x = df_house.loc[df_house['district'] == bj_districts[i]]['area']
    y = df_house.loc[df_house['district'] == bj_districts[i]]['price']
    A, b = optimize.curve_fit(linear_fit, x, y)[0]
    xx = np.arange(0, 500, 100)
    yy = A * xx + b
    plt.plot(xx, yy, c=colors[i], marker=markers[i], label=bj_districts[i], linewidth=2)

plt.legend(loc=1,bbox_to_anchor=(1.138,1.0),fontsize=12)
plt.xlim(0, 400)
plt.ylim(0, 5000)
plt.title('北京各行政区内房屋面积对房价的影响（线性拟合）',fontsize=20)
plt.xlabel('面积（平米）',fontsize=16)
plt.ylabel('均价（元/平米）', fontsize=16)
plt.show()
