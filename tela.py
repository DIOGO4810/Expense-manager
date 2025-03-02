import platform
import ctypes
import tkinter as tk


def calcularDimensoes(textBox, screenHeight, screenWidth):
    wText, hText = textBox.winfo_reqwidth(), textBox.winfo_reqheight()

    xCenter = (screenWidth - wText) / 2
    yCenter = (screenHeight - (hText + 10)) / 2  # 10px de espaçamento

    return [xCenter, yCenter]



def salvarGrafico(fig,nome):
    
        path = f"SavedGraphs/{nome}.png"
        fig.savefig(path)
        print(f"Gráfico salvo como {path}")


def mostrarCaixaDeTexto(fig,root):
    dialog = tk.Toplevel(root)
    dialog.title("Salvar Gráfico")
    dialog.geometry("400x300")

    label = tk.Label(dialog, text="Digite o nome do gráfico:", font=("Arial", 12))
    label.pack(pady=10)

    
    entry = tk.Entry(dialog, font=("Arial", 12), fg="black")  # Cor do texto aqui
    entry.pack(pady=10)

    def salvar():
        nomeGrafico = entry.get().strip()
        
        print(f"Gráfico será salvo com o nome: {nomeGrafico}")
        salvarGrafico(fig, nomeGrafico)  
        dialog.destroy()  
        

    save_button = tk.Button(dialog, text="Salvar", command=salvar)
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