import pandas as pd
import matplotlib.pyplot as plt

N = 100 #Nombre d'échantillons à prendre en compte


def mean(path):
    data_1a = pd.read_csv(path+'/data1.csv').tail(N)
    data_1b = pd.read_csv(path+'/data2.csv').tail(N)

    mean_1a = sum(data_1a['sender_rssi']) / N
    mean_1b = sum(data_1b['sender_rssi']) / N

    return (mean_1a, mean_1b)

#DO: calcule la moyenne des échantillons pour chaque expérience, et trace la courbe du rssi moyen en fonction de la distance entre les noeux
#en associant chaque donnée à une valeur de distance
#INPUT: Prend un tableau de chaines de caractères avec le path vers chacun des répertoires contenant les données (data1.csv et data2.csv)
#d'une expérience, classés par ordre de distance montante (paths[0]=distance9, path[1]=distance12, etc...)
def trace_means_dist(paths):
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

#DO: calcule la moyenne des échantillons pour chaque expérience, et trace la courbe du rssi moyen en fonction de la puissance d'émission
#en associant chaque donnée à une valeur de puissance
#INPUT: Prend un tableau de chaines de caractères avec le path vers chacun des répertoires contenant les données (data1.csv et data2.csv)
#d'une expérience, classés par ordre de puissance montante (paths[0]=power3, path[1]=power6, etc...)
def trace_means_pow(paths):
    means_node_1 = []
    means_node_2 = []

    pow = 3
    power = []

    for path in paths:
        means_node_1.append(mean(path)[0])
        means_node_2.append(mean(path)[1])
    print('moyennes')
    print(means_node_1)
    print(means_node_2)

    for i in range(len(paths)):
        power.append(pow)
        pow += 3
    print("power", power)

    plt.plot(power, means_node_1, label='Sender 1')
    plt.plot(power, means_node_2, label='Sender 2')
    plt.xlabel('Puissance d\'émission (dB)')
    plt.ylabel('moyenne RSSI sur 100 paquets')
    plt.legend(loc='upper left')
    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    trace_means_pow(['./data/E5/E51', './data/E5/E52'])
