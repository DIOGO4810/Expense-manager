import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from tela import is_dark_mode,mostrarCaixaDeTexto
import tkinter as tk

labels = ['Poupança']
sizes = [200]
colors = ['#99ff99']


def salvarDados(fig,root):
    dados = {
        "labels": labels,
        "sizes": sizes,
        "colors": colors
    }
    mostrarCaixaDeTexto(fig,root,dados)



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

    return screenHeight,screenWidth

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


    novo_valor = int(size)  
    sizes[0] = sizes[0] - novo_valor


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
    



def getPercentage (size):

    total = sum(sizes)

    return round((float(size)/total) * 100,1)




def setLegenda (legendas,i,tipo,despesaValues,mensalValues):

    if tipo == "despesa":

        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=10)  

        labelSide = tk.Label(entryFrame, textvariable=despesaValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50,0))  

        corFrame = tk.Frame(entryFrame, width=60, height=20, bg=colors[i])  
        corFrame.pack(side="left", padx=5)
    elif ("mensal") :
        entryFrame = tk.Frame(legendas, bg="#202020")  
        entryFrame.pack(pady=5)  

        labelSide = tk.Label(entryFrame, textvariable=mensalValues, font=("Arial", 14), fg="white", bg="#202020")
        labelSide.pack(side="left", padx=(50,0))  

        corFrame = tk.Frame(entryFrame, width=60, height=20, bg=colors[i])  
        corFrame.pack(side="left", padx=5)  

    else:
        print("SetLegenda com tipo fora do comum")


def getLabel (i):
    return labels[i]


def getSize (i):
    return sizes[i]