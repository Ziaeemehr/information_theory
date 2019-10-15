import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mutual_info_score


def shan_entropy(c):
    c_normalized = c / float(np.sum(c))
    c_normalized = c_normalized[np.nonzero(c_normalized)]
    H = -sum(c_normalized * np.log2(c_normalized))
    return H


def calc_MI(X, Y, bins=None):

    c_XY = np.histogram2d(X, Y, bins)[0]
    c_X = np.histogram(X, bins)[0]
    c_Y = np.histogram(Y, bins)[0]

    H_X = shan_entropy(c_X)
    H_Y = shan_entropy(c_Y)
    H_XY = shan_entropy(c_XY)

    MI = H_X + H_Y - H_XY
    return MI


def calc_MI_sklearn(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi


A = np.array([[2.0,  140.0,  128.23, -150.5, -5.4],
              [2.4,  153.11, 130.34, -130.1, -9.5],
              [1.2,  156.9,  120.11, -110.45, -1.12]])

# bins = 5  # ?
# n = A.shape[1]
# matMI = np.zeros((n, n))
# for ix in np.arange(n):
#     for jx in np.arange(ix+1, n):
#         matMI[ix, jx] = calc_MI(A[:, ix], A[:, jx], bins)


# print(matMI)

x = np.random.normal(0, 1, 100000)
y = 2.0 * x * np.random.rand(100000) - 0.5

# y = np.random.normal(0, 1, 100000)

rho = pearsonr(x, y)[0]
print(rho)
print(-0.5*np.log2(1-rho*rho))
print(calc_MI_sklearn(x, y, 100))
# print(calc_MI(x, y, 5))
