import tkinter as tk
from pieChart import exibirGrafico, atualizarGraph, criarMensal,setScreen,getPercentage,setLegenda,getLabel,getSize,salvarDados


flag = False
i = 0
numDespesas = 0

def submeterMensal(event,text_widget, canvas, ax,mensalValues):
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
        botaoSalvar = tk.Button(root, text="Salvar Gráfico", command=lambda:salvarDados(fig,root))
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


canvas,ax,fig = exibirGrafico(root)


# Zona do rendimento mensal

label = tk.Label(root, text="Exiba o seu orçamento mensal liquido", font=("Arial", 14), fg="white", bg="#282828")
label.pack(pady=10)
textBox = tk.Text(root, height=1, width=30, bg="white", fg="black")
textBox.pack(pady=10)
mensalValues = tk.StringVar()

textBox.bind("<Return>", lambda event: submeterMensal(event, textBox, canvas, ax,mensalValues))


# Zona das Despesas

label1 = tk.Label(root, text="Exiba a sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
numberBox = tk.Entry(root, width=30, bg="white", fg="black")

label2 = tk.Label(root, text="Exiba o nome da sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
textDespesaBox = tk.Entry(root, width=30, bg="white", fg="black")


submeterButton = tk.Button(root,text="Submeter Despesa", command=lambda:processarDespesa(mensalValues))


  


root.mainloop()
