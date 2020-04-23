import pandas as pd
import matplotlib.pyplot as plt

N = 100 #Nombre d'échantillons à prendre en compte

def mean(path):
    data_1a = pd.read_csv(path+'/data1.csv').tail(N)
    data_1b = pd.read_csv(path+'/data2.csv').tail(N)

    mean_1a = sum(data_1a['sender_rssi']) / N
    mean_1b = sum(data_1b['sender_rssi']) / N

    return (mean_1a, mean_1b)

def trace_means(paths):
    means_node_1 = []
    means_node_2 = []

    dist = 9
    distance = []

    for path in paths:
        means_node_1.append(mean(path)[0])
        means_node_2.append(mean(path)[1])

    for i in range(len(paths)):
        distance.append(dist)
        dist += 3
    print("dist", distance)

    plt.plot(distance, means_node_1, label='Sender 1')
    plt.plot(distance, means_node_2, label='Sender 2')
    plt.xlabel('Distance (m)')
    plt.ylabel('moyenne RSSI sur 100 paquets')
    plt.legend(loc='upper left')
    plt.tight_layout()

    plt.show()
    
if __name__ == '__main__':
    trace_means(['./data/E1', './data/E2', './data/E3', './data/E4'])
