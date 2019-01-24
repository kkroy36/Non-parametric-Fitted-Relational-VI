import matplotlib.pyplot as plt

inferred_values = None
true_values = None

with open("inferred_values.txt") as fp:
    lines = fp.read().splitlines()
    inferred_values = [float(item) for item in lines]

with open("true_values.txt") as fp:
    lines = fp.read().splitlines()
    true_values = [float(item) for item in lines]
    
plt.plot(inferred_values,color='r')
plt.plot(true_values,color='g')
plt.ylabel('Values')
plt.show()
