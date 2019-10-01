#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:23:08 2019

@author: zhongjiulu
"""
from sklearn.cluster import KMeans
import pandas as pd

X_all = pd.read_csv('EnglishPlayers.csv')
#just the attributes (Excludes name and url). 
#We don't want to cluster players based on name and url.
X = X_all.iloc[:,2:]

from sklearn.cluster import KMeans

#Runs kmeans
kmeans = KMeans(n_clusters=4, random_state=3425).fit(X)

#adds the cluster number as a new column to the dataframe
X_all["cluster_nr"] = kmeans.labels_

# We'll first look how many members there are per cluster. 
# We can see thatn clusters 0, 1 and 3 have over 120 players; however, cluster 2 has only 35.

num_players_per_cluster = X_all.groupby(['cluster_nr']).count()

"""
We'll now look into every attribute for each cluster and create a description, 
hoping that we're able to find a right label based on the clusters' charactersitics.
"""

#calculates the mean of every column
total_mean = X_all.mean()
total_mean = total_mean.to_frame().transpose()

#calculates the average for every attribute column (e.g. Crossing) based on the cluster (called 0, 1, 2, 3)
all_mean_values = X_all.groupby(['cluster_nr']).mean()
#adds the average of every column to the dataframe
all_mean_values = all_mean_values.append(total_mean)


#views first 12 columns. the first 4 rows are the 4 clusters.  
#The last row represents the mean, independently of the cluster.
all_mean_values.iloc[:,0:12] 

all_mean_values.iloc[:,12:24] 