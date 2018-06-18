import os
import torch
import numpy as np
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from IPython.core.debugger import Tracer
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import copy
from torch.autograd import grad
import time
from torchvision import datasets, transforms
from torch.autograd import Variable
import copy
import matplotlib
import operator
from BNN_Util import *
from BNN_Q_D import *
from BNN_Model_def import *
from BNN_Sampler import *
from BNN_training_func import *
from BNN_Dataloader import *

torch.set_default_tensor_type('torch.cuda.FloatTensor')



def ReadStoredSamples(FilePath):
    tensor_state_list=torch.load(FilePath)
    state_list_tmp=list(torch.split(tensor_state_list,1,dim=0))
    state_list=[]
    for i in state_list_tmp:
        state_list.append(torch.squeeze(i))
    return state_list



'''

For different tasks (Network Architecture Gen/ Sigmoid Gen), please change to corresponding folder, file name and act_func. The file should contain the samples drawn by the sampler. Same for other long_run_plot_ scripts.

'''


# act_func='ReLU'
# root_folder='./ReLU_Generalization_Long_Run/'

# File_Path_nnsghmc_list=['%slong_run_nnsghmc_1_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_2_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_3_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_4_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_5_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_6_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_7_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_8_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_9_broad_0.2_fd_0.18'%(root_folder),
#                 '%slong_run_nnsghmc_10_broad_0.2_fd_0.18'%(root_folder)
#                ]
# File_Path_sghmc_list=['%slong_run_sghmc_1'%(root_folder),
#                       '%slong_run_sghmc_2'%(root_folder),
#                       '%slong_run_sghmc_3'%(root_folder),
#                       '%slong_run_sghmc_4'%(root_folder),
#                       '%slong_run_sghmc_5'%(root_folder),
#                       '%slong_run_sghmc_6'%(root_folder),
#                       '%slong_run_sghmc_7'%(root_folder),
#                       '%slong_run_sghmc_8'%(root_folder),
#                       '%slong_run_sghmc_9'%(root_folder),
#                       '%slong_run_sghmc_10'%(root_folder)
#                      ]

# File_Path_sgld_list=['%slong_run_sgld_1_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_2_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_3_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_4_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_5_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_6_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_7_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_8_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_9_correct_noise_0.2'%(root_folder),
#                      '%slong_run_sgld_10_correct_noise_0.2'%(root_folder)
#                     ]






train_loader = datasets.MNIST('./BNN_MNIST/data/', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ]))
test_loader = datasets.MNIST('./BNN_MNIST/data/', train=False, transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ]))

train_X,train_Y,test_X,test_Y=SelectImage_All(train_loader,test_loader)
train_class=NewMNISTLoader(train_X,train_Y,flag_train=True)
test_class=NewMNISTLoader(test_X,test_Y,flag_train=False)

train_loader=DataLoader(train_class, batch_size=500,
                        shuffle=True)
test_loader=DataLoader(test_class,batch_size=500,shuffle=True)




MLP_mnist=BNN(dim=784,hidden=40,layer_num=3,dim_out=10,act_func=act_func)

length=len(File_Path_nnsghmc_list)
avg_time_nnsghmc=12000/12000
avg_time_sghmc=12000/12000
avg_time_sgld=12000/12000

Acc_sghmc_avg=[]
Acc_nnsghmc_avg=[]
Acc_SGLD_avg=[]
NLL_sghmc_avg=[]
NLL_nnsghmc_avg=[]
NLL_SGLD_avg=[]

for ind in range(length):
    print('Current ind:%s'%(ind+1))
    FilePath_nnsghmc=File_Path_nnsghmc_list[ind]
    FilePath_sghmc=File_Path_sghmc_list[ind]
    FilePath_sgld=File_Path_sgld_list[ind]
    
    state_list_nnsghmc=ReadStoredSamples(FilePath_nnsghmc)
    state_list_sghmc=ReadStoredSamples(FilePath_sghmc)
    state_list_sgld=ReadStoredSamples(FilePath_sgld)
    
    Acc_sghmc_list_comp,Acc_nnsghmc_list_comp,Acc_sgld_list_comp,NLL_sghmc_list_comp,NLL_nnsghmc_list_comp,NLL_sgld_list_comp,time_list_sghmc,time_list_nnsghmc,time_list_sgld=generate_accuracy(test_loader,MLP_mnist,state_list_sghmc,state_list_nnsghmc,state_list_sgld
                  ,interval=100,limit=120,avg_time_nnsghmc=avg_time_nnsghmc
                      ,avg_time_sghmc=avg_time_sghmc,avg_time_sgld=avg_time_sgld)
    
    
    Acc_sghmc_avg.append(Acc_sghmc_list_comp)
    Acc_nnsghmc_avg.append(Acc_nnsghmc_list_comp)
    Acc_SGLD_avg.append(Acc_sgld_list_comp)
    NLL_sghmc_avg.append(NLL_sghmc_list_comp)
    NLL_nnsghmc_avg.append(NLL_nnsghmc_list_comp)
    NLL_SGLD_avg.append(NLL_sgld_list_comp)
    
    
    
    
