import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from tela import is_dark_mode,mostrarCaixaDeTexto
import tkinter as tk
import json

labels = ['Poupança']
sizes = [200]
colors = ['#99ff99']
defice = 0

def salvarDados(fig,root,widgets):
    dados = {
        "labels": labels,
        "sizes": sizes,
        "colors": colors
    }
    mostrarCaixaDeTexto(fig,root,dados,widgets)



def setScreen (root):
    root.title("Expense Manager")

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    root.geometry(f"{screenWidth}x{screenHeight}")

    darkMode = is_dark_mode()
    bgColor = "#282828" if darkMode else "white"
    fgColor = "white" if darkMode else "black"

    root.configure(bg=bgColor)
    root.option_add("*foreground", fgColor)

 

def exibirGrafico(root):
    fig, ax = plt.subplots()  
    fig.patch.set_facecolor('#282828')
    font_properties = {'color': 'white', 'fontsize': 12}  

    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops=font_properties, labeldistance=1.2)
    ax.axis('equal')  

   
    canvas = FigureCanvasTkAgg(fig, master=root) 
    canvas.draw()
    canvas.get_tk_widget().pack()  # Exibir o gráfico
    return canvas, ax,fig



def criarMensal(canvas, ax, input):
    ax.clear()
    novoSize = int(input)
    sizes[0] = novoSize

    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',textprops = {'color': 'white', 'fontsize': 12},  labeldistance=1.2)
    ax.axis('equal')  

    canvas.draw()

def atualizarGraph(canvas, ax, size,nome,numDespesas):
    global defice

    novo_valor = int(size)  
    possibleLeftover = sizes[0]  
    sizes[0] = sizes[0] - novo_valor
    if sizes[0] < 0 :
        labels[0] = nome
        sizes[0] = possibleLeftover
        defice +=abs(sizes[0] - novo_valor)
        ax.clear()  
        ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})
        ax.axis('equal')  
        canvas.draw() 
        return 1

    sizes.append(novo_valor)
    labels.append(nome)
    colors.append(f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}')

    ax.clear()  
    if(numDespesas < 3):    
        ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})
    else:
        ax.pie(sizes, colors=colors, labels=None, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})

    ax.axis('equal')  

    canvas.draw()  
    print(labels)
    print(sizes)
    print(defice)
    



def getPercentage (size):

    total = sum(sizes)

    return round((float(size)/total) * 100,1)


def atualizaLegendaPoupanca (legendas,nome,value,percentagem):
    primeiro_frame = legendas.winfo_children()[0]  # Acessa o primeiro Frame
    labelSide = primeiro_frame.winfo_children()[0]  # Acessa o primeiro widget (labelSide) dentro desse Frame
    despesaValues = tk.StringVar()
    despesaValues.set(f"{nome}  {value}€  {percentagem}%")
    labelSide.config(textvariable=despesaValues)  # Atualiza o texto no Label


def setLegenda (legendas,i,tipo,despesaValues,mensalValues):

    if tipo == "despesa":

        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=10)  

        labelSide = tk.Label(entryFrame, textvariable=despesaValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50,0))  

        corFrame = tk.Frame(entryFrame, width=60, height=20, bg=colors[i])  
        corFrame.pack(side="left", padx=5)
    elif tipo == "mensal" :
        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=5)  

        labelSide = tk.Label(entryFrame, textvariable=mensalValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50,0))  

        corFrame = tk.Frame(entryFrame, width=60, height=20, bg=colors[i])  
        corFrame.pack(side="left", padx=5)  

    else:
        print("SetLegenda com tipo fora do comum")

def setLegendaSalvadas(data,legendas):
    for widget in legendas.winfo_children():
        widget.destroy()

    numLegendas = len(data["labels"])
    i = 0
    for i in range(numLegendas):
        despesaValues = tk.StringVar()

        total = sum(data['sizes'])
        percentagem = round((float(data['sizes'][i]) / total) * 100, 1)

        despesaValues.set(f"{data['labels'][i]}  {data['sizes'][i]}€  {percentagem}%")

        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=10)  

        labelSide = tk.Label(entryFrame, textvariable=despesaValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50, 0))  

        corFrame = tk.Frame(entryFrame, width=60, height=20, bg=data["colors"][i])  
        corFrame.pack(side="left", padx=5)



def setChartValues(data):
    global labels, sizes, colors  
    labels.clear()
    sizes.clear()
    colors.clear()
    labels = data["labels"]
    sizes = data["sizes"]
    colors = data["colors"]




def getLabel (i):
    return labels[i]


def getSize (i):
    return sizes[i]







