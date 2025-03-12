import platform
import ctypes
import tkinter as tk
import json
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




def calcularDimensoes(textBox, screenHeight, screenWidth):
    wText, hText = textBox.winfo_reqwidth(), textBox.winfo_reqheight()

    xCenter = (screenWidth - wText) / 2
    yCenter = (screenHeight - (hText + 10)) / 2  # 10px de espaçamento

    return [xCenter, yCenter]



def exibirSalvado(imagePath, root,widgets):
    # Remover a extensão .png do imagePath
    baseName = os.path.splitext(imagePath)[0]  


    with open(f"{baseName}.json", "r", encoding="utf-8") as file:
        data = json.load(file)  

    fig, ax = plt.subplots()  
    fig.patch.set_facecolor('#282828')
    font_properties = {'color': 'white', 'fontsize': 12}  

    widgets.setNumDespesas(len(data["labels"]) - 1)
    
    if widgets.numDespesas < 3:
        ax.pie(x=data["sizes"], labels=data["labels"], colors=data["colors"],
            autopct='%1.1f%%', textprops=font_properties, labeldistance=1.2)
    else :
        ax.pie(x=data["sizes"], labels=None, colors=data["colors"],
            autopct='%1.1f%%', textprops=font_properties, labeldistance=1.2)

    ax.axis('equal')  

    
    canvas = widgets.getCanvas()

    canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root) 
    canvas.draw()
    canvas.get_tk_widget().pack()  
    widgets.setCanvas(canvas)
    widgets.setAx(ax)
    widgets.setFig(fig)
    widgets.setDeficeVar(data["defice"]) 
    

    widgets.atualizarInput(data)
    


def exibir_imagem(caminho_imagem,grafSystem,mainRoot,widgets):
    imagem = Image.open(caminho_imagem)
    
    imagem = imagem.resize((200, 200), Image.Resampling.LANCZOS)
    
    imagem_tk = ImageTk.PhotoImage(imagem)
    
    # Exibir a imagem em um label
    label_imagem = tk.Label(grafSystem, image=imagem_tk)
    label_imagem.image = imagem_tk  
    label_imagem.pack(pady=10,padx=12)

    label_imagem.bind("<Double-Button-1>",lambda event: exibirSalvado(caminho_imagem,mainRoot,widgets))

    

def carregar_imagens_da_pasta(pasta, root,mainRoot,widgets):

    # Limpar o grafSystem antes de adicionar novas imagens
    for widget in root.winfo_children():
        widget.destroy()  # Remove todos os widgets antigos do grafSystem
    
    # Listar todos os arquivos .png na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith('.png'):
            caminho_imagem = os.path.join(pasta, arquivo)
            exibir_imagem(caminho_imagem, root,mainRoot,widgets)


def salvarGrafico(fig,nome,dados,widgets,root):

        path = f"SavedGraphs/{nome}.png"
        pathjson = f"SavedGraphs/{nome}.json"
        fig.savefig(path)
        with open(pathjson, "w") as f:
            json.dump(dados, f, indent=4)  # `indent=4` para formatação bonita

        carregar_imagens_da_pasta("SavedGraphs",widgets.grafSystem,root,widgets)

def mostrarCaixaDeTexto(fig,root,dados,widgets):
    dialog = tk.Toplevel(root)
    dialog.title("Salvar Gráfico")
    dialog.geometry("400x300")

    label = tk.Label(dialog, text="Digite o nome do gráfico:", font=("Arial", 12))
    label.pack(pady=10)

    
    entry = tk.Entry(dialog, font=("Arial", 12), fg="black")  # Cor do texto aqui
    entry.pack(pady=10)

    def salvar(dados,widgets,root):
        nomeGrafico = entry.get().strip()
        
        print(f"Gráfico será salvo com o nome: {nomeGrafico}")
        salvarGrafico(fig, nomeGrafico,dados,widgets,root)  
        dialog.destroy()  
        

    save_button = tk.Button(dialog, text="Salvar", command=lambda:salvar(dados,widgets,root))
    save_button.bind("<Return>", lambda event: salvar(dados,widgets,root))

    save_button.pack(pady=10)

    cancel_button = tk.Button(dialog, text="Cancelar", command=dialog.destroy)
    cancel_button.bind("<Return>", lambda event:dialog.destroy())

    cancel_button.pack(pady=10)



# Função para verificar se o modo escuro está ativo
def is_dark_mode():
    system = platform.system()
    
    if system == "Windows":
        try:
            key = ctypes.windll.user32.GetSysColor(30)
            return key == 0
        except Exception:
            return False
    
    elif system == "Darwin":  # macOS
        import subprocess
        result = subprocess.run(['osascript', '-e', 'tell app "System Events" to get dark mode of appearance preferences'], capture_output=True, text=True)
        return result.stdout.strip() == 'true'
    
    else:
        return True  # Assume escuro para Linux
    
def update_scroll_region(self, event=None):
    """Atualiza a região de rolagem para o canvas."""
    self.telaGraficos.update_idletasks()
    self.telaGraficos.config(scrollregion=self.telaGraficos.bbox("all"))
    
def on_mouse_wheel(self, event):
    """Processa a rolagem do mouse (Windows/Linux)."""
    # Para Windows e plataformas com event.delta
    if event.delta:
        self.telaGraficos.yview_scroll(-1 * (event.delta // 120), "units")
    # Para sistemas Unix/Linux com Button-4 e Button-5
    elif event.num == 4:  # Rolagem para cima
        self.telaGraficos.yview_scroll(-1, "units")
    elif event.num == 5:  # Rolagem para baixo
        self.telaGraficos.yview_scroll(1, "units")



