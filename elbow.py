#!/usr/bin/env python
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
#from mpl_toolkits.mplot3d import Axes3D
import glob

#import dask.dataframe as dd
#df = pd.read_csv("/media/sf_ubuntuSharing/googlecluster11/clusterdata-2011-2/job_events/part-00000-of-00500.csv.gz", sep=",", header=None)
#alldata = dd.read_csv("/home/ecrm/WorkloadTraces/1EucalyptusIaaS/DS*.csv", sep=",",names=['event','timestamp','instanceid','node-name','corecount'], header=None)
#df=alldata.iloc[:,4]


df=pd.concat([pd.read_csv(f, low_memory=True , sep=",",names=['event','timestamp','instanceid','node-name','corecount'], header=None) for f in glob.glob('/home/ecrm/WorkloadTraces/1EucalyptusIaaS/DS*.csv')], ignore_index = True)

a=df.corecount.values.reshape(-1,1)
wcss = []
for i in range(1, 10):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(a)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 10), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()





#kmeans = KMeans(n_clusters=8, init='k-means++', max_iter=10, n_init=4, random_state=0)
#pred_y = kmeans.fit_predict(df)
#df = df.compute()

#fig=plt.figure()
#ax = fig.add_subplot(111, projection = '3d')
#ax.scatter(df.iloc[:,0], df.iloc[:,1],df.iloc[:,2])
#ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], s=300, c='red')
#ax.show()


#plt.scatter(df.iloc[:,0].dropna(), df.iloc[:,1].dropna(),df.iloc[:,2].dropna(),df.iloc[:,3].dropna(),df.iloc[:,4].dropna())
#plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], kmeans.cluster_centers_[:, 3], kmeans.cluster_centers_[:, 4], s=300, c='red')
#plt.show()



