import platform
import ctypes




def calcularDimensoes(textBox, screenHeight, screenWidth):
    wText, hText = textBox.winfo_reqwidth(), textBox.winfo_reqheight()

    # Calcular posição centralizada
    xCenter = (screenWidth - wText) / 2
    yCenter = (screenHeight - (hText + 10)) / 2  # 10px de espaçamento

    return [xCenter, yCenter]





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