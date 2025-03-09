import tkinter as tk
from pieChart import (
    exibirGrafico, atualizarGraph, criarMensal, setScreen, getPercentage, setLegenda,
    getLabel, getSize, salvarDados, setLegendaSalvadas, atualizaLegendaPoupanca,
    setChartValues, setLegendaDefice
)
from tela import carregar_imagens_da_pasta,on_mouse_wheel,update_scroll_region


class Widgets:
    def __init__(self, root):
        self.root = root
        self.criarWidgets()
        self.configurarScroll()
        self.inicializarVariáveis()
      

    def criarWidgets(self):
        self.label = tk.Label(self.root, text="Exiba o seu orçamento mensal liquido", font=("Arial", 14), fg="white", bg="#282828")
        self.textBox = tk.Text(self.root, height=1, width=30, bg="white", fg="black")
        self.textBox.bind("<Return>", self.submeterMensal)
        
        self.label1 = tk.Label(self.root, text="Exiba uma despesa", font=("Arial", 14), fg="white", bg="#282828")
        self.numberBox = tk.Entry(self.root, width=30, bg="white", fg="black")
        self.label2 = tk.Label(self.root, text="Exiba o nome da sua despesa", font=("Arial", 14), fg="white", bg="#282828")
        self.textDespesaBox = tk.Entry(self.root, width=30, bg="white", fg="black")
        self.submeterButton = tk.Button(self.root, text="Submeter Despesa", command=self.processarDespesa)
        self.submeterButton.bind("<Return>",lambda event: self.processarDespesa())
        
        self.botaoSalvar = tk.Button(self.root, text="Salvar Gráfico", command=lambda: salvarDados(self.fig, self.root, self))
        self.botaoSalvar.bind("<Return>", lambda event: salvarDados(self.fig, self.root, self))
        self.legendas = tk.Frame(self.root, width=400, bg="#202020")
        
    def configurarScroll(self):
        """Cria o sistema de rolagem para os gráficos."""
        frameScroll = tk.Frame(self.root)
        frameScroll.pack(side="left", fill="y")

        self.telaGraficos = tk.Canvas(frameScroll, bg="#202020", width=230)
        self.telaGraficos.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frameScroll, orient="vertical", command=self.telaGraficos.yview)
        scrollbar.pack(side="right", fill="y")
        self.telaGraficos.configure(yscrollcommand=scrollbar.set)

        self.grafSystem = tk.Frame(self.telaGraficos, bg="#202020")
        self.telaGraficos.create_window((0, 0), window=self.grafSystem, anchor="nw")
        
        self.grafSystem.bind("<Configure>", lambda event: update_scroll_region(self, event))
        self.telaGraficos.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(self, event))  
        self.telaGraficos.bind_all("<Button-4>", lambda event: on_mouse_wheel(self, event))   
        self.telaGraficos.bind_all("<Button-5>", lambda event: on_mouse_wheel(self, event))        

    def inicializarVariáveis(self):
        """Inicializa as variáveis de controle."""
        self.canvas = None
        self.ax = None
        self.fig = None
        self.mensalValues = tk.StringVar()
        self.colorIndice = 0
        self.numDespesas = 0
        self.flag = False
    

    def inicializarWidgets(self):   
        self.label.pack(pady=10)
        self.textBox.pack(pady=10)

    
    def submeterMensal(self, event):
        texto = self.textBox.get("1.0", tk.END).strip()
        self.textBox.delete("1.0", tk.END)
        criarMensal(self.canvas, self.ax, texto)
        
        percentagem = getPercentage(texto)
        labelPoupanca = getLabel(0)
        self.mensalValues.set(f"{labelPoupanca}  {texto}€  {percentagem}%")
        setLegenda(self.legendas, 0, "mensal", None, self.mensalValues)
        
        if not self.flag:
            self.flag = True
            self.mostrarDespesasInput()


    def mostrarDespesasInput(self):
        for widget in [self.label1, self.numberBox, self.label2, self.textDespesaBox, self.submeterButton, self.botaoSalvar]:
            widget.pack(pady=10)
        self.textBox.pack_forget()
        self.label.pack_forget()

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
        setLegendaSalvadas(data,self.legendas,self)

    def processarDespesa(self):
        value = self.numberBox.get().strip()
        nome = self.textDespesaBox.get().strip()
        deficeFlag = atualizarGraph(self.canvas, self.ax, value, nome, self.numDespesas)
        self.numDespesas += 1
        
        self.numberBox.delete(0, tk.END)
        self.textDespesaBox.delete(0, tk.END)
        sizePoupanca = getSize(0)
        self.colorIndice += 1
        
        if deficeFlag == 1:
            atualizaLegendaPoupanca(self.legendas, nome, sizePoupanca, getPercentage(sizePoupanca)) #Tratar do issue do primeiro defice
            return
        elif deficeFlag == 2:
            setLegendaDefice(self.legendas, nome, value)
            return
        
        percentagemPoupanca = getPercentage(sizePoupanca)
        labelPoupanca = getLabel(0)
        print("Antes de atualizar:", self.mensalValues.get())  # DEBUG
        self.mensalValues.set(f"{labelPoupanca}  {sizePoupanca}€  {percentagemPoupanca}%")
        print("Depois de atualizar:", self.mensalValues.get())  # DEBUG
        despesaValues = tk.StringVar()
        despesaValues.set(f"{nome}  {value}€  {getPercentage(value)}%")
        setLegenda(self.legendas, self.colorIndice, "despesa", despesaValues, None)
    
    def exibirGrafico(self):
        self.canvas, self.ax, self.fig = exibirGrafico(self.root)


    def setCanvas(self, newCanvas):
        self.canvas = newCanvas
    
    def setAx(self,newAx):
        self.ax = newAx

    def setFig(self,newFig):
        self.fig = newFig

    def setcolorIndice(self,newcolorIndice):
        self.colorIndice =newcolorIndice

    def setMensalValues(self,mensalvalues):
        self.mensalValues = mensalvalues

    def setLegendas(self,newLegendas):
        self.legendas = newLegendas
    
    def setNumDespesas(self,newNum):
        self.numDespesas = newNum

    def getCanvas(self):
        return self.canvas
    
        



def main():
    root = tk.Tk()
    setScreen(root)
    widgets = Widgets(root)
    widgets.legendas.pack(side="right", fill="y")
    widgets.exibirGrafico()
    carregar_imagens_da_pasta("SavedGraphs", widgets.grafSystem, root, widgets)
    widgets.inicializarWidgets()
    root.mainloop()


if __name__ == "__main__":
    main()
