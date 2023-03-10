import torch
import torch.utils.data
import os
import logging
import numpy as np

class MLZDataset(torch.utils.data.Dataset):
    def __init__(self,window,lag,data_name='2012',set_type='train',data_dir='./data'):
        assert type(set_type) == type('str')
        self.window = window
        self.lag = lag
        self.data_dir = data_dir
        self.set_type = set_type
        file_path = os.path.join(data_dir, data_name, '{}_{}.txt'.format(data_name, set_type))
        rawdata = np.loadtxt(open(file_path), delimiter=',')
        self.len, self.var_num = rawdata.shape
        self.sample_num = max(self.len - self.window - self.lag + 1, 0)
        self.samples, self.labels = self.__getsamples(rawdata)
    def __getsamples(self, data):
        X = torch.zeros((self.sample_num, self.window, self.var_num))
        Y = torch.zeros((self.sample_num, 1, self.var_num))
        for i in range(self.sample_num):
            start = i
            end = i + self.window
            X[i, :, :] = torch.from_numpy(data[start:end, :])
            Y[i, :, :] = torch.from_numpy(data[end+self.lag-1, :])
        Y = torch.transpose(Y, 1, 2)
        return (X, Y)

    def __len__(self):
        return self.sample_num

    def __getitem__(self, idx):
        sample = [self.samples[idx, :, :], self.labels[idx, :, :]]
        return sample

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Test: data from .txt file')
    dataset = MLZDataset(window=24,lag=3,data_name='2012_15',set_type='train',data_dir='./data')