All_Acc_sghmc=np.stack(tuple(Acc_sghmc_avg),axis=0)
All_Acc_nnsghmc=np.stack(tuple(Acc_nnsghmc_avg),axis=0)
All_Acc_SGLD=np.stack(tuple(Acc_SGLD_avg),axis=0)
All_NLL_sghmc=np.stack(tuple(NLL_sghmc_avg),axis=0)
All_NLL_nnsghmc=np.stack(tuple(NLL_nnsghmc_avg),axis=0)
All_NLL_SGLD=np.stack(tuple(NLL_SGLD_avg),axis=0)


Acc_sghmc=np.mean(np.stack(tuple(Acc_sghmc_avg),axis=0),axis=0)
Acc_nnsghmc=np.mean(np.stack(tuple(Acc_nnsghmc_avg),axis=0),axis=0)
Acc_SGLD=np.mean(np.stack(tuple(Acc_SGLD_avg),axis=0),axis=0)
NLL_sghmc=np.mean(np.stack(tuple(NLL_sghmc_avg),axis=0),axis=0)
NLL_nnsghmc=np.mean(np.stack(tuple(NLL_nnsghmc_avg),axis=0),axis=0)
NLL_SGLD=np.mean(np.stack(tuple(NLL_SGLD_avg),axis=0),axis=0)

np.savetxt('%sAcc_Avg_sghmc_TEST'%(root_folder),Acc_sghmc)
np.savetxt('%sAcc_Avg_nnsghmc_TEST'%(root_folder),Acc_nnsghmc)
np.savetxt('%sAcc_Avg_sgld_TEST'%(root_folder),Acc_SGLD)

np.savetxt('%sNLL_Avg_sghmc_TEST'%(root_folder),NLL_sghmc)
np.savetxt('%sNLL_Avg_nnsghmc_TEST'%(root_folder),NLL_nnsghmc)
np.savetxt('%sNLL_Avg_sgld_TEST'%(root_folder),NLL_SGLD)





np.savetxt('%sAll_Acc_sghmc_TEST'%(root_folder),All_Acc_sghmc)
np.savetxt('%sAll_Acc_nnsghmc_TEST'%(root_folder),All_Acc_nnsghmc)
np.savetxt('%sAll_Acc_sgld_TEST'%(root_folder),All_Acc_SGLD)
np.savetxt('%sAll_NLL_sghmc_TEST'%(root_folder),All_NLL_sghmc)
np.savetxt('%sAll_NLL_nnsghmc_TEST'%(root_folder),All_NLL_nnsghmc)
np.savetxt('%sAll_NLL_sgld_TEST'%(root_folder),All_NLL_SGLD)




Acc_sghmc_std=np.std(np.stack(tuple(Acc_sghmc_avg),axis=0),axis=0)
Acc_nnsghmc_std=np.std(np.stack(tuple(Acc_nnsghmc_avg),axis=0),axis=0)
Acc_SGLD_std=np.std(np.stack(tuple(Acc_SGLD_avg),axis=0),axis=0)
NLL_sghmc_std=np.std(np.stack(tuple(NLL_sghmc_avg),axis=0),axis=0)
NLL_nnsghmc_std=np.std(np.stack(tuple(NLL_nnsghmc_avg),axis=0),axis=0)
NLL_SGLD_std=np.std(np.stack(tuple(NLL_SGLD_avg),axis=0),axis=0)


np.savetxt('%sAcc_Std_sghmc_TEST'%(root_folder),Acc_sghmc_std)
np.savetxt('%sAcc_Std_nnsghmc_TEST'%(root_folder),Acc_nnsghmc_std)
np.savetxt('%sAcc_Std_sgld_TEST'%(root_folder),Acc_SGLD_std)

np.savetxt('%sNLL_Std_sghmc_TEST'%(root_folder),NLL_sghmc_std)
np.savetxt('%sNLL_Std_nnsghmc_TEST'%(root_folder),NLL_nnsghmc_std)
np.savetxt('%sNLL_Std_sgld_TEST'%(root_folder),NLL_SGLD_std)





