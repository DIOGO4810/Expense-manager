import tkinter as tk
from pieChart import exibirGrafico, atualizarGraph, criarMensal,setScreen,getPercentage,setLegenda,getLabel,getSize,salvarDados
from tela import carregar_imagens_da_pasta

flag = False
i = 0
numDespesas = 0

def submeterMensal(event,text_widget, canvas, ax,mensalValues,grafSystem):
    global flag  # Para modificar a variável global
    texto = text_widget.get("1.0", tk.END).strip()

    text_widget.delete("1.0", tk.END)
    criarMensal(canvas, ax, texto)
    percentagem = getPercentage(texto)
    labelPoupanca = getLabel(0)
    mensalValues.set(f"{labelPoupanca}  {texto}€  {percentagem}%")

    setLegenda(legendas,0,"mensal",None,mensalValues) 

    
    if not flag:  # Apenas cria os widgets na primeira submissão
        flag = True
        label1.pack(pady=10)
        numberBox.pack(pady=10)
        label2.pack(pady=10)
        textDespesaBox.pack(pady=10)
        submeterButton.pack(pady=10)
        botaoSalvar = tk.Button(root, text="Salvar Gráfico", command=lambda:salvarDados(fig,root,grafSystem))
        botaoSalvar.pack(pady=10)
        textBox.pack_forget()
        label.pack_forget()


def processarDespesa(mensalValues):
    global i
    global numDespesas
    value = numberBox.get().strip()
    nome = textDespesaBox.get().strip()

    atualizarGraph(canvas, ax, value, nome,numDespesas)
    numDespesas +=1
    
    numberBox.delete(0, tk.END)
    textDespesaBox.delete(0, tk.END)
    
    i += 1
    percentagem = getPercentage(value)
    sizePoupanca = getSize(0)
    percentagemPoupanca = getPercentage(sizePoupanca)
    labelPoupanca = getLabel(0)
    mensalValues.set(f"{labelPoupanca}  {sizePoupanca}€  {percentagemPoupanca}%")

    despesaValues = tk.StringVar()
    despesaValues.set(f"{nome}  {value}€  {percentagem}%")

    setLegenda(legendas,i,"despesa",despesaValues,None)    




# Zona do Set da tela e gráfico Inicial

root = tk.Tk()

screenHeight,screenWidth = setScreen(root)

legendas = tk.Frame(root,width=400,bg="#202020")
legendas.pack(side="right", fill="y")

# Criar o Canvas dentro do Frame principal
canvas = tk.Canvas(root, bg="#202020",width=230)
canvas.pack(side="left",fill="y")

# Adicionar a barra de rolagem no Canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="left", fill="y")

# Configurar o Canvas para trabalhar com a barra de rolagem
canvas.config(yscrollcommand=scrollbar.set)

# Criar o Frame grafSystem dentro do Canvas
grafSystem = tk.Frame(canvas, bg="#202020")
canvas.create_window(0, 0, window=grafSystem, anchor="nw")

# Carregar as imagens da pasta SavedGraphs e exibir no grafSystem
carregar_imagens_da_pasta("SavedGraphs", grafSystem)

# Atualizar a área rolável e configurar a rolagem corretamente
grafSystem.update_idletasks()  # Atualiza o layout do grafSystem
canvas.config(scrollregion=canvas.bbox("all"))  # Atualiza o tamanho da área rolável


canvas,ax,fig = exibirGrafico(root)


# Zona do rendimento mensal

label = tk.Label(root, text="Exiba o seu orçamento mensal liquido", font=("Arial", 14), fg="white", bg="#282828")
label.pack(pady=10)
textBox = tk.Text(root, height=1, width=30, bg="white", fg="black")
textBox.pack(pady=10)
mensalValues = tk.StringVar()

textBox.bind("<Return>", lambda event: submeterMensal(event, textBox, canvas, ax,mensalValues,grafSystem))


# Zona das Despesas

label1 = tk.Label(root, text="Exiba a sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
numberBox = tk.Entry(root, width=30, bg="white", fg="black")

label2 = tk.Label(root, text="Exiba o nome da sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
textDespesaBox = tk.Entry(root, width=30, bg="white", fg="black")


submeterButton = tk.Button(root,text="Submeter Despesa", command=lambda:processarDespesa(mensalValues))


  


root.mainloop()
