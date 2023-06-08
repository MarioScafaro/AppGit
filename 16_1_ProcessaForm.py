import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
lista = []


class Indumento:
    def __init__(self, tipologia, marca, prezzo):
        self.tipologia = tipologia
        self.marca = marca
        self.prezzo = prezzo

    def __str__(self):
        return f"tipologia={self.tipologia}, marca={self.marca}, prezzo={self.prezzo}"


@app.route('/')
def home():
    return render_template("homepage.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form.get('nm')
        if user == "Gioiello":
            p1 = Indumento("Gioiello", "gucci", 250)
        elif user == "Maglia":
            p1 = Indumento("Maglia", "Versace", 70)
        elif user == "Zaino":
            p1 = Indumento("Zaino", "Adidas", 35)
        elif user == "Pantalone":
            p1 = Indumento("Pantalone", "Nike", 50)
        elif user == "Scarpa":
            p1 = Indumento("Scarpa", "Nike", 80)
        elif user == "Accessorio":
            p1 = Indumento("Accessorio", "Ok", 70)
        else:
            return redirect(url_for('home'))

        lista.append(p1)
        return redirect(url_for('success', name=user))
    else:
        return redirect(url_for('home'))


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/categoria', methods=['POST', 'GET'])
def categoria():
    categories = {}
    for indumento in lista:
        tipologia = indumento.tipologia
        if tipologia in categories:
            categories[tipologia] += 1
        else:
            categories[tipologia] = 1

    # Cancella eventuali grafici precedenti
    for filename in os.listdir('static'):
        if filename.endswith('.png'):
            os.remove(os.path.join('static', filename))

    # Prepara i dati per il grafico a torta
    labels = list(categories.keys())
    values = list(categories.values())

    # Genera il grafico a torta
    plt.figure(figsize=(6, 6))
    plt.subplot(211)
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')  # Assicura un aspetto circolare al grafico
    plt.title('Grafico a torta')

    # Prepara i dati per l'istogramma
    labels_istogramma = list(categories.keys())
    values_istogramma = list(categories.values())

    # Genera l'istogramma
    plt.subplot(212)
    plt.bar(labels_istogramma, values_istogramma)
    plt.xlabel('Nome')
    plt.ylabel('Conteggio')
    plt.title('Istogramma')

    # Calcola la retta di regressione lineare
    x = np.arange(len(values_istogramma))
    y = np.array(values_istogramma)
    slope, intercept = np.polyfit(x, y, 1)
    regression_line = slope * x + intercept

    # Aggiungi la previsione lineare al grafico a torta e all'istogramma
    plt.subplot(211)
    plt.plot(x, regression_line, color='red', label='Previsione lineare')
    plt.legend()

    plt.subplot(212)
    plt.plot(x, regression_line, color='red', label='Previsione lineare')
    plt.legend()

    # Salva il grafico come immagine
    graph_path = 'static/graph.png'  # Percorso dell'immagine di output
    plt.savefig(graph_path)
    plt.close()  # Chiudi il grafico per liberare la memoria

    return render_template("categoria.html", graph_path=graph_path, lista=lista)


if __name__ == '__main__':
    app.run()
