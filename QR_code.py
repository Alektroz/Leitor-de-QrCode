import cv2
import tkinter as tk
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import csv
import os
from datetime import datetime

# Função para carregar os dados dos produtos a partir do arquivo CSV
def carregar_produtos(caminho_arquivo):
    """Carrega os dados de produtos de um arquivo CSV para um dicionário."""
    produtos = {}
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for linha in leitor:
                produtos[linha['codigo_qr']] = linha
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None
    return produtos

# Função para registrar a leitura do produto no arquivo de log
def registrar_log(produto):
    """Registra a leitura do produto no arquivo de log."""
    agora = datetime.now()
    data_hora = agora.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{data_hora}] Leitura: {produto['nome']} | Código: {produto['codigo_produto']} | Preço: {produto['preco']}\n"
    with open('historico_leituras.log', 'a', encoding='utf-8') as log_file:
        log_file.write(log_message)

# --- CLASSE DA INTERFACE GRÁFICA ---

class QRCodeApp:
    def __init__(self, window, window_title, banco_de_dados):
        self.window = window
        self.window.title(window_title)
        self.banco_de_dados = banco_de_dados
        self.ultimo_qr_lido = None

        # Configura a captura de vídeo
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro: Não foi possível acessar a webcam.")
            self.window.destroy()
            return
            
        # Cria a área para o vídeo
        self.video_label = tk.Label(window)
        self.video_label.pack(padx=10, pady=10)
        
        # Cria a área para as informações do produto
        self.info_label = tk.Label(window, text="Mire um QR Code na câmera...", font=("Arial", 14), fg="blue")
        self.info_label.pack(padx=10, pady=5)
        
        # Área para exibir a imagem do produto
        self.image_label = tk.Label(window)
        self.image_label.pack(pady=10)
        
        # Inicia o loop de atualização do vídeo
        self.update_video()
        
        # Adiciona um botão para fechar a janela
        self.btn_exit = tk.Button(window, text="Sair", width=15, command=self.close_app)
        self.btn_exit.pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        
    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Processa o frame para detecção de QR Code
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objects = decode(gray_frame)

            if decoded_objects:
                obj = decoded_objects[0]
                qr_data = obj.data.decode('utf-8')

                if qr_data != self.ultimo_qr_lido:
                    self.ultimo_qr_lido = qr_data
                    if qr_data in self.banco_de_dados:
                        produto = self.banco_de_dados[qr_data]
                        
                        # Exibe as informações do produto
                        self.info_label.config(text=f"Produto: {produto['nome']}\nCódigo: {produto['codigo_produto']}\nPreço: {produto['preco']}", fg="green")
                        
                        # Exibe a imagem do produto
                        caminho_imagem = produto.get('caminho_imagem')
                        if caminho_imagem and os.path.exists(caminho_imagem):
                            img = Image.open(caminho_imagem)
                            img = img.resize((200, 200), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            self.image_label.config(image=photo)
                            self.image_label.image = photo
                        else:
                            self.image_label.config(image='')
                            
                        # Registra no log
                        registrar_log(produto)
                    else:
                        self.info_label.config(text=f"QR Code não encontrado: {qr_data}", fg="red")
                        self.image_label.config(image='')
            else:
                self.ultimo_qr_lido = None
                
            # Converte o frame do OpenCV para um formato que o Tkinter possa usar
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo_video = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video_label.config(image=self.photo_video)
        
        self.window.after(10, self.update_video)

    def close_app(self):
        self.cap.release()
        self.window.destroy()

# --- INÍCIO DO PROGRAMA ---

caminho_do_arquivo_csv = 'produtos.csv'
banco_de_dados_produtos = carregar_produtos(caminho_do_arquivo_csv)

if banco_de_dados_produtos:
    root = tk.Tk()
    app = QRCodeApp(root, "Leitor de QR Code", banco_de_dados_produtos)
    root.mainloop()