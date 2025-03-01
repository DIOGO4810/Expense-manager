import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from tela import is_dark_mode



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

def exibirGrafico(sizes,colors,labels,root):
    fig, ax = plt.subplots()  
    fig.patch.set_facecolor('#282828')
    font_properties = {'color': 'white', 'fontsize': 12}  

    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops=font_properties, labeldistance=1.2)
    ax.axis('equal')  

    # Inserir o gráfico na interface Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # Conectar o gráfico à janela Tkinter
    canvas.draw()
    canvas.get_tk_widget().pack()  # Exibir o gráfico
    return canvas, ax



def criarMensal(sizes,colors,labels,canvas, ax, input):
    ax.clear()
    novoSize = int(input)
    sizes[0] = novoSize

    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',textprops = {'color': 'white', 'fontsize': 12},  labeldistance=1.2)
    ax.axis('equal')  

    canvas.draw()

def atualizarGraph(sizes,colors,labels,canvas, ax, size,nome):
    if not size.strip():  # Evita valores vazios
        return

    novo_valor = int(size)  
    sizes[0] = sizes[0] - novo_valor


    sizes.append(novo_valor)
    labels.append(nome)
    colors.append(f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}')

    ax.clear()  
    
    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', labeldistance=1.2,textprops = {'color': 'white', 'fontsize': 12})
    ax.axis('equal')  

    canvas.draw()  
    print(labels)
    print(sizes)