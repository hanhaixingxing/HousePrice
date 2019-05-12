import pymysql
import pandas as pd
import re
import numpy as np
import warnings
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import xgboost as xgb
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


def data_read():
    # 连接MySQL 并读取数据
    # conn = pymysql.connect('127.0.0.1', 'root', '123456', 'lianjia', autocommit=True)
    # sql = "select * from tbl_house_new;"
    # df_house = pd.read_sql(sql, conn)
    df_house = pd.read_csv('./house_data.csv')
    return df_house


def data_preprocess(df_house):
    # 去除车位记录
    total_count = df_house.shape[0]
    df_house = df_house[df_house['model'] != '车位']
    print("过滤车位信息 %d 条" % (total_count - df_house.shape[0]))
    # 处理房源面积信息
    df_house['area'] = df_house['area'].apply(lambda x: float(x.strip()[:-2]))
    # 计算房龄
    house_years = []
    house_type = []
    for info in df_house['build_time']:
        try:
            house_years.append(2019 - int(info.strip().split('/')[0][:4]))
        except:
            house_years.append(-1)
        try:
            house_type.append(info.strip().split('/')[1])
        except:
            house_type.append('暂无数据')
    df_house['house_years'] = np.array(house_years)
    df_house['house_type'] = np.array(house_type)

    # 计算卧室数量与客厅数量
    room_num = []
    ting_num = []
    for info in df_house['model']:
        s = re.findall("\d+", info)
        if len(s) == 2:
            room_num.append(int(s[0]))
            ting_num.append(int(s[1]))
        else:
            room_num.append(-1)
            ting_num.append(-1)
    df_house['room_num'] = np.array(room_num)
    df_house['ting_num'] = np.array(ting_num)

    df_house = df_house[df_house['house_years'] >= 0]
    df_house = df_house[df_house['room_num'] >= 0]
    df_house = df_house[df_house['ting_num'] >= 0]
    total_count = df_house.shape[0]
    df_house = df_house[df_house['house_type'] != '暂无数据']
    print("过滤信息 %d 条" % (total_count - df_house.shape[0]))

    df_house.drop(
        ['id', 'title', 'community', 'model', 'build_time', 'average_price','link','Latitude','Longitude'],
        axis=1, inplace=True)
    return df_house


def feature_generate(df_house):
    # 房屋建造类型向量化  行政区划向量化
    house_type = pd.get_dummies(df_house['house_type'], prefix='house_type')
    district = pd.get_dummies(df_house['district'], prefix='district')
    df_house.drop(['house_type', 'district'], axis=1, inplace=True)
    df_house = pd.concat([df_house, house_type, district], axis=1)

    print(df_house.columns)

    # 划分数据集
    y = np.array(df_house['price'])
    x = df_house.drop(['price'], axis=1)
    x = np.array(x)
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=41, test_size=0.3)
    print(df_house.shape)
    print(X_train.shape)
    print(X_test.shape)
    return X_train, X_test, y_train, y_test


def model_train(model, X_train, X_test, y_train):
    model.fit(X_train, y_train)
    y_pre = model.predict(X_test)
    print(model)
    return y_pre


def model_envulate(y_pre, y_test):
    mse = mean_squared_error(y_test, y_pre)
    r2 = r2_score(y_test, y_pre)
    return mse, r2


def visualize(y_test, y_pre, model_name):
    plt.scatter(y_test, y_pre)
    x = np.linspace(0, 10000, 500)
    plt.plot(x, x, color='red', linestyle='--', linewidth=2.5)
    plt.xlim(0, 10000)
    plt.ylim(0, 10000)
    plt.title(model_name+'模型的预测效果')
    plt.xlabel('真实值')
    plt.ylabel('预测值')
    plt.show()


if __name__ == '__main__':
    df_house = data_read()
    df_house = data_preprocess(df_house)
    X_train, X_test, y_train, y_test = feature_generate(df_house)
    # 线性回归
    lin_model = LinearRegression()
    y_pre = model_train(lin_model, X_train, X_test, y_train)
    mse, r2 = model_envulate(y_pre, y_test)
    print("线性回归MSE为"+str(mse)+"  R2为"+str(r2))
    visualize(y_test, y_pre, "线性回归")

    # 随机森林
    rf = RandomForestRegressor()
    y_pre = model_train(rf, X_train, X_test, y_train)
    mse, r2 = model_envulate(y_pre, y_test)
    print("随机森林MSE为" + str(mse) + "  R2为" + str(r2))


    # XGBoost
    m = xgb.XGBRegressor()
    y_pre = model_train(m, X_train, X_test, y_train)
    print(m.feature_importances_)
    mse, r2 = model_envulate(y_pre, y_test)
    print("XGBoostMSE为" + str(mse) + "  R2为" + str(r2))
    visualize(y_test, y_pre, "XGBoost")

    # 神经网络
    mlp = MLPRegressor()
    y_pre = model_train(mlp, X_train, X_test, y_train)
    mse, r2 = model_envulate(y_pre, y_test)
    print("多层神经网络MSE为" + str(mse) + "  R2为" + str(r2))