import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np



from torch.autograd import Variable, Function
import math



class Config(object):

    def __init__(self):
        self.model_name = 'TextCNN'
        self.dropout = 0.1                                            
        self.require_improvement = 1000                                 
        self.num_classes = 2                                      
        self.n_vocab = 30522                                                
        self.num_epochs = 20                                            
        self.batch_size = 128                                          
        self.pad_size = 32                                              
        self.learning_rate = 1e-3                                       
        self.embed = 768
        self.filter_sizes = (3,)                                   
        self.num_filters = 100                                          



class EncoderModel(nn.Module):
    def __init__(self):
        super(EncoderModel, self).__init__()
        config = Config()
        
        self.dropout = nn.Dropout(config.dropout)

        self.fc1 = nn.Linear(768, 768)
        self.fc2 = nn.Linear(768, config.num_classes)

        self.activation = nn.ReLU()


    def forward(self, out,var):



        if self.training:


            if var != 0.0:
                
            
                feat = self.fc1(out)
                feat = self.activation(feat)
                feat_n = feat+torch.empty(feat.shape[0],feat.shape[1]).normal_(mean=0,std=var).to(feat.device)

                out = self.fc2(feat_n)
            else:
                feat = self.fc1(out)
                feat = self.activation(feat)
                feat_n = self.dropout(feat)
                
                out = self.fc2(feat_n)
        else:
            feat = self.fc1(out)
            feat = self.activation(feat)
            feat = self.dropout(feat)
            out = self.fc2(feat)


        
        return [out, feat]
