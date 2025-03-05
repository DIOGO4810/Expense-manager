import tkinter as tk
from pieChart import (exibirGrafico, atualizarGraph, criarMensal, setScreen, getPercentage, setLegenda, getLabel, 
                      getSize, salvarDados,setLegendaSalvadas,atualizaLegendaPoupanca,setChartValues)
from tela import carregar_imagens_da_pasta

class Widgets:
    def __init__(self, root):
        # Definição dos widgets
        self.root = root
        self.label = tk.Label(root, text="Exiba o seu orçamento mensal liquido", font=("Arial", 14), fg="white", bg="#282828")
        self.textBox = tk.Text(root, height=1, width=30, bg="white", fg="black")
        self.label1 = tk.Label(root, text="Exiba uma despesa", font=("Arial", 14), fg="white", bg="#282828")
        self.numberBox = tk.Entry(root, width=30, bg="white", fg="black")
        self.label2 = tk.Label(root, text="Exiba o nome da sua despesa", font=("Arial", 14), fg="white", bg="#282828")
        self.textDespesaBox = tk.Entry(root, width=30, bg="white", fg="black")
        self.submeterButton = tk.Button(root, text="Submeter Despesa", command=self.processarDespesa)
        self.telaGraficos = tk.Canvas(root, bg="#202020", width=230)
        self.grafSystem = tk.Frame(self.telaGraficos, bg="#202020")
        self.legendas = tk.Frame(root, width=400, bg="#202020")


        self.botaoSalvar = tk.Button(root, text="Salvar Gráfico", command=lambda: salvarDados(self.fig, self.root, self))

        # Variáveis de controle
        self.canvas = None
        self.ax = None
        self.fig = None
        self.mensalValues = tk.StringVar()
        self.i = 0
        self.numDespesas = 0
        self.flag = False

    def submeterMensal(self, event):
        texto = self.textBox.get("1.0", tk.END).strip()
        self.textBox.delete("1.0", tk.END)
        criarMensal(self.canvas, self.ax, texto)
        percentagem = getPercentage(texto)
        labelPoupanca = getLabel(0)
        self.mensalValues.set(f"{labelPoupanca}  {texto}€  {percentagem}%")
        setLegenda(self.legendas, 0, "mensal", None, self.mensalValues)

        if not self.flag:  # Apenas cria os widgets na primeira submissão
            self.flag = True
            self.label1.pack(pady=10)
            self.numberBox.pack(pady=10)
            self.label2.pack(pady=10)
            self.textDespesaBox.pack(pady=10)
            self.submeterButton.pack(pady=10)
            self.botaoSalvar.pack(pady=10)
            self.textBox.pack_forget()
            self.label.pack_forget()

    def processarDespesa(self):
        value = self.numberBox.get().strip()
        nome = self.textDespesaBox.get().strip()

        deficeFlag = atualizarGraph(self.canvas, self.ax, value, nome, self.numDespesas)
        
        self.numDespesas += 1

        self.numberBox.delete(0, tk.END)
        self.textDespesaBox.delete(0, tk.END)
        sizePoupanca = getSize(0)

        if(deficeFlag == 1):
            percentagem = getPercentage(sizePoupanca)
            atualizaLegendaPoupanca(self.legendas,nome,sizePoupanca,percentagem)
            return
        
        percentagem = getPercentage(value)
        self.i += 1
        percentagemPoupanca = getPercentage(sizePoupanca)
        labelPoupanca = getLabel(0)
        self.mensalValues.set(f"{labelPoupanca}  {sizePoupanca}€  {percentagemPoupanca}%")

        despesaValues = tk.StringVar()
        despesaValues.set(f"{nome}  {value}€  {percentagem}%")

        setLegenda(self.legendas, self.i, "despesa", despesaValues, None)

    def atualizarInput(self,data):
        self.textBox.pack_forget()
        self.label.pack_forget()

        self.label1.pack_forget()
        self.numberBox.pack_forget()
        self.label2.pack_forget()
        self.textDespesaBox.pack_forget()
        self.submeterButton.pack_forget()
        self.botaoSalvar.pack_forget()

        self.label1.pack(pady=10)
        self.numberBox.pack(pady=10)
        self.label2.pack(pady=10)
        self.textDespesaBox.pack(pady=10)
        self.submeterButton.pack(pady=10)
        self.botaoSalvar.pack(pady=10)
        setChartValues(data)
        setLegendaSalvadas(data,self.legendas)

    def setCanvas(self, newCanvas):
        self.canvas = newCanvas
    
    def setAx(self,newAx):
        self.ax = newAx

    def getCanvas(self):
        return self.canvas

    def exibirGrafico(self):
        self.canvas, self.ax, self.fig = exibirGrafico(self.root)
        self.setCanvas(self.canvas)

    def inicializarWidgets(self):
        self.label.pack(pady=10)
        self.textBox.pack(pady=10)
        self.textBox.bind("<Return>", self.submeterMensal)

def main():
    global root

    # Zona do Set da tela e gráfico Inicial
    root = tk.Tk()

    setScreen(root)


    widgets = Widgets(root)


    widgets.legendas.pack(side="right", fill="y")

    widgets.telaGraficos.pack(side="left", fill="y")

    scrollbar = tk.Scrollbar(root, orient="vertical", command=widgets.telaGraficos.yview)
    scrollbar.pack(side="left", fill="y")

    widgets.telaGraficos.config(yscrollcommand=scrollbar.set)

    widgets.telaGraficos.create_window(0, 0, window=widgets.grafSystem, anchor="nw")

    widgets.grafSystem.update_idletasks()
    widgets.telaGraficos.config(scrollregion=widgets.telaGraficos.bbox("all"))


    widgets.exibirGrafico()

    carregar_imagens_da_pasta("SavedGraphs", widgets.grafSystem, root, widgets)

    widgets.inicializarWidgets()

    root.mainloop()

if __name__ == "__main__":
    main()
