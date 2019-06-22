#%matplotlib inline
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

stop_data = np.loadtxt('stopfilt.txt')
walk_data = np.loadtxt('walkfilt.txt')

stop_y = np.loadtxt('stop_y.txt')
walk_y = np.loadtxt('walk_y.txt')

data_x = np.append(stop_data, walk_data)
data_y = np.append(stop_y, walk_y)

data_x =[]
data_y = []

i=0
for stop in stop_data:
	data_x.append([stop,stop_y[i]])
	data_y.append(1)
	i = i+1
i=0
for walk in walk_data:
	data_x.append([walk,walk_y[i]])
	data_y.append(2) 
	i =i +1

plt.plot(data_x)
plt.show()
#再把7.2課程的分類資料再做一次出來
#宣告四個點（以二維陣列的方式宣告）
#x = np.array([[-3,2],[-6,5],[3,-4],[2,-8]])
#四個點依序分類為第一類、第一類、第二類、第二類
#y = np.array([1,1,2,2])

#然後要開一台SVC
clf = SVC(gamma='auto')

#開始訓練：clf.fit(輸入資料,正確答案)
clf.fit(data_x,data_y)

#正式的把四個點全部代入
#順利得到分類答案：array([1, 1, 2, 2])
#ps.當然會順利得到正確答案，因為剛剛透過clf.fit()訓練時，已經有先給答案了 = ="
#成功！目前為止上面的程式碼只是用來載入之前訓練的結果clf.fit(x,y)
#還沒有進入正題 @@"
clf.predict(data_x)

#上面的predict的結果，是以array的方式顯示
#以下要展示的是使用圖的方式來顯示預測的結果
#首先示範一個簡單的例子做meshgrid
#瞭解meshgrid之後才能繼續下去
#假設這裡有四個x座標1, 2, 3, 4以及四個y座標5, 6, 7, 8
xx = [1,2,3,4]
yy = [5,6,7,8]

#meshgrid執行之後，得到的 一堆X座標, 以及一堆Y座標
X, Y = np.meshgrid(xx,yy)
#然後透過ravel()把X拉平為一維陣列座標
#方便之後的plt.scatter畫圖以及clf.predict預測分類可以直接吃一維陣列
X = X.ravel()
#同樣的，Y也要拉平
Y = Y.ravel()
#最後利用plt.scatter畫在曲線圖上的話，這個圖的所有座標點就可以填滿 x=1~4, y=5~8 的部分
#這就是meshgrid功用
plt.scatter(X,Y)
plt.show()

#要回頭來進行下一步之前，先清空X, Y
X = []
Y = []

#接下來利用相同的meshgrid方法去處理 7.2課程中瞎掰的那幾個點
#取的點的數量隨意，這裡是設定為30個，設定數字越大的時候，最後畫出來的圖上的點越密集就是了
X, Y = np.meshgrid(np.linspace(-6,3,30),np.linspace(-8,5,30))
X = X.ravel()
Y = Y.ravel()

#然後畫圖就可以看到密密麻麻的一堆座標點
#當然這些點尚未做分類
plt.scatter(X,Y)
plt.show()

#接下來要利用clf.predict幫這些密密麻麻的點做分類
#不過clf.predict吃的參數是座標，所以 X, Y必須修正為座標的形式才能代入
#利用zip()函數即可做到合併為座標(加上list()才能正確執行並顯示結果)
list(zip(X,Y))

#那麼接下來就把這個合併後的座標代入clf.predict()
#就可以順利得到預測分類的結果！這個預測分類的結果的形式是array
clf.predict(list(zip(X,Y)))

#當然最後的目的就是要畫出完整的分類結果圖：
#這樣就完成了！可以看到密密麻麻的點被分類成兩個顏色喔 :D
plt.scatter(X,Y, c=clf.predict(list(zip(X,Y))))
plt.show()
