import os
from PIL import Image
from bing_image_downloader import downloader
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def baixar_imagens():
    termo_pesquisa = entry_termo.get().strip()
    destino = entry_destino.get().strip()

    if not termo_pesquisa:
        messagebox.showerror("Erro", "Por favor, insira o termo de pesquisa.")
        return
    if not destino:
        messagebox.showerror("Erro", "Por favor, selecione o destino das imagens.")
        return

    # Baixar as imagens
    print('Iniciando downloads...')
    try:
        downloader.download(termo_pesquisa, limit=50, output_dir=destino, adult_filter_off=True, force_replace=False, timeout=40)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar imagens: {e}")
        return

    # Caminho da pasta onde as imagens foram baixadas
    pasta_imagens = os.path.join(destino, termo_pesquisa)

    # Renomear e converter as imagens para .jpg
    print('Renomeando e convertendo imagens...')
    try:
        for i, filename in enumerate(os.listdir(pasta_imagens)):
            file_path = os.path.join(pasta_imagens, filename)
            with Image.open(file_path) as img:
                # Obter o timestamp atual (data e hora)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = os.path.join(pasta_imagens, f'{timestamp}.jpg')

                # Verifica se já existe uma imagem com o mesmo timestamp e adiciona um sufixo se necessário
                suffix = 1
                while os.path.exists(new_filename):
                    new_filename = os.path.join(pasta_imagens, f'{timestamp}_{suffix}.jpg')
                    suffix += 1

                # Converter para JPEG e salvar
                img.convert('RGB').save(new_filename, 'JPEG')
                os.remove(file_path)  # Remove o arquivo original
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a imagem {filename}: {e}")
        return

    messagebox.showinfo("Sucesso", "Downloads e renomeações concluídos.")
    print('Downloads e renomeações concluídos.')

def selecionar_destino():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, pasta_selecionada)

# Criação da interface gráfica
root = tk.Tk()
root.title("Downloader de Imagens - Bing")

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Campo para o termo de pesquisa
tk.Label(frame, text="Termo de Pesquisa:").grid(row=0, column=0, sticky="e")
entry_termo = tk.Entry(frame, width=40)
entry_termo.grid(row=0, column=1, padx=5, pady=5)

# Campo para o destino
tk.Label(frame, text="Destino das Imagens:").grid(row=1, column=0, sticky="e")
entry_destino = tk.Entry(frame, width=40)
entry_destino.grid(row=1, column=1, padx=5, pady=5)

# Botão para selecionar destino
btn_selecionar_destino = tk.Button(frame, text="Selecionar", command=selecionar_destino)
btn_selecionar_destino.grid(row=1, column=2, padx=5, pady=5)

# Botão para iniciar o download
btn_baixar = tk.Button(frame, text="Baixar Imagens", command=baixar_imagens)
btn_baixar.grid(row=2, column=1, pady=10)

# Executar a interface gráfica
root.mainloop()
