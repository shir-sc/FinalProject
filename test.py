import numpy as np
import tile_coding
import scipy
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import geom



# state_size= (4,2)
# print(state_size+(len([1,2,3,4,5,6]),))
# print('Q_table')
# Q_table= np.zeros(shape=(state_size+(len([1,2,3,4,5,6]),)))
# print(Q_table)

# feature_ranges = [[0, 180], [0, 90]]  # 2 features
# number_tilings = 3
# bins = [[4, 2], [4, 2], [4, 2]]  # each tiling has a 4*2 grid
# offsets = [[0, 0], [15, 15], [30, 30]]  # each tiling has different offset from the 0,0
# tilings = tile_coding.create_tilings(feature_ranges, number_tilings, bins, offsets)
#
#
# state_sizes = [tuple(len(splits)+1 for splits in tiling) for tiling in tilings]
# print (state_sizes)
# print('Q_tables')
# Q_tables= [np.zeros(shape=(state_size+(len([1,2,3,4,5,6]),)))for state_size in state_sizes]
# print (Q_tables)


# actions=range(6)
# print(actions)
# state = [(7,8),1,1,1]
# print ((state[0])[1])

#
# # np.expand.grid(0:5,0:8,0:3,0:7,0:2)
# Rono = np.array(np.meshgrid([1, 2, 3, 4, 5,6], [1,2,3,4,5,6,7,8,9], [0,1,2,3],[0,1,2,3,4,5,6,7],[0,1,2])).T.reshape(-1,5)
# print(len(Rono))
# print (Rono)

# Rono = np.array(np.meshgrid((np.array(np.meshgrid([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6,7,8])).T.reshape(-1,2)), [0,1,2,3],[0,1,2,3,4,5,6,7],[0,1,2])).T.reshape(-1,4)
# print(len(Rono))
# print (Rono)

# print (len(np.array(np.meshgrid([0, 1, 2, 3], [0, 1],[0, 1, 2, 3], [0, 1],[0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7],
#                                   [0, 1, 2])).T.reshape(-1, 9)))

#
# state = [(0,1),2,3,4]
# NewState = ((state[0])[0],(state[0])[1],state[1],state[2],state[3])
# print(NewState)
# smart = [(item for t in state[0] for item in t],state[1],state[2],state[3])

# # Python code to convert list of tuples into list
#
# # List of tuple initialization
# lt = [('Geeks', 2), ('For', 4), ('geek', '6')]
#
# # using list comprehension
# out = [item for t in lt for item in t]
#
# # printing output
# print(out)

# offsets = [[i, j] for i, j in zip(np.linspace(0, 180, 3), np.linspace(0, 90, 3))]
# print (offsets)
#
# bins = [[16, 16] for _ in range(3)]
# print(bins)

# print((-5)%0)
data= [[100, 0, 0, 3, 53, 3, 1, 0, 0, 1, 2, 13, 0, 15, 1, 0, 0, 100, 1, 7, 0, 0, 0, 100, 0, 0, 0, 0, 1, 7, 1, 0, 41, 1, 1, 81, 0, 29, 6, 0, 11, 0, 0, 0, 1, 1, 0, 0, 0, 0, 100, 0, 0, 0, 3, 0, 0, 2, 19, 5, 0, 0, 99, 100, 0, 0, 1, 0, 0, 0, 41, 0, 0, 100, 100, 0, 0, 0, 1, 100, 1, 0, 0, 0, 0, 0, 0, 0, 2, 100, 0, 43, 0, 100, 0, 0, 3, 0, 0, 0]
,[100, 0, 0, 3, 53, 3, 1, 0, 0, 1, 2, 13, 0, 15, 1, 0, 0, 100, 1, 7, 0, 0, 0, 100, 0, 0, 0, 0, 1, 7, 1, 0, 41, 1, 1, 81, 0, 29, 6, 0, 11, 0, 0, 0, 1, 1, 0, 0, 0, 0, 100, 0, 0, 0, 3, 0, 0, 2, 19, 5, 0, 0, 99, 100, 0, 0, 1, 0, 0, 0, 41, 0, 0, 100, 100, 0, 0, 0, 1, 100, 1, 0, 0, 0, 0, 0, 0, 0, 2, 100, 0, 43, 0, 100, 0, 0, 3, 0, 0, 0]
,[100, 0, 0, 3, 53, 3, 1, 0, 0, 1, 2, 13, 0, 15, 1, 0, 0, 100, 1, 7, 0, 0, 0, 100, 0, 0, 0, 0, 1, 7, 1, 0, 41, 1, 1, 81, 0, 29, 6, 0, 11, 0, 0, 0, 1, 1, 0, 0, 0, 0, 100, 0, 0, 0, 3, 0, 0, 2, 19, 5, 0, 0, 99, 100, 0, 0, 1, 0, 0, 0, 41, 0, 0, 100, 100, 0, 0, 0, 1, 100, 1, 0, 0, 0, 0, 0, 0, 0, 2, 100, 0, 43, 0, 100, 0, 0, 3, 0, 0, 0]
,[100, 0, 0, 3, 53, 3, 1, 0, 0, 1, 2, 13, 0, 15, 1, 0, 0, 100, 1, 7, 0, 0, 0, 100, 0, 0, 0, 0, 1, 7, 1, 0, 41, 1, 1, 81, 0, 29, 6, 0, 11, 0, 0, 0, 1, 1, 0, 0, 0, 0, 100, 0, 0, 0, 3, 0, 0, 2, 19, 5, 0, 0, 99, 100, 0, 0, 1, 0, 0, 0, 41, 0, 0, 100, 100, 0, 0, 0, 1, 100, 1, 0, 0, 0, 0, 0, 0, 0, 2, 100, 0, 43, 0, 100, 0, 0, 3, 0, 0, 0]
]

# pX2oneStep = 1/np.mean(data[1])
# print ('pX2oneStep', pX2oneStep)
# pX2twoSteps = 1/np.mean(data[3])
# print ('pX2twoSteps', pX2twoSteps)
#
# bins = np.linspace(0, 100,100)
# plt.hist(data[1], density=True, bins=bins)
# plt.show()

fig, ax = plt.subplots(1, 1)

data[1]= filter(lambda number: number != 100, data[1])
print(data[1])
print(np.mean(data[1]))


_, bins, _ = ax.hist(data[1],density=True, bins=100)
# values,unique_counts = np.unique(data[1], return_counts= True)
# unique_counts = unique_counts.astype(np.float32)
# probability_per_num_mesirot = unique_counts/len(data[1])
pX2oneStep = 1/np.mean(data[1])
# best_fit_line = scipy.stats.geom.pmf(bins,pX2oneStep)
# plt.plot(bins, best_fit_line)
# plt.show()

# fig, ax = plt.subplots(1, 1)
ax.set_title('Geometric Distribution')
ax.set_xlabel('Num Mesirot')
ax.set_ylabel('Probability')
x = np.arange(0,100)
dist = ax.plot(geom.pmf(x, pX2oneStep), 'r-', ms=8, label='geom pmf')
# plt.plot(bins, dist)
plt.show()
# # plt.plot(bins, fitted_data, 'r-')
# Theoretical distrebution
#
# print(fig)
# print(ax)
# # mean, var, skew, kurt = geom.stats(pX2oneStep, moments='mvsk')
# # x = np.arange(0,100)
# # print x
# # ax.plot(geom.pmf(x, pX2oneStep), 'bo', ms=8, label='geom pmf')
# # ax.vlines(x, 0, geom.pmf(x, pX2oneStep), colors='b', lw=5, alpha=0.5)
# plt.show()