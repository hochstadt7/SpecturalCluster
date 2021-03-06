import DataGen
import GraphGen
from sklearn.cluster import KMeans
import argparse

from GramSchmidt import *
#from KMeans import *
from Qr import *
from EigenGapSelection import *
from matplotlib import pyplot as plt
import section_four as foury

parser = argparse.ArgumentParser()
parser.add_argument("k", type=int)
parser.add_argument("n", type=int)
parser.add_argument("Random", type=bool)
args = parser.parse_args()
k = int(args.k)
n = int(args.n)
d = 2

data = DataGen.generate_data(n, d, k)

clusters = KMeans(n_clusters=k).fit(data)
print(clusters.labels_)
colors = ['r', 'g', 'b', 'y', 'c', 'm']
fig, ax = plt.subplots()
for i in range(k):
    points = np.array([data[j] for j in range(len(data)) if clusters.labels_[j] == i])
    ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
plt.savefig('plot_kmeans.pdf')


weights = GraphGen.get_weight_matrix(n, data)
diagonal = GraphGen.get_diagonal_degree_matrix(n, weights)
laplacian = GraphGen.get_laplacian_matrix(n, diagonal, weights)

ret=foury.calc_eigen_values_vectors(laplacian.tolist(),n)
print('woowwow')

#e_vectors, e_values_diag = qr_iter(laplacian, n)
e_values = np.diagonal(ret[1])
k, vectors = eigen_gap_heuristic(ret[0], e_values, n)
clusters = KMeans(n_clusters=k).fit(vectors.tolist())
print(clusters.labels_)
colors = ['r', 'g', 'b', 'y', 'c', 'm']
fig, ax = plt.subplots()
for i in range(k):
    points = np.array([data[j] for j in range(len(data)) if clusters.labels_[j] == i])
    ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
plt.savefig('plot_spectral.pdf')
# fig, ax = plt.subplots()
# for i in range(k):
#     points = np.array([vectors[j] for j in range(len(vectors)) if clusters.labels_[j] == i])
#     ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
# plt.savefig('plot_spectral1.pdf')
# fig, ax = plt.subplots()
# for i in range(k):
#     points = np.array([vectors[j] for j in range(len(vectors)) if clusters.labels_[j] == i])
#     ax.scatter(points[:, 0], points[:, 2], s=7, c=colors[i])
# plt.savefig('plot_spectral2.pdf')
# fig, ax = plt.subplots()
# for i in range(k):
#     points = np.array([vectors[j] for j in range(len(vectors)) if clusters.labels_[j] == i])
#     ax.scatter(points[:, 1], points[:, 2], s=7, c=colors[i])
# plt.savefig('plot_spectral3.pdf')

