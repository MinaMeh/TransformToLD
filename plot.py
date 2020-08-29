"""
===============================
Legend using pre-defined labels
===============================

Defining legend labels with plots.
"""


import numpy as np
import matplotlib.pyplot as plt


def plot_with_x(x, x_label, extract, preprocess, mapping, convert, total, title, legend_pos='upper right'):
    # Make some fake data.
    # Create plots with pre-defined labels.
    fig, ax = plt.subplots()
    ax.plot(x, extract, 'r', label='Temps d\'extraction', marker='o')
    ax.plot(x, preprocess, 'b', label='Temps de prétraitement', marker='o')
    ax.plot(x, mapping, 'g', label='Temps d\'alignement', marker='o')
    ax.plot(x, convert, 'm', label='Temps de conversion', marker='o')
    ax.plot(x, total, 'c', label='Temps total d\'exécution', marker='o')
    plt.set_cmap('Paired')

    legend = ax.legend(loc=legend_pos)
    plt.grid(b=True, color='#666666', linestyle='dotted')
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    ax.set_ylabel('Temps d\'éxecution (s)')
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.show()


def plot_for_nb_triplets(x, x_label, y):
    fig, ax = plt.subplots()
    ax.plot(x, y, 'r', marker='o')
    plt.set_cmap('Paired')
    legend = ax.legend(loc='upper left')
    plt.grid(b=True, color='#666666', linestyle='dotted')
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    ax.set_ylabel('Nombre de triplets')
    ax.set_xlabel(x_label)
    ax.set_title(
        'Nombre de triplets en fonction du nombre de phrases')
    plt.show()


taille = [0.5, 7.4, 39.6, 100]
nb_phrases = [4, 57, 387, 1412]
extract = [200, 1.93, 5.11, 12.67]
preprocess = [3.77, 42.78, 311.71, 1953.23]
mapping = [17.10, 88.14, 480.92, 954.3]
convert = [0.01, 0.02, 0.01, 1.2]
total = [21.71, 132.85, 797.65, 2908.59]

plot_with_x(taille, 'Taille du fichier (kB)', extract,
            preprocess, mapping, convert, total, 'le temps d\'exécution en fonction de la taille du fichier', legend_pos="upper left")
nb_triplets = [6, 107, 661, 1542]
plot_for_nb_triplets(
    taille, 'Nombre de phrases du fichier', nb_triplets)
