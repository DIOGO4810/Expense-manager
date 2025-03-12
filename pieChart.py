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
deficeSizes = []

def salvarDados(fig,root,widgets):
    dados = {
        "labels": labels,
        "sizes": sizes,
        "colors": colors,
        "defice": defice,
        "deficeSizes": deficeSizes

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

def atualizarGraph(widgets,size,nome):
    global defice
    novo_valor = int(size)
    if defice > 0 :
        defice += novo_valor
        widgets.deficeVar.set(defice)
        print(f"aqui{deficeSizes}")

        deficeSizes.append(novo_valor)
        labels.append(nome)
        colors.append("#ff0000")
        print(deficeSizes)

        return 2
    
    possibleLeftover = sizes[0]  
    sizes[0] = sizes[0] - novo_valor

    if sizes[0] < 0 and labels[0] == "Poupança":
        labels[0] = nome
        sizes[0] = possibleLeftover
        defice +=abs(sizes[0] - novo_valor)
        widgets.ax.clear()  
        if(widgets.numDespesas < 3):    
            widgets.ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})
        else:
            widgets.ax.pie(sizes, colors=colors, labels=None, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})

        widgets.ax.axis('equal')  
        widgets.canvas.draw() 
        widgets.setDeficeVar(defice)
        deficeSizes.append(defice)
        labels.append(nome)
        colors.append("#ff0000")
        return 1

    sizes.append(novo_valor)
    labels.append(nome)
    colors.append(f'#{random.randint(30, 255):02x}{random.randint(30, 230):02x}{random.randint(30, 255):02x}')

    widgets.ax.clear()  
    if(widgets.numDespesas < 3):    
        widgets.ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})
    else:
        widgets.ax.pie(sizes, colors=colors, labels=None, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})

    widgets.ax.axis('equal')  

    widgets.canvas.draw()  
    print(labels)
    print(sizes)
    



def getPercentage (size):

    total = sum(sizes)

    return round((float(size)/total) * 100,1)


def atualizaLegendaPoupanca (legendas,nome,valorPoupanca,value):
    primeiro_frame = legendas.winfo_children()[0]  # Acessa o primeiro Frame
    labelSide = primeiro_frame.winfo_children()[0]  # Acessa o primeiro widget (labelSide) dentro desse Frame

    despesaValues = tk.StringVar()
    percentagemPoupança = getPercentage(valorPoupanca)
    despesaValues.set(f"{nome}  {valorPoupanca}€  {percentagemPoupança}%")
    labelSide.config(textvariable=despesaValues)  # Atualiza o texto no Label

    valueInt = int(value)
    deficeValues = tk.StringVar()
    deficeValues.set(f"{nome}  {valueInt - valorPoupanca}€ ")
    setLegenda(legendas,-1,"despesa",deficeValues,None)


def setLegenda (legendas,i,tipo,despesaValues,mensalValues):

    if tipo == "despesa":

        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=10)  

        labelSide = tk.Label(entryFrame, textvariable=despesaValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50,0))  

        if i >= 0:
            corFrame = tk.Frame(entryFrame, width=60, height=20, bg=colors[i])  
            corFrame.pack(side="left", padx=5)
        else:
            corFrame = tk.Frame(entryFrame, width=60, height=20, bg="#ff0000")  
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

def setLegendaSalvadas(data,legendas,widgets):
    for widget in legendas.winfo_children():
        widget.destroy()

    numLegendas = len(data["sizes"])
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
        if i == 0:
            widgets.setMensalValues(despesaValues)
    
    numDefices = len(data["deficeSizes"])
    for i in range(numDefices):
        despesaValues = tk.StringVar()

        despesaValues.set(f"{data['labels'][i+numLegendas]}  {data['deficeSizes'][i]}€")

        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=10)  

        labelSide = tk.Label(entryFrame, textvariable=despesaValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50, 0))  

        corFrame = tk.Frame(entryFrame, width=60, height=20, bg="#ff0000")  
        corFrame.pack(side="left", padx=5)

    widgets.setcolorIndice(i)

    

    
    
    

def setLegendaDefice(legendas,nome,value):
    deficeValues = tk.StringVar()
    deficeValues.set(f"{nome}  {value}")

    entryFrame = tk.Frame(legendas, bg="#202020")  
    entryFrame.pack(pady=5)  

    labelSide = tk.Label(entryFrame, textvariable=deficeValues, font=("Arial", 14), fg="white", bg="#202020")
    labelSide.pack(side="left", padx=(50,0)) 

    corFrame = tk.Frame(entryFrame, width=60, height=20, bg="#ff0000")  
    corFrame.pack(side="left", padx=5)  



def setChartValues(data):
    global labels, sizes, colors,deficeSizes
    labels.clear()
    sizes.clear()
    colors.clear()
    deficeSizes.clear()
    labels = data["labels"]
    sizes = data["sizes"]
    colors = data["colors"]
    deficeSizes = data["deficeSizes"]
    




def getLabel (i):
    return labels[i]


def getSize (i):
    return sizes[i]

def setDefice(newDefice):
    global defice
    defice = newDefice






