import platform
import ctypes
import tkinter as tk
import json
from tkinter import PhotoImage
from PIL import Image, ImageTk

import os



def calcularDimensoes(textBox, screenHeight, screenWidth):
    wText, hText = textBox.winfo_reqwidth(), textBox.winfo_reqheight()

    xCenter = (screenWidth - wText) / 2
    yCenter = (screenHeight - (hText + 10)) / 2  # 10px de espaçamento

    return [xCenter, yCenter]


def carregar_imagens_da_pasta(pasta, root):

    # Limpar o grafSystem antes de adicionar novas imagens
    for widget in root.winfo_children():
        widget.destroy()  # Remove todos os widgets antigos do grafSystem
    

    # Listar todos os arquivos .png na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith('.png'):
            caminho_imagem = os.path.join(pasta, arquivo)
            exibir_imagem(caminho_imagem, root)


def salvarGrafico(fig,nome,dados,grafSystem):

        path = f"SavedGraphs/{nome}.png"
        pathjson = f"SavedGraphs/{nome}.json"
        fig.savefig(path)
        with open(pathjson, "w") as f:
            json.dump(dados, f, indent=4)  # `indent=4` para formatação bonita

        carregar_imagens_da_pasta("SavedGraphs",grafSystem)

def exibir_imagem(caminho_imagem,grafSystem):
    imagem = Image.open(caminho_imagem)
    
    imagem = imagem.resize((200, 200), Image.Resampling.LANCZOS)
    
    imagem_tk = ImageTk.PhotoImage(imagem)
    
    # Exibir a imagem em um label
    label_imagem = tk.Label(grafSystem, image=imagem_tk)
    label_imagem.image = imagem_tk  
    label_imagem.pack(pady=10)


def mostrarCaixaDeTexto(fig,root,dados,grafSystem):
    dialog = tk.Toplevel(root)
    dialog.title("Salvar Gráfico")
    dialog.geometry("400x300")

    label = tk.Label(dialog, text="Digite o nome do gráfico:", font=("Arial", 12))
    label.pack(pady=10)

    
    entry = tk.Entry(dialog, font=("Arial", 12), fg="black")  # Cor do texto aqui
    entry.pack(pady=10)

    def salvar(dados,grafSystem):
        nomeGrafico = entry.get().strip()
        
        print(f"Gráfico será salvo com o nome: {nomeGrafico}")
        salvarGrafico(fig, nomeGrafico,dados,grafSystem)  
        dialog.destroy()  
        

    save_button = tk.Button(dialog, text="Salvar", command=lambda:salvar(dados,grafSystem))
    save_button.pack(pady=10)

    cancel_button = tk.Button(dialog, text="Cancelar", command=dialog.destroy)
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
    


