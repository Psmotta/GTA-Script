import tkinter as tk
from tkinter import ttk, messagebox
import time
import keyboard
import sys
from PIL import Image, ImageTk
import threading
import os

class ProdutoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Produção de Cocaína")
        self.root.geometry("500x880")
        self.root.resizable(False, False)
        
        # Configura o ícone da janela
        try:
            # Obtém o caminho do executável
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, 'coca.ico')
            logo_path = os.path.join(application_path, 'cocaine.png')
            
            self.root.iconbitmap(icon_path)
            
            # Carrega e redimensiona a logo
            self.logo_img = Image.open(logo_path)
            self.logo_img = self.logo_img.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        except Exception as e:
            print(f"Erro ao carregar recursos: {e}")
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5, font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 10))
        
        # Frame principal
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo
        self.logo_label = ttk.Label(self.main_frame, image=self.logo_photo)
        self.logo_label.pack(pady=10)
        
        # Título
        self.title_label = ttk.Label(self.main_frame, 
                                   text="Produção de Cocaína", 
                                   font=('Helvetica', 16, 'bold'))
        self.title_label.pack(pady=5)
        
        # Frame para opções
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Opções de Produção", padding="10")
        self.options_frame.pack(fill=tk.X, pady=5)
        
        # Frame para radiobuttons
        self.radio_frame = ttk.Frame(self.options_frame)
        self.radio_frame.pack(fill=tk.X, pady=5)
        
        # Radiobuttons para escolha do produto
        self.produto_var = tk.StringVar(value="1")
        self.rb_pasta = ttk.Radiobutton(self.radio_frame, 
                                      text="Criar pasta base", 
                                      value="1", 
                                      variable=self.produto_var)
        self.rb_pasta.pack(side=tk.LEFT, padx=20)
        
        self.rb_cocaina = ttk.Radiobutton(self.radio_frame, 
                                        text="Criar cocaína", 
                                        value="2", 
                                        variable=self.produto_var)
        self.rb_cocaina.pack(side=tk.LEFT, padx=20)
        
        # Separador horizontal
        ttk.Separator(self.options_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Frame para quantidade
        self.qtd_frame = ttk.Frame(self.options_frame)
        self.qtd_frame.pack(fill=tk.X, pady=5)
        
        self.qtd_label = ttk.Label(self.qtd_frame, text="Quantidade de matéria prima:")
        self.qtd_label.pack(side=tk.LEFT, padx=5)
        
        vcmd_quantidade = (self.root.register(self.validar_input_quantidade), '%P')
        self.qtd_var = tk.StringVar()
        self.qtd_entry = ttk.Entry(self.qtd_frame, 
                                 textvariable=self.qtd_var,
                                 validate='key',
                                 validatecommand=vcmd_quantidade,
                                 width=10)
        self.qtd_entry.pack(side=tk.LEFT, padx=5)
        
        # Frame para teclas de ação
        self.teclas_frame = ttk.LabelFrame(self.main_frame, text="Teclas de Ação", padding="10")
        self.teclas_frame.pack(fill=tk.X, pady=5)
        
        # Checkbox para ativar comer/beber
        self.comer_beber_var = tk.BooleanVar(value=False)
        self.cb_comer_beber = ttk.Checkbutton(self.teclas_frame,
                                           text="Ativar comer e beber durante execução",
                                           variable=self.comer_beber_var,
                                           command=self.toggle_teclas_entries)
        self.cb_comer_beber.pack(anchor=tk.W, pady=5)
        
        # Frame para tecla de comer
        self.comer_frame = ttk.Frame(self.teclas_frame)
        self.comer_frame.pack(fill=tk.X, pady=2)
        
        self.comer_label = ttk.Label(self.comer_frame, text="Tecla para comer (1-5):")
        self.comer_label.pack(side=tk.LEFT, padx=5)
        
        self.comer_tecla_var = tk.StringVar(value="1")
        vcmd_teclas = (self.root.register(self.validar_input_teclas), '%P')
        self.comer_tecla = ttk.Entry(self.comer_frame, 
                                    textvariable=self.comer_tecla_var, 
                                    width=5, 
                                    state='disabled',
                                    validate='key',
                                    validatecommand=vcmd_teclas)
        self.comer_tecla.pack(side=tk.LEFT, padx=5)
        
        # Frame para tecla de beber
        self.beber_frame = ttk.Frame(self.teclas_frame)
        self.beber_frame.pack(fill=tk.X, pady=2)
        
        self.beber_label = ttk.Label(self.beber_frame, text="Tecla para beber (1-5):")
        self.beber_label.pack(side=tk.LEFT, padx=5)
        
        self.beber_tecla_var = tk.StringVar(value="2")
        vcmd_teclas = (self.root.register(self.validar_input_teclas), '%P')
        self.beber_tecla = ttk.Entry(self.beber_frame, 
                                    textvariable=self.beber_tecla_var, 
                                    width=5, 
                                    state='disabled',
                                    validate='key',
                                    validatecommand=vcmd_teclas)
        self.beber_tecla.pack(side=tk.LEFT, padx=5)
        
        # Frame para intervalo de alimentação
        self.intervalo_frame = ttk.Frame(self.teclas_frame)
        self.intervalo_frame.pack(fill=tk.X, pady=2)
        
        self.intervalo_label = ttk.Label(self.intervalo_frame, text="Intervalo para alimentação (minutos):")
        self.intervalo_label.pack(side=tk.LEFT, padx=5)
        
        self.intervalo_var = tk.StringVar(value="50")
        vcmd_minutos = (self.root.register(self.validar_input_minutos), '%P')
        self.intervalo_entry = ttk.Entry(self.intervalo_frame, 
                                       textvariable=self.intervalo_var, 
                                       width=5, 
                                       state='disabled',
                                       validate='key',
                                       validatecommand=vcmd_minutos)
        self.intervalo_entry.pack(side=tk.LEFT, padx=5)
        
        # Após todas as configurações de comer/beber, adiciona o checkbox de config avançadas
        self.config_frame = ttk.Frame(self.teclas_frame)
        self.config_frame.pack(fill=tk.X, pady=5)
        
        ttk.Separator(self.teclas_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Botão para mostrar/esconder configurações avançadas
        self.show_config_var = tk.BooleanVar(value=False)
        self.show_config_btn = ttk.Checkbutton(self.teclas_frame,
                                             text="Mostrar configurações avançadas",
                                             variable=self.show_config_var,
                                             command=self.toggle_config)
        self.show_config_btn.pack(anchor=tk.W)
        
        # Botão iniciar
        self.start_button = ttk.Button(self.main_frame, 
                                     text="Iniciar Produção", 
                                     command=self.iniciar_producao)
        self.start_button.pack(pady=10)
        
        # Text widget para log
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Log de Produção", padding="10")
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(self.log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para o log
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", 
                                     command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Adiciona handler para quando a janela for fechada
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variável para controlar o thread de produção
        self.producao_thread = None
        self.running = False
        
        # Frame para configuraões avançadas (inicialmente oculto)
        self.advanced_frame = ttk.LabelFrame(self.main_frame, text="Configurações Avançadas", padding="10")
        
        # Frame para tecla de produção
        self.prod_key_frame = ttk.Frame(self.advanced_frame)
        self.prod_key_frame.pack(fill=tk.X, pady=2)
        
        self.prod_key_label = ttk.Label(self.prod_key_frame, text="Tecla para produzir:")
        self.prod_key_label.pack(side=tk.LEFT, padx=5)
        
        self.prod_key_var = tk.StringVar(value="e")
        vcmd_prod_key = (self.root.register(self.validar_input_producao), '%P')
        self.prod_key = ttk.Entry(self.prod_key_frame,
                           textvariable=self.prod_key_var,
                           width=5,
                           validate='key',
                           validatecommand=vcmd_prod_key)
        self.prod_key.pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(self.advanced_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Checkbox para desligamento automático
        self.shutdown_var = tk.BooleanVar(value=False)
        self.shutdown_check = ttk.Checkbutton(self.advanced_frame,
                                          text="Desligar computador ao finalizar",
                                          variable=self.shutdown_var)
        self.shutdown_check.pack(anchor=tk.W, pady=5)

    def on_closing(self):
        if self.running:
            if messagebox.askokcancel("Confirmação", "Uma produção está em andamento. Deseja realmente sair?"):
                self.running = False
                self.root.after(1000, self.force_close)  # Espera 1 segundo antes de forçar o fechamento
        else:
            self.root.destroy()

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def validar_quantidade(self, quantidade):
        try:
            qtd = int(quantidade)
            if qtd <= 0:
                messagebox.showwarning("Aviso", "A quantidade deve ser maior que zero!")
                return False
            if qtd % 5 != 0:
                messagebox.showwarning("Aviso", "A quantidade deve ser divisível por 5!\nExemplo: 5, 10, 15, 20, etc.")
                return False
            return True
        except ValueError:
            messagebox.showwarning("Aviso", "Por favor, digite um número válido!")
            return False

    def validar_teclas(self):
        try:
            tecla_comer = int(self.comer_tecla_var.get())
            tecla_beber = int(self.beber_tecla_var.get())
            
            if not (1 <= tecla_comer <= 5 and 1 <= tecla_beber <= 5):
                messagebox.showwarning("Aviso", "As teclas devem estar entre 1 e 5!")
                return False
                
            if tecla_comer == tecla_beber:
                messagebox.showwarning("Aviso", "As teclas devem ser diferentes!")
                return False
                
            return True
        except ValueError:
            messagebox.showwarning("Aviso", "Digite apenas números para as teclas!")
            return False

    def validar_intervalo(self):
        try:
            intervalo = int(self.intervalo_var.get())
            if intervalo <= 0:
                messagebox.showwarning("Aviso", "O intervalo deve ser maior que zero!")
                return False
            return True
        except ValueError:
            messagebox.showwarning("Aviso", "Digite apenas números para o intervalo!")
            return False

    def processo_producao(self):
        try:
            if self.comer_beber_var.get():
                if not self.validar_teclas() or not self.validar_intervalo():
                    return
            
            # Cache de variáveis para evitar múltiplos acessos
            opcao = int(self.produto_var.get())
            quantidade_total = int(self.qtd_var.get())
            deve_comer_beber = self.comer_beber_var.get()
            
            # Cache de teclas se necessário
            tecla_comer = self.comer_tecla_var.get() if deve_comer_beber else None
            tecla_beber = self.beber_tecla_var.get() if deve_comer_beber else None
            intervalo = int(self.intervalo_var.get()) * 60 if deve_comer_beber else 0
            tecla_producao = self.prod_key_var.get().lower()  # Cache da tecla de produção
            
            # Pré-cálculos
            tempo_espera = 80.2 if opcao == 1 else 60.7
            produto = "pasta base" if opcao == 1 else "cocaína"
            materia_prima = "folhas de coca" if opcao == 1 else "pasta base"
            numero_producoes = quantidade_total // 5
            quantidade_produzida = quantidade_total if opcao == 1 else (quantidade_total * 2)
            
            # Cálculo do tempo total estimado
            tempo_total_segundos = (tempo_espera * numero_producoes) + 10  # +10 da espera inicial
            
            # Se tiver alimentação, adiciona o tempo das pausas
            if deve_comer_beber:
                # Calcula quantas vezes vai precisar comer/beber
                intervalo_segundos = intervalo * 60
                numero_alimentacoes = int(tempo_total_segundos // intervalo_segundos)
                tempo_total_segundos += (numero_alimentacoes * 30)  # 30 segundos por pausa (15 comer + 15 beber)
            
            # Converte para horas, minutos e segundos
            horas = int(tempo_total_segundos // 3600)
            minutos = int((tempo_total_segundos % 3600) // 60)
            segundos = int(tempo_total_segundos % 60)
            
            # Formata o tempo estimado
            tempo_estimado = []
            if horas > 0:
                tempo_estimado.append(f"{horas} hora{'s' if horas > 1 else ''}")
            if minutos > 0:
                tempo_estimado.append(f"{minutos} minuto{'s' if minutos > 1 else ''}")
            if segundos > 0:
                tempo_estimado.append(f"{segundos} segundo{'s' if segundos > 1 else ''}")
            
            tempo_formatado = " e ".join(tempo_estimado) if tempo_estimado else "menos de 1 segundo"
            
            self.log(f"\n=== Iniciando produção de {produto.upper()} ===")
            self.log(f"Quantidade de {materia_prima}: {quantidade_total}")
            self.log(f"Serão realizadas {numero_producoes} produções")
            self.log(f"Tempo estimado: {tempo_formatado}")
            if deve_comer_beber:
                self.log("Comer e beber durante execução: ATIVADO")
                self.log(f"Tecla para comer: {self.comer_tecla_var.get()}")
                self.log(f"Tecla para beber: {self.beber_tecla_var.get()}")
                self.log(f"Intervalo de alimentação: {self.intervalo_var.get()} minutos\n")
            else:
                self.log("Comer e beber durante execução: DESATIVADO\n")
            
            tempo_ultima_alimentacao = 0
            producao = 1
            
            # Espera inicial otimizada
            if numero_producoes > 0:
                self.log("Esperando 10 segundos...")
                time.sleep(10)
            
            while producao <= numero_producoes and self.running:
                if (deve_comer_beber and 
                    producao < numero_producoes and 
                    tempo_ultima_alimentacao >= intervalo):
                    
                    self.log("\nHora de se alimentar...")
                    
                    # Pressiona tecla de comer
                    self.log("Comendo...")
                    keyboard.press(tecla_comer)
                    time.sleep(0.5)
                    keyboard.release(tecla_comer)
                    
                    time.sleep(15)
                    
                    # Pressiona tecla de beber
                    self.log("Bebendo...")
                    keyboard.press(tecla_beber)
                    time.sleep(0.5)
                    keyboard.release(tecla_beber)
                    
                    time.sleep(15)
                    
                    tempo_ultima_alimentacao = 0
                    self.log("Alimentação concluída!\n")
                
                self.log(f"\n=== Iniciando Produção {producao} de {numero_producoes} ===")
                
                self.log(f"Pressionando a tecla '{tecla_producao}'")
                keyboard.press(tecla_producao)
                time.sleep(0.5)
                keyboard.release(tecla_producao)
                
                self.log("Aguardando produzir...")
                time.sleep(tempo_espera)
                
                tempo_ultima_alimentacao += tempo_espera
                self.log("Produção concluída!")
                producao += 1
            
            if self.running:
                self.log(f"\nProdução total finalizada: {quantidade_produzida} unidades de {produto} produzidas.")
                self.log(f"(Usando {quantidade_total} unidades de {materia_prima})")
                
                # Verifica se deve desligar o PC
                if self.shutdown_var.get():
                    self.log("\nIniciando processo de desligamento em 10 segundos...")
                    self.log("Pressione Ctrl+C para cancelar")
                    time.sleep(10)
                    self.log("Desligando...")
                    
                    # Processo de sair do servidor
                    self.log("Saindo do servidor FiveM...")
                    keyboard.press('f8')
                    time.sleep(0.5)
                    keyboard.release('f8')
                    time.sleep(0.5)
                    keyboard.write('quit')
                    time.sleep(0.5)
                    keyboard.press_and_release('enter')
                    time.sleep(3)  # Espera 3 segundos para garantir que saiu do servidor
                    
                    # Executa o comando de desligamento
                    keyboard.press_and_release('win+r')
                    time.sleep(0.5)
                    keyboard.write('shutdown /s /t 0')
                    time.sleep(0.5)
                    keyboard.press_and_release('enter')
        
        except Exception as e:
            if self.running:
                messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
        finally:
            if not self.root._is_being_destroyed:
                self.root.after(0, self.reset_button)
            self.running = False

    def reset_button(self):
        """Método separado para resetar o botão de forma thread-safe"""
        self.start_button.configure(text="Iniciar Produção", command=self.iniciar_producao)

    def iniciar_producao(self):
        # Verifica se já está rodando
        if self.running or (self.producao_thread and self.producao_thread.is_alive()):
            return
        
        if not self.validar_quantidade(self.qtd_var.get()):
            return
        
        self.running = True
        self.start_button.configure(text="Parar Produção", command=self.parar_producao)
        self.log_text.delete(1.0, tk.END)
        self.producao_thread = threading.Thread(target=self.processo_producao)
        self.producao_thread.start()

    def parar_producao(self):
        if not self.running:
            return
        
        self.running = False
        self.log("\nInterrompendo produção...")
        self.start_button.configure(text="Iniciar Produção", command=self.iniciar_producao)

    def force_close(self):
        """Método para forçar o fechamento da janela após timeout"""
        if self.producao_thread and self.producao_thread.is_alive():
            self.producao_thread.join(timeout=0.1)
        self.root.destroy()

    def toggle_teclas_entries(self):
        """Habilita/desabilita os campos de entrada baseado no checkbox"""
        state = 'normal' if self.comer_beber_var.get() else 'disabled'
        self.comer_tecla.configure(state=state)
        self.beber_tecla.configure(state=state)
        self.intervalo_entry.configure(state=state)

    def validar_input_teclas(self, valor):
        """Valida input das teclas em tempo real"""
        if valor == "":  # Permite campo vazio
            return True
        try:
            numero = int(valor)
            return 1 <= numero <= 5
        except ValueError:
            return False

    def validar_input_minutos(self, valor):
        """Valida input dos minutos em tempo real"""
        if valor == "":  # Permite campo vazio
            return True
        try:
            numero = int(valor)
            return 1 <= numero <= 60
        except ValueError:
            return False

    def validar_input_quantidade(self, valor):
        """Valida input da quantidade em tempo real"""
        if valor == "":  # Permite campo vazio
            return True
        try:
            numero = int(valor)
            return numero > 0  # Permite qualquer número positivo
        except ValueError:
            return False

    def toggle_config(self):
        """Mostra/esconde o frame de configurações avançadas"""
        if self.show_config_var.get():
            self.advanced_frame.pack(fill=tk.X, pady=5, before=self.log_frame)
        else:
            self.advanced_frame.pack_forget()

    def validar_input_producao(self, valor):
        """Valida input da tecla de produção em tempo real"""
        if valor == "":  # Permite campo vazio
            return True
        return len(valor) == 1  # Aceita apenas um caractere

if __name__ == "__main__":
    root = tk.Tk()
    app = ProdutoraApp(root)
    root.mainloop() 