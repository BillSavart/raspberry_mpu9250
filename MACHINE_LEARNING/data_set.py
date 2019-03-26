import torch
from torch.autograd import Variable
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
root="./"
count = 1

# -----------------ready the dataset--------------------------
def default_loader(path):
    print("return loader\n")
    return Image.open(path)    
    #return Image.open(path).convert('RGB')
class MyDataset(torch.utils.data.Dataset): 
    def __init__(self,txt, transform=None, target_transform=None): 
        #print("super init\n")
        super(MyDataset,self).__init__()
        #print("data set init\n")
        fh = open(txt, 'r') 
        imgs = []                      
        for line in fh:                
            line = line.rstrip()       
            words = line.split()   
            imgs.append((words[0],int(words[1]))) 
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
 
    def __getitem__(self, index):
        global count
       # print("get item ",count,"\n")
        count = count+1    
        fn, label = self.imgs[index] 
        #img = Image.open(root+fn)
        img = Image.open(root+fn).convert('RGB') 
 
        if self.transform is not None:
            img = self.transform(img) 
        return img,label  
 
    def __len__(self):
        print("return len")
        return len(self.imgs)


train_data=MyDataset(txt=root+'dataSetForm.txt', transform=transforms.ToTensor())
test_data=MyDataset(txt=root+'dataSetForm.txt', transform=transforms.ToTensor())
train_loader = DataLoader(dataset=train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(dataset=test_data, batch_size=64)


#-----------------create the Net and training------------------------

class Net(torch.nn.Module):
    def __init__(self):
        #print("Super Net init\n")
        super(Net, self).__init__()
        #print("Net init\n")
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(3, 3, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2))
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(3, 3, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(3, 3, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)
        )
        self.dense = torch.nn.Sequential(
            torch.nn.Linear(24570, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 10)
        )

    def forward(self, x):
        #print("forward net\n")
        conv1_out = self.conv1(x)
       # print("con1 finish\n")
        conv2_out = self.conv2(conv1_out)
        #print("con2 finish\n")
        conv3_out = self.conv3(conv2_out)
        #print("con3 finish\n")
        res = conv3_out.view(conv3_out.size(0), -1)
        #print("ready get out\n")
        out = self.dense(res)
        return out


model = Net()
#print(model)

#print("\n")
#print(Net)

optimizer = torch.optim.Adam(model.parameters())
loss_func = torch.nn.CrossEntropyLoss()

print("Start Training\n")

for epoch in range(10):
    print('epoch {}'.format(epoch + 1))
    # training-----------------------------
    train_loss = 0.
    train_acc = 0.
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = Variable(batch_x), Variable(batch_y)
        out = model(batch_x)
        loss = loss_func(out, batch_y)
        train_loss += loss.data
        pred = torch.max(out, 1)[1]
        train_correct = (pred == batch_y).sum()
        train_acc += (train_correct.data)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print('Train Loss: {:.6f}, Acc: {:.6f}'.format(train_loss / (len(
        train_data)), train_acc / (len(train_data))))

    # evaluation--------------------------------
    model.eval()
    eval_loss = 0.
    eval_acc = 0.
    for batch_x, batch_y in test_loader:
        batch_x, batch_y = Variable(batch_x, volatile=True), Variable(batch_y, volatile=True)
        out = model(batch_x)
        loss = loss_func(out, batch_y)
        eval_loss += loss.data
        pred = torch.max(out, 1)[1]
        num_correct = (pred == batch_y).sum()
        eval_acc += (num_correct.data)
    print('Test Loss: {:.6f}, Acc: {:.6f}'.format(eval_loss / (len(
        test_data)), eval_acc / (len(test_data))))
