import numpy as np


class BagLearner(object):

    def __init__(self, learner, kwargs, bags=20, boost = False, verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []

    def author(self):
        return 'wli626' # replace tb34 with your Georgia Tech username

    def add_evidence(self, X, y):

        for i in range(0, self.bags):
            # sampling with replacement to get a bag of data
            sample = np.random.choice(a=X.shape[0], size=y.shape[0], replace=True)  # get 60% data for sample
            X_bag = X[sample]
            y_bag = y[sample]

            # Each bag of data corresponds to a learner
            learner = self.learner(**self.kwargs)
            learner.add_evidence(X_bag, y_bag)
            self.learners.append(learner)

    def query(self, points):


        y_hat = []
        for learner in self.learners:
            y_hat.append(learner.query(points))

        # take the average of predictions
        return np.mean(y_hat, axis=0)


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
