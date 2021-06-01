from Flow_v1_be import *
from Flow_v1_fe import *

# Aplicação ------------------------------------------------------------------------------------------------------------
class Flow:
    # Construtor -------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Construtor.
        """
        # Janela principal ---------------------------------------------------------------------------------------------
        self.app = Tk()

        # Icone da janela
        self.icone_64 = Img_ico(0)
        self.icone_decodificado = base64.b64decode(self.icone_64)
        self.arquivo_temporario_icone = "icone_principal.ico"
        self.arquivo_icone = open(self.arquivo_temporario_icone, "wb")
        self.arquivo_icone.write(self.icone_decodificado)
        self.arquivo_icone.close()

        # Dimensões da janela
        self.largura_janela_principal = 1000
        self.altura_janela_principal = 625

        # Frames -------------------------------------------------------------------------------------------------------
        self.frame_0 = Frame(self.app, relief='raised', borderwidth=2)
        self.frame_1 = Frame(self.app, relief='raised', borderwidth=2)
        self.frame_2 = Frame(self.app, relief='raised', borderwidth=2)

        # Frame 0 ------------------------------------------------------------------------------------------------------
        # Dimensões
        self.largura_frame_0 = self.largura_janela_principal-10
        self.altura_frame_0 = 40

        # Figuras dos botões
        self.figuras_botoes_frame_0 = [PhotoImage(data=Img_ico(2)), PhotoImage(data=Img_ico(3)),
                                       PhotoImage(data=Img_ico(4)), PhotoImage(data=Img_ico(8)),
                                       PhotoImage(data=Img_ico(11)), PhotoImage(data=Img_ico(14)),
                                       PhotoImage(data=Img_ico(16)), PhotoImage(data=Img_ico(17))]

        # Comandos dos botões
        self.comandos_botoes_frame_0 = [lambda: self.Acionar_bts_frame_0(0), lambda: self.Acionar_bts_frame_0(1),
                                        lambda: self.Acionar_bts_frame_0(2), lambda: self.Acionar_bts_frame_0(3),
                                        lambda: self.Acionar_bts_frame_0(4), lambda: self.Acionar_bts_frame_0(5),
                                        lambda: self.Acionar_bts_frame_0(6), lambda: self.Acionar_bts_frame_0(7)]

        # Botões
        self.botoes_frame_0 = []
        if len(self.figuras_botoes_frame_0) == len(self.comandos_botoes_frame_0):
            for c in range(0, len(self.comandos_botoes_frame_0)):
                self.botoes_frame_0.append(Button(self.frame_0, image=self.figuras_botoes_frame_0[c],
                                                  command=self.comandos_botoes_frame_0[c]))

        # Frame 1 ------------------------------------------------------------------------------------------------------
        # Dimensões
        self.largura_frame_1 = 210
        self.altura_frame_1 = self.altura_janela_principal-self.altura_frame_0-15

        self.texto_label_frame_1 = ['Identificação da seção transversal', " Nome do corpo d'água:", ' -', ' Localização:', ' -',
                                    ' Nome da seção:', ' -', 'Coleta de dados', ' Data:', ' -', ' Hora de início:',
                                    ' -', ' Hora de término:', ' -']

        self.label_frame_1 = []
        for c in range(0, len(self.texto_label_frame_1)):
            self.label_frame_1.append(Label(self.frame_1, text=self.texto_label_frame_1[c], anchor=W,
                                            font=('arial', 10, 'normal')))

        # Frame 2 ------------------------------------------------------------------------------------------------------
        # Dimensões
        self.largura_frame_2 = self.largura_janela_principal-self.largura_frame_1-15
        self.altura_frame_2 = self.altura_janela_principal-self.altura_frame_0-15

        # Número de elementos
        self.num_label_frame_2 = 448
        self.num_botao_frame_2 = 20
        self.num_entry_frame_2 = 49
        self.num_text_frame_2 = 1

        # Label
        self.label_frame_2 = []
        for c in range(0, self.num_label_frame_2):
            self.label_frame_2.append(Label(self.frame_2, anchor=W, font=('arial', 10, 'normal')))

        # Texto Label Identificação
        self.texto_label_id = ['Arquivo da seção transversal', 'Identificação da seção transversal', 'Coleta de dados',
                               'Hidrometria', 'Topografia', 'Cálculo dos parâmetros hidráulicos',
                               'Extrapolação dos parâmetros', 'Sobre']

        # Figuras label
        self.fig_label = [PhotoImage(data=Img_ico(18)), PhotoImage(data=Img_ico(19)), PhotoImage(data=Img_ico(20))]

        # Entry
        self.entry_frame_2 = []
        for c in range(0, self.num_entry_frame_2):
            self.entry_frame_2.append(Entry(self.frame_2, font=('arial', 10, 'normal')))

        # Text
        self.text_frame_2 = []
        for c in range(0, self.num_text_frame_2):
            self.text_frame_2.append(Text(self.frame_2, font=('arial', 10, 'normal')))

        # Botões
        self.figuras_botoes_frame_2 =[PhotoImage(data=Img_ico(5)), PhotoImage(data=Img_ico(6)),
                                      PhotoImage(data=Img_ico(7)), PhotoImage(data=Img_ico(9)),
                                      PhotoImage(data=Img_ico(10)), PhotoImage(data=Img_ico(12)),
                                      PhotoImage(data=Img_ico(13)), PhotoImage(data=Img_ico(15))]

        self.botoes_frame_2 = []
        for c in range(0, self.num_botao_frame_2):
            self.botoes_frame_2.append(Button(self.frame_2, font=('arial', 10, 'normal')))

        # Comando do botão 0
        self.comandos_botao_0_frame_2 = [lambda: self.Acionar_bt_0_frame_2(0), lambda: self.Acionar_bt_0_frame_2(1),
                                         lambda: self.Acionar_bt_0_frame_2(2), lambda: self.Acionar_bt_0_frame_2(3),
                                         lambda: self.Acionar_bt_0_frame_2(4), lambda: self.Acionar_bt_0_frame_2(5),
                                         lambda: self.Acionar_bt_0_frame_2(6), lambda: self.Acionar_bt_0_frame_2(7)]

        # Radio buttom
        # Tipo de arquivo
        self.radiobuttom_frame_2_arquivo =[]
        for c in range(0, 2):
            self.radiobuttom_frame_2_arquivo.append(Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W))

        # Topografia declividade/margem 0/ margem n
        self.opcao_topo_decli_margem = IntVar()
        self.radiobuttom_frame_2_topo_decli = Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W,
                                                           text='Declividade', value=0, variable=self.opcao_topo_decli_margem,
                                                           command=lambda: self.Exibir_dados_topografia(0))
        self.radiobuttom_frame_2_topo_margem_0= Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W,
                                                           text='Margem 0', value=1, variable=self.opcao_topo_decli_margem,
                                                           command=lambda: self.Exibir_dados_topografia(0))

        self.radiobuttom_frame_2_topo_margem_n = Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W,
                                                             text='Margem n', value=2,
                                                             variable=self.opcao_topo_decli_margem,
                                                             command=lambda: self.Exibir_dados_topografia(0))

        # Topografia teodolito/coordenada/régua
        self.opcao_topo_teo_coord_reg = IntVar()
        self.radiobuttom_frame_2_topo_teo = Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W,
                                                        text='Teodolito', value=0,
                                                        variable=self.opcao_topo_teo_coord_reg,
                                                        command=lambda: self.Exibir_dados_topografia(0))
        self.radiobuttom_frame_2_topo_coord = Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W,
                                                          text='Coordenadas', value=1,
                                                             variable=self.opcao_topo_teo_coord_reg,
                                                             command=lambda: self.Exibir_dados_topografia(0))
        self.radiobuttom_frame_2_topo_reg = Radiobutton(self.frame_2, font=('arial', 10, 'normal'), anchor=W,
                                                          text='Réguas', value=2,
                                                          variable=self.opcao_topo_teo_coord_reg,
                                                          command=lambda: self.Exibir_dados_topografia(0))

        # Variáveis ----------------------------------------------------------------------------------------------------
        self.botao_ativo_frame_0 = 0

        self.opcao_arquivo_secao = 0

        self.diretorio_arquivo_carregado = ''

        self.dados_secao_carregada = ['-', '-', '-', '-', 'False']

        self.pagina_dados_coleta_frame_2 = 0

        self.numero_dados_coleta = -1

        self.id_dado_carregado = -1

        self.numero_dados_hidrometria = 2

        self.pagina_dados_hidrometria_frame_2 = 0

        self.alteracao_vertical_0 = False

        self.alteracao_vertical_n = False

        self.numero_dados_topo_decli_teo = 0

        self.numero_dados_topo_decli_coord = 0

        self.numero_dados_topo_decli_reg = 0

        self.numero_dados_topo_margem_teo = 0

        self.numero_dados_topo_margem_coord = 0

        self.pagina_dados_topografia_frame_2 = 0

        self.pagina_dados_op_declividade_frame_2 = 0

        self.pagina_dados_coord_rel_secao = 0

        return

    # Exibição dos elementos gráficos fixos ----------------------------------------------------------------------------
    def Tela(self):
        """
        Função Tela: Exibe a janela do programa.
        :return: Não retorna valores.
        """

        # Janela principal ---------------------------------------------------------------------------------------------
        self.app.title('Flow')
        self.app.geometry(str(self.largura_janela_principal)+'x'+str(self.altura_janela_principal))
        self.app.resizable(False, False)
        self.app.wm_iconbitmap(self.arquivo_temporario_icone)
        os.remove(self.arquivo_temporario_icone)

        # Frames -------------------------------------------------------------------------------------------------------
        self.frame_0.place(x=5, y=5, width=self.largura_frame_0, height=self.altura_frame_0)
        self.frame_1.place(x=5, y=50, width=self.largura_frame_1, height=self.altura_frame_1)
        self.frame_2.place(x=220, y=50, width=self.largura_frame_2, height=self.altura_frame_2)

        # Frame 0 ------------------------------------------------------------------------------------------------------
        # Botões
        for c in range(0, len(self.botoes_frame_0)):
            self.botoes_frame_0[c].place(x=5+35*c, y=5, width=30, height=30)

        # Frame 1 ------------------------------------------------------------------------------------------------------
        # Labels
        for c in range(0, len(self.label_frame_1)):
            self.label_frame_1[c].place(x=5, y=5+25*c, width=self.largura_frame_1-10, height=20)

        # Frame 2 ------------------------------------------------------------------------------------------------------
        # Label identificação
        self.label_frame_2[0].place(x=5, y=5, width=self.largura_frame_2-10, height=20)

        # Botão de confirmação
        self.botoes_frame_2[0].place(x=self.largura_frame_2-105, y=self.altura_frame_2-35, width=100, height=30)
        self.botoes_frame_2[0].configure(text='Enviar')

    # Exibição dos elementos gráficos variáveis ------------------------------------------------------------------------
    def Acionar_bts_frame_0(self, n_bt):
        """
        Função Acionar_bts_frame_0: Usada para exibir os elementos gráficos do botão correspondente.
        :param n_bt: Número do botão ativado.
        :return: Não retorna valores.
        """
        # Botão frame 0 ativo
        self.botao_ativo_frame_0 = n_bt

        # Função do botão 0 do frame 2
        self.botoes_frame_2[0].configure(command=self.comandos_botao_0_frame_2[n_bt])

        # Label de identificação
        self.label_frame_2[0].configure(text=self.texto_label_id[n_bt])

        # Remoção dos elemntos gráficos presentes
        self.Limpar_frame_2()

        # Status do botão 0 do frame 2
        self.botoes_frame_2[0]['state'] = 'normal'

        # Inserção dos elementos gráficos
        if n_bt == 0:
            # Radio buttom
            self.radiobuttom_frame_2_arquivo[0].place(x=5, y=30, width=self.largura_frame_2-10, height=20)
            self.radiobuttom_frame_2_arquivo[0].configure(text='Nova seção transversal', value=0,
                                                  variable=self.opcao_arquivo_secao, command=lambda: self.Opcao_arquivo_secao(0))

            self.radiobuttom_frame_2_arquivo[1].place(x=5, y=55, width=self.largura_frame_2-10, height=20)
            self.radiobuttom_frame_2_arquivo[1].configure(text='Seção transversal existente', value=1,
                                                  variable=self.opcao_arquivo_secao, command=lambda: self.Opcao_arquivo_secao(1))
            # Opções preliminares
            self.radiobuttom_frame_2_arquivo[self.opcao_arquivo_secao].select()
            self.Opcao_arquivo_secao(self.opcao_arquivo_secao)

        elif n_bt == 1:
            # Caso um arquivo não esteja carregado
            if self.diretorio_arquivo_carregado == '':
                # Label
                self.label_frame_2[4].place(x=5, y=30, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[4].configure(text="Preencha os dados de 'Arquivo da seção transversal' para continuar.")

                # Status do botão 0 do frame 2
                self.botoes_frame_2[0]['state'] = 'disabled'

            # Caso um arquivo esteja carregado
            else:
                # Remoção das notificações de erro
                lista_labels = [5, 6, 7, 8]
                for elemento in lista_labels:
                    self.Notifica_erro(elemento, True)

                # Label
                texto_label = ["  Nome do corpo d'água:", ' Localização:', ' Nome da seção:', ' Descrição:']
                for c in range(0, 4):
                    self.label_frame_2[c+5].place(x=5, y=30+50*c, width=self.largura_frame_2 - 10, height=20)
                    self.label_frame_2[c+5].configure(text=texto_label[c])

                # Entry
                for c in range(0, 3):
                    self.entry_frame_2[c+3].place(x=5, y=55+50*c, width=self.largura_frame_2 - 10, height=20)
                    self.entry_frame_2[c+3].delete(0, END)
                    self.entry_frame_2[c+3].insert(0, self.dados_secao_carregada[c])

                # Text
                self.text_frame_2[0].place(x=5, y=205, width=self.largura_frame_2 - 10, height=100)
                self.text_frame_2[0].delete('1.0', END)
                self.text_frame_2[0].insert('1.0', self.dados_secao_carregada[3])

        elif n_bt == 2:
            # Caso uma seção não esteja carregada
            if self.dados_secao_carregada[4] == 'False':
                # Label
                self.label_frame_2[9].place(x=5, y=30, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[9].configure(
                    text="Preencha os dados de 'Identificação da seção transversal' para continuar.")

                # Status do botão 0 do frame 2
                self.botoes_frame_2[0]['state'] = 'disabled'

            # Caso uma seção esteja carregada
            else:
                # Remoção das notificações de erro
                lista_labels = [54, 55, 56, 57]
                for elemento in lista_labels:
                    self.Notifica_erro(elemento, True)

                # Label 1
                texto_labels = ['Coleta\nnúmero', 'Data\n(dd/mm/aaaa)', 'Hora de início\n(hh:mm)', 'Hora de término\n(hh:mm)']
                for c in range(0, 4):
                    self.label_frame_2[10+c].place(x=5+105*c, y=30, width=100, height=40)
                    self.label_frame_2[10+c].configure(text=texto_labels[c], anchor=S)
                    self.label_frame_2[54+c].place(x=5+105*c, y=self.altura_frame_2-105, width=100, height=40)
                    self.label_frame_2[54+c].configure(text=texto_labels[c], anchor=S)

                    # Entry
                    self.entry_frame_2[6+c].place(x=5+105*c, y=self.altura_frame_2-60, width=100, height=20)

                # Label 2
                self.Exibir_dados_coletas_frame_2(0)

                # Botões
                for c in range(1, 6):
                    self.botoes_frame_2[c].place(x=self.largura_frame_2-105-c*35, y=self.altura_frame_2-35, width=30, height=30)
                self.botoes_frame_2[5].configure(image=self.figuras_botoes_frame_2[2], command=lambda: self.Editar_dado_coleta_1())
                self.botoes_frame_2[4].configure(image=self.figuras_botoes_frame_2[0], command=lambda: self.Excluir_dado_coleta_1())
                self.botoes_frame_2[3].configure(image=self.figuras_botoes_frame_2[1], command=lambda: self.Carregar_coleta_1())
                self.botoes_frame_2[2].configure(text='<<', command=lambda: self.Exibir_dados_coletas_frame_2(-1))
                self.botoes_frame_2[1].configure(text='>>', command=lambda: self.Exibir_dados_coletas_frame_2(1))

        elif n_bt == 3:
            # Caso uma coleta não esteja carregada
            if self.id_dado_carregado == -1:
                # Label
                self.label_frame_2[58].place(x=5, y=30, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[58].configure(
                    text="Preencha os dados de 'Coleta de dados' para continuar.")

                # Status do botão 0 do frame 2
                self.botoes_frame_2[0]['state'] = 'disabled'

            # Caso uma seção esteja carregada
            else:
                # Remoção das notificações de erro
                lista_labels = [60, 61]
                for c in range(184, 197):
                    lista_labels.append(c)
                for elemento in lista_labels:
                    self.Notifica_erro(elemento, True)

                # Equação do molinete
                self.label_frame_2[59].place(x=5, y=30, width=380, height=50)
                self.label_frame_2[59].configure(anchor = CENTER, text='Equação do molinete: v = ar + b\nOnde: v = Velocidade (m/s); r = Velocidade angular;\na e b = Constantes de calibração.')
                self.label_frame_2[60].place(x=390, y=30, width=30, height=20)
                self.label_frame_2[60].configure(text='a: ', anchor=E)
                self.label_frame_2[61].place(x=390, y=55, width=30, height=20)
                self.label_frame_2[61].configure(text='b: ', anchor=E)
                self.entry_frame_2[10].place(x=425, y=30, width=100, height=20)
                self.entry_frame_2[11].place(x=425, y=55, width=100, height=20)

                # Títulos hidrometria 1
                texto_titulo = ['Vertical\nnúmero', 'Distância do\nponto de\nreferência (m)', 'Profundidade\n(m)',
                                'Velocidade angular', 'S', '0.2p', '0.4p', '0.6p', '0.8p', 'F', 'a', 'b']
                for c in range(0, 3):
                    self.label_frame_2[62+c].place(x=5+105*c, y=85, width=100, height=60)
                    self.label_frame_2[62+c].configure(text=texto_titulo[c], anchor=S)

                self.label_frame_2[65].place(x=320, y=100, width=235, height=20)
                self.label_frame_2[65].configure(text=texto_titulo[3], anchor=S)

                for c in range(0, 6):
                    self.label_frame_2[68+c].place(x=320+40*c, y= 125, width=35, height=20)
                    self.label_frame_2[68+c].configure(text=texto_titulo[c+4], anchor=S)

                self.label_frame_2[66].place(x=560, y=85, width=100, height=60)
                self.label_frame_2[66].configure(text=texto_titulo[10], anchor=S)
                self.label_frame_2[67].place(x=665, y=85, width=100, height=60)
                self.label_frame_2[67].configure(text=texto_titulo[11], anchor=S)

                # Títulos hidrometria 2
                for c in range(0, 3):
                    self.label_frame_2[184+c].place(x=5+105*c, y=self.altura_frame_2-125, width=100, height=60)
                    self.label_frame_2[184+c].configure(text=texto_titulo[c], anchor=S)

                self.label_frame_2[187].place(x=320, y=self.altura_frame_2-110, width=235, height=20)
                self.label_frame_2[187].configure(text=texto_titulo[3], anchor=S)

                for c in range(0, 6):
                    self.label_frame_2[188+c].place(x=320+40*c, y= self.altura_frame_2-85, width=35, height=20)
                    self.label_frame_2[188+c].configure(text=texto_titulo[c+4], anchor=S)

                # Entrada dados
                for c in range(0, 3):
                    self.entry_frame_2[12+c].place(x=5+c*105, y=self.altura_frame_2-60, width=100, height=20)
                for c in range(0, 6):
                    self.entry_frame_2[15+c].place(x=320+c*40, y=self.altura_frame_2-60, width=35, height=20)

                # Botões
                for c in range(6, 10):
                    self.botoes_frame_2[c].place(x=self.largura_frame_2-140-(c-6)*35, y=self.altura_frame_2 - 35,
                                                 width=30, height=30)
                self.botoes_frame_2[9].configure(image=self.figuras_botoes_frame_2[4],
                                                 command=lambda: self.Editar_dado_hidrometria_1())
                self.botoes_frame_2[8].configure(image=self.figuras_botoes_frame_2[3],
                                                 command=lambda: self.Excluir_dado_hidrometria_1())
                self.botoes_frame_2[7].configure(text='<<', command=lambda: self.Exibir_dados_hidrometria_frame_2(-1))
                self.botoes_frame_2[6].configure(text='>>', command=lambda: self.Exibir_dados_hidrometria_frame_2(1))

                # Label com dados
                self.Exibir_dados_hidrometria_frame_2(0)

        elif n_bt == 4:
            # Caso uma coleta não esteja carregada
            if self.id_dado_carregado == -1:
                # Label
                self.label_frame_2[197].place(x=5, y=30, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[197].configure(
                    text="Preencha os dados de 'Coleta de dados' para continuar.")

                # Status do botão 0 do frame 2
                self.botoes_frame_2[0]['state'] = 'disabled'

            # Caso uma coleta esteja carregada
            else:
                # Elementos variáveis
                self.Exibir_dados_topografia(0)

                # Elementos fixos
                # Radio buttom declividade/margem
                self.radiobuttom_frame_2_topo_decli.place(x=5, y=30, width=205, height=20)
                self.radiobuttom_frame_2_topo_margem_0.place(x=5, y=55, width=205, height=20)
                self.radiobuttom_frame_2_topo_margem_n.place(x=5, y=80, width=205, height=20)

                # Radio buttom teodolito/coordenadas
                self.radiobuttom_frame_2_topo_teo.place(x=215, y=30, width=205, height=20)
                self.radiobuttom_frame_2_topo_coord.place(x=215, y=55, width=205, height=20)

                # Botões
                for c in range(10, 14):
                    self.botoes_frame_2[c].place(x=self.largura_frame_2-140-(c-10)*35, y=self.altura_frame_2 - 35,
                                                 width=30, height=30)
                self.botoes_frame_2[13].configure(image=self.figuras_botoes_frame_2[6],
                                                 command=lambda: self.Editar_dado_topografia_1())
                self.botoes_frame_2[12].configure(image=self.figuras_botoes_frame_2[5],
                                                 command=lambda: self.Excluir_dado_topografia_1())
                self.botoes_frame_2[11].configure(text='<<', command=lambda: self.Exibir_dados_topografia(-1))
                self.botoes_frame_2[10].configure(text='>>', command=lambda: self.Exibir_dados_topografia(1))

        elif n_bt == 5:
            # Caso uma coleta não esteja carregada
            if self.id_dado_carregado == -1:
                # Label
                self.label_frame_2[294].place(x=5, y=30, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[294].configure(
                    text="Preencha os dados de 'Coleta de dados' para continuar.")

                # Status do botão 0 do frame 2
                self.botoes_frame_2[0]['state'] = 'disabled'

            # Caso uma coleta esteja carregada
            else:
                # Parâmetros
                texto_parametros = [' Largura (m):', ' Perímetro molhado (m):', ' Área molhada (m2):',
                                    ' Raio hidráulico (m):', ' Profundidade média (m):', ' Vazão (m3/s):',
                                    ' Velocidade média (m/s):', ' Declividade T (m/m):', ' Declividade C (m/m):',
                                    ' Declividade R (m/m):', ' Rugosidade de Manning T:', ' Rugosidade de Manning C:',
                                    ' Rugosidade de Manning R:']
                for c in range(0, 7):
                    self.label_frame_2[295+c].place(x=5, y=55+25*c, width=200, height=20)
                    self.label_frame_2[295+c].configure(text=texto_parametros[c], anchor=W)
                    self.label_frame_2[302+c].place(x=210, y=55 + 25 * c, width=200, height=20)

                for c in range(0, 6):
                    if c < 3:
                        y=0
                    else:
                        y=25
                    self.label_frame_2[309+c].place(x=315, y=55+25*c+y, width=200, height=20)
                    self.label_frame_2[309+c].configure(text=texto_parametros[c+7], anchor=W)
                    self.label_frame_2[315+c].place(x=520, y=55+25*c+y, width=200, height=20)

                self.label_frame_2[321].place(x=5, y=30, width=305, height=20)
                self.label_frame_2[321].configure(text='Hidrometria', anchor = W)
                self.label_frame_2[322].place(x=315, y=30, width=305, height=20)
                self.label_frame_2[322].configure(text='Topografia', anchor=W)
                self.label_frame_2[323].place(x=315, y=130, width=305, height=20)
                self.label_frame_2[323].configure(text='Hidrometria + Topografia', anchor=W)

                # Detalhamento das declividades e rugosidade
                self.label_frame_2[324].place(x=5, y=235, width=455, height = 20)
                self.label_frame_2[324].configure(text='Detalhamento da declividade e da rugosidade')

                texto_detalhes = ['Método', 'Pontos/Réguas', 'Declividade (m/m)', 'Rugosidade']

                for c in range(0, 4):
                    self.label_frame_2[325+c].place(x=5+115*c, y=260, width=110, height=20)
                    self.label_frame_2[325+c].configure(text=texto_detalhes[c], anchor =CENTER)

                for c0 in range(0, 10):
                    for c1 in range(0, 4):
                        self.label_frame_2[329+4*c0+c1].place(x=5+115*c1, y=285+25*c0, width=110, height=20)

                # Botões
                for c in range(14, 17):
                    self.botoes_frame_2[c].place(x=self.largura_frame_2-140-(c-14)*35, y=self.altura_frame_2 - 35,
                                                 width=30, height=30)
                self.botoes_frame_2[16].configure(image=self.figuras_botoes_frame_2[7] ,command=lambda: self.Janela_salvar_parametros())
                self.botoes_frame_2[15].configure(text='<<', command=lambda: self.Exibir_parametros(-1))
                self.botoes_frame_2[14].configure(text='>>', command=lambda: self.Exibir_parametros(1))

                self.Exibir_parametros(0)

        elif n_bt == 6:
            # Caso uma coleta não esteja carregada, nem hidrometria
            hidro_editada = Verificar_hidrometria(self.diretorio_arquivo_carregado, self.id_dado_carregado)
            if self.id_dado_carregado == -1 or hidro_editada == False:
                # Label
                self.label_frame_2[369].place(x=5, y=30, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[369].configure(text="Preencha os dados de 'Hidrometria' para continuar.")
                self.label_frame_2[382].place(x=5, y=55, width=self.largura_frame_2 - 10, height=20)
                self.label_frame_2[382].configure(text="É recomendado preencher também 'Topografia - Margem 0' e 'Topografia - Margem n'")

                # Status do botão 0 do frame 2
                self.botoes_frame_2[0]['state'] = 'disabled'

            # Caso uma coleta esteja carregada
            else:
                # Remoção das notificações de erro
                for c in range(370, 383):
                    self.Notifica_erro(c, True)

                n_intervalos = Intervalos_decli_rug(self.diretorio_arquivo_carregado)
                textos_dados_extrapolacao = [' Declividade mínima (m/m):', 'Declividade máxima (m/m):',
                                             'Incremento de declividade:', f'Intervalo observado\nna seção (m/m)\n{n_intervalos[0][0]} a {n_intervalos[0][1]}',
                                             ' Rugosidade mínima:', 'Rugosidade máxima:', 'Incremento de rugosidade:',
                                              f'Intervalo observado\nna seção\n{n_intervalos[1][0]} a {n_intervalos[1][1]}']

                for c0 in range(0, 2):
                    for c1 in range(0, 4):
                        if c1 < 3:
                            self.label_frame_2[370+4*c0+c1].place(x=5+175*c1, y=30+50*c0, width=170, height=20)
                            self.label_frame_2[370+4*c0+c1].configure(text=textos_dados_extrapolacao[c0*4+c1])
                            self.entry_frame_2[41+3*c0+c1].place(x=5+175*c1, y=55+50*c0, width=170, height=20)
                        else:
                            self.label_frame_2[370+4*c0+c1].place(x=5+175*c1, y=30 + 50 * c0, width=170, height=45)
                            self.label_frame_2[370+4*c0+c1].configure(text=textos_dados_extrapolacao[c0*4+c1], anchor=CENTER)


                self.label_frame_2[378].place(x=5, y= 135, width= self.largura_frame_2-10, height=20)
                self.label_frame_2[378].configure(text='Obter dados da extrapolação')

                texto_obter_arq = [' *Nome dos arquivos:', ' Salvar em:']

                for c in range(0, 2):
                    self.label_frame_2[379+c].place(x=5, y=160+50*c, width=self.largura_frame_2-10, height=20)
                    self.label_frame_2[379+c].configure(text=texto_obter_arq[c])
                    self.entry_frame_2[47+c].place(x=5, y=185+50*c, width=self.largura_frame_2-10, height=20)

                self.label_frame_2[381].place(x=5, y=260, width=self.largura_frame_2-10, height=40)
                self.label_frame_2[381].configure(anchor = W, font =('arial', 8, 'normal'), text=' *De acordo com os intervalos de declividade e rugosidade adotados, poderão ser gerados um ou mais arquivos, nomeados de acordo\ncom o nome inserido, a técnica de levantamento topográfico e um sufixo referente à declividade e a rugosidade analisada.')

                self.label_frame_2[382].place(x=5, y=305, width=735, height= 20)
                self.label_frame_2[382].configure(text='Coordenadas relativas da forma da seção transversal')

                for c in range(17, 20):
                    self.botoes_frame_2[c].place(x=self.largura_frame_2 - 140 - (c - 17) * 35,
                                                 y=self.altura_frame_2 - 35,
                                                 width=30, height=30)
                self.botoes_frame_2[19].configure(image=self.figuras_botoes_frame_2[7],
                                                  command=lambda: self.Salvar_extrapolacao())
                self.botoes_frame_2[18].configure(text='<<', command=lambda: self.Exibir_coordenadas_rel_secao(-1))
                self.botoes_frame_2[17].configure(text='>>', command=lambda: self.Exibir_coordenadas_rel_secao(1))

                self.Exibir_coordenadas_rel_secao(0)

        elif n_bt == 7:
            # Labels
            texto_labels = [' Flow é o resultado da iniciação científica realizada em 2020/2021 por Diniz Ferrarezi Neto',
                            ' orientado pelo Prof. Dr. André Luís Sotero Salustiano Martim.',
                            ' O uso do programa é livre, sendo o mesmo direcionado ao cálculo de parâmetros hidráulicos de',
                            ' seções transversais de rios e canais.',
                            '',
                            f' Agradecimentos: Serviço de Apoio ao Estudante (SAE).',
                            f'                           Universidade Estadual de Campinas (UNICAMP).',
                            f'                           Faculdade de Engenharia Civil, Arquitetura e Urbanismo (FEC).']
            for c in range(0, len(texto_labels)):
                self.label_frame_2[437+c].place(x=5, y=30+c*25, width=self.largura_frame_2-10, height=20)
                self.label_frame_2[437+c].configure(text=texto_labels[c])

            # Figura logos
            self.label_frame_2[445].configure(image=self.fig_label[0])
            self.label_frame_2[446].configure(image=self.fig_label[1])
            self.label_frame_2[447].configure(image=self.fig_label[2])
            self.label_frame_2[445].place(x=52, y=30+25*len(texto_labels), width=235, height= 100)
            self.label_frame_2[446].place(x=337, y=30 + 25 * len(texto_labels), width=100, height=100)
            self.label_frame_2[447].place(x=532, y=30 + 25 * len(texto_labels), width=148, height=100)

            # Status do botão 0 do frame 2
            self.botoes_frame_2[0]['state'] = 'disabled'

        return

    # Validação dos dados inseridos e conexão com o backend ------------------------------------------------------------
    def Acionar_bt_0_frame_2(self, n_bt):
        """
        Função Acionar_bt_0_frame_2: Faz a validação dos dados inseridos, assim como a conexão com a função backend.
        :param n_bt: Número do botão do frame 0 ativo.
        :return: Não retorna valores.
        """
        if n_bt == 0:
            # Descarregar coleta
            self.Carregar_coleta_1(fora=True)

            # Validação das entradas

            # Novo arquivo
            validade = []
            if self.opcao_arquivo_secao == 0:
                validade.append(Validacao_Entradas('str', str(self.entry_frame_2[0].get()).strip()))
                validade.append(Validacao_Entradas('dir', str(self.entry_frame_2[1].get()).strip()))
                self.Notifica_erro(1, validade[0])
                self.Notifica_erro(2, validade[1])

            # Arquivo existente
            else:
                validade.append(Validacao_Entradas('.db', str(self.entry_frame_2[2].get()).strip()))
                self.Notifica_erro(3, validade[0])

            # Função Backend em caso de entradas válidas
            if False not in validade:
                # Criação de um novo arquivo
                if self.opcao_arquivo_secao == 0:
                    exito = Criar_arquivo_db(str(self.entry_frame_2[1].get()).strip(), str(self.entry_frame_2[0].get()).strip())
                    self.Notifica_erro(1, exito)

                    # Determinação do diretório
                    if exito:
                        self.diretorio_arquivo_carregado = str(self.entry_frame_2[1].get()).strip() +'\ '.strip() +\
                                                           str(self.entry_frame_2[0].get()).strip() + '.db'
                        self.entry_frame_2[2].delete(0, END)
                        self.entry_frame_2[2].insert(0, self.diretorio_arquivo_carregado)

                        self.entry_frame_2[0].delete(0, END)
                        self.entry_frame_2[1].delete(0, END)

                        self.radiobuttom_frame_2_arquivo[1].select()
                        self.Opcao_arquivo_secao(1)

                        # Tentativa de carregar a seção
                        self.Carregar_secao_transversal_1()
                # Arquivo existente
                else:
                    self.diretorio_arquivo_carregado = str(self.entry_frame_2[2].get()).strip()

                    # Tentativa de carregar a seção
                    self.Carregar_secao_transversal_1()

        elif n_bt == 1:
            # Validação das entradas
            validade = []
            # Entry
            for c in range(0, 3):
                validade.append(Validacao_Entradas('sstr', str(self.entry_frame_2[c+3].get()).strip()))
                self.Notifica_erro(c+5, validade[c])

            # Text
            validade.append(Validacao_Entradas('sstr', str(self.text_frame_2[0].get('1.0', END)).strip()))
            self.Notifica_erro(8, validade[3])

            # Caso as entradas sejam válidas
            if False not in validade:
                # Alterar informações do banco de dados

                Alterar_info_secao(self.diretorio_arquivo_carregado, str(self.entry_frame_2[3].get()).strip(),
                                   str(self.entry_frame_2[4].get()).strip(), str(self.entry_frame_2[5].get()).strip(),
                                   str(self.text_frame_2[0].get('1.0', END)).strip(), 'True')

                # Carregar seção
                self.Carregar_secao_transversal_1()

        elif n_bt == 2:
            # Validação das entradas
            validade = []
            verificacoes = ['int+', 'data', 'hora', 'hora']

            for c in range(0, 4):
                validade.append(Validacao_Entradas(verificacoes[c], str(self.entry_frame_2[6+c].get()).strip()))
                self.Notifica_erro(54+c, validade[c])

            if False not in validade:
                if int(self.entry_frame_2[6].get()) < self.numero_dados_coleta:
                    validade[0] = False
                    self.Notifica_erro(54, validade[0])

            # Inserção no banco de dados
            if False not in validade:
                # 2 Verificação
                h_i = int(str(self.entry_frame_2[8].get()).replace(':', ''))
                h_t = int(str(self.entry_frame_2[9].get()).replace(':', ''))

                if h_t < h_i:
                    self.Notifica_erro(56, False)
                    self.Notifica_erro(57, False)
                else:
                    Inserir_dado_coleta(self.diretorio_arquivo_carregado, str(self.entry_frame_2[7].get()).strip(),
                                        str(self.entry_frame_2[8].get()).strip(), str(self.entry_frame_2[9].get()).strip())

                    self.Exibir_dados_coletas_frame_2(0)

        elif n_bt == 3:
            # Validação das entradas
            validade = []
            conjunto_labels = [60, 61, 184, 185, 186]
            alteracoes_v_angular = []
            opcoes_calculo_velocidade = [[False, False, False, True, False, False],
                                         [False, True, False, False, True, False],
                                         [False, True, False, True, True, False],
                                         [False, True, True, True, True, False],
                                         [True, True, True, True, True, True]]
            insercao_fim = True

            for c in range(0, 11):
                if c < 2 or (c > 2 and c < 5):
                    validade.append(Validacao_Entradas('float+', str(self.entry_frame_2[c+10].get()).replace(',', '.').strip()))
                    self.Notifica_erro(conjunto_labels[c], validade[c])


                elif c == 2:
                    validade.append(Validacao_Entradas('int+', str(self.entry_frame_2[c+10].get()).strip()))
                    if validade[c]:
                        if int(self.entry_frame_2[c + 10].get()) == 0 or int(self.entry_frame_2[c + 10].get()) > self.numero_dados_hidrometria - 1:
                            validade[c] = False

                        if self.numero_dados_hidrometria - 1 != int(self.entry_frame_2[c + 10].get()):
                            insercao_fim = False

                    self.Notifica_erro(conjunto_labels[c], validade[c])

                else:
                    # Verificação dos valores das entradas
                    if str(self.entry_frame_2[c+10].get()).strip() != '':
                        validade.append(Validacao_Entradas('float+', str(self.entry_frame_2[c+10].get()).replace(',', '.').strip()))
                        self.Notifica_erro(183+c, validade[c])
                        alteracoes_v_angular.append(True)
                    else:
                        validade.append(True)
                        alteracoes_v_angular.append(False)
                    self.Notifica_erro(183+c, validade[c])

            if alteracoes_v_angular in opcoes_calculo_velocidade:
                validade.append(True)
            else:
                validade.append(False)
            self.Notifica_erro(187, validade[11])

            # Alteração das distâncias 0 e n
            validade.append(self.alteracao_vertical_0)
            validade.append(self.alteracao_vertical_n)

            if False not in validade:
                Inserir_dados_hidrometria(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                          str(self.entry_frame_2[12].get()).strip(), str(self.entry_frame_2[13].get().replace(',','.').strip()),
                                          str(self.entry_frame_2[14].get().replace(',','.')).strip(), str(self.entry_frame_2[15].get()).strip(),
                                          str(self.entry_frame_2[16].get()).strip(), str(self.entry_frame_2[17].get()).strip(),
                                          str(self.entry_frame_2[18].get()).strip(), str(self.entry_frame_2[19].get()).strip(),
                                          str(self.entry_frame_2[20].get()).strip(), str(self.entry_frame_2[10].get().replace(',','.')).strip(),
                                          str(self.entry_frame_2[11].get().strip().replace(',','.')), insercao_fim)

                self.Exibir_dados_hidrometria_frame_2(0)

        elif n_bt == 4:
            dados_inserir = []
            # Teodolito
            if self.opcao_topo_teo_coord_reg.get() == 0:
                # Declividade
                if self.opcao_topo_decli_margem.get() == 0:
                    # Validação das entradas
                    validade = []
                    str_validacao = ['int+', 't_decli', 'float+', 'float+', 'float+', 'ang', 'ang', 'float+']

                    for c in range(0, 8):
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[c+21].get()).replace(',','.').strip()))
                        if c == 0 and validade[0]:
                            if int(self.entry_frame_2[21].get()) >= self.numero_dados_topo_decli_teo + 1:
                                validade[0] = False

                        if c == 5 and validade[5]:
                            if int(str(self.entry_frame_2[c+21].get()).replace(' ', '')) > 1800000:
                                validade[c] = False

                        self.Notifica_erro(286+c, validade[c])

                    if validade[2] and validade[3] and validade[4]:
                        # fi fm fs
                        fi = float(str(self.entry_frame_2[23].get()).replace(',', '.'))
                        fm = float(str(self.entry_frame_2[24].get()).replace(',', '.'))
                        fs = float(str(self.entry_frame_2[25].get()).replace(',', '.'))

                        if fi >= fm or fi >= fs or fm >= fs or f'{fm-fi:.3f}' != f'{fs-fm:.3f}':
                            for c in range(0, 3):
                                validade[c+2] = False
                                self.Notifica_erro(288 + c, validade[c+2])
                        else:
                            for c in range(0, 3):
                                validade[c+2] = True
                                self.Notifica_erro(288 + c, validade[c+2])

                    if False not in validade:
                        for c in range(0, 8):
                            dados_inserir.append(str(self.entry_frame_2[21+c].get()).replace(',','.'))

                # Margem
                else:
                    # Validação das entradas
                    validade = []
                    str_validacao = ['int+', 'null', 'float+', 'float+', 'float+', 'ang', 'ang', 'float+']

                    for c in range(0, 8):
                        validade.append(Validacao_Entradas(str_validacao[c],
                                                           str(self.entry_frame_2[c + 21].get()).replace(',', '.').strip()))
                        if c == 0 and validade[0]:
                            if int(self.entry_frame_2[21].get()) >= self.numero_dados_topo_margem_teo + 1:
                                validade[0] = False

                        if c == 5 and validade[5]:
                            if int(str(self.entry_frame_2[c+21].get()).replace(' ', '')) > 1800000:
                                validade[c] = False

                        self.Notifica_erro(286 + c, validade[c])

                    if validade[2] and validade[3] and validade[4]:
                        # fi fm fs
                        fi = float(str(self.entry_frame_2[23].get()).replace(',', '.'))
                        fm = float(str(self.entry_frame_2[24].get()).replace(',', '.'))
                        fs = float(str(self.entry_frame_2[25].get()).replace(',', '.'))

                        if fi >= fm or fi >= fs or fm >= fs or f'{fm - fi:.3f}' != f'{fs - fm:.3f}':
                            for c in range(0, 3):
                                validade[c + 2] = False
                                self.Notifica_erro(288 + c, validade[c + 2])
                        else:
                            for c in range(0, 3):
                                validade[c + 2] = True
                                self.Notifica_erro(288 + c, validade[c + 2])

                    if False not in validade:
                        for c in range(0, 8):
                            if c != 1:
                                dados_inserir.append(str(self.entry_frame_2[21 + c].get()).replace(',', '.').strip())

            # Coordenada
            elif self.opcao_topo_teo_coord_reg.get() == 1:
                # Declividade
                if self.opcao_topo_decli_margem.get() == 0:
                    # Validação das entradas
                    validade = []
                    str_validacao = ['int+', 't_decli', 'float', 'float', 'float']
                    for c in range(0, 5):
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[29+c].get()).replace(',', '.').strip()))
                        self.Notifica_erro(286+c, validade[c])

                    if validade[0]:
                        if int(self.entry_frame_2[29].get()) >= self.numero_dados_topo_decli_coord + 1:
                            validade[0] = False
                            self.Notifica_erro(286, validade[0])

                    if False not in validade:
                        for c in range(0, 5):
                            dados_inserir.append(str(self.entry_frame_2[29+c].get()).replace(',','.').strip())

                # Margem
                else:
                    # Validação das entradas
                    validade = []
                    str_validacao = ['int+', 'null', 'float', 'float', 'float']
                    for c in range(0, 5):
                        validade.append(Validacao_Entradas(str_validacao[c],
                                                           str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip()))
                        self.Notifica_erro(286 + c, validade[c])

                    if validade[0]:
                        if int(self.entry_frame_2[29].get()) >= self.numero_dados_topo_margem_coord + 1:
                            validade[0] = False
                            self.Notifica_erro(286, validade[0])

                    if False not in validade:
                        for c in range(0, 5):
                            if c != 1:
                                dados_inserir.append(str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip())

            # Réguas
            elif self.opcao_topo_teo_coord_reg.get() == 2:
                # Declividade
                if self.opcao_topo_decli_margem.get() == 0:
                    # Validação das entradas
                    validade = []
                    str_validacao = ['int+', 't_decli', 'float+', 'float', 'float', 'float']
                    for c in range(0, 6):
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[34+c].get()).replace(',', '.').strip()))
                        self.Notifica_erro(286+c, validade[c])

                    if validade[0]:
                        if int(self.entry_frame_2[34].get()) >= self.numero_dados_topo_decli_reg + 1:
                            validade[0] = False
                            self.Notifica_erro(286, validade[0])

                    if False not in validade:
                        for c in range(0, 6):
                            dados_inserir.append(str(self.entry_frame_2[34+c].get()).replace(',','.').strip())


            if False not in validade:
                Inserir_dado_topografia(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                        self.opcao_topo_decli_margem.get(), self.opcao_topo_teo_coord_reg.get(),
                                        dados_inserir)

                self.Exibir_dados_topografia(0)

        elif n_bt == 5:
            # Cálculo dos parâmetros
            Calcula_parametros_h(self.diretorio_arquivo_carregado, self.id_dado_carregado)
            Calcula_parametros_t(self.diretorio_arquivo_carregado, self.id_dado_carregado)

            self.Exibir_parametros(0)

        elif n_bt == 6:
            # Calculo das coordenadas da seção
            Determinar_coordenadas_rel_secao(self.diretorio_arquivo_carregado, self.id_dado_carregado)
            self.Exibir_coordenadas_rel_secao(0)

        return

    # Funções auxiliares -----------------------------------------------------------------------------------------------
    def Carregar_coleta_1(self, fora=False):
        """
        Função Carregar_coleta_1: Usada para carregar uma coleta.
        :param fora: Se a função está sendo aplicada sem acionar o botão de carregar coleta.
        :return: Não retorna valores.
        """
        # Dados de hidrometria

        if fora:
            self.id_dado_carregado = -1
            self.label_frame_1[9].configure(text='-')
            self.label_frame_1[11].configure(text='-')
            self.label_frame_1[13].configure(text='-')

        else:
            # Validação da entrada
            validade = Validacao_Entradas('int+', str(self.entry_frame_2[6].get()).strip())
            if validade:
                if int(self.entry_frame_2[6].get()) >= self.numero_dados_coleta:
                    validade = False
            self.Notifica_erro(54, validade)
            self.Notifica_erro(55, True)
            self.Notifica_erro(56, True)
            self.Notifica_erro(57, True)

            if validade:
                # Carregar coleta
                dados_coleta=Carregar_coleta(self.diretorio_arquivo_carregado, int(self.entry_frame_2[6].get()))
                self.id_dado_carregado = dados_coleta[3]
                self.label_frame_1[9].configure(text=dados_coleta[0])
                self.label_frame_1[11].configure(text=dados_coleta[1])
                self.label_frame_1[13].configure(text=dados_coleta[2])

        return

    def Carregar_secao_transversal_1(self):
        """
        Função Carregar_secao_transversal_1: Usada para carregar a seção transversal.
        :return: Não retorna valores.
        """
        self.dados_secao_carregada = Carregar_secao_transversal(self.diretorio_arquivo_carregado)
        if self.dados_secao_carregada[4] == 'True':
            self.label_frame_1[2].configure(text=self.dados_secao_carregada[0])
            self.label_frame_1[4].configure(text=self.dados_secao_carregada[1])
            self.label_frame_1[6].configure(text=self.dados_secao_carregada[2])
        else:
            self.label_frame_1[2].configure(text='-')
            self.label_frame_1[4].configure(text='-')
            self.label_frame_1[6].configure(text='-')

        return

    def Editar_dado_coleta_1(self):
        """
        Função Editar_dado_coleta_1: Usada para editar os dados de uma coleta.
        :return: Não retorna valores
        """
        # Validação das entradas
        validade = []
        verificacoes = ['int+', 'data', 'hora', 'hora']
        alteracoes = [False, False, False]

        validade.append(Validacao_Entradas('int+', str(self.entry_frame_2[6].get()).strip()))
        if validade[0]:
            if int(self.entry_frame_2[6].get()) >= self.numero_dados_coleta:
                validade[0] = False
        self.Notifica_erro(54, validade[0])

        for c in range(1, 4):
            if str(self.entry_frame_2[6 + c].get()).strip() != '':
                validade.append(Validacao_Entradas(verificacoes[c], str(self.entry_frame_2[6 + c].get()).strip()))
                if validade[c]:
                    alteracoes[c-1] = True
            else:
                validade.append(True)

            self.Notifica_erro(54 + c, validade[c])

        # Editar dado
        if False not in validade:
            compara_id = Editar_dado_coleta(self.diretorio_arquivo_carregado, int(self.entry_frame_2[6].get()),
                               str(self.entry_frame_2[7].get()).strip(), str(self.entry_frame_2[8].get()).strip(),
                               str(self.entry_frame_2[9].get()).strip(), self.id_dado_carregado, alteracoes)

            if compara_id:
                self.Carregar_coleta_1()

        self.Exibir_dados_coletas_frame_2(0)

        return

    def Editar_dado_hidrometria_1(self):
        """
        Função Editar_dado_hidrometria_1: Usanda para auxiliar na edição de um dado de hidrometria.
        :return: Não retorna valores.
        """
        # Validação das entradas
        validade = []
        entrada_vertical = str(self.entry_frame_2[12].get()).strip()

        # Edição distâncias vertival 0 e n
        if entrada_vertical == '0' or entrada_vertical == 'n':
            validade.append(Validacao_Entradas('float+', str(self.entry_frame_2[13].get()).replace(',','.').strip()))
            self.Notifica_erro(60, True)
            self.Notifica_erro(61, True)
            self.Notifica_erro(184, True)
            self.Notifica_erro(185, validade[0])
            for c in range(186, 197):
                self.Notifica_erro(c, True)

            if False not in validade:
                # Alterar dado no banco
                Editar_dado_hidrometria(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                              str(self.entry_frame_2[12].get()).strip(),
                                        str(self.entry_frame_2[13].get().replace(',','.')).strip(), 0, '', '', '', '',
                                        '', '', 0, 0)

                self.Exibir_dados_hidrometria_frame_2(0)

        # Edição demais elementos
        else:
            conjunto_labels = [60, 61, 184, 185, 186]
            alteracoes_v_angular = []
            opcoes_calculo_velocidade = [[False, False, False, True, False, False],
                                         [False, True, False, False, True, False],
                                         [False, True, False, True, True, False],
                                         [False, True, True, True, True, False],
                                         [True, True, True, True, True, True]]
            alteracoes = []

            # Validação das entradas
            for c in range(0, 11):
                if c < 2 or (c > 2 and c < 5):
                    entrada_dado = str(self.entry_frame_2[c + 10].get()).replace(',', '.').strip()
                    if entrada_dado!= '':
                        validade.append(Validacao_Entradas('float+', entrada_dado))
                        self.Notifica_erro(conjunto_labels[c], validade[c])
                        alteracoes.append(True)
                    else:
                        validade.append(True)
                        self.Notifica_erro(conjunto_labels[c], validade[c])
                        alteracoes.append(False)


                elif c == 2:
                    validade.append(Validacao_Entradas('int+', str(self.entry_frame_2[c + 10].get()).strip()))
                    if validade[c]:
                        if int(self.entry_frame_2[c + 10].get()) > self.numero_dados_hidrometria-2:
                            validade[c] = False

                    self.Notifica_erro(conjunto_labels[c], validade[c])
                    alteracoes.append(False)

                else:
                    # Verificação dos valores das entradas
                    if str(self.entry_frame_2[c + 10].get()).strip() != '':
                        validade.append(
                            Validacao_Entradas('float+', str(self.entry_frame_2[c + 10].get()).replace(',', '.').strip()))
                        self.Notifica_erro(183 + c, validade[c])
                        alteracoes_v_angular.append(True)
                    else:
                        validade.append(True)
                        alteracoes_v_angular.append(False)
                    self.Notifica_erro(183 + c, validade[c])
                    alteracoes.append(True)

            if alteracoes_v_angular in opcoes_calculo_velocidade:
                validade.append(True)
            else:
                validade.append(False)
            self.Notifica_erro(187, validade[11])

            if False not in validade:
                # Alterar dado no banco
                Editar_dado_hidrometria(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                              str(self.entry_frame_2[12].get()).strip(), str(self.entry_frame_2[13].get().replace(',','.')).strip(),
                                              str(self.entry_frame_2[14].get().replace(',','.')).strip(), str(self.entry_frame_2[15].get()).strip(),
                                              str(self.entry_frame_2[16].get()).strip(), str(self.entry_frame_2[17].get()).strip(),
                                              str(self.entry_frame_2[18].get()).strip(), str(self.entry_frame_2[19].get()).strip(),
                                              str(self.entry_frame_2[20].get()).strip(), str(self.entry_frame_2[10].get().replace(',','.')).strip(),
                                              str(self.entry_frame_2[11].get()).strip().replace(',','.'), alteracoes)

                self.Exibir_dados_hidrometria_frame_2(0)

        return

    def Editar_dado_topografia_1(self):
        """
        Função Editar_dado_topografia_1: Usada para editar um dado de topografia.
        :return: Não retorna valores.
        """
        dados_inserir = []
        alteracao = []
        validade = []
        # Teodolito
        if self.opcao_topo_teo_coord_reg.get() == 0:
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                # Validação das entradas
                str_validacao = ['int+', 't_decli', 'float+', 'float+', 'float+', 'ang', 'ang', 'float+']

                for c in range(0, 8):
                    if str(self.entry_frame_2[c + 21].get()).replace(',', '.').strip() == '' and c != 0:
                        validade.append(True)
                        alteracao.append(False)
                    else:
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[c + 21].get()).replace(',', '.').strip()))
                        alteracao.append(True)
                        if c == 0 and validade[0]:
                            if int(self.entry_frame_2[21].get()) >= self.numero_dados_topo_decli_teo:
                                validade[0] = False

                        self.Notifica_erro(286 + c, validade[c])

                if False not in validade:
                    for c in range(0, 8):
                        dados_inserir.append(str(self.entry_frame_2[21 + c].get()).replace(',', '.').strip())

            # Margem
            else:
                # Validação das entradas
                str_validacao = ['int+', 'null', 'float+', 'float+', 'float+', 'ang', 'ang', 'float+']

                for c in range(0, 8):
                    if (str(self.entry_frame_2[c + 21].get()).replace(',', '.').strip() == '' and c != 0) or c == 1:
                        validade.append(True)
                        alteracao.append(False)
                    else:
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[c + 21].get()).replace(',', '.').strip()))
                        alteracao.append(True)
                        if c == 0 and validade[0]:
                            if int(self.entry_frame_2[21].get()) >= self.numero_dados_topo_margem_teo:
                                validade[0] = False

                        self.Notifica_erro(286 + c, validade[c])

                if False not in validade:
                    for c in range(0, 8):
                        if c != 1:
                            dados_inserir.append(str(self.entry_frame_2[21 + c].get()).replace(',', '.').strip())
                        else:
                            dados_inserir.append('')

        # Coordenada
        elif self.opcao_topo_teo_coord_reg.get() == 1:
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                # Validação das entradas
                str_validacao = ['int+', 't_decli', 'float', 'float', 'float']
                for c in range(0, 5):
                    if str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip() == '' and c != 0:
                        validade.append(True)
                        alteracao.append(False)
                    else:
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip()))
                        alteracao.append(True)
                        self.Notifica_erro(286 + c, validade[c])

                if validade[0]:
                    if int(self.entry_frame_2[29].get()) >= self.numero_dados_topo_decli_coord:
                        validade[0] = False
                        self.Notifica_erro(286, validade[0])

                if False not in validade:
                    for c in range(0, 5):
                        dados_inserir.append(str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip())

            # Margem
            else:
                # Validação das entradas
                str_validacao = ['int+', 'null', 'float', 'float', 'float']
                for c in range(0, 5):
                    if (str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip() == '' and c != 0) or c == 1:
                        validade.append(True)
                        alteracao.append(False)
                    else:
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip()))
                        alteracao.append(True)
                        self.Notifica_erro(286 + c, validade[c])

                if validade[0]:
                    if int(self.entry_frame_2[29].get()) >= self.numero_dados_topo_margem_coord:
                        validade[0] = False
                        self.Notifica_erro(286, validade[0])

                if False not in validade:
                    for c in range(0, 5):
                        if c != 1:
                            dados_inserir.append(str(self.entry_frame_2[29 + c].get()).replace(',', '.').strip())
                        else:
                            dados_inserir.append('')

        # Réguas
        elif self.opcao_topo_teo_coord_reg.get() == 2:
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                # Validação das entradas
                str_validacao = ['int+', 't_decli', 'float+', 'float', 'float', 'float']
                for c in range(0, 6):
                    if str(self.entry_frame_2[34 + c].get()).replace(',', '.').strip() == '' and c != 0:
                        validade.append(True)
                        alteracao.append(False)
                    else:
                        validade.append(Validacao_Entradas(str_validacao[c], str(self.entry_frame_2[34 + c].get()).replace(',', '.').strip()))
                        alteracao.append(True)
                        self.Notifica_erro(286 + c, validade[c])

                if validade[0]:
                    if int(self.entry_frame_2[34].get()) >= self.numero_dados_topo_decli_reg:
                        validade[0] = False
                        self.Notifica_erro(286, validade[0])

                if False not in validade:
                    for c in range(0, 6):
                        dados_inserir.append(str(self.entry_frame_2[34 + c].get()).replace(',', '.').strip())

        if False not in validade:
            Editar_dado_topografia(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                    self.opcao_topo_decli_margem.get(), self.opcao_topo_teo_coord_reg.get(), dados_inserir, alteracao)

            self.Exibir_dados_topografia(0)

        return

    def Excluir_dado_coleta_1(self):
        """
        Função Excluir_dado_coleta_1: Usada para excluir os dados de uma coleta.
        :return: Não retorna valores.
        """
        # Validação da entrada
        validade = Validacao_Entradas('int+', str(self.entry_frame_2[6].get()).strip())
        if validade:
            if int(self.entry_frame_2[6].get()) >= self.numero_dados_coleta:
                validade = False
        self.Notifica_erro(54, validade)
        self.Notifica_erro(55, True)
        self.Notifica_erro(56, True)
        self.Notifica_erro(57, True)

        # Excluir dado
        if validade:
            # Comparação id
            compara_id = Excluir_dado_coleta(self.diretorio_arquivo_carregado, int(self.entry_frame_2[6].get()), self.id_dado_carregado)
            self.Exibir_dados_coletas_frame_2(0)
            if compara_id:
                self.Carregar_coleta_1(fora=True)

        return

    def Excluir_dado_hidrometria_1(self):
        """
        Função Excluir_dado_hidrometria_1: Usada para excluir um dado de hidrometria.
        :return: Não retorna valores.
        """
        # Validação das entradas
        entrada = str(self.entry_frame_2[12].get()).strip()
        validade = Validacao_Entradas('int+', entrada)

        # Excluir dado
        if validade and entrada != '0' and int(entrada) < self.numero_dados_hidrometria-1:
            Excluir_dado_hidrometria(self.diretorio_arquivo_carregado, self.id_dado_carregado, entrada)
            self.Exibir_dados_hidrometria_frame_2(0)
        else:
            validade = False

        self.Notifica_erro(60, True)
        self.Notifica_erro(61, True)
        self.Notifica_erro(184, validade)
        for c in range(185, 197):
            self.Notifica_erro(c, True)

        return

    def Excluir_dado_topografia_1(self):
        """
        Função Excluir_dado_topografia_1: Usada para excluir um dado de topografia.
        :return: Não retorna valores.
        """
        # Validação das entradas
        # Teodolito
        if self.opcao_topo_teo_coord_reg.get() == 0:
            ponto = self.entry_frame_2[21].get()
            validade = Validacao_Entradas('int+', str(ponto))
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                if validade:
                    if int(ponto) >= self.numero_dados_topo_decli_teo:
                        validade = False
                self.Notifica_erro(286, validade)

            # Margem
            else:
                if validade:
                    if int(ponto) >= self.numero_dados_topo_margem_teo:
                        validade = False
                self.Notifica_erro(286, validade)

        # Coordenadas
        elif self.opcao_topo_teo_coord_reg.get() == 1:
            ponto = self.entry_frame_2[29].get()
            validade = Validacao_Entradas('int+', str(ponto))
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                if validade:
                    if int(ponto) >= self.numero_dados_topo_decli_coord:
                        validade = False
                self.Notifica_erro(286, validade)

            # Margem
            else:
                if validade:
                    if int(ponto) >= self.numero_dados_topo_margem_coord:
                        validade = False
                self.Notifica_erro(286, validade)

        # Réguas
        elif self.opcao_topo_teo_coord_reg.get() == 2:
            ponto = self.entry_frame_2[34].get()
            validade = Validacao_Entradas('int+', str(ponto))
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                if validade:
                    if int(ponto) >= self.numero_dados_topo_decli_reg:
                        validade = False
                self.Notifica_erro(286, validade)

        if validade:
            Excluir_Dado_Topogafia(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                   self.opcao_topo_decli_margem.get(), self.opcao_topo_teo_coord_reg.get(), str(ponto))
            self.Exibir_dados_topografia(0)

        return

    def Exibir_dados_coletas_frame_2(self, m):
        """
        Função Exibir_dados_coletas_frame_2: Usada para exibir os dados de coleta no frame 2.
        :param m: O número de páginas para avançar (+m valor positivo) ou retornar(-m valor negativo).
        :return: Não retorna valores.
        """

        # Dados
        dados = Acessar_tabela_Info_coletas(self.diretorio_arquivo_carregado)

        self.numero_dados_coleta = len(dados[1])

        # Páginas (0, 1, 2, ..., n)
        numero_paginas = len(dados[1])/10
        if numero_paginas - int(numero_paginas) > 0 or numero_paginas == 0:
            numero_paginas = int(numero_paginas)+1
        elif numero_paginas - int(numero_paginas) == 0 and numero_paginas != 0:
            numero_paginas = int(numero_paginas)

        if self.pagina_dados_coleta_frame_2+m >= numero_paginas:
            self.pagina_dados_coleta_frame_2 = 0
        elif self.pagina_dados_coleta_frame_2+m < 0:
            self.pagina_dados_coleta_frame_2 = numero_paginas-1
        else:
            self.pagina_dados_coleta_frame_2 = self.pagina_dados_coleta_frame_2 + m

        # Elementos gráficos
        # Labels

        for c0 in range(0, 10):
            for c1 in range(0, 4):
                self.label_frame_2[14+4*c0+c1].place(x=5+105*c1, y=75+25*c0, width=100, height=20)
                if self.pagina_dados_coleta_frame_2*10+c0 < len(dados[1]):
                    if c1 == 0:
                        self.label_frame_2[14 + 4 * c0 + c1].configure(text=self.pagina_dados_coleta_frame_2*10+c0, anchor=CENTER)
                    else:
                        self.label_frame_2[14 + 4 * c0 + c1].configure(text=dados[1][self.pagina_dados_coleta_frame_2*10+c0][c1-1], anchor=CENTER)
                else:
                    self.label_frame_2[14 + 4 * c0 + c1].configure(text='', anchor=CENTER)

        # Entry
        self.entry_frame_2[6].delete(0, END)
        self.entry_frame_2[6].insert(0, len(dados[1]))

        return

    def Exibir_coordenadas_rel_secao(self, m):
        """
        Função Exibir_coordenadas_rel_secao: Usada para exiir as coordenadas relativas da seção transversal.
        :param m: O número de páginas para avançar (+m valor positivo) ou retornar(-m valor negativo).
        :return: Não retorna valores.
        """

        dados = Acessar_tabela_coord_rel_sec(self.diretorio_arquivo_carregado, self.id_dado_carregado)
        numero_dados_coord_rel = len(dados)

        # Páginas (0, 1, 2, ..., n)
        numero_paginas = numero_dados_coord_rel / 15
        if numero_paginas - int(numero_paginas) > 0 or numero_paginas == 0:
            numero_paginas = int(numero_paginas) + 1
        elif numero_paginas - int(numero_paginas) == 0 and numero_paginas != 0:
            numero_paginas = int(numero_paginas)

        if self.pagina_dados_coord_rel_secao + m >= numero_paginas:
            self.pagina_dados_coord_rel_secao = 0
        elif self.pagina_dados_coord_rel_secao + m < 0:
            self.pagina_dados_coord_rel_secao = numero_paginas - 1
        else:
            self.pagina_dados_coord_rel_secao = self.pagina_dados_coord_rel_secao + m

        x_t = [5, 255, 505]
        titulo_colunas = [False, False, False]

        for c0 in range(0, 5): # linha
            for c1 in range(0, 3): # coluna
                for c2 in range(0, 3): # elemento da coluna
                    self.label_frame_2[386+3*c0+18*c1+c2].place(x=x_t[c1]+80*c2, y=375+c0*25, width=75, height=20)

                    try:
                        self.label_frame_2[386+3*c0+18*c1+c2].configure(text=dados[15*self.pagina_dados_coord_rel_secao+c0+5*c1][c2], anchor=CENTER)
                        titulo_colunas[c1] = True

                    except Exception:
                        self.label_frame_2[386+3*c0+18*c1+c2].configure(text='', anchor=CENTER)

        texto_colunas = ['Descrição', "Coordenada\nx' (m)", "Coordenada\ny' (m)"]
        for c0 in range(0, 3): # Colunas
            for c1 in range(0, 3): # Elementos
                self.label_frame_2[383+c0*18+c1].place(x=x_t[c0]+80*c1, y=330, width=75, height=40)
                if titulo_colunas[c0]:
                    self.label_frame_2[383+c0*18+c1].configure(text=texto_colunas[c1], anchor=CENTER)
                else:
                    self.label_frame_2[383 + c0 * 18 + c1].configure(text='', anchor=CENTER)

        return

    def Exibir_dados_hidrometria_frame_2(self, m):
        """
        Função Exibir_dados_hidrometria_frame_2: Usada para exibir os dados de hidrometria no frame 2.
        :param m: O número de páginas para avançar (+m valor positivo) ou retornar(-m valor negativo).
        :return: Não retorna valores.
        """
        # Dados
        dados = Acessar_tabela_Hidrometria_id(self.diretorio_arquivo_carregado, self.id_dado_carregado)
        self.numero_dados_hidrometria = len(dados[1])

        # Páginas (0, 1, 2, ..., n)
        numero_paginas = self.numero_dados_hidrometria/10
        if numero_paginas - int(numero_paginas) > 0 or numero_paginas == 0:
            numero_paginas = int(numero_paginas)+1
        elif numero_paginas - int(numero_paginas) == 0 and numero_paginas != 0:
            numero_paginas = int(numero_paginas)

        if self.pagina_dados_hidrometria_frame_2 + m >= numero_paginas:
            self.pagina_dados_hidrometria_frame_2 = 0
        elif self.pagina_dados_hidrometria_frame_2 + m < 0:
            self.pagina_dados_hidrometria_frame_2 = numero_paginas-1
        else:
            self.pagina_dados_hidrometria_frame_2 = self.pagina_dados_hidrometria_frame_2 + m

        # Elementos gráficos
        # Labels
        for c0 in range(0, 10):
            for c1 in range(0, 11):
                if c1 < 3:
                    self.label_frame_2[74+c0*11+c1].place(x=5+105*c1, y=150+25*c0, width=100, height=20)
                elif c1 < 9:
                    self.label_frame_2[74+c0*11+c1].place(x=320+40*(c1-3), y=150+25*c0, width=35, height=20)
                else:
                    self.label_frame_2[74+c0*11+c1].place(x=560+105*(c1-9), y=150+25*c0, width=100, height=20)

                if self.pagina_dados_hidrometria_frame_2*10+c0 < len(dados[1]):
                    self.label_frame_2[74+c0*11+c1].configure(text=dados[1][self.pagina_dados_hidrometria_frame_2*10+c0][c1], anchor=S)

                    #Labels de distância verticais 0 e n
                    if self.numero_dados_hidrometria%10 != 0:
                        n_label = 75+11*((self.numero_dados_hidrometria%10)-1)
                    else:
                        n_label = 174

                    if (74+c0*11+c1 == 75 or 74+c0*11+c1 == n_label) and str(dados[1][self.pagina_dados_hidrometria_frame_2*10+c0][c1]) == 'Editar':
                        self.Notifica_erro(74+c0*11+c1, False)
                    else:
                        self.Notifica_erro(74+c0*11+c1, True)

                    if (74+c0*11+c1==75) and str(dados[1][self.pagina_dados_hidrometria_frame_2*10+c0][c1]) != 'Editar':
                        self.alteracao_vertical_0 = True
                    elif (74+c0*11+c1==75) and str(dados[1][self.pagina_dados_hidrometria_frame_2*10+c0][c1]) == 'Editar':
                        self.alteracao_vertical_0 = False

                    if (74+c0*11+c1== n_label) and str(dados[1][self.pagina_dados_hidrometria_frame_2*10+c0][c1]) != 'Editar':
                        self.alteracao_vertical_n = True
                    elif (74+c0*11+c1== n_label) and str(dados[1][self.pagina_dados_hidrometria_frame_2*10+c0][c1]) == 'Editar':
                        self.alteracao_vertical_n = False

                else:
                    self.label_frame_2[74+c0*11+c1].configure(text='', anchor=CENTER)

        # Entry
        self.entry_frame_2[12].delete(0, END)
        self.entry_frame_2[12].insert(0, self.numero_dados_hidrometria-1)

        return

    def Exibir_dados_topografia(self, m):
        """
        Função Exibir_dados_topografia: Usada para auxiliar na exibição dos dados de topografia.
        :param m: O número de páginas para avançar (+m valor positivo) ou retornar(-m valor negativo).
        :return: Não retorna valores.
        """
        # Remover elementos
        self.Limpar_frame_2(radio_b=False, botao=False)

        # Remoção das notificações de erro
        lista_labels = []
        for c in range(286, 294):
            lista_labels.append(c)
        for elemento in lista_labels:
            self.Notifica_erro(elemento, True)

        # Radio buttom régua
        self.Exibir_dado_topografia_regua()

        # Dados
        dados = Acessar_tabela_Topo_x_id(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                         self.opcao_topo_decli_margem.get(), self.opcao_topo_teo_coord_reg.get())

        # Teodolito
        if self.opcao_topo_teo_coord_reg.get() == 0:
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                texto_dados = ['Ponto\nnúmero', 'Tipo\n(m, s, j)', 'FI (m)', 'FM (m)', 'FS (m)',
                               'Ângulo zenital\n(ggg mm ss)', 'Ângulo horizontal\n(ggg mm ss)', 'Altura do\nequipamento (m)']
                larguras = [75, 75, 75, 75, 75, 100, 100, 100]

                self.numero_dados_topo_decli_teo = len(dados)
                numero_dados_pag = len(dados)

                self.entry_frame_2[21].delete(0, END)
                self.entry_frame_2[21].insert(0, self.numero_dados_topo_decli_teo)

            # Margem
            else:
                texto_dados = ['Ponto\nnúmero', '', 'FI (m)', 'FM (m)', 'FS (m)',
                               'Ângulo zenital\n(ggg mm ss)', 'Ângulo horizontal\n(ggg mm ss)',
                               'Altura do\nequipamento (m)']
                larguras = [100, 0, 100, 100, 100, 100, 100, 100]

                self.numero_dados_topo_margem_teo = len(dados)
                numero_dados_pag = len(dados)

                self.entry_frame_2[21].delete(0, END)
                self.entry_frame_2[21].insert(0, self.numero_dados_topo_margem_teo)

            # Entry
            for c in range(0, 8):
                if larguras[c] != 0:
                    self.entry_frame_2[21+c].place(x=Pos_x(c, larguras), y=self.altura_frame_2-60, width=larguras[c], height=20)
                else:
                    self.entry_frame_2[21 + c].place_forget()

        # Coordenada
        elif self.opcao_topo_teo_coord_reg.get() == 1:
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                texto_dados = ['Ponto\nnúmero', 'Tipo\n(m, s, j)', 'Coordenada\nx (m)', 'Coordenada\ny (m)',
                               'Coordenada\nz (m)', '', '', '']
                larguras = [100, 100, 100, 100, 100, 0, 0, 0]

                self.numero_dados_topo_decli_coord = len(dados)
                numero_dados_pag = len(dados)

                self.entry_frame_2[29].delete(0, END)
                self.entry_frame_2[29].insert(0, self.numero_dados_topo_decli_coord)

            # Margem
            else:
                texto_dados = ['Ponto\nnúmero', '', 'Coordenada\nx (m)', 'Coordenada\ny (m)',
                               'Coordenada\nz (m)', '', '', '']
                larguras = [100, 0, 100, 100, 100, 0, 0, 0]

                self.numero_dados_topo_margem_coord = len(dados)
                numero_dados_pag = len(dados)

                self.entry_frame_2[29].delete(0, END)
                self.entry_frame_2[29].insert(0, self.numero_dados_topo_margem_coord)

            # Entry
            for c in range(0, 5):
                if larguras[c] != 0:
                    self.entry_frame_2[29+c].place(x=Pos_x(c, larguras), y=self.altura_frame_2-60, width=larguras[c], height=20)
                else:
                    self.entry_frame_2[29 + c].place_forget()

        # Réguas
        elif self.opcao_topo_teo_coord_reg.get() == 2:
            # Declividade
            if self.opcao_topo_decli_margem.get() == 0:
                texto_dados = ['Régua\nnúmero', 'Tipo\n(m, s, j)', 'Leitura (m)', 'Coordenada\nx (m)', 'Coordenada\ny (m)', 'Coordenada\nz (m)', '', '']
                larguras = [100, 100, 100, 100, 100, 100, 0, 0]

                self.numero_dados_topo_decli_reg = len(dados)
                numero_dados_pag = len(dados)

                self.entry_frame_2[34].delete(0, END)
                self.entry_frame_2[34].insert(0, self.numero_dados_topo_decli_reg)

            # Entry
            for c in range(0, 6):
                if larguras[c] != 0:
                    self.entry_frame_2[34 + c].place(x=Pos_x(c, larguras), y=self.altura_frame_2 - 60,
                                                     width=larguras[c], height=20)
                else:
                    self.entry_frame_2[34 + c].place_forget()

        # Labels títulos
        for c in range(0, 8):
            self.label_frame_2[198+c].place(x=Pos_x(c, larguras), y=105, width=larguras[c], height=40)
            self.label_frame_2[198+c].configure(text=texto_dados[c], anchor=S)
            self.label_frame_2[286+c].place(x=Pos_x(c, larguras), y=self.altura_frame_2-105, width=larguras[c], height=40)
            self.label_frame_2[286+c].configure(text=texto_dados[c], anchor=S)

        # Páginas (0, 1, 2, ..., n)
        numero_paginas = numero_dados_pag / 10
        if numero_paginas - int(numero_paginas) > 0 or numero_paginas == 0:
            numero_paginas = int(numero_paginas) + 1
        elif numero_paginas - int(numero_paginas) == 0 and numero_paginas != 0:
            numero_paginas = int(numero_paginas)

        if self.pagina_dados_topografia_frame_2 + m >= numero_paginas:
            self.pagina_dados_topografia_frame_2 = 0
        elif self.pagina_dados_topografia_frame_2 + m < 0:
            self.pagina_dados_topografia_frame_2 = numero_paginas - 1
        else:
            self.pagina_dados_topografia_frame_2 = self.pagina_dados_topografia_frame_2 + m

        # Labels com os dados
        for c0 in range(0, 10):
            cont = 0
            for c1 in range(0, 8):
                self.label_frame_2[206+c0*8+c1].place(x=Pos_x(c1, larguras), y=150 + 25 * c0, width=larguras[c1], height=20)

                if larguras[c1] > 0:
                    try:
                        self.label_frame_2[206 + c0 * 8 + c1].configure(text=dados[c0+self.pagina_dados_topografia_frame_2*10][cont], anchor=CENTER)
                        cont += 1
                    except Exception:
                        self.label_frame_2[206 + c0 * 8 + c1].configure(text='', anchor=CENTER)
                else:
                    self.label_frame_2[206 + c0 * 8 + c1].configure(text='', anchor=CENTER)

        return

    def Exibir_dado_topografia_regua(self):
        """
        Função Exibir_dado_topografia_regua: Usada para exibir/remover o radio buttom referente à régua.
        :return: Não retorna valores
        """
        # Radio buttom réguas
        if self.opcao_topo_decli_margem.get() == 0:
            self.radiobuttom_frame_2_topo_reg.place(x=215, y=80, width=205, height=20)
        else:
            self.radiobuttom_frame_2_topo_reg.place_forget()
            if self.opcao_topo_teo_coord_reg.get() == 2:
                self.radiobuttom_frame_2_topo_teo.select()

        return

    def Exibir_parametros(self, m):
        """
        Função Exibir_parametros: Usada para exibir os valores dos parâmetros hidráulicos.
        :param m: O número de páginas para avançar (+m valor positivo) ou retornar(-m valor negativo).
        :return: Não retorna valores
        """

        dados = Acessar_tabela_Parametros(self.diretorio_arquivo_carregado, self.id_dado_carregado)

        for c in range(0, 7):
            self.label_frame_2[302+c].configure(text=dados[c+1], anchor=W)
            if dados[c+1] == 'Erro':
                self.Notifica_erro(302+c, False)
            else:
                self.Notifica_erro(302+c, True)

        for c in range(0, 6):
            self.label_frame_2[315 + c].configure(text=dados[c+8], anchor=W)
            if dados[c+8] == 'Erro':
                self.Notifica_erro(315+c, False)
            else:
                self.Notifica_erro(315+c, True)

        dados_detalhamento = Acessar_tabela_op_declividade(self.diretorio_arquivo_carregado, self.id_dado_carregado)

        # Páginas (0, 1, 2, ..., n)
        numero_dados_pag = len(dados_detalhamento)
        numero_paginas = numero_dados_pag / 10
        if numero_paginas - int(numero_paginas) > 0 or numero_paginas == 0:
            numero_paginas = int(numero_paginas) + 1
        elif numero_paginas - int(numero_paginas) == 0 and numero_paginas != 0:
            numero_paginas = int(numero_paginas)

        if self.pagina_dados_op_declividade_frame_2 + m >= numero_paginas:
            self.pagina_dados_op_declividade_frame_2 = 0
        elif self.pagina_dados_op_declividade_frame_2 + m < 0:
            self.pagina_dados_op_declividade_frame_2 = numero_paginas - 1
        else:
            self.pagina_dados_op_declividade_frame_2 = self.pagina_dados_op_declividade_frame_2 + m

        for c0 in range(0, 10):
            for c1 in range(0, 4):
                try:
                    texto_dado = dados_detalhamento[c0+self.pagina_dados_op_declividade_frame_2*10][c1]
                except Exception:
                    texto_dado = ''

                self.label_frame_2[329+c0*4+c1].configure(text=texto_dado, anchor=CENTER)

                if texto_dado == 'Erro':
                    self.Notifica_erro(329+c0*4+c1, False)
                else:
                    self.Notifica_erro(329+c0*4+c1, True)

        return

    def Salvar_extrapolacao(self):
        """
        Função Salvar_extrapolacao: Usada para validar as entradas dos dados e salvar os arquivos da extrapolação.
        :return: Não retorna valores.
        """
        #self.Dados_extrapolacao_provisoria()
        tipos_validação = ['float+', 'float+', 'float+', 'float+', 'float+', 'float+', 'str', 'dir']
        num_labels = [370, 371, 372, 374, 375, 376, 379, 380]
        validade = []
        for c in range(0, 8):
            if c < 6:
                validade.append(
                    Validacao_Entradas(tipos_validação[c], str(self.entry_frame_2[41 + c].get()).replace(',', '.').strip()))
            else:
                validade.append(Validacao_Entradas(tipos_validação[c], str(self.entry_frame_2[41 + c].get()).strip()))
            self.Notifica_erro(num_labels[c], validade[c])

        if False not in validade:
            lista_entry = [41, 42, 44, 45]
            lista_label = [370, 371, 374, 375]
            for c in range(0, 4):
                if float(str(self.entry_frame_2[lista_entry[c]].get()).replace(',', '.')) == 0:
                    validade[lista_entry[c]-41] = False
                    self.Notifica_erro(lista_label[c], False)

            for c in range(0, 2):
                if float(str(self.entry_frame_2[41+c*3].get()).replace(',', '.')) > float(str(self.entry_frame_2[42+c*3].get()).replace(',', '.')):
                    validade[0+c*3] = False
                    validade[1+c*3] = False
                    self.Notifica_erro(370+c*3+c, False)
                    self.Notifica_erro(371+c*3+c, False)

        if False not in validade:
            dados_decli = [str(self.entry_frame_2[41].get()).replace(',', '.').strip(),
                           str(self.entry_frame_2[42].get()).replace(',', '.').strip(),
                           str(self.entry_frame_2[43].get()).replace(',', '.').strip()]
            dados_rug = [str(self.entry_frame_2[44].get()).replace(',', '.').strip(),
                         str(self.entry_frame_2[45].get()).replace(',', '.').strip(),
                         str(self.entry_frame_2[46].get()).replace(',', '.').strip()]
            dados_arq = [str(self.entry_frame_2[47].get()).strip(), str(self.entry_frame_2[48].get()).strip()]

            exito = Extrapolar_parametros(self.diretorio_arquivo_carregado, self.id_dado_carregado, dados_decli, dados_rug, dados_arq)
            if exito[0]:
                self.Notifica_erro(379, True)
                self.Notifica_erro(382, True)
            else:
                if exito[1] == 1:
                    self.Notifica_erro(382, False)

                elif exito[1] == 2:
                    self.Notifica_erro(379, False)
        return

    def Limpar_frame_2(self, label=True, entry=True, text=True, botao=True, radio_b=True):
        """
        Função Limpar_frame_2: Usada para remover os elementos gráficos do frame 2.
        :return: Não retorna valores.
        """
        # Label
        if label:
            for c in range(1, len(self.label_frame_2)):
                try:
                    self.label_frame_2[c].place_forget()
                except Exception:
                    pass

        # Entry
        if entry:
            for c in range(0, len(self.entry_frame_2)):
                try:
                    self.entry_frame_2[c].place_forget()
                except Exception:
                    pass

        # Text
        if text:
            for c in range(0, len(self.text_frame_2)):
                try:
                    self.text_frame_2[c].place_forget()
                except Exception:
                    pass

        # Botão
        if botao:
            for c in range(1, len(self.botoes_frame_2)):
                try:
                    self.botoes_frame_2[c].place_forget()
                except Exception:
                    pass

        # Radio Buttom
        if radio_b:
            for c in range(0, 2):
                try:
                    self.radiobuttom_frame_2_arquivo[c].place_forget()
                except Exception:
                    pass

            self.radiobuttom_frame_2_topo_decli.place_forget()
            self.radiobuttom_frame_2_topo_margem_0.place_forget()
            self.radiobuttom_frame_2_topo_margem_n.place_forget()

            # Radio buttom teodolito/coordenadas
            self.radiobuttom_frame_2_topo_teo.place_forget()
            self.radiobuttom_frame_2_topo_coord.place_forget()
            self.radiobuttom_frame_2_topo_reg.place_forget()

        return

    def Notifica_erro(self, n_label, validade):
        """
        Função Notifica_erro: Usada para notificar o erro de uma entrada.
        :param n_label: O número da label analisada.
        :param validade: A validade da entrada.
        :return: Não retorna valores
        """

        if validade:
            self.label_frame_2[n_label].configure(fg='#000000')
        else:
            self.label_frame_2[n_label].configure(fg='#B22222')

        return

    def Opcao_arquivo_secao(self, n_op):
        """
        Função Opcao_arquivo_secao: Usada para exibir os elementos gráfcos de criação de um novo arquivo
        ou de arwquivo existente.
        :param n_op: O número da opção. 0 - Novo arquivo.
                                        1 - Arquivo existente.
        :return: Não retorna valores.
        """
        # Remoção dos elementos existentes
        self.Limpar_frame_2(radio_b=False)

        # Alteração da opção
        self.opcao_arquivo_secao = n_op

        # Remoção das notificações de erro
        lista_labels = [1, 2, 3]
        for elemento in lista_labels:
            self.Notifica_erro(elemento, True)

        # Novo arquivo
        if n_op == 0:
            # Label
            self.label_frame_2[1].place(x=5, y=80, width=self.largura_frame_2 - 10, height=20)
            self.label_frame_2[1].configure(text='  Nome do arquivo:')
            self.label_frame_2[2].place(x=5, y=130, width=self.largura_frame_2 - 10, height=20)
            self.label_frame_2[2].configure(text='  Salvar em:')
            # Entry
            self.entry_frame_2[0].place(x=5, y=105, width=self.largura_frame_2 - 10, height=20)
            self.entry_frame_2[1].place(x=5, y=155, width=self.largura_frame_2 - 10, height=20)

        # Arquivo existente
        else:
            # Label
            self.label_frame_2[3].place(x=5, y=80, width=self.largura_frame_2 - 10, height=20)
            self.label_frame_2[3].configure(text='  Diretório:')
            # Entry
            self.entry_frame_2[2].place(x=5, y=105, width=self.largura_frame_2 - 10, height=20)

        return

    # Janelas secundárias ----------------------------------------------------------------------------------------------
    def Janela_salvar_parametros(self):
        """
        Função Janela_salvar_parametros: Usada para cirar uma janela para obter os parâmetros em formato .txt.
        :return: Não retorna valores.
        """
        # Janela
        self.janela_salvar_parametros = Toplevel(self.app)
        largura_j_sec = 785
        altura_j_sec = 150
        self.janela_salvar_parametros.geometry(str(largura_j_sec) + 'x' + str(altura_j_sec))
        self.janela_salvar_parametros.resizable(False, False)
        self.janela_salvar_parametros.title('Obter dados dos parâmetros hidráulicos')

        # Frame
        self.frame_sec_0 = Frame(self.janela_salvar_parametros, relief='raised', borderwidth=2)
        largura_frame_j_sec = largura_j_sec - 10
        altura_frame_j_sec = altura_j_sec - 10

        # Label
        self.label_frame_sec_0 = Label(self.frame_sec_0, anchor=W, font=('arial', 10, 'normal'))
        self.label_frame_sec_1 = Label(self.frame_sec_0, anchor=W, font=('arial', 10, 'normal'))

        # Entry
        self.entry_frame_sec_0 = Entry(self.frame_sec_0, font=('arial', 10, 'normal'))
        self.entry_frame_sec_1 = Entry(self.frame_sec_0, font=('arial', 10, 'normal'))

        # Botão
        self.botao_frame_sec_0 = Button(self.frame_sec_0, font=('arial', 10, 'normal'))

        # Inserção dos elementos
        self.frame_sec_0.place(x=5, y=5, width=largura_frame_j_sec, height=altura_frame_j_sec)

        self.label_frame_sec_0.place(x=5, y=5, width=largura_frame_j_sec-10, height=20)
        self.label_frame_sec_0.configure(text='Nome do arquivo:')
        self.label_frame_sec_1.place(x=5, y=55, width=largura_frame_j_sec - 10, height=20)
        self.label_frame_sec_1.configure(text='Salvar em:')

        self.entry_frame_sec_0.place(x=5, y=30, width=largura_frame_j_sec-10, height=20)
        self.entry_frame_sec_1.place(x=5, y=80, width=largura_frame_j_sec - 10, height=20)

        self.botao_frame_sec_0.place(x=largura_frame_j_sec-105, y=altura_frame_j_sec-35, width=100, height=30)
        self.botao_frame_sec_0.configure(text='Enviar', command=lambda: self.Salvar_parametros())

        return

    def Salvar_parametros(self):
        """
        Função Salvar_parametros: Usada para validar as entradas do nome do arquivo e diretório para obter os dados.
        :return: Não retorna valores.
        """
        # Validação das entradas
        validade = [Validacao_Entradas('str', str(self.entry_frame_sec_0.get()).strip()), Validacao_Entradas('dir', str(self.entry_frame_sec_1.get()).strip())]

        if validade[0]:
            self.label_frame_sec_0.configure(fg='#000000')
        else:
            self.label_frame_sec_0.configure(fg='#B22222')

        if validade[1]:
            self.label_frame_sec_1.configure(fg='#000000')
        else:
            self.label_frame_sec_1.configure(fg='#B22222')

        if False not in validade:
            exito = Obter_txt_parametros(self.diretorio_arquivo_carregado, self.id_dado_carregado,
                                         str(self.entry_frame_sec_1.get()).strip(), str(self.entry_frame_sec_0.get()).strip())

            if exito:
                self.label_frame_sec_0.configure(fg='#000000')
                self.label_frame_sec_1.configure(fg='#000000')
                self.janela_salvar_parametros.destroy()

            else:
                self.label_frame_sec_0.configure(fg='#B22222')
                self.label_frame_sec_1.configure(fg='#B22222')

        return

    # Execução do programa ---------------------------------------------------------------------------------------------
    def Executar(self):
        """
        Função Executar: Usada para executar o programa.
        :return: Não retorna valores.
        """
        self.Tela()
        self.Acionar_bts_frame_0(0)
        self.app.mainloop()
        return

Flow().Executar()
