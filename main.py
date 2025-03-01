import tkinter as tk
from pieChart import exibirGrafico, atualizarGraph, criarMensal,setScreen
from tela import mostrarCaixaDeTexto,salvarGrafico


labels = ['Poupança']
sizes = [200]
colors = ['#99ff99']
flag = False

def submeterMensal(event, text_widget, canvas, ax):
    global flag  # Para modificar a variável global
    texto = text_widget.get("1.0", tk.END).strip()
    print("Texto submetido:", texto)
    text_widget.delete("1.0", tk.END)
    criarMensal(sizes,colors,labels,canvas, ax, texto)
    
    if not flag:  # Apenas cria os widgets na primeira submissão
        flag = True
        label1.pack(pady=10)
        numberBox.pack(pady=10)
        label2.pack(pady=10)
        textDespesaBox.pack(pady=10)
        submeterButton.pack(pady=10)
        botaoSalvar = tk.Button(root, text="Salvar Gráfico", command=lambda:mostrarCaixaDeTexto(fig,root))
        botaoSalvar.pack(pady=10)
        textBox.pack_forget()
        label.pack_forget()

def processarDespesa ():
    value = numberBox.get().strip()
    nome = textDespesaBox.get().strip()
    atualizarGraph(sizes,colors,labels,canvas,ax,value,nome)
    numberBox.delete(0, tk.END)
    textDespesaBox.delete(0, tk.END)
    

root = tk.Tk()

screenHeight,screenWidth = setScreen(root)
canvas,ax,fig = exibirGrafico(sizes,colors,labels,root)

label = tk.Label(root, text="Exiba o seu orçamento mensal liquido", font=("Arial", 14), fg="white", bg="#282828")
label.pack(pady=10)
textBox = tk.Text(root, height=1, width=30, bg="white", fg="black")
textBox.pack(pady=10)
textBox.bind("<Return>", lambda event: submeterMensal(event, textBox, canvas, ax))


label1 = tk.Label(root, text="Exiba a sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
numberBox = tk.Entry(root, width=30, bg="white", fg="black")

label2 = tk.Label(root, text="Exiba o nome da sua primeira despesa", font=("Arial", 14), fg="white", bg="#282828")
textDespesaBox = tk.Entry(root, width=30, bg="white", fg="black")







submeterButton = tk.Button(root,text="Submeter Despesa", command=processarDespesa)


  


root.mainloop()
