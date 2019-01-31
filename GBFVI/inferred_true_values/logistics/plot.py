import matplotlib.pyplot as plt

inferred_values90 = None
true_values90 = None

inferred_values70 = None
true_values70 = None

inferred_values50 = None
true_values50 = None

def diff(l1,l2):
    x = [abs(l1[i]-l2[i]) for i in range(len(l1))]
    return (x)

with open("inferred_values0.9.txt") as fp:
    lines = fp.read().splitlines()
    inferred_values90 = [float(item) for item in lines]


with open("true_values0.9.txt") as fp:
    lines = fp.read().splitlines()
    true_values90 = [float(item) for item in lines]

with open("inferred_values0.7.txt") as fp:
    lines = fp.read().splitlines()
    inferred_values70 = [float(item) for item in lines]


with open("true_values0.7.txt") as fp:
    lines = fp.read().splitlines()
    true_values70 = [float(item) for item in lines]

with open("inferred_values0.5.txt") as fp:
    lines = fp.read().splitlines()
    inferred_values50 = [float(item) for item in lines]


with open("true_values0.5.txt") as fp:
    lines = fp.read().splitlines()
    true_values50 = [float(item) for item in lines]

    
diff90 = diff(inferred_values90,true_values90)
diff70 = diff(inferred_values70,true_values70)
diff50 = diff(inferred_values50,true_values50)

#nine = plt.plot(diff90,color='g',label = 'error (0.9)')
#seven= plt.plot(diff70,color='g',label = 'error (0.7)')
five = plt.plot(diff50,color='g',label = 'error (0.5)')

plt.ylabel('Errors')
plt.legend()
plt.show()
