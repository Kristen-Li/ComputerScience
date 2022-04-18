"""
Random Tree Leaner ML4T Spring 2022 by Wanjun Li
"""

import numpy as np


class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None
        pass

    def author(self):
        return 'wli626' # replace tb34 with your Georgia Tech username

    def buildTree(self, X, y):
        # when the number of observations is less than LE the leaf_size, they will all be included in a leaf.
        # when there's only one value left for y, splitting will result in a 0 element tree, hence no splitting
        if X.shape[0] <= self.leaf_size or np.std(y) == 0:
            return np.array([[-1,np.mean(y), -1, -1]]) # -1 represents a leaf node
        idx = np.random.randint(X.shape[1])
        split_feature = X[:,idx]
        split_point = np.median(split_feature)
        # cannot have a 0 element tree
        if np.all(split_feature <= split_point):
            return np.array([[-1,np.mean(y),-1,-1]])
        r_idx = split_feature > split_point
        l_idx = split_feature <= split_point

        r_X = X[r_idx]
        r_y = y[r_idx]
        l_X = X[l_idx]
        l_y = y[l_idx]

        l_tree = self.buildTree(l_X,l_y)
        r_tree = self.buildTree(r_X,r_y)
        root = np.array([[idx, split_point, 1, l_tree.shape[0] + 1]])

        return np.vstack((root,l_tree, r_tree))

    def add_evidence(self, X, y):
        self.tree = self.buildTree(X,y)

    def query(self, points):
        y_hat = []
        for point in points:
            y_hat.append(self.get_pred(point))
        return np.asarray(y_hat)

    def get_pred(self,point):
        node = 0
        y_hat = 0
        flag = True
        while flag:
            check = int(self.tree[node, 0])
            if check == -1:
                y_hat = self.tree[node, 1]
                flag = False
            else:
                split_point = self.tree[node, 1]
                if point[check] <= split_point:
                    node += int(self.tree[node, 2]) # search left tree
                else:
                    node += int(self.tree[node, 3]) # search right tree
        return y_hat

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")