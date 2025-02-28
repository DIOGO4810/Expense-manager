import tkinter as tk
from tela import calcularDimensoes, is_dark_mode
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

labels = ['Poupança']
sizes = [200]
colors = ['#99ff99']
flag = False

def exibirGrafico():
    # Dados do gráfico de pizza
    fig, ax = plt.subplots()  # Criar o gráfico
    fig.patch.set_facecolor('#282828')
    font_properties = {'color': 'white', 'fontsize': 12}  # Cor e tamanho da fonte

    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops=font_properties, labeldistance=0.8)
    ax.axis('equal')  # Garantir que o gráfico seja circular

    # Inserir o gráfico na interface Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # Conectar o gráfico à janela Tkinter
    canvas.draw()
    canvas.get_tk_widget().pack()  # Exibir o gráfico
    return canvas, ax

def criarMensal(canvas, ax, input):
    ax.clear()
    novoSize = int(input)
    sizes[0] = novoSize

    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    ax.axis('equal')  # Garantir que o gráfico seja circular

    canvas.draw()

def random_color():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))

# Valor fixo inicial
valor_inicial = 2000

def atualizarSize(canvas, ax, input):
    if not input.strip():  # Evita valores vazios
        return
    
    novo_valor = int(input)  # Converte o valor de entrada para inteiro
    sizes[0] = sizes[0] - novo_valor
    # Adiciona o novo valor à lista de 'sizes'
    sizes.append(novo_valor)
    
    
    
    # Atualiza o gráfico com o novo conjunto de dados
    ax.clear()  # Limpa o gráfico atual
    
    # Atualiza o gráfico com o novo conjunto de dados e percentagens
    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    ax.axis('equal')  # Garante que o gráfico seja circular

    canvas.draw()  # Desenha o gráfico atualizado


def atualizarLabel(canvas, ax, input):
    if not input.strip():  # Evita adicionar rótulos vazios
        return
    
    ax.clear()
    labels.append(input)
    colors.append(f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}')
    print(labels)
    if len(sizes) < len(labels):  # Garantir que há um valor correspondente
        sizes.append(1)  # Adiciona um valor padrão (ex: 1) para a nova despesa

    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    ax.axis('equal')  

    canvas.draw()

root = tk.Tk()
root.title("Expense Manager")

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"{screenWidth}x{screenHeight}")

# Aplicar tema
darkMode = is_dark_mode()
bgColor = "#282828" if darkMode else "white"
fgColor = "white" if darkMode else "black"

root.configure(bg=bgColor)
root.option_add("*foreground", fgColor)

# Widgets criados aqui para referenciá-los antes
label1 = tk.Label(root, text="Exiba a sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
numberBox = tk.Text(root, height=1, width=30, bg="white", fg="black")

label2 = tk.Label(root, text="Exiba o nome da sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
textDespesaBox = tk.Text(root, height=1, width=30, bg="white", fg="black")

def submeterMensal(event, text_widget, canvas, ax):
    global flag  # Para modificar a variável global
    texto = text_widget.get("1.0", tk.END).strip()
    print("Texto submetido:", texto)
    text_widget.delete("1.0", tk.END)
    criarMensal(canvas, ax, texto)
    
    if not flag:  # Apenas cria os widgets na primeira submissão
        flag = True
        label1.pack(pady=10)
        numberBox.pack(pady=10)
        label2.pack(pady=10)
        textDespesaBox.pack(pady=10)
        textBox.pack_forget()

def submeterDespesa(event, text_widget, canvas, ax):
    texto = text_widget.get("1.0", tk.END).strip()  # Pega o texto da caixa de texto
    print("Texto submetido:", texto)  # Substitua por sua lógica de submissão
    text_widget.delete("1.0", tk.END)  # Limpa a caixa de texto após submissão (opcional)
    atualizarLabel(canvas, ax, texto)

def submeterDespesaN(event, text_widget, canvas, ax):
    texto = text_widget.get("1.0", tk.END).strip()  # Pega o texto da caixa de texto
    print("Texto submetido:" + texto)  # Substitua por sua lógica de submissão
    text_widget.delete("1.0", tk.END)  # Limpa a caixa de texto após submissão (opcional)
    atualizarSize(canvas, ax, texto)

# Atualizar janela para calcular tamanho dos widgets
root.update_idletasks()
textBox = tk.Text(root, height=1, width=30, bg="white", fg="black")
numberBox = tk.Text(root, height=1, width=30, bg="white", fg="black")
textDespesaBox = tk.Text(root, height=1, width=30, bg="white", fg="black")

[xCenter, yCenter] = calcularDimensoes(textBox, screenHeight, screenWidth)

canvas, ax = exibirGrafico()
textBox.bind("<Return>", lambda event: submeterMensal(event, textBox, canvas, ax))
numberBox.bind("<Return>", lambda event: submeterDespesaN(event, numberBox, canvas, ax))
textDespesaBox.bind("<Return>", lambda event: submeterDespesa(event, textDespesaBox, canvas, ax))

label = tk.Label(root, text="Exiba o seu orçamento mensal liquido", font=("Arial", 14), fg="white", bg="#282828")
label.pack(pady=10)  
textBox.pack(pady=10)

root.mainloop()
