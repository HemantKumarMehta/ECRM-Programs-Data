import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, integrate

df = pd.read_csv("/home/ecrm/WorkloadTraces/googlecluster11/clusterdata-2011-2/machine_events/part-00000-of-00001.csv", sep=",", usecols=[4, 5], names=['cpus','memory'], header=None)
cpusdata=df.cpus

kdecpus = stats.gaussian_kde(df.cpus.dropna())
xcpus=kdecpus.resample(100)*4
xcpus.round()/4

kdememory=stats.gaussian_kde(df.memory.dropna())
xmemory=kdememory.resample(100)*4
xmemory=xmemory.round()/4
xmemory=np.where(xmemory==0.0,0.125,xmemory)
xmemory
