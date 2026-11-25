import tkinter as tk
from tkinter import messagebox, ttk

from models.acervo import Acervo
from models.buscador import BuscadorFichaTecnica
from models.cassete import K7
from models.cd import CD
from models.registro_compra import RegistroCompra
from models.repositorio import ErroRepositorio
from models.vinil import Vinil
from views.dados_exemplo import carregar_dados_exemplo


# Paleta de cores personalizada (Tema Dark Vinyl Studio)
COR_FUNDO = "#121216"
COR_PAINEL = "#1C1C24"
COR_CARD = "#252530"
COR_BORDA = "#343444"
COR_TEXTO = "#F4F4F6"
COR_TEXTO_SUAVE = "#A0A0B2"

COR_PRIMARIA = "#E5A93C"       # Âmbar / Dourado
COR_PRIMARIA_HOVER = "#F2BC57"
COR_TEXTO_ESCURO = "#121216"

COR_SECUNDARIA = "#2E3244"
COR_SECUNDARIA_HOVER = "#3D4259"

COR_INFO = "#2B6CB0"
COR_INFO_HOVER = "#3B82F6"

COR_SUCESSO = "#2E7D5B"
COR_SUCESSO_HOVER = "#38996F"

COR_PERIGO = "#B83B3B"
COR_PERIGO_HOVER = "#D64545"


class BotaoEstilizado(tk.Button):
    """Botão personalizado com borda limpa, cursor de mão e efeito hover."""

    def __init__(self, master, text, command=None, bg=COR_SECUNDARIA,
                 hover_bg=COR_SECUNDARIA_HOVER, fg=COR_TEXTO, width=None, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            **kwargs,
        )
        if width is not None:
            self.configure(width=width)

        self._bg_normal = bg
        self._bg_hover = hover_bg
        self.bind("<Enter>", lambda _e: self.configure(bg=self._bg_hover))
        self.bind("<Leave>", lambda _e: self.configure(bg=self._bg_normal))


