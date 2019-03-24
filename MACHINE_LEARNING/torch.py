import torch
from matplotlib import pyplot as plt
import torch.nn.functional as F


# 自定义一个Net类，继承于torch.nn.Module类
# 这个神经网络的设计是只有一层隐含层，隐含层神经元个数可随意指定
class Net(torch.nn.Module):
    # Net类的初始化函数
    def __init__(self, n_feature, n_hidden, n_output):
        # 继承父类的初始化函数
        super(Net, self).__init__()
        # 网络的隐藏层创建，名称可以随便起
        self.hidden_layer = torch.nn.Linear(n_feature, n_hidden)
        # 输出层(预测层)创建，接收来自隐含层的数据
        self.predict_layer = torch.nn.Linear(n_hidden, n_output)

    # 网络的前向传播函数，构造计算图
    def forward(self, x):
        # 用relu函数处理隐含层输出的结果并传给输出层
        hidden_result = self.hidden_layer(x)
        relu_result = F.relu(hidden_result)
        predict_result = self.predict_layer(relu_result)
        return predict_result


# 训练次数
TRAIN_TIMES = 200
# 输入输出的数据维度
INPUT_FEATURE_DIM = 2
OUTPUT_FEATURE_DIM = 2
# 隐含层中神经元的个数
NEURON_NUM = 10
# 学习率，越大学的越快，但也容易造成不稳定，准确率上下波动的情况
LEARNING_RATE = 0.01

# 数据构造
# 先生成一个100行，2列的基础数据
n_data = torch.ones(100, 2)
# normal函数用于生成符合指定条件的正太分布数据，传入的参数是均值和标准差
x0 = torch.normal(2 * n_data, 1)
x1 = torch.normal(-2 * n_data, 1)
# 这里的y并不是y坐标的意思，而是代表数据的类型标签，是整个网络的输出，以0、1表示不同类别
# 输入：(x[0],x[1])   输出：y
y0 = torch.zeros(100)
y1 = torch.ones(100)
# torch.cat是在合并数据,将a,b按行放在一起，如果第二个参数是0，则按列放在一起
x = torch.cat((x0, x1), 0).type(torch.FloatTensor)  # FloatTensor = 32-bit floating
y = torch.cat((y0, y1), ).type(torch.LongTensor)  # LongTensor = 64-bit integer

# 建立网络
net = Net(n_feature=INPUT_FEATURE_DIM, n_hidden=NEURON_NUM, n_output=OUTPUT_FEATURE_DIM)
print(net)

# 训练网络
# 这里也可以使用其它的优化方法
optimizer = torch.optim.Adam(net.parameters(), lr=LEARNING_RATE)
# 定义一个误差计算方法，分类问题可以采用交叉熵来衡量
loss_func = torch.nn.CrossEntropyLoss()

for i in range(TRAIN_TIMES):
    # 输入数据进行预测
    prediction = net(x)
    # 计算预测值与真值误差，注意参数顺序问题
    # 第一个参数为预测值，第二个为真值
    loss = loss_func(prediction, y)

    # 开始优化步骤
    # 每次开始优化前将梯度置为0
    optimizer.zero_grad()
    # 误差反向传播
    loss.backward()
    # 按照最小loss优化参数
    optimizer.step()

    # 可视化训练结果
    plt.cla()
    prediction = torch.max(prediction, 1)[1]
    pred_y = prediction.data.numpy().squeeze()
    target_y = y.data.numpy()
    plt.scatter(x.data.numpy()[:, 0], x.data.numpy()[:, 1], c=pred_y, s=100, lw=0, cmap='RdYlGn')
    accuracy = float((pred_y == target_y).astype(int).sum()) / float(target_y.size)
    plt.text(-1, -4.7, 'Time=%d Accuracy=%.2f' % (i, accuracy), fontdict={'size': 15, 'color': 'red'})
    plt.pause(0.1)
