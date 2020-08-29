"""
===============================
Legend using pre-defined labels
===============================

Defining legend labels with plots.
"""


import numpy as np
import matplotlib.pyplot as plt


def plot_with_x(x, x_label, total, title, legend_pos='upper right', color="b"):
    # Make some fake data.
    # Create plots with pre-defined labels.
    fig, ax = plt.subplots()
    ax.plot(x, total, color, marker='o')
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


taille = [1.4, 24, 162, 3100]
nb_tables = [2, 8, 13, 540]
nb_paragraphs = [3, 7, 10, 286]
total = [2.5, 5.64, 16.7, 421.9]

plot_with_x(taille, 'Taille du fichier (kB)', total,
            'le temps d\'exécution en fonction de la taille du fichier', legend_pos="upper left", color="g")
plot_with_x(nb_tables, 'Nombre des tableaux', total,
            'le temps d\'exécution en fonction du nombre des tableaux', legend_pos="upper left", color="b")
plot_with_x(nb_paragraphs, 'Nombre des paragraphes', total,
            'le temps d\'exécution en fonction du nombre des paragraphes', legend_pos="upper left", color='c')

nb_triplets = [6, 107, 661, 1542]
plot_for_nb_triplets(
    taille, 'Nombre de phrases du fichier', nb_triplets)
