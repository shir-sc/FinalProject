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


data = [2303, 0, 0, 0, 0, 1, 0, 10, 0, 0, 1, 601, 0, 0, 3030, 0, 7, 0, 0, 3, 6, 1, 0, 0, 0, 0, 7, 0, 967, 0, 0, 807, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6, 0, 3, 1, 0, 0, 56, 121, 0, 3, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 313, 0, 3138, 0, 1127, 0, 11067, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2148, 0, 33, 2, 0, 0, 4404, 0, 3, 0, 1, 0, 0, 0, 0, 0, 7559, 0, 0, 2, 0, 0, 2, 0, 1, 0, 0, 2, 1, 0, 10, 0, 0, 0, 0, 31, 0, 4466, 1, 54, 1, 1029, 0, 1, 0, 1572, 2427, 1, 821, 5, 339, 1, 0, 292, 0, 54, 141, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 4292, 9, 0, 0, 0, 1, 0, 0, 0, 11, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3, 0, 0, 0, 29, 0, 3, 0, 3, 0, 0, 413, 0, 0, 0, 2, 0, 0, 0, 0, 907, 0, 0, 0, 1, 0, 0, 684, 0, 0, 0, 0, 0, 4883, 0, 8725, 13, 4910, 2769, 0, 0, 0, 1775, 3042, 51, 3082, 1, 0, 1, 0, 1, 0, 0, 20145, 0, 3, 3, 1, 4, 0, 0, 0, 355, 0, 0, 1, 0, 0, 0, 0, 0, 1, 9, 0, 0, 32, 251, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 5153, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 4431, 0, 0, 0, 0, 0, 5, 1, 0, 1, 1, 0, 0, 0, 0, 7, 2, 0, 5, 5, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 31, 0, 2, 0, 0, 0, 0, 6, 102, 11, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 171, 0, 0, 0, 7, 0, 0, 0, 0, 280, 0, 0, 2, 3, 0, 7, 5, 0, 0, 1, 1, 9, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 7, 1, 1, 0, 0, 0, 71, 0, 8, 0, 0, 0, 2, 0, 711, 8, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 1393, 0, 45, 117, 0, 659, 0, 0, 0, 1384, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3, 0, 11, 0, 11, 530, 0, 7, 0, 120, 0, 15, 2, 2, 101, 1, 0, 67, 13, 0, 1, 2, 11, 0, 0, 2117, 0, 0, 0, 269, 0, 1, 0, 0, 0, 0, 0, 20, 5, 2898, 0, 2040, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 17, 0, 0, 285, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 3, 1, 0, 0, 285, 0, 0, 10, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 43, 0, 1988, 0, 0, 0, 9, 2, 0, 0, 0, 0, 3, 73, 0, 636, 0, 417, 0, 0, 1, 0, 21, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2992, 0, 12, 0, 0, 0, 81, 3, 0, 0, 0, 0, 4704, 0, 0, 0, 1, 1, 3, 124, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 57, 5, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 121, 21, 0, 0, 0, 13, 0, 9, 0, 65, 0, 0, 51, 0, 0, 1815, 2705, 0, 33, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 3, 0, 1, 0, 0, 15, 0, 0, 126, 3, 3, 0, 5269, 44, 224, 1233, 1300, 9, 2, 0, 5, 0, 1, 22, 0, 1, 2176, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 3, 13, 0, 0, 101, 0, 0, 0, 0, 0, 0, 511, 0, 0, 0, 0, 0, 13, 5, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6587, 4, 0, 0, 0, 1, 0, 0, 0, 2, 3522, 0, 1, 0, 0, 0, 0, 0, 0, 74, 0, 8, 5, 0, 0, 2, 0, 0, 0, 1, 0, 1, 1, 0, 0, 5, 1046, 813, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 1, 0, 12, 1, 5, 0, 23, 0, 2, 0, 0, 1, 4, 47, 0, 12, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 36, 0, 0, 0, 0, 3, 0, 2, 1, 1, 1, 0, 1, 0, 0, 0, 0, 5, 0, 0, 271, 0, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 968, 73, 0, 1, 6, 0, 0, 0, 0, 0, 0, 3179, 1, 0, 0, 0, 0, 0, 0, 15, 0, 0, 37, 8, 0, 0, 409, 0, 1, 16, 0, 0, 0, 0, 44, 0, 0, 9, 1, 52, 0, 0, 1, 0, 0, 0, 0, 19, 1, 4, 0, 0, 0, 146, 0, 8314, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8361, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 17544, 3, 4, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 5, 11, 0, 0]
for i in data:
    if i >1000:
        data.remove(i)
print (len(data))
p = 1/np.mean(data)
print (np.mean(data))
print p

print (np.max(data))
# bins = np.linspace(0, 100,1000)
# fitted_data = scipy.stats.distributions.chi2.pdf(bins, p)
plt.hist(data, density=True)
# # plt.plot(bins, fitted_data, 'r-')
plt.show()



# Theoretical distrebution
fig, ax = plt.subplots(1, 1)

mean, var, skew, kurt = geom.stats(p, moments='mvsk')
print (mean)
print (var)
print (skew)
print (kurt)

x = np.arange(geom.ppf(0.00001, p),geom.ppf(0.99999, p))
print x
ax.plot(x, geom.pmf(x, p), 'bo', ms=8, label='geom pmf')
ax.vlines(x, 0, geom.pmf(x, p), colors='b', lw=5, alpha=0.5)
plt.show()