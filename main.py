from GradientBoosting import GradientBoosting

clf = GradientBoosting(regression=True)
clf.setTargets(["medv"])
clf.learn(loss = "Huber") #loss can be either "Huber", "LAD" or "LS"
clf.infer()
