from GradientBoosting import GradientBoosting

clf = GradientBoosting(regression=True)
clf.setTargets(["medv"])
clf.learn()
clf.infer()
