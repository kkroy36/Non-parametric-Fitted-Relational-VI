import matplotlib.pyplot as plt

inferred_values = None
true_values = None

with open("inferred_values0.9.txt") as fp:
    lines = fp.read().splitlines()
    inferred_values = [float(item) for item in lines]


with open("true_values0.9.txt") as fp:
    lines = fp.read().splitlines()
    true_values = [float(item) for item in lines]

    
red = plt.plot(inferred_values,color='r')
green = plt.plot(true_values,color='g')
plt.ylabel('Values 0.9')
plt.legend([red,green])
plt.show()