class InterfaceGrafica:
    """Interface gráfica desktop (Tkinter/ttk) para o GrooveManager."""

    OPCOES_CONSERVACAO = ["Lacrado", "Excelente", "Bom", "Ruim"]
    MAPA_FORMATOS = {"Vinil": Vinil, "CD": CD, "K7": K7}

    def __init__(self, acervo=None):
        self.acervo = acervo if acervo is not None else Acervo()
        self.root = tk.Tk()
        self.root.title("GrooveManager — Catálogo de Mídias Físicas")
        self.root.geometry("1040x640")
        self.root.minsize(920, 560)
        self.root.configure(bg=COR_FUNDO)

        self._midias_exibidas = []
        self._configurar_estilos()
        self._construir_tela_principal()
        self._atualizar_tabela()

    def iniciar(self):
        self.root.mainloop()

    # =========================================================================
    # ESTILOS PERSONALIZADOS (ttk.Style)
    # =========================================================================
    def _configurar_estilos(self):
        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")

        estilo.configure(
            "Groove.Treeview",
            background=COR_PAINEL,
            foreground=COR_TEXTO,
            fieldbackground=COR_PAINEL,
            borderwidth=0,
            rowheight=32,
            font=("Segoe UI", 10),
        )
        estilo.map(
            "Groove.Treeview",
            background=[("selected", COR_PRIMARIA)],
            foreground=[("selected", COR_TEXTO_ESCURO)],
        )
        estilo.configure(
            "Groove.Treeview.Heading",
            background=COR_CARD,
            foreground=COR_PRIMARIA,
            relief="flat",
            padding=(8, 8),
            font=("Segoe UI", 10, "bold"),
        )
        estilo.map(
            "Groove.Treeview.Heading",
            background=[("active", COR_BORDA)],
        )

        estilo.configure(
            "Groove.TCombobox",
            fieldbackground=COR_CARD,
            background=COR_CARD,
            foreground=COR_TEXTO,
            arrowcolor=COR_PRIMARIA,
            borderwidth=1,
            padding=5,
        )
        estilo.map(
            "Groove.TCombobox",
            fieldbackground=[("readonly", COR_CARD)],
            foreground=[("readonly", COR_TEXTO)],
            selectbackground=[("readonly", COR_CARD)],
            selectforeground=[("readonly", COR_TEXTO)],
        )

        estilo.configure("Groove.TNotebook", background=COR_FUNDO, borderwidth=0)
        estilo.configure(
            "Groove.TNotebook.Tab",
            background=COR_CARD,
            foreground=COR_TEXTO_SUAVE,
            padding=(14, 7),
            font=("Segoe UI", 9, "bold"),
        )
        estilo.map(
            "Groove.TNotebook.Tab",
            background=[("selected", COR_PRIMARIA)],
            foreground=[("selected", COR_TEXTO_ESCURO)],
        )

    # =========================================================================
    # JANELA PRINCIPAL
    # =========================================================================
    def _construir_tela_principal(self):
        # Cabeçalho
        cabecalho = tk.Frame(self.root, bg=COR_PAINEL, height=68)
        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        bloco_titulo = tk.Frame(cabecalho, bg=COR_PAINEL)
        bloco_titulo.pack(side="left", padx=22, pady=10)

        tk.Label(
            bloco_titulo,
            text="GROOVEMANAGER",
            bg=COR_PAINEL,
            fg=COR_PRIMARIA,
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        tk.Label(
            bloco_titulo,
            text="Catálogo de Vinil, CD e Fita Cassete • Persistência SQLite",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        # Botões utilitários no canto superior direito
        bloco_topo_dir = tk.Frame(cabecalho, bg=COR_PAINEL)
        bloco_topo_dir.pack(side="right", padx=20)

        BotaoEstilizado(
            bloco_topo_dir,
            text="Carregar Exemplos",
            command=self._acao_carregar_exemplos,
            bg=COR_SUCESSO,
            hover_bg=COR_SUCESSO_HOVER,
        ).pack(side="left", padx=5)

        BotaoEstilizado(
            bloco_topo_dir,
            text="Listar Artistas",
            command=self._abrir_janela_artistas,
            bg=COR_SECUNDARIA,
            hover_bg=COR_SECUNDARIA_HOVER,
        ).pack(side="left", padx=5)

        BotaoEstilizado(
            bloco_topo_dir,
            text="Banco SQLite",
            command=self._abrir_janela_banco,
            bg=COR_SECUNDARIA,
            hover_bg=COR_SECUNDARIA_HOVER,
        ).pack(side="left", padx=5)

        # Barra de busca e filtros
        barra_busca = tk.Frame(self.root, bg=COR_FUNDO)
        barra_busca.pack(fill="x", padx=22, pady=(14, 10))

        tk.Label(
            barra_busca,
            text="Buscar:",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 8))

        self.var_criterio_busca = tk.StringVar(value="Título")
        combo_criterio = ttk.Combobox(
            barra_busca,
            textvariable=self.var_criterio_busca,
            values=["Título", "Artista"],
            state="readonly",
            width=10,
            style="Groove.TCombobox",
        )
        combo_criterio.pack(side="left", padx=(0, 8))

        self.var_termo_busca = tk.StringVar()
        entrada_busca = tk.Entry(
            barra_busca,
            textvariable=self.var_termo_busca,
            bg=COR_CARD,
            fg=COR_TEXTO,
            insertbackground=COR_PRIMARIA,
            relief="flat",
            font=("Segoe UI", 10),
            width=28,
        )
        entrada_busca.pack(side="left", ipady=6, padx=(0, 10))
        entrada_busca.bind("<Return>", lambda _e: self._aplicar_filtros())

        tk.Label(
            barra_busca,
            text="Formato:",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(4, 8))

        self.var_filtro_formato = tk.StringVar(value="Todos")
        combo_formato = ttk.Combobox(
            barra_busca,
            textvariable=self.var_filtro_formato,
            values=["Todos", "Vinil", "CD", "K7"],
            state="readonly",
            width=10,
            style="Groove.TCombobox",
        )
        combo_formato.pack(side="left", padx=(0, 10))
        combo_formato.bind("<<ComboboxSelected>>", lambda _e: self._aplicar_filtros())

        BotaoEstilizado(
            barra_busca,
            text="Filtrar",
            command=self._aplicar_filtros,
            bg=COR_PRIMARIA,
            hover_bg=COR_PRIMARIA_HOVER,
            fg=COR_TEXTO_ESCURO,
        ).pack(side="left", padx=(0, 6))

        BotaoEstilizado(
            barra_busca,
            text="Limpar",
            command=self._limpar_filtros,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="left")

        # Área central com a tabela do acervo
        frame_tabela = tk.Frame(self.root, bg=COR_BORDA, bd=1)
        frame_tabela.pack(fill="both", expand=True, padx=22, pady=4)

        colunas = ("indice", "formato", "titulo", "artista", "ano", "estado", "valor")
        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            style="Groove.Treeview",
            selectmode="browse",
        )

        cabecalhos = {
            "indice": ("#", 48, "center"),
            "formato": ("Formato", 90, "center"),
            "titulo": ("Título do Álbum", 270, "w"),
            "artista": ("Artista", 200, "w"),
            "ano": ("Ano", 75, "center"),
            "estado": ("Conservação", 120, "center"),
            "valor": ("Valor Pago", 115, "e"),
        }
        for col, (texto, largura, alinhamento) in cabecalhos.items():
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=largura, anchor=alinhamento, stretch=(col in ("titulo", "artista")))

        self.tabela.tag_configure("par", background=COR_PAINEL)
        self.tabela.tag_configure("impar", background="#17171E")
        self.tabela.bind("<Double-1>", lambda _e: self._abrir_janela_detalhes())

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Barra inferior de ações CRUD + Wikipedia + Sair
        barra_acoes = tk.Frame(self.root, bg=COR_FUNDO)
        barra_acoes.pack(fill="x", padx=22, pady=(12, 6))

        BotaoEstilizado(
            barra_acoes,
            text="+ Cadastrar Mídia",
            command=self._abrir_janela_cadastro,
            bg=COR_PRIMARIA,
            hover_bg=COR_PRIMARIA_HOVER,
            fg=COR_TEXTO_ESCURO,
        ).pack(side="left", padx=(0, 8))

        BotaoEstilizado(
            barra_acoes,
            text="Ver Ficha Técnica",
            command=self._abrir_janela_detalhes,
            bg=COR_INFO,
            hover_bg=COR_INFO_HOVER,
        ).pack(side="left", padx=(0, 8))

        BotaoEstilizado(
            barra_acoes,
            text="Editar Conservação",
            command=self._abrir_janela_edicao,
            bg=COR_SECUNDARIA,
            hover_bg=COR_SECUNDARIA_HOVER,
        ).pack(side="left", padx=(0, 8))

        BotaoEstilizado(
            barra_acoes,
            text="Pesquisar Wikipedia",
            command=self._acao_pesquisar_wikipedia,
            bg=COR_SECUNDARIA,
            hover_bg=COR_SECUNDARIA_HOVER,
        ).pack(side="left", padx=(0, 8))

        BotaoEstilizado(
            barra_acoes,
            text="Remover Mídia",
            command=self._acao_remover_midia,
            bg=COR_PERIGO,
            hover_bg=COR_PERIGO_HOVER,
        ).pack(side="left")

        BotaoEstilizado(
            barra_acoes,
            text="Sair",
            command=self.root.destroy,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="right")

        # Rodapé de status
        self.var_status = tk.StringVar()
        rodape = tk.Label(
            self.root,
            textvariable=self.var_status,
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            anchor="w",
            padx=22,
            pady=6,
            font=("Segoe UI", 9),
        )
        rodape.pack(fill="x", side="bottom")

    # =========================================================================
    # ATUALIZAÇÃO E FILTRAGEM DA TABELA
    # =========================================================================
    def _atualizar_tabela(self, lista_midias=None):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        if lista_midias is None:
            lista_midias = list(self.acervo._midias)

        self._midias_exibidas = lista_midias

        for pos, midia in enumerate(lista_midias):
            indice_real = self.acervo._midias.index(midia)
            formato = type(midia).__name__
            valor_fmt = f"R$ {midia.registro_compra.valor:.2f}".replace(".", ",")
            tag = "par" if pos % 2 == 0 else "impar"
            self.tabela.insert(
                "",
                "end",
                iid=str(indice_real),
                values=(
                    indice_real,
                    formato,
                    midia.titulo,
                    midia.artista.nome,
                    midia.data_lancamento,
                    midia.estado_conservacao,
                    valor_fmt,
                ),
                tags=(tag,),
            )

        total_acervo = len(self.acervo._midias)
        total_artistas = len(self.acervo._artistas)
        if total_acervo == 0:
            self.var_status.set("Acervo vazio. Clique em '+ Cadastrar Mídia' ou 'Carregar Exemplos'.")
        else:
            self.var_status.set(
                f"Exibindo {len(lista_midias)} de {total_acervo} mídia(s) | "
                f"{total_artistas} artista(s) cadastrado(s) no SQLite."
            )

    def _aplicar_filtros(self):
        termo = self.var_termo_busca.get().strip()
        criterio = self.var_criterio_busca.get()
        formato_escolhido = self.var_filtro_formato.get()

        if termo:
            if criterio == "Título":
                resultados = self.acervo.buscar_por_titulo(termo)
            else:
                resultados = self.acervo.buscar_por_artista(termo)
        else:
            resultados = list(self.acervo._midias)

        if formato_escolhido != "Todos":
            classe_formato = self.MAPA_FORMATOS[formato_escolhido]
            resultados = [m for m in resultados if isinstance(m, classe_formato)]

        self._atualizar_tabela(resultados)

        if not resultados and self.acervo._midias:
            messagebox.showinfo(
                "Busca sem resultados",
                "Nenhuma mídia encontrada com os filtros informados.",
                parent=self.root,
            )

    def _limpar_filtros(self):
        self.var_termo_busca.set("")
        self.var_criterio_busca.set("Título")
        self.var_filtro_formato.set("Todos")
        self._atualizar_tabela()

    def _obter_indice_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning(
                "Nenhuma mídia selecionada",
                "Selecione uma mídia na tabela primeiro.",
                parent=self.root,
            )
            return None
        return int(selecao[0])

    # =========================================================================
    # UTILITÁRIO DE JANELA SECUNDÁRIA (Toplevel)
    # =========================================================================
    def _criar_janela_modal(self, titulo, largura, altura):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.configure(bg=COR_FUNDO)
        janela.resizable(False, False)
        janela.transient(self.root)
        janela.grab_set()

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - largura) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - altura) // 2
        janela.geometry(f"{largura}x{altura}+{max(x, 40)}+{max(y, 40)}")
        return janela

    # =========================================================================
    # JANELA 1: CADASTRAR MÍDIA
    # =========================================================================
    def _abrir_janela_cadastro(self):
        janela = self._criar_janela_modal("Cadastrar Nova Mídia", 470, 560)

        tk.Label(
            janela,
            text="Cadastrar Nova Mídia",
            bg=COR_FUNDO,
            fg=COR_PRIMARIA,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=24, pady=(18, 4))

        tk.Label(
            janela,
            text="Preencha os dados da mídia e do registro de compra.",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SUAVE,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=24, pady=(0, 14))

        form = tk.Frame(janela, bg=COR_PAINEL, padx=20, pady=16)
        form.pack(fill="both", expand=True, padx=24, pady=(0, 14))

        # Formato
        tk.Label(form, text="Formato da Mídia:", bg=COR_PAINEL, fg=COR_TEXTO, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=0, sticky="w", pady=6
        )
        var_formato = tk.StringVar(value="Vinil")
        frame_radios = tk.Frame(form, bg=COR_PAINEL)
        frame_radios.grid(row=0, column=1, sticky="w", pady=6)
        for texto_fmt, val_fmt in [("Vinil", "Vinil"), ("CD", "CD"), ("Fita Cassete (K7)", "K7")]:
            tk.Radiobutton(
                frame_radios,
                text=texto_fmt,
                variable=var_formato,
                value=val_fmt,
                bg=COR_PAINEL,
                fg=COR_TEXTO,
                selectcolor=COR_CARD,
                activebackground=COR_PAINEL,
                activeforeground=COR_PRIMARIA,
                font=("Segoe UI", 9),
            ).pack(side="left", padx=(0, 10))

        def criar_campo(linha, rotulo, default=""):
            tk.Label(form, text=rotulo, bg=COR_PAINEL, fg=COR_TEXTO, font=("Segoe UI", 9, "bold")).grid(
                row=linha, column=0, sticky="w", pady=6
            )
            entrada = tk.Entry(
                form,
                bg=COR_CARD,
                fg=COR_TEXTO,
                insertbackground=COR_PRIMARIA,
                relief="flat",
                font=("Segoe UI", 10),
                width=28,
            )
            entrada.grid(row=linha, column=1, sticky="ew", ipady=5, pady=6)
            if default:
                entrada.insert(0, default)
            return entrada

        ent_titulo = criar_campo(1, "Título do álbum:")
        ent_ano = criar_campo(2, "Ano de lançamento:")
        ent_artista = criar_campo(3, "Nome do artista:")

        lbl_status_artista = tk.Label(
            form,
            text="Digite o nome do artista (agregação)",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            font=("Segoe UI", 8, "italic"),
        )
        lbl_status_artista.grid(row=4, column=1, sticky="w", pady=(0, 4))

        ent_pais = criar_campo(5, "País do artista:")

        # Feedback visual em tempo real para Agregação de Artista
        def verificar_artista(_event=None):
            nome = ent_artista.get().strip()
            if not nome:
                lbl_status_artista.configure(text="Digite o nome do artista", fg=COR_TEXTO_SUAVE)
                ent_pais.configure(state="normal", bg=COR_CARD)
                return

            existente = self.acervo.buscar_artista(nome)
            if existente is not None:
                lbl_status_artista.configure(
                    text=f"✓ Artista já cadastrado — reaproveitando ({existente.pais_origem})",
                    fg="#4ADE80",
                )
                ent_pais.configure(state="normal")
                ent_pais.delete(0, "end")
                ent_pais.insert(0, existente.pais_origem)
                ent_pais.configure(state="disabled", disabledbackground="#181820", disabledforeground=COR_TEXTO_SUAVE)
            else:
                lbl_status_artista.configure(
                    text="Novo artista — informe o país de origem",
                    fg=COR_PRIMARIA,
                )
                if str(ent_pais.cget("state")) == "disabled":
                    ent_pais.configure(state="normal", bg=COR_CARD)
                    ent_pais.delete(0, "end")

        ent_artista.bind("<KeyRelease>", verificar_artista)

        # Estado de conservação
        tk.Label(form, text="Conservação:", bg=COR_PAINEL, fg=COR_TEXTO, font=("Segoe UI", 9, "bold")).grid(
            row=6, column=0, sticky="w", pady=6
        )
        var_estado = tk.StringVar(value="Excelente")
        combo_estado = ttk.Combobox(
            form,
            textvariable=var_estado,
            values=self.OPCOES_CONSERVACAO,
            state="readonly",
            style="Groove.TCombobox",
            width=26,
        )
        combo_estado.grid(row=6, column=1, sticky="ew", pady=6)

        ent_valor = criar_campo(7, "Valor pago (R$):")
        ent_data_prens = criar_campo(8, "Data de prensagem:")
        ent_local_prens = criar_campo(9, "Local de prensagem:")

        form.columnconfigure(1, weight=1)

        def salvar():
            titulo = ent_titulo.get().strip()
            if not titulo:
                messagebox.showerror("Campo obrigatório", "O título do álbum não pode ficar vazio.", parent=janela)
                ent_titulo.focus()
                return

            try:
                ano = int(ent_ano.get().strip())
                if not (1877 <= ano <= 2100):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Ano inválido",
                    "Digite um ano inteiro válido entre 1877 e 2100.",
                    parent=janela,
                )
                ent_ano.focus()
                return

            nome_artista = ent_artista.get().strip()
            if not nome_artista:
                messagebox.showerror("Campo obrigatório", "O nome do artista não pode ficar vazio.", parent=janela)
                ent_artista.focus()
                return

            try:
                valor_float = float(ent_valor.get().strip().replace(",", "."))
                if valor_float < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Valor inválido",
                    "Digite um valor numérico válido e não negativo (ex: 150,00).",
                    parent=janela,
                )
                ent_valor.focus()
                return

            pais = ent_pais.get().strip() or "Desconhecido"
            estado = var_estado.get()
            data_prensagem = ent_data_prens.get().strip()
            local_prensagem = ent_local_prens.get().strip()

            try:
                artista_obj = self.acervo.obter_ou_criar_artista(nome_artista, pais)
                registro = RegistroCompra(valor_float, data_prensagem, local_prensagem)
                classe_midia = self.MAPA_FORMATOS[var_formato.get()]
                nova_midia = classe_midia(titulo, str(ano), artista_obj, estado, registro)
                self.acervo.adicionar_midia(nova_midia)
            except (ValueError, ErroRepositorio) as erro:
                messagebox.showerror("Erro ao salvar", str(erro), parent=janela)
                return

            self._limpar_filtros()
            janela.destroy()
            messagebox.showinfo("Sucesso", f"'{titulo}' cadastrado e salvo no SQLite!", parent=self.root)

        botoes = tk.Frame(janela, bg=COR_FUNDO)
        botoes.pack(fill="x", padx=24, pady=(0, 18))

        BotaoEstilizado(
            botoes,
            text="Salvar Mídia",
            command=salvar,
            bg=COR_PRIMARIA,
            hover_bg=COR_PRIMARIA_HOVER,
            fg=COR_TEXTO_ESCURO,
        ).pack(side="right", padx=(8, 0))

        BotaoEstilizado(
            botoes,
            text="Cancelar",
            command=janela.destroy,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="right")

        ent_titulo.focus()

    # =========================================================================
    # JANELA 2: VER DETALHES / FICHA TÉCNICA
    # =========================================================================
    def _abrir_janela_detalhes(self):
        indice = self._obter_indice_selecionado()
        if indice is None:
            return

        midia = self.acervo._midias[indice]
        formato = type(midia).__name__
        nome_formato = {"Vinil": "Disco de Vinil", "CD": "CD", "K7": "Fita Cassete (K7)"}[formato]

        janela = self._criar_janela_modal(f"Ficha Técnica — {midia.titulo}", 450, 420)

        topo = tk.Frame(janela, bg=COR_PAINEL, padx=22, pady=14)
        topo.pack(fill="x")

        tk.Label(
            topo,
            text=nome_formato.upper(),
            bg=COR_PRIMARIA,
            fg=COR_TEXTO_ESCURO,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
        ).pack(anchor="w")

        tk.Label(
            topo,
            text=midia.titulo,
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(6, 0))

        corpo = tk.Frame(janela, bg=COR_FUNDO, padx=24, pady=14)
        corpo.pack(fill="both", expand=True)

        def linha_info(container, chave, valor):
            row = tk.Frame(container, bg=COR_CARD, padx=12, pady=6)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=chave, bg=COR_CARD, fg=COR_TEXTO_SUAVE, font=("Segoe UI", 9, "bold")).pack(side="left")
            tk.Label(row, text=valor, bg=COR_CARD, fg=COR_TEXTO, font=("Segoe UI", 9)).pack(side="right")

        linha_info(corpo, "Artista (Agregação):", f"{midia.artista.nome} ({midia.artista.pais_origem})")
        linha_info(corpo, "Ano de lançamento:", midia.data_lancamento)
        linha_info(corpo, "Estado de conservação:", midia.estado_conservacao)

        tk.Label(
            corpo,
            text="Registro de Compra (Composição)",
            bg=COR_FUNDO,
            fg=COR_PRIMARIA,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(12, 4))

        reg = midia.registro_compra
        linha_info(corpo, "Valor pago:", f"R$ {reg.valor:.2f}".replace(".", ","))
        linha_info(corpo, "Data de prensagem:", reg.data_prensagem or "Não informada")
        linha_info(corpo, "Local de prensagem:", reg.local_prensagem or "Não informado")

        rodape = tk.Frame(janela, bg=COR_FUNDO, padx=24, pady=12)
        rodape.pack(fill="x")

        BotaoEstilizado(
            rodape,
            text="Abrir na Wikipedia",
            command=lambda: BuscadorFichaTecnica().pesquisar_wikipedia(midia),
            bg=COR_INFO,
            hover_bg=COR_INFO_HOVER,
        ).pack(side="left")

        BotaoEstilizado(
            rodape,
            text="Fechar",
            command=janela.destroy,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="right")

    # =========================================================================
    # JANELA 3: EDITAR ESTADO DE CONSERVAÇÃO
    # =========================================================================
    def _abrir_janela_edicao(self):
        indice = self._obter_indice_selecionado()
        if indice is None:
            return

        midia = self.acervo._midias[indice]
        janela = self._criar_janela_modal("Editar Estado de Conservação", 400, 240)

        tk.Label(
            janela,
            text="Editar Conservação",
            bg=COR_FUNDO,
            fg=COR_PRIMARIA,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=24, pady=(18, 4))

        tk.Label(
            janela,
            text=f"{midia.titulo} — {midia.artista.nome}",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=24, pady=(0, 14))

        painel = tk.Frame(janela, bg=COR_PAINEL, padx=18, pady=14)
        painel.pack(fill="x", padx=24)

        tk.Label(
            painel,
            text="Novo estado de conservação:",
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        var_novo_estado = tk.StringVar(value=midia.estado_conservacao)
        combo = ttk.Combobox(
            painel,
            textvariable=var_novo_estado,
            values=self.OPCOES_CONSERVACAO,
            state="readonly",
            style="Groove.TCombobox",
        )
        combo.pack(fill="x")

        def confirmar_edicao():
            novo_estado = var_novo_estado.get()
            try:
                self.acervo.editar_estado_midia(indice, novo_estado)
            except ErroRepositorio as erro:
                messagebox.showerror("Erro no banco", str(erro), parent=janela)
                return

            self._aplicar_filtros()
            janela.destroy()
            messagebox.showinfo(
                "Atualizado",
                f"Estado de '{midia.titulo}' alterado para '{novo_estado}'.",
                parent=self.root,
            )

        botoes = tk.Frame(janela, bg=COR_FUNDO, padx=24, pady=16)
        botoes.pack(fill="x")

        BotaoEstilizado(
            botoes,
            text="Salvar Alteração",
            command=confirmar_edicao,
            bg=COR_PRIMARIA,
            hover_bg=COR_PRIMARIA_HOVER,
            fg=COR_TEXTO_ESCURO,
        ).pack(side="right", padx=(8, 0))

        BotaoEstilizado(
            botoes,
            text="Cancelar",
            command=janela.destroy,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="right")

    # =========================================================================
    # JANELA 4: LISTAR ARTISTAS (AGREGAÇÃO)
    # =========================================================================
    def _abrir_janela_artistas(self):
        janela = self._criar_janela_modal("Artistas Cadastrados (Agregação)", 520, 380)

        tk.Label(
            janela,
            text="Artistas no Acervo",
            bg=COR_FUNDO,
            fg=COR_PRIMARIA,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=22, pady=(16, 2))

        tk.Label(
            janela,
            text="Artistas existem independentemente das mídias (permanecem mesmo com 0 mídias).",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SUAVE,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=22, pady=(0, 12))

        frame_tree = tk.Frame(janela, bg=COR_BORDA, bd=1)
        frame_tree.pack(fill="both", expand=True, padx=22)

        tree = ttk.Treeview(
            frame_tree,
            columns=("nome", "pais", "qtd"),
            show="headings",
            style="Groove.Treeview",
        )
        tree.heading("nome", text="Artista")
        tree.heading("pais", text="País de Origem")
        tree.heading("qtd", text="Mídias no Acervo")

        tree.column("nome", width=210, anchor="w")
        tree.column("pais", width=150, anchor="w")
        tree.column("qtd", width=110, anchor="center")

        for idx, artista in enumerate(self.acervo._artistas):
            qtd = sum(1 for m in self.acervo._midias if m.artista == artista)
            tag = "par" if idx % 2 == 0 else "impar"
            tree.insert("", "end", values=(artista.nome, artista.pais_origem, qtd), tags=(tag,))

        tree.tag_configure("par", background=COR_PAINEL)
        tree.tag_configure("impar", background="#17171E")
        tree.pack(fill="both", expand=True)

        rodape = tk.Frame(janela, bg=COR_FUNDO, padx=22, pady=12)
        rodape.pack(fill="x")

        BotaoEstilizado(
            rodape,
            text="Fechar",
            command=janela.destroy,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="right")

    # =========================================================================
    # JANELA 5: CONSULTAR BANCO DE DADOS (SQLite)
    # =========================================================================
    def _abrir_janela_banco(self):
        tabelas = self.acervo.consultar_banco()
        if tabelas is None:
            messagebox.showwarning(
                "Sem banco conectado",
                "O acervo não está conectado a um banco SQLite.",
                parent=self.root,
            )
            return

        janela = self._criar_janela_modal("Inspeção do Banco de Dados (SQLite)", 760, 440)

        tk.Label(
            janela,
            text="Tabelas do Banco SQLite (groovemanager.db)",
            bg=COR_FUNDO,
            fg=COR_PRIMARIA,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=22, pady=(16, 10))

        notebook = ttk.Notebook(janela, style="Groove.TNotebook")
        notebook.pack(fill="both", expand=True, padx=22)

        for nome_tabela, (colunas, linhas) in tabelas.items():
            aba = tk.Frame(notebook, bg=COR_PAINEL)
            notebook.add(aba, text=f" {nome_tabela} ({len(linhas)}) ")

            tree = ttk.Treeview(
                aba,
                columns=colunas,
                show="headings",
                style="Groove.Treeview",
            )
            for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, width=max(90, 680 // len(colunas)), anchor="center")

            for idx, linha in enumerate(linhas):
                tag = "par" if idx % 2 == 0 else "impar"
                tree.insert("", "end", values=linha, tags=(tag,))

            tree.tag_configure("par", background=COR_PAINEL)
            tree.tag_configure("impar", background="#17171E")
            tree.pack(fill="both", expand=True, padx=6, pady=6)

        rodape = tk.Frame(janela, bg=COR_FUNDO, padx=22, pady=12)
        rodape.pack(fill="x")

        BotaoEstilizado(
            rodape,
            text="Fechar",
            command=janela.destroy,
            bg=COR_CARD,
            hover_bg=COR_BORDA,
        ).pack(side="right")

    # =========================================================================
    # AÇÕES DIRETAS (REMOVER, EXEMPLOS, WIKIPEDIA)
    # =========================================================================
    def _acao_remover_midia(self):
        indice = self._obter_indice_selecionado()
        if indice is None:
            return

        midia = self.acervo._midias[indice]
        confirmou = messagebox.askyesno(
            "Confirmar remoção",
            f"Deseja remover '{midia.titulo}' ({midia.artista.nome})?\n\n"
            "O registro de compra será apagado junto (Composição), "
            "mas o artista continuará cadastrado (Agregação).",
            parent=self.root,
        )
        if not confirmou:
            return

        try:
            removida = self.acervo.remover_midia(indice)
        except ErroRepositorio as erro:
            messagebox.showerror("Erro no banco", str(erro), parent=self.root)
            return

        self._aplicar_filtros()
        messagebox.showinfo("Removida", f"Mídia '{removida.titulo}' removida com sucesso.", parent=self.root)

    def _acao_carregar_exemplos(self):
        try:
            adicionadas = carregar_dados_exemplo(self.acervo)
        except ErroRepositorio as erro:
            messagebox.showerror("Erro no banco", str(erro), parent=self.root)
            return

        self._limpar_filtros()
        if adicionadas == 0:
            messagebox.showinfo(
                "Dados de exemplo",
                "Os dados de exemplo já estão cadastrados no acervo.",
                parent=self.root,
            )
        else:
            messagebox.showinfo(
                "Dados de exemplo",
                f"{adicionadas} mídia(s) de exemplo carregada(s) no SQLite!",
                parent=self.root,
            )

    def _acao_pesquisar_wikipedia(self):
        indice = self._obter_indice_selecionado()
        if indice is None:
            return

        midia = self.acervo._midias[indice]
        BuscadorFichaTecnica().pesquisar_wikipedia(midia)