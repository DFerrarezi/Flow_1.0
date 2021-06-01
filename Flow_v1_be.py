import os
import sqlite3
import math
from datetime import datetime
from numpy import polyfit

# Funções principais (Referentes ao frame 0, aplicadas com o botão 0 do frame 2) ---------------------------------------

# Bt 0
def Criar_arquivo_db(caminho, nome_arquivo):
    """
    Função Criar_arquivo_db: Cria um arquivo .db.
    :param caminho: O diretório do arquivo.
    :param nome_arquivo: O nome do arquivo.
    :return: Retorna True se o qrquivo foi criado com êxito e False caso contrário.
    """
    exito = False
    diretorio = caminho + '\ '.strip() + nome_arquivo + '.db'

    # Existencia do arquivo
    if not os.path.exists(diretorio):
        # Criação do arquivo
        try:
            conexao_bd = sqlite3.connect(diretorio)
            cursor_bd = conexao_bd.cursor()

            # Criação das tabelas

            # Info_secao (Informações da seção transversal)
            cursor_bd.execute(
                "CREATE TABLE IF NOT EXISTS Info_secao (nome_corpo_dagua TEXT, localizacao TEXT, nome_secao TEXT, descricao TEXT, secao_carregada TEXT)")
            cursor_bd.execute(
                "INSERT INTO Info_secao (nome_corpo_dagua, localizacao, nome_secao, descricao, secao_carregada) VALUES(?, ?, ?, ?, ?)",
                ('-', '-', '-', '-', 'False'))

            # Id_ultima_coleta (O id da próxima coleta)
            cursor_bd.execute("CREATE TABLE IF NOT EXISTS Id_ultima_coleta (id INTEGER)")
            cursor_bd.execute("INSERT INTO Id_ultima_coleta (id) VALUES(?)", (0,))

            # Info_coletas (Informações de cada coleta)
            cursor_bd.execute("CREATE TABLE IF NOT EXISTS Info_coletas (data TEXT, hora_i TEXT, hota_t TEXT, id INTEGER, ordem INTEGER)")

            # Parametros (Os parâmetros hidráulicos das coletas)
            cursor_bd.execute("CREATE TABLE IF NOT EXISTS Parametros (id TEXT, largura TEXT, peri_mo TEXT, area_mo TEXT, raio_h TEXT, prof_med TEXT, vazao TEXT, vel_media TEXT, decli_t TEXT, decli_c TEXT, decli_r TEXT, rug_t TEXT, rug_c TEXT, rug_r TEXT)")

            conexao_bd.commit()
            conexao_bd.close()

            exito = True

        except Exception:
            pass

    return exito

# Bt 0 e 1
def Carregar_secao_transversal(diretorio):
    """
    Função Carregar_secao_transversal: Usada para acessar os elemntos da tabela Info_secao.
    :param diretorio: O diretório do banco de dados.
    :return: Uma lista com a forma: [nome_corpo_dagua, localizacao, nome_secao, descricao, secao_carregada]
    """
    retorno = []

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    try:
        for linha in cursor_bd.execute('SELECT * FROM Info_secao'):
            for cont in linha:
                retorno.append(cont)

    except Exception:
        retorno = ['-', '-', '-', '-', 'False']

    conexao_bd.close()

    return retorno

# Bt 1
def Alterar_info_secao(diretorio, nome_corpo_dagua, localizacao, nome_secao, descricao, secao_carregada):
    """
    Função Alterar_info_secao: Usada para alterar as informações sobre a seção trasnversal.
    :param diretorio: O diretório do banco de dados.
    :return: Não retorna valores.
    """
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    nome_corpo_dagua_antigo = ''

    for linha in cursor_bd.execute('SELECT * FROM Info_secao'):
        nome_corpo_dagua_antigo = linha[0]

    cursor_bd.execute("UPDATE Info_secao SET nome_corpo_dagua = ?, localizacao = ?, nome_secao = ?, descricao = ?, secao_carregada = ? WHERE nome_corpo_dagua = ?",
                      (nome_corpo_dagua, localizacao, nome_secao, descricao, secao_carregada, nome_corpo_dagua_antigo))

    conexao_bd.commit()
    conexao_bd.close()

    return

# Bt 2
def Inserir_dado_coleta(diretorio, data, hora_inicio, hora_termino):
    """
    Função Inserir_dado_coleta: Usada para inserir os dados de uma coleta
    :param diretorio: O diretório do banco de dados.
    :param data: Uma string com a data.
    :param hora_inicio: Uma string com a hora de inicio.
    :param hora_termino: Uma string com a hora de termino.
    :return: Não retorna valores.
    """

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Id
    for linha in cursor_bd.execute('SELECT * FROM Id_ultima_coleta'):
        id = linha[0]
    cursor_bd.execute("UPDATE Id_ultima_coleta SET id= ? WHERE id = ?", (id+1, id))

    # Verificação da tabela vazia
    tabela_vazia = True
    for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
        tabela_vazia = False
        break

    # Inserção dos elementos
    # Tabela vazia
    if tabela_vazia:
        cursor_bd.execute("INSERT INTO Info_coletas (data, hora_i, hota_t, id, ordem) VALUES(?, ?, ?, ?, ?)",
                          (data, hora_inicio, hora_termino, id, Ordenar_entradas_coletas(data, hora_inicio, hora_termino)))

    #Tabela não vazia
    else:
        # Matriz com dados
        dados_novos = (data, hora_inicio, hora_termino, id, Ordenar_entradas_coletas(data, hora_inicio, hora_termino))
        dados_antigos = []

        for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
            dados_antigos.append(linha)

        # Posição à inserir o novo elemento
        cont = -1
        pos = False
        for c in range(0, len(dados_antigos)):
            cont += 1
            if dados_novos[4] >= dados_antigos[c][4]:
                pos = True
                break

        if pos == False:
            cont += 1

        # Inserção do elemento
        for c in range(0, len(dados_antigos)):
            cursor_bd.execute("DELETE FROM Info_coletas WHERE id = ?", (dados_antigos[c][3],))

        dados_antigos.insert(cont, dados_novos)

        for c in range(0, len(dados_antigos)):
            cursor_bd.execute("INSERT INTO Info_coletas (data, hora_i, hota_t, id, ordem) VALUES(?, ?, ?, ?, ?)",
                              (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2], dados_antigos[c][3], dados_antigos[c][4]))

    # Tabelas de acordo com o id
    # Hidrometria

    nome_tabela_hidrometria = 'Hidrometria_id'+str(id)

    str_comando_0 = 'CREATE TABLE IF NOT EXISTS '+ nome_tabela_hidrometria +' (vertical TEXT, distancia TEXT, profundidade TEXT, va_s TEXT, va_02 TEXT, va_04 TEXT, va_06 TEXT, va_08 TEXT, va_f TEXT, a TEXT, b TEXT)'
    cursor_bd.execute(str_comando_0)

    str_comando_0 = 'INSERT INTO '+ nome_tabela_hidrometria + '(vertical, distancia, profundidade, va_s, va_02, va_04, va_06, va_08, va_f, a, b) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor_bd.execute(str_comando_0, ('0', 'Editar', '0', '-', '-', '-', '-', '-', '-', '0', '0'))
    cursor_bd.execute(str_comando_0, ('n', 'Editar', '0', '-', '-', '-', '-', '-', '-', '0', '0'))

    # Topografia

    # Declividade e teodolito
    nome_tabela_topo_decli_teo = 'Topo_decli_teo_id'+str(id)
    str_comando_1 = 'CREATE TABLE IF NOT EXISTS '+ nome_tabela_topo_decli_teo + ' (n_ponto TEXT, tipo TEXT, fi TEXT, fm TEXT, fs TEXT, ang_z TEXT, ang_h TEXT, h_equip TEXT)'
    cursor_bd.execute(str_comando_1)

    # Declividade e coordenadas
    nome_tabela_topo_decli_coord = 'Topo_decli_coord_id'+str(id)
    str_comando_2 = 'CREATE TABLE IF NOT EXISTS '+ nome_tabela_topo_decli_coord + ' (n_ponto TEXT, tipo TEXT, coord_x TEXT, coord_y TEXT, coord_z TEXT)'
    cursor_bd.execute(str_comando_2)

    # Declividade e regua
    nome_tabela_topo_decli_coord = 'Topo_decli_reg_id' + str(id)
    str_comando_2 = 'CREATE TABLE IF NOT EXISTS ' + nome_tabela_topo_decli_coord + ' (n_reg TEXT, tipo TEXT, leitura TEXT, coord_x TEXT, coord_y TEXT, coord_z TEXT)'
    cursor_bd.execute(str_comando_2)

    # Margem e teodolito
    nome_tabela_topo_margem_0_teo = 'Topo_margem_0_teo_id'+str(id)
    str_comando_3 = 'CREATE TABLE IF NOT EXISTS ' + nome_tabela_topo_margem_0_teo + ' (n_ponto TEXT, fi TEXT, fm TEXT, fs TEXT, ang_z TEXT, ang_h TEXT, h_equip TEXT)'
    cursor_bd.execute(str_comando_3)

    nome_tabela_topo_margem_n_teo = 'Topo_margem_n_teo_id' + str(id)
    str_comando_3_1 = 'CREATE TABLE IF NOT EXISTS ' + nome_tabela_topo_margem_n_teo + ' (n_ponto TEXT, fi TEXT, fm TEXT, fs TEXT, ang_z TEXT, ang_h TEXT, h_equip TEXT)'
    cursor_bd.execute(str_comando_3_1)

    # Margem e coordenadas
    nome_tabela_topo_margem_0_coord = 'Topo_margem_0_coord_id'+str(id)
    str_comando_4 = 'CREATE TABLE IF NOT EXISTS '+ nome_tabela_topo_margem_0_coord + ' (n_ponto TEXT, coord_x TEXT, coord_y TEXT, coord_z TEXT)'
    cursor_bd.execute(str_comando_4)

    nome_tabela_topo_margem_n_coord = 'Topo_margem_n_coord_id' + str(id)
    str_comando_4_1 = 'CREATE TABLE IF NOT EXISTS ' + nome_tabela_topo_margem_n_coord + ' (n_ponto TEXT, coord_x TEXT, coord_y TEXT, coord_z TEXT)'
    cursor_bd.execute(str_comando_4_1)

    # Parâmetros
    cursor_bd.execute("INSERT INTO Parametros (id, largura, peri_mo, area_mo, raio_h, prof_med, vazao, vel_media, decli_t, decli_c, decli_r, rug_t, rug_c, rug_r) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(id), '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'))

    # Declividades e rugosidades
    cursor_bd.execute('CREATE TABLE IF NOT EXISTS Opcoes_declividade_' + str(id) + ' (tipo TEXT, pontos TEXT, decli TEXT, rug TEXT)')

    # Coordenadas relativas da seção
    cursor_bd.execute('CREATE TABLE IF NOT EXISTS Coord_rel_sec_' + str(id) + ' (tipo TEXT, coord_x TEXT, coord_y TEXT)')

    conexao_bd.commit()
    conexao_bd.close()

    return

def Carregar_coleta(diretorio, n_coleta):
    """
    Função Carregar_coleta: Usada para carregar uma coleta de dados.
    :param diretorio: O diretório do banco de dados.
    :param n_coleta: O número da coleta.
    :return: Vetor na forma: [data, hora_inicio, hora_término, id]
    """
    returno = []

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    cont = -1
    for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
        cont += 1
        if cont == n_coleta:
            returno = [linha[0], linha[1], linha[2], linha[3]]
            break

    conexao_bd.close()

    return returno

def Editar_dado_coleta(diretorio, n_coleta, data, hora_inicio, hora_termino, id_coleta_carregada,alterar = [False, False, False]):
    """
    Função Editar_dado_coleta: Usada para editar os dados de uma coleta.
    :param diretorio: O diretório do banco de dados.
    :param n_coleta: O número da coleta.
    :param data: Uma string com a data.
    :param hora_inicio: Uma string com a hora de inicio.
    :param hora_termino: Uma string com a hora de termino.
    :param id_coleta_carregada: O id da coleta carregada.
    :param alterar: Um vetor contendo [True/False, True/False, True/False], referentes à alteração da data, hora_i e hora_t.
    :return: Compara os ids das coletas carregada e a ser excluida: True/False
    """
    compara_id = False

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Verificação da tabela vazia
    tabela_vazia = True
    for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
        tabela_vazia = False
        break

    # Atualização do elementos
    # Tabela não vazia
    if tabela_vazia == False:

        # Dados na forma original
        dados_antigos = []
        dados_update = []
        dados_antigos_1 =[]
        cont = -1
        for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
            cont += 1
            dados_antigos.append(linha)
            if cont == n_coleta:
                dados_update = [linha[0], linha[1], linha[2], linha[3], linha[4]]
                dados_antigos_1 = linha
                if linha[3] == id_coleta_carregada:
                    compara_id = True

        try:
            # Atualizando os dados
            if alterar[0] == True:
                dados_update[0] = data

            if alterar[1] == True:
                dados_update[1] = hora_inicio

            if alterar[2] == True:
                dados_update[2] = hora_termino

            dados_update[4] = Ordenar_entradas_coletas(dados_update[0], dados_update[1], dados_update[2])

            # Exclusão do elemento antigo
            for c in range(0, len(dados_antigos)):
                cursor_bd.execute("DELETE FROM Info_coletas WHERE id = ?", (dados_antigos[c][3],))

            dados_antigos.remove(dados_antigos_1)

            # Posição à inserir o novo elemento
            cont = -1
            pos = False
            for c in range(0, len(dados_antigos)):
                cont += 1
                if dados_update[4] >= dados_antigos[c][4]:
                    pos = True
                    break

            if pos == False:
                cont += 1

            dados_antigos.insert(cont, dados_update)

            for c in range(0, len(dados_antigos)):
                cursor_bd.execute("INSERT INTO Info_coletas (data, hora_i, hota_t, id, ordem) VALUES(?, ?, ?, ?, ?)",
                                  (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2], dados_antigos[c][3],
                                   dados_antigos[c][4]))

        except Exception:
            pass

    conexao_bd.commit()
    conexao_bd.close()

    return compara_id

def Excluir_dado_coleta(diretorio, n_coleta, id_coleta_carregada):
    """
    Função Excluir_dado_coleta: Usada para excluir os dados de uma coleta.
    :param diretorio: O diretório do banco de dados.
    :param n_coleta: O número da coleta.
    :param id_coleta_carregada: O id da coleta carregada.
    :return: Compara os ids das coletas carregada e a ser excluida: True/False
    """
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    cont = 0
    id = -2
    compara_id = False

    for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
        if cont == n_coleta:
            id = linha[3]
            break
        cont += 1

    if id == id_coleta_carregada:
        compara_id = True

    try:
        cursor_bd.execute("DELETE FROM Info_coletas WHERE id = ?", (id,))
    except Exception:
        pass

    # Tabelas de acordo com o id
    # Hidrometria
    nome_tabela_hidrometria = 'Hidrometria_id' + str(id)
    cursor_bd.execute('DELETE FROM ' + nome_tabela_hidrometria)

    # Topografia
    nomes_tabela_topo = ['Topo_decli_teo_id' + str(id), 'Topo_decli_coord_id' + str(id), 'Topo_decli_reg_id' + str(id),
                         'Topo_margem_0_teo_id' + str(id), 'Topo_margem_n_teo_id' + str(id),
                         'Topo_margem_0_coord_id' + str(id), 'Topo_margem_n_coord_id' + str(id)]

    for c in range(0, len(nomes_tabela_topo)):
        cursor_bd.execute('DELETE FROM ' + nomes_tabela_topo[c])

    # Parametros hidráulicos
    cursor_bd.execute('DELETE FROM Parametros WHERE id = ?', (str(id),))


    # Declividades e rugosidades
    cursor_bd.execute('DELETE FROM Opcoes_declividade_' + str(id))

    conexao_bd.commit()
    conexao_bd.close()

    return compara_id

# Bt 3
def Inserir_dados_hidrometria(diretorio, id, n_vertical, dist_ponto_ref, profun, s, p02, p04, p06, p08, f, a, b, insercao_fim):
    """
    Função Inserir_dados_hidrometria: Usada para inserir no banco os dados de hidrometria.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta carregada.
    :param n_vertical: O número da vertical
    :param dist_ponto_ref: A distância da vertical até o ponto de referncia.
    :param profun: A profundidade da vertical.
    :param s: A velocidade angular na superfície.
    :param p02: A velocidade angular à 0.2 profundidade.
    :param p04: A velocidade angular à 0.4 profundidade.
    :param p06: A velocidade angular à 0.6 profundidade.
    :param p08: A velocidade angular à 0.8 profundidade.
    :param f: A velocidade angular no fundo.
    :param a: Coeficiente a da equação do molinete.
    :param b: Coeficiente b da equação do molinete.
    :param insercao_fim: True caso a inserção do elemento seja na posição n-1 e False caso contrário.
    :return: Não retorna valores.
    """
    nome_tabela_hidrometria = 'Hidrometria_id' + str(id)

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    if insercao_fim:

        dado_n_me_1 = []
        for linha in cursor_bd.execute('SELECT * FROM ' + nome_tabela_hidrometria):
            if linha[0] == 'n':
                for elemento in linha:
                    dado_n_me_1.append(elemento)
                break

        if s == '':
            s='-'
        if p02 == '':
            p02='-'
        if p04 == '':
            p04='-'
        if p06 == '':
            p06='-'
        if p08 == '':
            p08='-'
        if f == '':
            f='-'

        str_comando_0 = 'INSERT INTO ' + nome_tabela_hidrometria + ' (vertical, distancia, profundidade, va_s, va_02, va_04, va_06, va_08, va_f, a, b) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cursor_bd.execute(str_comando_0, (n_vertical, dist_ponto_ref, profun, s, p02, p04, p06, p08, f, a, b))

        str_comando_1 = 'DELETE FROM ' + nome_tabela_hidrometria + ' WHERE vertical = ?'
        cursor_bd.execute(str_comando_1, ('n',))

        cursor_bd.execute(str_comando_0, (dado_n_me_1[0], dado_n_me_1[1], dado_n_me_1[2], dado_n_me_1[3], dado_n_me_1[4], dado_n_me_1[5], dado_n_me_1[6], dado_n_me_1[7], dado_n_me_1[8], dado_n_me_1[9], dado_n_me_1[10]))

    else:
        # Matriz com dados
        dados_novos = [n_vertical, dist_ponto_ref, profun, s, p02, p04, p06, p08, f, a, b]
        dados_antigos = []
        dados_antigos_1 = []

        for linha in cursor_bd.execute('SELECT * FROM ' + nome_tabela_hidrometria):
            for elemento in linha:
                dados_antigos_1.append(elemento)
            dados_antigos.append(dados_antigos_1)
            dados_antigos_1= []

        # Posição à inserir o novo elemento
        cont = -1
        for c in range(0, len(dados_antigos)):
            cont += 1
            if dados_novos[0] == dados_antigos[c][0]:
                break

        # Excluir dados da tabela
        for c in range(0, len(dados_antigos)):
            cursor_bd.execute('DELETE FROM '+nome_tabela_hidrometria+' WHERE vertical = ?', (dados_antigos[c][0],))

        # Inserção do elemento
        dados_antigos.insert(cont, dados_novos)

        # Atualização dos valores das verticais
        for c in range(1, len(dados_antigos)):
            if dados_antigos[c][0] == dados_antigos[c-1][0]:
                dados_antigos[c][0] = str(int(dados_antigos[c][0])+1)

        for c in range(0, len(dados_antigos)):
            str_comando_0 = 'INSERT INTO ' + nome_tabela_hidrometria + ' (vertical, distancia, profundidade, va_s, va_02, va_04, va_06, va_08, va_f, a, b) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor_bd.execute(str_comando_0, (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2], dados_antigos[c][3], dados_antigos[c][4], dados_antigos[c][5], dados_antigos[c][6], dados_antigos[c][7], dados_antigos[c][8], dados_antigos[c][9], dados_antigos[c][10]))

    conexao_bd.commit()
    conexao_bd.close()

    return

def Editar_dado_hidrometria(diretorio, id, n_vertical, dist_ponto_ref, profun, s, p02, p04, p06, p08, f, a, b, alteracoes=[]):
    """
    Função Editar_dados_hidrometria: Usada para editar o banco os dados de hidrometria.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta carregada.
    :param n_vertical: O número da vertical
    :param dist_ponto_ref: A distância da vertical até o ponto de referncia.
    :param profun: A profundidade da vertical.
    :param s: A velocidade angular na superfície.
    :param p02: A velocidade angular à 0.2 profundidade.
    :param p04: A velocidade angular à 0.4 profundidade.
    :param p06: A velocidade angular à 0.6 profundidade.
    :param p08: A velocidade angular à 0.8 profundidade.
    :param f: A velocidade angular no fundo.
    :param a: Coeficiente a da equação do molinete.
    :param b: Coeficiente b da equação do molinete.
    :param alteracoes: Um vetor contendo True/False para alterar as colunas do dado correspondente
    :return: Não retorna valores.
    """
    nome_tabela_hidrometria = 'Hidrometria_id' + str(id)

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    if n_vertical == '0' or n_vertical == 'n':
        str_comando = 'UPDATE ' + nome_tabela_hidrometria + ' SET distancia = ? WHERE vertical = ?'
        cursor_bd.execute(str_comando, (dist_ponto_ref, n_vertical))

    else:
        nome_colunas = ['a', 'b', 'vertical', 'distancia', 'profundidade', 'va_s', 'va_02', 'va_04', 'va_06', 'va_08', 'va_f']
        entradas = [ a, b, n_vertical, dist_ponto_ref, profun, s, p02, p04, p06, p08, f]
        for c in range(0, 11):
            str_comando = 'UPDATE ' + nome_tabela_hidrometria + ' SET '
            if alteracoes [c]:
                str_comando = str_comando + nome_colunas[c] + ' = ? WHERE vertical = ?'
                if c > 4 and entradas[c] == '':
                    cursor_bd.execute(str_comando, ('-', n_vertical))
                else:
                    cursor_bd.execute(str_comando, (entradas[c], n_vertical))

    conexao_bd.commit()
    conexao_bd.close()

    return

def Excluir_dado_hidrometria(diretorio, id, n_vertical):
    """
    Função Excluir_dado_hidrometria: Usada para excluir um dado de hidrometria.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :param n_vertical: O numero da vertical a ser excluída.
    :return: Não retorna valores.
    """
    nome_tabela_hidrometria = 'Hidrometria_id' + str(id)

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    str_comando =  'DELETE FROM ' + nome_tabela_hidrometria + ' WHERE vertical = ?'
    cursor_bd.execute(str_comando, (n_vertical,))

    verticais_antigas = []
    verticais = []
    for linha in cursor_bd.execute('SELECT * FROM ' + nome_tabela_hidrometria):
        verticais_antigas.append(linha[0])
        verticais.append(linha[0])

    for c in range(0, len(verticais)):
        if verticais[c] != '0' and verticais[c] != 'n':
            if int(verticais[c]) >= int(verticais[c-1])+2:
                verticais[c] = str(int(verticais[c-1])+1)

    for c in range(0, len(verticais)):
        cursor_bd.execute('UPDATE ' + nome_tabela_hidrometria + ' SET vertical = ? WHERE vertical = ?',
                          (verticais[c], verticais_antigas[c]))

    conexao_bd.commit()
    conexao_bd.close()

    return

# Bt 4
def Inserir_dado_topografia(diretorio, id, op_decli_margem, op_teo_coord_reg, dados_inserir=[]):
    """
    Função Inserir_dado_topografia: Usada para inserir os dados de topografia no banco de dados.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :param op_decli_margem: 0 se declividade; 1 se margem.
    :param op_teo_coord_reg: 0 se teodolito; 1 se coordenada; 2 se réguas.
    :param dados_inserir: Uma vetor contendo os dados a serem inseridos.
    :return: Não retorna valores
    """
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Declividade
    if op_decli_margem == 0:
        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_decli_teo_id' + str(id)
            colunas = ' (n_ponto, tipo, fi, fm, fs, ang_z, ang_h, h_equip) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'

        # Coordenadas
        elif op_teo_coord_reg == 1:
            nome_tabela = 'Topo_decli_coord_id' + str(id)
            colunas = ' (n_ponto, tipo, coord_x, coord_y, coord_z) VALUES(?, ?, ?, ?, ?)'

        # Réguas
        elif op_teo_coord_reg == 2:
            nome_tabela = 'Topo_decli_reg_id' + str(id)
            colunas = ' (n_reg, tipo, leitura, coord_x, coord_y, coord_z) VALUES(?, ?, ?, ?, ?, ?)'

    # Margem
    else:
        if op_decli_margem == 1:
            margem = '0'

        else:
            margem = 'n'

        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_margem_'+margem+'_teo_id' + str(id)
            colunas = ' (n_ponto, fi, fm, fs, ang_z, ang_h, h_equip) VALUES(?, ?, ?, ?, ?, ?, ?)'

        # Coordenadas
        else:
            nome_tabela = 'Topo_margem_'+margem+'_coord_id' + str(id)
            colunas = ' (n_ponto, coord_x, coord_y, coord_z) VALUES(?, ?, ?, ?)'

    # Dados antigos e posição da inserção do dado novo
    dados_antigos = []
    pos_insercao_dados_novos = 0
    str_comando_0 ='SELECT * FROM '+ nome_tabela

    cont = -1
    pos = False
    linha_dado =[]
    for linha in cursor_bd.execute(str_comando_0):
        for elemento in linha:
            linha_dado.append(elemento)
        dados_antigos.append(linha_dado)
        linha_dado = []
        cont += 1
        if int(linha[0]) >= int(dados_inserir[0]) and pos == False:
            pos_insercao_dados_novos = cont
            pos = True

    if pos == False:
        cont += 1
        pos_insercao_dados_novos = cont

    # Exclusão dos dados antigos
    if op_decli_margem == 0 and op_teo_coord_reg == 2:
        col_0 = 'n_reg'
    else:
        col_0 = 'n_ponto'
    str_comando_1 = 'DELETE FROM ' + nome_tabela + ' WHERE '+ col_0 +' = ?'

    for c in range(0, len(dados_antigos)):
        cursor_bd.execute(str_comando_1, (dados_antigos[c][0],))

    # Atualização dos índices
    dados_antigos.insert(pos_insercao_dados_novos, dados_inserir)
    for c in range(0, len(dados_antigos)):
        dados_antigos[c][0]= str(c)

    # Inserção dos dados novos
    str_comando_2 = 'INSERT INTO ' + nome_tabela + colunas
    for c in range(0, len(dados_antigos)):
        if len(dados_antigos[c]) == 4:
            cursor_bd.execute(str_comando_2, (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2],
                                              dados_antigos[c][3]))
        elif len(dados_antigos[c]) == 5:
            cursor_bd.execute(str_comando_2, (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2],
                                              dados_antigos[c][3], dados_antigos[c][4]))

        elif len(dados_antigos[c]) == 6:
            cursor_bd.execute(str_comando_2, (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2],
                                              dados_antigos[c][3], dados_antigos[c][4], dados_antigos[c][5]))

        elif len(dados_antigos[c]) == 7:
            cursor_bd.execute(str_comando_2, (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2],
                                              dados_antigos[c][3], dados_antigos[c][4], dados_antigos[c][5],
                                              dados_antigos[c][6]))
        elif len(dados_antigos[c]) == 8:
            cursor_bd.execute(str_comando_2, (dados_antigos[c][0], dados_antigos[c][1], dados_antigos[c][2],
                                              dados_antigos[c][3], dados_antigos[c][4], dados_antigos[c][5],
                                              dados_antigos[c][6], dados_antigos[c][7]))

    conexao_bd.commit()
    conexao_bd.close()
    return

def Editar_dado_topografia(diretorio, id, op_decli_margem, op_teo_coord_reg, dados_inserir=[], alteracoes=[]):
    """
    Função Editar_dado_topografia: Usada para editar um dado de topografia.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :param op_decli_margem: 0 se declividade; 1 se margem.
    :param op_teo_coord_reg: 0 se teodolito; 1 se coordenada.
    :param dados_inserir: Um vetor com os dados a serem inseridos.
    :param alteracoes: O vetor de alterações.
    :return: Não retorna valores.
    """

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Declividade
    if op_decli_margem == 0:
        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_decli_teo_id' + str(id)
            colunas = ['n_ponto', 'tipo', 'fi', 'fm', 'fs', 'ang_z', 'ang_h', 'h_equip']

        # Coordenadas
        elif op_teo_coord_reg == 1:
            nome_tabela = 'Topo_decli_coord_id' + str(id)
            colunas = ['n_ponto', 'tipo', 'coord_x', 'coord_y', 'coord_z']

        # Réguas
        elif op_teo_coord_reg == 2:
            nome_tabela = 'Topo_decli_reg_id' + str(id)
            colunas = ['n_reg', 'tipo', 'leitura', 'coord_x', 'coord_y', 'coord_z']

    # Margem
    else:
        if op_decli_margem == 1:
            margem = '0'

        else:
            margem = 'n'
        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_margem_'+ margem +'_teo_id' + str(id)
            colunas = ['n_ponto', '', 'fi', 'fm', 'fs', 'ang_z', 'ang_h', 'h_equip']

        # Coordenadas
        else:
            nome_tabela = 'Topo_margem_'+ margem +'_coord_id' + str(id)
            colunas = ['n_ponto', '', 'coord_x', 'coord_y', 'coord_z']

    if op_decli_margem == 0 and op_teo_coord_reg == 2:
        col_0 = 'n_reg'
    else:
        col_0 = 'n_ponto'

    for c in range(1, len(dados_inserir)):
        if alteracoes[c]:
            cursor_bd.execute('UPDATE '+ nome_tabela + ' SET '+ colunas[c] + ' = ? WHERE '+ col_0 +' = ?', (dados_inserir[c], dados_inserir[0]))

    conexao_bd.commit()
    conexao_bd.close()

    return

def Excluir_Dado_Topogafia(diretorio, id, op_decli_margem, op_teo_coord_reg, num_pt):
    """
    Função Excluir_Dado_Topogafia: Usada para excluir um dado de topografia.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :param op_decli_margem: 0 se declividade; 1 se margem.
    :param op_teo_coord_reg: 0 se teodolito; 1 se coordenada.
    :param num_pt: O número do ponto a ser excluído.
    :return: Não retorna valores.
    """

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Declividade
    if op_decli_margem == 0:
        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_decli_teo_id' + str(id)
            colunas = ' (n_ponto, tipo, fi, fm, fs, ang_z, ang_h, h_equip) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'

        # Coordenadas
        elif op_teo_coord_reg == 1:
            nome_tabela = 'Topo_decli_coord_id' + str(id)
            colunas = ' (n_ponto, tipo, coord_x, coord_y, coord_z) VALUES(?, ?, ?, ?, ?)'

        # Réguas
        elif op_teo_coord_reg == 2:
            nome_tabela = 'Topo_decli_reg_id' + str(id)
            colunas = ' (n_reg, tipo, leitura, coord_x, coord_y, coord_z) VALUES(?, ?, ?, ?, ?, ?)'

    # Margem
    else:
        if op_decli_margem == 1:
            margem = '0'

        else:
            margem = 'n'
        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_margem_'+margem+'_teo_id' + str(id)
            colunas = ' (n_ponto, fi, fm, fs, ang_z, ang_h, h_equip) VALUES(?, ?, ?, ?, ?, ?, ?)'

        # Coordenadas
        else:
            nome_tabela = 'Topo_margem_'+margem+'_coord_id' + str(id)
            colunas = ' (n_ponto, coord_x, coord_y, coord_z) VALUES(?, ?, ?, ?)'

    if op_decli_margem == 0 and op_teo_coord_reg == 2:
        col_0 = 'n_reg'
    else:
        col_0 = 'n_ponto'

    str_comando_0 = 'DELETE FROM ' + nome_tabela + ' WHERE '+ col_0 +' = ?'
    cursor_bd.execute(str_comando_0, (num_pt,))

    str_comando_1 = 'SELECT * FROM ' + nome_tabela

    dados = []
    for linha in cursor_bd.execute(str_comando_1):
        dados_linha = []
        for elemento in linha:
            dados_linha.append(elemento)
        dados.append(dados_linha)

    for c in range(0, len(dados)):
        cursor_bd.execute(str_comando_0, (dados[c][0],))
        dados[c][0] = str(c)

    # Inserção dos dados novos
    str_comando_2 = 'INSERT INTO ' + nome_tabela + colunas
    for c in range(0, len(dados)):
        if len(dados[c]) == 4:
            cursor_bd.execute(str_comando_2, (dados[c][0], dados[c][1], dados[c][2],
                                              dados[c][3]))
        elif len(dados[c]) == 5:
            cursor_bd.execute(str_comando_2, (dados[c][0], dados[c][1], dados[c][2],
                                              dados[c][3], dados[c][4]))
        elif len(dados[c]) == 6:
            cursor_bd.execute(str_comando_2, (dados[c][0], dados[c][1], dados[c][2],
                                              dados[c][3], dados[c][4], dados[c][5]))
        elif len(dados[c]) == 7:
            cursor_bd.execute(str_comando_2, (dados[c][0], dados[c][1], dados[c][2],
                                              dados[c][3], dados[c][4], dados[c][5],
                                              dados[c][6]))
        elif len(dados[c]) == 8:
            cursor_bd.execute(str_comando_2, (dados[c][0], dados[c][1], dados[c][2],
                                              dados[c][3], dados[c][4], dados[c][5],
                                              dados[c][6], dados[c][7]))

    conexao_bd.commit()
    conexao_bd.close()

    return

#Bt_5
def Calcula_parametros_h(diretorio, id):
    """
    Função Calcula_parametros_h: Usada para cacular os parametros hidráulicos provenientes da hidrometria.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :return: Não retorna valores
    """
    # Nome das tabelas
    nome_tabela_hidrometria = 'Hidrometria_id' + str(id)

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Cálculo dos Parâmetros

    # Hidrometria
    # Dados
    dados_hidrometria = []
    for linha in cursor_bd.execute('SELECT * FROM ' + nome_tabela_hidrometria):
        dados_hidrometria.append(linha)

    if len(dados_hidrometria) == 2 and (dados_hidrometria[0][1] == 'Editar' or dados_hidrometria[1][1] == 'Editar'):
        pass
    else:
        # Largura
        m_0 = dados_hidrometria[0][1]
        m_n = dados_hidrometria[len(dados_hidrometria)-1][1]
        try:
            largura = float(m_n)-float(m_0)
            if largura > 0:
                largura = f'{largura:.6f}'
            else:
                largura = 'Erro'
        except Exception:
            largura = 'Erro'

        cursor_bd.execute("UPDATE Parametros SET largura = ? WHERE id = ?", (largura, str(id)))

        # Perímetro molhado
        perimetro_molhado = 0

        try:
            for c in range(len(dados_hidrometria)-1):
                if float(dados_hidrometria[c][1]) >= float(dados_hidrometria[c+1][1]):
                    perimetro_molhado = 'Erro'
                    break
                else:
                    perimetro_molhado = perimetro_molhado + Distancia(dados_hidrometria[c][1], dados_hidrometria[c+1][1],
                                                                      dados_hidrometria[c][2], dados_hidrometria[c+1][2])

        except Exception:
            perimetro_molhado = 'Erro'

        if perimetro_molhado != 'Erro':
            perimetro_molhado = f'{perimetro_molhado:.6f}'

        cursor_bd.execute("UPDATE Parametros SET peri_mo = ? WHERE id = ?", (perimetro_molhado, str(id)))

        # Área molhada
        area_molhada = 0
        area_molhada_parcial =[]

        if perimetro_molhado == 'Erro':
            area_molhada = 'Erro'

        else:
            try:
                for c in range(0, len(dados_hidrometria)-1):
                    area_molhada_parcial.append((float(dados_hidrometria[c+1][2])+float(dados_hidrometria[c][2]))*(float(dados_hidrometria[c+1][1])-float(dados_hidrometria[c][1]))/2)
                    area_molhada = area_molhada + area_molhada_parcial[c]

                area_molhada = f'{area_molhada:.6f}'

            except Exception:
                area_molhada = 'Erro'

        cursor_bd.execute("UPDATE Parametros SET area_mo = ? WHERE id = ?", (area_molhada, str(id)))

        # Raio hidráulico
        if area_molhada != 'Erro' and perimetro_molhado != 'Erro':
            try:
                raio_hidraulico = float(area_molhada)/float(perimetro_molhado)
                raio_hidraulico = f'{raio_hidraulico:.6f}'
            except Exception:
                raio_hidraulico = 'Erro'
        else:
            raio_hidraulico = 'Erro'

        cursor_bd.execute("UPDATE Parametros SET raio_h = ? WHERE id = ?", (raio_hidraulico, str(id)))

        # Profundidade média
        if largura != 'Erro' and area_molhada != 'Erro':
            try:
                prof_media = float(area_molhada)/float(largura)
                prof_media = f'{prof_media:.6f}'
            except Exception:
                prof_media = 'Erro'
        else:
            prof_media = 'Erro'

        cursor_bd.execute("UPDATE Parametros SET prof_med = ? WHERE id = ?", (prof_media, str(id)))

        # Velocidades nas verticais
        velocidade_vertical = []
        opcoes_calculo_velocidade = [[False, False, False, True, False, False],
                                     [False, True, False, False, True, False],
                                     [False, True, False, True, True, False],
                                     [False, True, True, True, True, False],
                                     [True, True, True, True, True, True]]

        for c0 in range(0, len(dados_hidrometria)):

            if c0 == 0 or c0 == len(dados_hidrometria) -1:
                velocidade_vertical.append(0)

            else:
                opcao_adotada = []
                vel_porcent_imercao = []
                for c1 in range(0, 6):
                    if dados_hidrometria[c0][c1+3] == '-':
                        opcao_adotada.append(False)
                        vel_porcent_imercao.append(0)
                    else:
                        opcao_adotada.append(True)
                        vel_porcent_imercao.append(float(dados_hidrometria[c0][9])*float(dados_hidrometria[c0][c1+3])+float(dados_hidrometria[c0][10]))

                for c2 in range(0, 5):
                    if opcao_adotada == opcoes_calculo_velocidade[c2]:
                        pos = c2

                coef_vel_verticais = [[0, 0, 0, 1, 0, 0], [0, 1/2, 0, 0, 1/2, 0], [0, 1/4, 0, 2/4, 1/4, 0],
                                      [0, 1/6, 2/6, 2/6, 1/6, 0], [1/10, 2/10, 2/10, 2/10, 2/10, 1/10]]

                velocidade_vertical_parcial = 0
                for c3 in range(0, 6):
                    velocidade_vertical_parcial = velocidade_vertical_parcial + coef_vel_verticais[pos][c3]*vel_porcent_imercao[c3]

                velocidade_vertical.append(velocidade_vertical_parcial)

        # Vazão
        if area_molhada == 'Erro':
            vazao = 'Erro'

        else:
            vazao_parcial = []
            vazao = 0
            for c in range(0, len(area_molhada_parcial)):
                vazao_parcial.append(float(area_molhada_parcial[c])*(velocidade_vertical[c]+velocidade_vertical[c+1])/2)
                vazao = vazao + vazao_parcial[c]

            vazao = f'{vazao:.6f}'

        cursor_bd.execute("UPDATE Parametros SET vazao = ? WHERE id = ?", (vazao, str(id)))

        # Velocidade média
        if vazao == 'Erro' or area_molhada == 'Erro':
            vel_media = 'Erro'
        else:
            try:
                vel_media = float(vazao)/float(area_molhada)
                vel_media = f'{vel_media:.6f}'
            except Exception:
                vel_media = 'Erro'

        cursor_bd.execute("UPDATE Parametros SET vel_media = ? WHERE id = ?", (vel_media, str(id)))

    conexao_bd.commit()
    conexao_bd.close()
    return

def Calcula_parametros_t(diretorio, id):
    """
    Função Calcula_parametros_t: Usada para cacular os parametros hidráulicos provenientes da topografia.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :return:
    """
    nome_tabela_topo_margem_0_teo = 'Topo_margem_0_teo_id' + str(id)
    nome_tabela_topo_margem_n_teo = 'Topo_margem_n_teo_id' + str(id)
    nome_tabela_topo_margem_0_coord = 'Topo_margem_0_coord_id' + str(id)
    nome_tabela_topo_margem_n_coord = 'Topo_margem_n_coord_id' + str(id)

    # Tabelas topografia
    nome_tabela_topo = ['Topo_decli_teo_id' + str(id), 'Topo_decli_coord_id' + str(id), 'Topo_decli_reg_id' + str(id)]
    metodo_coleta = ['t', 'c', 'r']

    # Tabela de opções de declividade
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    try:
        cursor_bd.execute('DELETE FROM Opcoes_declividade_' + str(id))

    except Exception:
        pass

    cursor_bd.execute('CREATE TABLE IF NOT EXISTS Opcoes_declividade_' + str(id) + ' (tipo TEXT, pontos TEXT, decli TEXT, rug TEXT)')

    for c0 in range(0, 3):
        # Dados
        dados_topo_decli_mont = []
        dados_topo_decli_sec = []
        dados_topo_decli_jus = []

        for linha in cursor_bd.execute('SELECT * FROM ' + nome_tabela_topo[c0]):
            if linha[1] == 'm':
                dados_topo_decli_mont.append(linha)
            elif linha[1] == 's':
                dados_topo_decli_sec.append(linha)
            else:
                dados_topo_decli_jus.append(linha)

        if (len(dados_topo_decli_mont) == 0 and len(dados_topo_decli_sec) == 0) or \
                (len(dados_topo_decli_jus) == 0 and len(dados_topo_decli_sec) == 0) or \
                (len(dados_topo_decli_mont) == 0 and len(dados_topo_decli_jus) == 0):
            cursor_bd.execute('UPDATE Parametros SET decli_'+ metodo_coleta[c0] +' = ? WHERE id = ?', ('-', str(id)))
            cursor_bd.execute('UPDATE Parametros SET rug_' + metodo_coleta[c0] + ' = ? WHERE id = ?', ('-', str(id)))

        else:
            declividades = []
            # Apenas pontos de montante e jusante da seção
            if len(dados_topo_decli_jus) == 0 or len(dados_topo_decli_sec) == 0 or len(dados_topo_decli_mont) == 0:

                dados_topo_cota_sup = []
                dados_topo_cota_inf = []

                if len(dados_topo_decli_mont) == 0:
                    dados_topo_cota_sup = dados_topo_decli_sec
                else:
                    dados_topo_cota_sup = dados_topo_decli_mont

                if len(dados_topo_decli_jus) == 0:
                    dados_topo_cota_inf = dados_topo_decli_sec
                else:
                    dados_topo_cota_inf = dados_topo_decli_jus

                for c1 in range(0, len(dados_topo_cota_inf)):
                    for c2 in range(0, len(dados_topo_cota_sup)):

                        # Teodolito
                        if c0 == 0:
                            coord_jus = Coord_teo(dados_topo_cota_inf[c1][2], dados_topo_cota_inf[c1][3],
                                                  dados_topo_cota_inf[c1][4], dados_topo_cota_inf[c1][5],
                                                  dados_topo_cota_inf[c1][6], dados_topo_cota_inf[c1][7])

                            coord_mont = Coord_teo(dados_topo_cota_sup[c2][2], dados_topo_cota_sup[c2][3],
                                                  dados_topo_cota_sup[c2][4], dados_topo_cota_sup[c2][5],
                                                  dados_topo_cota_sup[c2][6], dados_topo_cota_sup[c2][7])

                        # Coordenadas
                        elif c0 == 1:
                            if float(dados_topo_cota_inf[c1][4]) >= float(dados_topo_cota_sup[c2][4]):
                                coord_jus = [0, 0, 0, False]
                                coord_mont = [0, 0, 0, False]
                            else:
                                coord_jus = [float(dados_topo_cota_inf[c1][2]), float(dados_topo_cota_inf[c1][3]), float(dados_topo_cota_inf[c1][4]), True]
                                coord_mont = [float(dados_topo_cota_sup[c2][2]), float(dados_topo_cota_sup[c2][3]), float(dados_topo_cota_sup[c2][4]), True]

                        # Réguas
                        else:
                            if float(dados_topo_cota_inf[c1][5]) >= float(dados_topo_cota_sup[c2][5]):
                                coord_jus = [0, 0, 0, False]
                                coord_mont = [0, 0, 0, False]
                            else:
                                coord_jus = [float(dados_topo_cota_inf[c1][3]), float(dados_topo_cota_inf[c1][4]), float(dados_topo_cota_inf[c1][5])+float(dados_topo_cota_inf[c1][2]), True]
                                coord_mont = [float(dados_topo_cota_sup[c2][3]), float(dados_topo_cota_sup[c2][4]), float(dados_topo_cota_sup[c2][5])+float(dados_topo_cota_sup[c2][2]), True]

                        if coord_jus[3] and coord_mont[3]:
                            try:
                                declividade = (coord_mont[2] - coord_jus[2]) / Distancia(coord_mont[0], coord_jus[0], coord_mont[1], coord_jus[1])
                            except Exception:
                                declividade = 'Erro'

                        else:
                            declividade = 'Erro'

                        if declividade != 'Erro':
                            rugosidade = Rug_manning(diretorio, id, declividade)
                            declividade = f'{declividade:.6f}'
                            try:
                                if rugosidade == '-':
                                    pass
                                else:
                                    rugosidade = f'{rugosidade:.6f}'
                            except Exception:
                                rugosidade = 'Erro'

                        else:
                            rugosidade ='Erro'

                        declividades.append(declividade)

                        cursor_bd.execute('INSERT INTO Opcoes_declividade_' + str(id) + ' (tipo, pontos, decli, rug) VALUES (?, ?, ?, ?)', (metodo_coleta[c0].upper(), dados_topo_cota_inf[c1][0] + ' e ' + dados_topo_cota_sup[c2][0], declividade, rugosidade))

            # Ponto da seção presente
            else:
                for c1 in range(0, len(dados_topo_decli_jus)):
                    for c2 in range(0, len(dados_topo_decli_sec)):
                        for c3 in range(0, len(dados_topo_decli_mont)):

                            # Teodolito
                            if c0 == 0:
                                coord_jus = Coord_teo(dados_topo_decli_jus[c1][2], dados_topo_decli_jus[c1][3], dados_topo_decli_jus[c1][4], dados_topo_decli_jus[c1][5], dados_topo_decli_jus[c1][6], dados_topo_decli_jus[c1][7])
                                coord_sec = Coord_teo(dados_topo_decli_sec[c2][2], dados_topo_decli_sec[c2][3], dados_topo_decli_sec[c2][4], dados_topo_decli_sec[c2][5], dados_topo_decli_sec[c2][6], dados_topo_decli_sec[c2][7])
                                coord_mont = Coord_teo(dados_topo_decli_mont[c3][2], dados_topo_decli_mont[c3][3], dados_topo_decli_mont[c3][4], dados_topo_decli_mont[c3][5], dados_topo_decli_mont[c3][6], dados_topo_decli_mont[c3][7])

                            # Coordenadas
                            elif c0 == 1:
                                if float(dados_topo_decli_jus[c1][4]) >= float(dados_topo_decli_mont[c3][4]) or float(dados_topo_decli_sec[c2][4]) >= float(dados_topo_decli_mont[c3][4]) or float(dados_topo_decli_jus[c1][4]) >= float(dados_topo_decli_sec[c2][4]):
                                    coord_jus = [0, 0, 0, False]
                                    coord_sec = [0, 0, 0, False]
                                    coord_mont = [0, 0, 0, False]

                                else:
                                    coord_jus = [float(dados_topo_decli_jus[c1][2]), float(dados_topo_decli_jus[c1][3]), float(dados_topo_decli_jus[c1][4]), True]
                                    coord_sec = [float(dados_topo_decli_sec[c2][2]), float(dados_topo_decli_sec[c2][3]), float(dados_topo_decli_sec[c2][4]), True]
                                    coord_mont = [float(dados_topo_decli_mont[c3][2]), float(dados_topo_decli_mont[c3][3]), float(dados_topo_decli_mont[c3][4]), True]

                            # Réguas
                            else:
                                if float(dados_topo_decli_jus[c1][5]) >= float(dados_topo_decli_mont[c3][5]) or float(dados_topo_decli_jus[c1][5]) >= float(dados_topo_decli_sec[c2][5]) or float(dados_topo_decli_sec[c2][5]) >= float(dados_topo_decli_mont[c3][5]):
                                    coord_jus = [0, 0, 0, False]
                                    coord_sec = [0, 0, 0, False]
                                    coord_mont = [0, 0, 0, False]
                                else:
                                    coord_jus = [float(dados_topo_decli_jus[c1][3]), float(dados_topo_decli_jus[c1][4]), float(dados_topo_decli_jus[c1][5]) + float(dados_topo_decli_jus[c1][2]), True]
                                    coord_sec = [float(dados_topo_decli_sec[c2][3]), float(dados_topo_decli_sec[c2][4]), float(dados_topo_decli_sec[c2][5]) + float(dados_topo_decli_sec[c2][2]), True]
                                    coord_mont = [float(dados_topo_decli_mont[c3][3]), float(dados_topo_decli_mont[c3][4]), float(dados_topo_decli_mont[c3][5]) + float(dados_topo_decli_mont[c3][2]), True]

                            if coord_jus[3] and coord_sec[3] and coord_mont[3]:
                                try:
                                    declividade_m_s = (coord_mont[2] - coord_sec[2]) / Distancia(coord_mont[0], coord_sec[0], coord_mont[1], coord_sec[1])
                                    declividade_s_j = (coord_sec[2] - coord_jus[2]) / Distancia(coord_sec[0], coord_jus[0], coord_sec[1], coord_jus[1])
                                    declividade = (declividade_m_s + declividade_s_j)/2
                                except Exception:
                                    declividade = 'Erro'

                            else:
                                declividade = 'Erro'

                            if declividade != 'Erro':
                                try:
                                    rugosidade = Rug_manning(diretorio, id, declividade)
                                    declividade = f'{declividade:.6f}'
                                    if rugosidade == '-':
                                        pass
                                    else:
                                        rugosidade = f'{rugosidade:.6f}'
                                except Exception:
                                    rugosidade = 'Erro'

                            else:
                                rugosidade = 'Erro'

                            declividades.append(declividade)

                            cursor_bd.execute('INSERT INTO Opcoes_declividade_' + str(id) + ' (tipo, pontos, decli, rug) VALUES (?, ?, ?, ?)',
                                              (metodo_coleta[c0].upper(),
                                               dados_topo_decli_jus[c1][0] +', '+ dados_topo_decli_sec[c2][0]+' e ' + dados_topo_decli_mont[c3][0],
                                               declividade, rugosidade))

            # Valores finais de declividade e rugosidade
            decliviade_final = 0
            for c1 in range(0, len(declividades)):
                try:
                    decliviade_final = float(decliviade_final) + float(declividades[c1])
                except Exception:
                    decliviade_final = 'Erro'
                    break

            if decliviade_final != 'Erro':
                decliviade_final = decliviade_final / len(declividades)
                try:
                    rugosidade_final = Rug_manning(diretorio, id, decliviade_final)
                except Exception:
                    rugosidade_final = 'Erro'

                decliviade_final = f'{decliviade_final:.6f}'
            else:
                rugosidade_final = 'Erro'

            if rugosidade_final != 'Erro' and rugosidade_final != '-':
                rugosidade_final = f'{rugosidade_final:.6f}'

            cursor_bd.execute('UPDATE Parametros SET decli_' + metodo_coleta[c0] + ' = ? WHERE id = ?',
                              (decliviade_final, str(id)))
            cursor_bd.execute('UPDATE Parametros SET rug_' + metodo_coleta[c0] + ' = ? WHERE id = ?',
                              (rugosidade_final, str(id)))

    conexao_bd.commit()
    conexao_bd.close()

    return

def Obter_txt_parametros(diretorio_secao, id, diretorio_txt, nome_arq):
    """
    Função Obter_txt_parametros: Usada para obter um arquivo txt com os parâmetros.
    :param diretorio_secao: O diretório do banco de dados.
    :param id: O id da coleta carregada.
    :param diretorio_txt: O diretório do arquivo .txt.
    :param nome_arq: O nome do arquivo .txt.
    :return: O êxito em criar o arquivo True/False
    """
    try:
        # Arquivo existente
        try:
            with open(diretorio_txt+'//'+nome_arq+'.txt', 'x') as arquivo:
                pass
            arq = True

        except Exception:
            arq = False

        # Criação e escrita do arquivo
        if arq:
            conexao_bd = sqlite3.connect(diretorio_secao)
            cursor_bd = conexao_bd.cursor()

            num_t = 200
            with open(diretorio_txt + '//' + nome_arq + '.txt', 'w') as arquivo:

                # Data do processamento
                tempo_agora = str(datetime.now())
                tempo_agora = tempo_agora[:19]
                arquivo.write(f'Processado em: {tempo_agora}\n\n')

                # Informações da seção
                t_elementos_is = ["Nome do corpo d'água:", 'Localização:', 'Nome da seção:', 'Descrição:']
                cont0 = 0
                arquivo.write(f'{Tracos("Identificação da seção transversal", num_t)}\n')
                for linha in cursor_bd.execute('SELECT * FROM Info_secao'):
                    for elemento in linha:
                        arquivo.write(f'{t_elementos_is[cont0]}\n')
                        arquivo.write(f'{elemento}\n\n')
                        cont0 += 1
                        if cont0 == 4:
                            break

                # Informações da coleta
                t_elementos_ic = ['Data', 'Hora de início', 'Hora de término']
                arquivo.write(f'{Tracos("Coleta de dados", num_t)}\n')
                for linha in cursor_bd.execute('SELECT * FROM Info_coletas WHERE id = ?', (str(id),)):
                    arquivo.write(f'{t_elementos_ic[0]:^15}\t{t_elementos_ic[1]:^15}\t{t_elementos_ic[2]:^15}\n')
                    arquivo.write(f'{linha[0]:^15}\t{linha[1]:^15}\t{linha[2]:^15}\n\n')

                # Hidrometria
                arquivo.write(f'{Tracos("Hidrometria", num_t)}\n')
                t_elementos_h0 = ['Vertical número', 'Distância do ponto de referência (m)', 'Profundidade (m)',
                                 'Velocidade angular']
                t_elementos_h1 = ['(0)', '(1)', '(2)', 'S', '0.2p', '0.4p', '0.6p', '0.8p', 'F', 'a', 'b']
                for c in range(0, len(t_elementos_h0)):
                    arquivo.write(f'({c}) - {t_elementos_h0[c]}\n')

                arquivo.write('\n')
                for c in range(0, len(t_elementos_h1)):
                    if c > 2 and c < 9:
                        va = '(3) '
                    else:
                        va = ''
                    arquivo.write(f'{va+t_elementos_h1[c]:^10}')
                    if c != len(t_elementos_h1)-1:
                        arquivo.write('\t')
                    else:
                        arquivo.write('\n')

                for linha in cursor_bd.execute('SELECT * FROM Hidrometria_id' + str(id)):
                    for elemento in linha:
                        arquivo.write(f'{elemento:^10}\t')
                    arquivo.write('\n')
                arquivo.write('\n')

                # Topografia
                arquivo.write(f'{Tracos("Topografia - Declividade", num_t)}\n')

                metodo = ['Teodolito', 'Coordenadas', 'Réguas']
                titulos_topo = [['Ponto número', 'Tipo (m, s, j)', 'FI (m)', 'FM (m)', 'FS (m)', 'Ângulo zenital (ggg mm ss)', 'Ângulo horizontal (ggg mm ss)', 'Altura do equipamento (m)'],
                                ['Ponto número', 'Tipo (m, s, j)', 'Coordenada x (m)', 'Coordenada y (m)', 'Coordenada z (m)'],
                                ['Régua número', 'Tipo (m, s, j)', 'Leitura (m)', 'Coordenada x (m)', 'Coordenada y (m)', 'Coordenada z (m)']]
                nome_tabela_topo = ['Topo_decli_teo_id' + str(id), 'Topo_decli_coord_id' + str(id), 'Topo_decli_reg_id' + str(id)]

                for c0 in range(0, 3):
                    titulos_topo_1 = []
                    arquivo.write(f'{metodo[c0]}\n')
                    for c1 in range(0, len(titulos_topo[c0])):
                        arquivo.write(f'({c1}) - {titulos_topo[c0][c1]}\n')
                        titulos_topo_1.append(f'({c1})')
                    arquivo.write('\n')
                    for c2 in range(0, len(titulos_topo[c0])):
                        arquivo.write(f'{titulos_topo_1[c2]:^10}')
                        if c2 != len(titulos_topo[c0]) - 1:
                            arquivo.write('\t')
                        else:
                            arquivo.write('\n')
                    for linha in cursor_bd.execute('SELECT * FROM '+ nome_tabela_topo[c0]):
                        for elemento in linha:
                            arquivo.write(f'{elemento:^10}\t')
                        arquivo.write('\n')
                    arquivo.write('\n')

                # Cálculo dos parâmetros hidráulicos
                texto_parametros = [' Largura (m):', ' Perímetro molhado (m):', ' Área molhada (m2):',
                                    ' Raio hidráulico (m):', ' Profundidade média (m):', ' Vazão (m3/s):',
                                    ' Velocidade média (m/s):', ' Declividade T (m/m):', ' Declividade C (m/m):',
                                    ' Declividade R (m/m):', ' Rugosidade de Manning T:', ' Rugosidade de Manning C:',
                                    ' Rugosidade de Manning R:']

                arquivo.write(f'{Tracos("Cálculo dos parâmetros hidráulicos", num_t)}\n')

                for linha in cursor_bd.execute('SELECT * FROM Parametros WHERE id = ?', (id,)):
                    for c in range(1, len(linha)):
                        arquivo.write(f'{texto_parametros[c-1]:<30} {linha[c]:<15}\n')
                arquivo.write('\n')

                # Detalhamento da declividade e da rugosidade
                titulos_det_decli_rug = ['Método', 'Pontos/Réguas', 'Declividade (m/m)', 'Rugosidade']
                titulos_det_decli_rug_1 = []

                arquivo.write(f'{Tracos("Detalhamento da declividade e da rugosidade", num_t)}\n')

                for c in range(0, len(titulos_det_decli_rug)):
                    arquivo.write(f'({c}) - {titulos_det_decli_rug[c]}\n')
                    titulos_det_decli_rug_1.append(f'({c})')
                arquivo.write('\n')

                for c in range(0, len(titulos_det_decli_rug_1)):
                    arquivo.write(f'{titulos_det_decli_rug_1[c]:^10}')
                    if c != len(titulos_det_decli_rug_1)-1:
                        arquivo.write('\t')
                    else:
                        arquivo.write('\n')

                for linha in cursor_bd.execute('SELECT * FROM Opcoes_declividade_' + str(id)):
                    for elemento in linha:
                        arquivo.write(f'{elemento:^10}\t')
                    arquivo.write('\n')
                arquivo.write('\n')

                arquivo.close()
            conexao_bd.close()
            exito = True
        else:
            exito = False

    except Exception:
        exito = False

    return exito

def Tracos(texto, n):
    """
    Função Tracos: Usada para completar a linha de um texto com o caracter '-'.
    :param texto: O texto original.
    :param n: O número de caracteres da linha, incluindo o texto e os traços.
    :return: O texto retificado.
    """
    t = (n-len(texto)-1)*'-'
    return f'{texto} {t}'

# Bt 6
def Determinar_coordenadas_rel_secao(diretorio, id):
    """
    Função Determinar_coordenadas_rel_secao: Usada para determinar as coordenadas relativas da seção transversal.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta carregada.
    :return: Não retorna valores.
    """
    # Acesso dos dados
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    # Dados de hidrometria
    d_hidro = []
    for linha in cursor_bd.execute('SELECT * FROM Hidrometria_id' + str(id)):
        d_hidro.append(linha)

    # Dados margem e teodolito
    d_margem_0_teo = []
    for linha in cursor_bd.execute('SELECT * FROM Topo_margem_0_teo_id' + str(id)):
        d_margem_0_teo.append(linha)

    d_margem_n_teo = []
    for linha in cursor_bd.execute('SELECT * FROM Topo_margem_n_teo_id' + str(id)):
        d_margem_n_teo.append(linha)

    # Dados margem e coordenadas
    d_margem_0_coord =[]
    for linha in cursor_bd.execute('SELECT * FROM Topo_margem_0_coord_id' + str(id)):
        d_margem_0_coord.append(linha)

    d_margem_n_coord =[]
    for linha in cursor_bd.execute('SELECT * FROM Topo_margem_n_coord_id' + str(id)):
        d_margem_n_coord.append(linha)

    # Determinação das coordenadas relativas

    cursor_bd.execute('DELETE FROM Coord_rel_sec_' + str(id))

    cursor_bd.execute('CREATE TABLE IF NOT EXISTS Coord_rel_sec_' + str(id) + ' (tipo TEXT, coord_x TEXT, coord_y TEXT)')

    coord_rel_hidro = []
    # Hidrometria
    for c in range(0, len(d_hidro)):
        coord_rel_hidro.append([float(d_hidro[c][1])-float(d_hidro[0][1]), float(d_hidro[c][2])*-1])

    # Margens teodolito
    coord_rel_margem = [[[], []], [[], []]] # [[[m0 teo], [mn teo]], [[m0 coord], [mn coord]]]
    dado_margem = [[d_margem_0_teo, d_margem_n_teo], [d_margem_0_coord, d_margem_n_coord]]

    for c0 in range(0, 2): # 0-teodolito; 1-coordenada
        if len(dado_margem[c0][0]) != 0 and len(dado_margem[c0][1]) != 0:
            for c1 in range(0, 2): # 0-Margem 0; 1-Margem n

                # Coordenadas originais
                x_o = []
                y_o = []
                z_o = []
                pos_zmin = 0
                for c2 in range(0, len(dado_margem[c0][c1])):
                    if c0 == 0:
                        coord_teo = Coord_teo(dado_margem[c0][c1][c2][1], dado_margem[c0][c1][c2][2], dado_margem[c0][c1][c2][3], dado_margem[c0][c1][c2][4], dado_margem[c0][c1][c2][5], dado_margem[c0][c1][c2][6])
                        x_o.append(coord_teo[0])
                        y_o.append(coord_teo[1])
                        z_o.append(coord_teo[2])

                    else:
                        x_o.append(float(dado_margem[c0][c1][c2][1]))
                        y_o.append(float(dado_margem[c0][c1][c2][2]))
                        z_o.append(float(dado_margem[c0][c1][c2][3]))

                    if z_o[c2] < z_o[pos_zmin]:
                        pos_zmin = c2

                # Translação das coordenadas
                x_tr = []
                y_tr = []
                z_tr = []
                for c2 in range(0, len(dado_margem[c0][c1])):
                    x_tr.append(x_o[c2]-x_o[pos_zmin])
                    y_tr.append(y_o[c2]-y_o[pos_zmin])
                    z_tr.append(z_o[c2]-z_o[pos_zmin])

                # Rotação das coordenadas
                x_rt = []
                y_rt = []
                z_rt = []
                try:
                    coef = polyfit(x_tr, y_tr, 1)
                    alpha = math.atan(coef[0])
                except Exception:
                    alpha = math.radians(90)

                for c2 in range(0, len(dado_margem[c0][c1])):
                    x_rt.append(x_tr[c2]*math.cos(alpha) + y_tr[c2]*math.sin(alpha))
                    y_rt.append(-1*x_tr[c2]*math.sin(alpha) + y_tr[c2]*math.cos(alpha))
                    z_rt.append(z_tr[c2])
                    if (c1 == 0 and x_rt[c2] > 0) or (c1 == 1 and x_rt[c2] < 0):
                        x_rt[c2] = -1*x_rt[c2]

                # Coordenadas relativas finais
                if c1 == 0:
                    acres = 0
                else:
                    acres = coord_rel_hidro[len(coord_rel_hidro) - 1][0]

                for c2 in range(0, len(dado_margem[c0][c1])):
                    if f'{x_rt[c2]:.3f}' != '0.000' and f'{x_rt[c2]:.3f}' != '-0.000' and f'{z_rt[c2]:.3f}' != '0.000' and f'{z_rt[c2]:.3f}' != '-0.000':
                        if len(coord_rel_margem[c0][c1]) == 0:
                            coord_rel_margem[c0][c1].append([x_rt[c2]+acres, z_rt[c2]])
                        else:
                            inserido = False
                            for c3 in range(0, len(coord_rel_margem[c0][c1])):
                                if coord_rel_margem[c0][c1][c3][0] > x_rt[c2]+acres:
                                    coord_rel_margem[c0][c1].insert(c3, [x_rt[c2]+acres, z_rt[c2]])
                                    inserido = True
                                    break
                            if inserido == False:
                                coord_rel_margem[c0][c1].append([x_rt[c2]+acres, z_rt[c2]])

    # Inserção no banco de dados
    somente_hidro = True
    metodo = ['T', 'C']

    for c0 in range(0, 2): # 0-teodolito; 1-coordenada
        if len(coord_rel_margem[c0][0]) > 0 and len(coord_rel_margem[c0][1]) > 0:
            somente_hidro = False
            for c1 in range(0, len(coord_rel_margem[c0][0])):
                cursor_bd.execute('INSERT INTO Coord_rel_sec_' + str(id)+' (tipo , coord_x , coord_y) VALUES(?, ?, ?)', (metodo[c0] +' - 0', f'{coord_rel_margem[c0][0][c1][0]:.3f}', f'{coord_rel_margem[c0][0][c1][1]:.3f}'))

            for c1 in range(0, len(coord_rel_hidro)):
                cursor_bd.execute('INSERT INTO Coord_rel_sec_' + str(id)+' (tipo , coord_x , coord_y) VALUES(?, ?, ?)', (metodo[c0] + ' - h', f'{coord_rel_hidro[c1][0]:.3f}', f'{coord_rel_hidro[c1][1]:.3f}'))

            for c1 in range(0, len(coord_rel_margem[c0][1])):
                cursor_bd.execute('INSERT INTO Coord_rel_sec_' + str(id) + ' (tipo , coord_x , coord_y) VALUES(?, ?, ?)', (metodo[c0] + ' - n', f'{coord_rel_margem[c0][1][c1][0]:.3f}', f'{coord_rel_margem[c0][1][c1][1]:.3f}'))

    if somente_hidro:
        for c in range(0, len(coord_rel_hidro)):
            cursor_bd.execute('INSERT INTO Coord_rel_sec_' + str(id) + ' (tipo , coord_x , coord_y) VALUES(?, ?, ?)', ('h', f'{coord_rel_hidro[c][0]:.3f}', f'{coord_rel_hidro[c][1]:.3f}'))

    conexao_bd.commit()
    conexao_bd.close()

    return

def Extrapolar_parametros(diretorio, id, dados_decli=[], dados_rug=[], dados_arqs=[]):
    """
    Função Extrapolar_parametros: Usada para realizar as extrapolações dos parametros assim como criar os arquivos para as mesmos.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta carregada.
    :param dados_decli: Um vetor na forma: [decli_min, decli_max, incremento_decli]
    :param dados_rug: Um vetor na forma: [rug_min, rug_max, incremento_rug]
    :param dados_arqs: [nome_arquivos, diretorio_arquivos]
    :return: Êxito em concluir a operação. Um vetor na forma [True/False, n]
                                           Onde n = 0: Não há erro.
                                                n = 1: Erro nas coordenadas.
                                                n = 2: Arquivos existentes.
    """
    exito = [True, 0]

    # Intervalo declividade
    i_decli = [float(dados_decli[0])]
    if float(dados_decli[2]) == 0 and dados_decli[0] != dados_decli[1]:
        i_decli.append(float(dados_decli[1]))
    elif dados_decli[0] == dados_decli[1]:
        pass
    else:
        cont0 = 1
        while i_decli[len(i_decli)-1] + float(dados_decli[2]) < float(dados_decli[1]):
            i_decli.append(float(dados_decli[0]) + float(dados_decli[2])*cont0)
            cont0 += 1
        i_decli.append(float(dados_decli[1]))

    # Intervalo rugosidade
    i_rug = [float(dados_rug[0])]
    if float(dados_rug[2]) == 0 and dados_rug[0] != dados_rug[1]:
        i_rug.append(float(dados_rug[1]))
    elif dados_rug[0] == dados_rug[1]:
        pass
    else:
        cont1 = 1
        while i_rug[len(i_rug)-1] + float(dados_rug[2]) < float(dados_rug[1]):
            i_rug.append(float(dados_rug[0]) + float(dados_rug[2])*cont1)
            cont1 += 1
        i_rug.append(float(dados_rug[1]))

    # Coordenadas
    coords = Acessar_tabela_coord_rel_sec(diretorio, id)
    coords_sel = [[], [], []]
    metodos = ['T', 'C', 'h']
    for linha in coords:
        for c in range(0, 3):
            if c != 2 and metodos[c] in linha[0]:
                vet = []
                for c1 in range(0, len(linha)):
                    try:
                        vet.append(float(linha[c1]))
                    except Exception:
                        vet.append(str(linha[c1]))
                coords_sel[c].append(vet)
            elif c == 2 and metodos[c] == linha[0]:
                vet = []
                for c1 in range(0, len(linha)):
                    try:
                        vet.append(float(linha[c1]))
                    except Exception:
                        vet.append(str(linha[c1]))
                coords_sel[c].append(vet)

    # Extrapolação
    for c0 in range(0, 3):  # c0 - métodos
        if len(coords_sel[c0]) > 0:
            # Intervalo de variação da profundidade
            # Cota mínima
            cota_min_min = True
            vert = -1
            vert_min = -1
            cont_ind_vert_min = -1
            ind_vert_min = -1
            c_ad_fundo_0 = []
            c_ad_fundo_1 = []
            for c01 in range(0, len(coords_sel[c0])):
                cont_ind_vert_min +=1
                if 'h' in coords_sel[c0][c01][0]:
                    vert += 1
                    if abs(float(coords_sel[c0][c01][2])) != 0 and (cota_min_min == True or float(coords_sel[c0][c01][2]) <= cota_min_min):#< cota_min_min):#abs(float(coords_sel[c0][c01][2])) != 0 and cota_min_min == '': #and cota_min == '':
                        if cota_min_min == True or float(coords_sel[c0][c01][2]) < cota_min_min:
                            c_ad_fundo_1 = []
                            for c02 in range(0, 3):
                                try:
                                    d1 = abs(float(coords_sel[c0][c01-c02-1][2])-float(coords_sel[c0][c01][2]))/abs(float(coords_sel[c0][c01-c02-1][1])-float(coords_sel[c0][c01][1]))
                                    d2 = abs(float(coords_sel[c0][c01+c02+1][2])-float(coords_sel[c0][c01][2]))/abs(float(coords_sel[c0][c01+c02+1][1])-float(coords_sel[c0][c01][1]))
                                    c_ad_fundo_1.append(d1 + d2)
                                except Exception:
                                    c_ad_fundo_1.append(None)
                            nova_cota_min_min = True

                        else:
                            # Cotas adjacentes
                            c_ad_fundo_0 = []
                            for c02 in range(0, 3):
                                try:
                                    d1 = abs(float(coords_sel[c0][c01 - c02 - 1][2]) - float(coords_sel[c0][c01][2])) / abs(float(coords_sel[c0][c01 - c02 - 1][1]) - float(coords_sel[c0][c01][1]))
                                    d2 = abs(float(coords_sel[c0][c01 + c02 + 1][2]) - float(coords_sel[c0][c01][2])) / abs(float(coords_sel[c0][c01 + c02 + 1][1]) - float(coords_sel[c0][c01][1]))
                                    c_ad_fundo_0.append(d1 + d2)
                                except Exception:
                                    c_ad_fundo_0.append(None)

                            if c_ad_fundo_0[0] < c_ad_fundo_1[0]:
                                nova_cota_min_min = True

                            elif c_ad_fundo_0[0] == c_ad_fundo_1[0] and c_ad_fundo_0[1] < c_ad_fundo_1[1]:
                                nova_cota_min_min = True

                            elif c_ad_fundo_0[0] == c_ad_fundo_1[0] and c_ad_fundo_0[1] == c_ad_fundo_1[1] and c_ad_fundo_0[2] < c_ad_fundo_1[2]:
                                nova_cota_min_min = True

                            else:
                                nova_cota_min_min = False

                            if nova_cota_min_min:
                                c_ad_fundo_1 = []
                                for c03 in range(0, len(c_ad_fundo_0)):
                                    c_ad_fundo_1.append(c_ad_fundo_0[c03])

                        if nova_cota_min_min:
                            cota_min_min = float(coords_sel[c0][c01][2])
                            vert_min = vert
                            ind_vert_min = cont_ind_vert_min

            incr_cota = 0.01
            cota_min = cota_min_min + incr_cota

            # Cota máxima
            cota_max_m_0 = []
            cota_max_m_n = []
            if c0 != 2:
                for c01 in range(0, len(coords_sel[c0])):
                    if '0' in coords_sel[c0][c01][0] and abs(float(coords_sel[c0][c01][2])) != 0:
                        cota_max_m_0.append(float(coords_sel[c0][c01][2]))

                    if 'n' in coords_sel[c0][c01][0] and abs(float(coords_sel[c0][c01][2])) != 0:
                        cota_max_m_n.append(float(coords_sel[c0][c01][2]))

                cota_max = min(max(cota_max_m_0), max(cota_max_m_n))
            else:
                cota_max = 0

            # Verificação das coordenadas
            for c1 in range(0, len(coords_sel[c0])-1):
                if coords_sel[c0][c1+1][1] <= coords_sel[c0][c1][1]:
                    return [False, 1]

            # Correçao em relação à vertical de profundidade mínima
            for c1 in range(0, len(coords_sel[c0])):
                coords_sel[c0][c1][2] = coords_sel[c0][c1][2]-cota_min_min

            # Variação da profundidade em relação à vertical da cota mínima
            cota_min = cota_min-cota_min_min
            cota_max = cota_max-cota_min_min
            i_cota = [cota_min]
            if cota_min == cota_max:
                pass
            else:
                cont2 = 1
                while i_cota[len(i_cota)-1] + incr_cota < cota_max:
                    i_cota.append(cota_min + incr_cota*cont2)
                    cont2 += 1
                i_cota.append(cota_max)

            # Arquivo com as extrapolações
            diretorio_principal = dados_arqs[1]+'/'+dados_arqs[0]
            # Verificação da existência dos arquivos
            for c1 in range(0, len(i_decli)): # c1 - declividade
                for c2 in range(0, len(i_rug)): # c2 - rugosidade
                    try:
                        with open(diretorio_principal + '_' + metodos[c0] + '_' + 'd' + str(f'{i_decli[c1]:.6f}').replace('.', ',') + '_' + 'r' + str(f'{i_rug[c2]:.6f}').replace('.', ',') + '.txt','x') as arquivo:
                            arquivo.close()
                    except Exception:
                        return [False, 2]

            # Caso os arquivos não existam
            for c1 in range(0, len(i_decli)):  # c1 - declividade
                for c2 in range(0, len(i_rug)):  # c2 - rugosidade
                    with open(diretorio_principal+'_'+metodos[c0]+'_'+'d'+str(f'{i_decli[c1]:.6f}').replace('.', ',')+'_'+'r'+str(f'{i_rug[c2]:.6f}').replace('.', ',')+'.txt', 'w') as arquivo:
                        # Escrita do arquivo
                        # Data do processamento
                        tempo_agora = str(datetime.now())
                        tempo_agora = tempo_agora[:19]
                        arquivo.write(f'Processado em: {tempo_agora}\n\n')

                        # Informações da seção
                        t_elementos_is = ["Nome do corpo d'água:", 'Localização:', 'Nome da seção:', 'Descrição:']
                        cont00 = 0
                        arquivo.write(f'Identificação da seção transversal\n')
                        conexao_bd = sqlite3.connect(diretorio)
                        cursor_bd = conexao_bd.cursor()
                        for linha in cursor_bd.execute('SELECT * FROM Info_secao'):
                            for elemento in linha:
                                arquivo.write(f'{t_elementos_is[cont00]}\n')
                                arquivo.write(f'{elemento}\n\n')
                                cont00 += 1
                                if cont00 == 4:
                                    break
                        conexao_bd.close()

                        # Declividade e rugosidade
                        arquivo.write(f'Declividade {i_decli[c1]:.6f} m/m\nRugosidade de Manning {i_rug[c2]:.6f}\n')

                        # Método de coleta de dados
                        if metodos[c0] == 'T':
                            met = 'Teodolito, hidrometria.'
                        elif metodos[c0] == 'C':
                            met = 'Coordenadas, hidrometria.'
                        elif metodos[c0] == 'h':
                            met = 'Hidrometria.'

                        arquivo.write(f'Dados obtidos por {met}\n\n')

                        # Coordenadas
                        arquivo.write(f'Coordenadas relativas da seção (x, y) origem (Superfície da Vertical 0, Leito da Vertical {vert_min})\n')
                        titulos_coords = ['x (m)', 'y (m)']
                        arquivo.write(f'{titulos_coords[0]:^7}\t{titulos_coords[1]:^7}\n')
                        for c3 in range(0, len(coords_sel[c0])):
                            arquivo.write(f'{coords_sel[c0][c3][1]:^7.3f}\t{coords_sel[c0][c3][2]:^7.3f}\n')
                        arquivo.write('\n')

                        # Lista de títulos das extrapolações
                        lista_titulos = [f'Profundidade na vertical {vert_min}', 'Largura (m)', 'Perímetro molhado (m)', 'Área molhada (m2)', 'Raio hidráulico (m)', 'Profundidade média (m)', 'Vazão (m3/s)', 'Velocidade média (m/s)']
                        for c3 in range(0, len(lista_titulos)):
                            arquivo.write(f'({c3}) - {lista_titulos[c3]}\n')
                        arquivo.write('\n')

                        # Títulos parametros
                        for c3 in range(0, len(lista_titulos)):
                            titulo_num = f'({c3})'
                            arquivo.write(f'{titulo_num:^7}\t')
                        arquivo.write('\n')

                        # Variação da profundidade
                        for c3 in range(0, len(i_cota)):
                            # Determinação do pontos de interese
                            pt_e = []
                            pt_d = []

                            # Ponto extremo esquerdo
                            for c4 in range(ind_vert_min, 0, -1):
                                if coords_sel[c0][c4][2] <= i_cota[c3] and coords_sel[c0][c4-1][2] >= i_cota[c3]:

                                    xa = coords_sel[c0][c4][1]
                                    xb = coords_sel[c0][c4-1][1]
                                    ya = coords_sel[c0][c4][2]
                                    yb = coords_sel[c0][c4-1][2]

                                    pt_e = [(i_cota[c3]-ya+xa*((yb-ya)/(xb-xa)))*((xb-xa)/(yb-ya)), i_cota[c3]]
                                    break

                            # Ponto extremo direito
                            for c4 in range(ind_vert_min, len(coords_sel[c0])-1):
                                if coords_sel[c0][c4][2] <= i_cota[c3] and coords_sel[c0][c4+1][2] >= i_cota[c3]:

                                    xa = coords_sel[c0][c4+1][1]
                                    xb = coords_sel[c0][c4][1]
                                    ya = coords_sel[c0][c4+1][2]
                                    yb = coords_sel[c0][c4][2]

                                    pt_d = [(i_cota[c3] - ya + xa * ((yb - ya) / (xb - xa))) * ((xb - xa) / (yb - ya)), i_cota[c3]]
                                    break

                            coords_calc = [pt_e, pt_d]

                            for c4 in range(0, len(coords_sel[c0])):
                                if coords_sel[c0][c4][1] > coords_calc[0][0] and coords_sel[c0][c4][1] < coords_calc[len(coords_calc)-1][0]:
                                    coords_calc.insert(len(coords_calc)-1, [coords_sel[c0][c4][1], coords_sel[c0][c4][2]])

                            # Cálculo dos parâmetros
                            try:
                                larg = abs(pt_d[0]-pt_e[0])

                                per_mo = 0
                                for c4 in range(0, len(coords_calc)-1):
                                    per_mo = per_mo + Distancia(coords_calc[c4][0], coords_calc[c4+1][0], coords_calc[c4][1], coords_calc[c4+1][1])

                                p1 = coords_calc[0][1] * coords_calc[len(coords_calc)-1][0]
                                for c4 in range(0, len(coords_calc) - 1):
                                    p1 = p1 + coords_calc[c4][0] * coords_calc[c4+1][1]
                                p2 = coords_calc[0][0] * coords_calc[len(coords_calc) - 1][1]
                                for c4 in range(0, len(coords_calc) - 1):
                                    p2 = p2 + coords_calc[c4][1] * coords_calc[c4+1][0]

                                area_mo = abs(p1 - p2)/2

                                raio_h = area_mo/per_mo

                                prof_m = area_mo/larg

                                vazao = (area_mo*(raio_h**(2/3))*(i_decli[c1]**(1/2)))/(i_rug[c2])

                                vel_m = vazao/area_mo

                                # Escrita dos parametros no arquivo
                                arquivo.write(f'{i_cota[c3]:^7.3f}\t{larg:^7.3f}\t{per_mo:^7.3f}\t{area_mo:^7.3f}\t{raio_h:^7.3f}\t{prof_m:^7.3f}\t{vazao:^7.3f}\t{vel_m:^7.3f}\n')
                            except Exception:
                                return [False, 1]

    return exito

# Funções auxiliares para entrada dos dados ----------------------------------------------------------------------------
def Acessar_tabela_coord_rel_sec(diretorio, id):
    """
    Função Acessar_tabela_coord_rel_sec: Usada para acessar a tabela de coordenadas relativas da seção transversal.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :return: Uma matriz na forma [(0), ..., (n)] contendo os dados acessados.
    """
    dados = []
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    for linha in cursor_bd.execute('SELECT * FROM Coord_rel_sec_' + str(id)):
        dados.append(linha)

    conexao_bd.close()

    return dados

def Acessar_tabela_Hidrometria_id(diretorio, id):
    """
    Função Acessar_tabela_Hidrometria_id: Usada para acessar os elementos das tabelas Hidrometria_id.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :return: Uma matriz na forma [exito, [(0), ..., (n)]], onde:
                                                   - exito: Exito ao acessar a tabela, sendo True ou False.
                                                   - [(0), ..., (n)]: Matriz com os dados obtidos.
    """
    dados = []
    exito = False
    nome_tabela_hidrometria = 'Hidrometria_id' + str(id)

    try:
        conexao_bd = sqlite3.connect(diretorio)
        cursor_bd = conexao_bd.cursor()

        for linha in cursor_bd.execute('SELECT * FROM '+ nome_tabela_hidrometria):
            dados.append(linha)

        conexao_bd.close()

        exito = True
    except Exception:
        pass

    return [exito, dados]

def Acessar_tabela_Info_coletas(diretorio):
    """
    Função Acessar_tabela_Info_coletas: Usada para acessar os elementos da tabela Info_coletas.
    :param diretorio: O diretório do banco de dados.
    :return: Uma matriz na forma [exito, [(0), ..., (n)]], onde:
                                                   - exito: Exito ao acessar a tabela, sendo True ou False.
                                                   - [(0), ..., (n)]: Matriz com os dados obtidos.
    """
    dados = []
    exito = False

    try:
        conexao_bd = sqlite3.connect(diretorio)
        cursor_bd = conexao_bd.cursor()

        for linha in cursor_bd.execute('SELECT * FROM Info_coletas'):
            dados.append(linha)

        conexao_bd.close()

        exito = True
    except Exception:
        pass

    return [exito, dados]

def Acessar_tabela_op_declividade(diretorio, id):
    """
    Função Acessar_tabela_op_declividade: Usada para acessar os dados da tabela de opções de declividade.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta.
    :return: Uma matriz na forma [(0), ..., (n)], onde: (0), ..., (n): São os dados obtidos.
    """
    dados = []

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    for linha in cursor_bd.execute('SELECT * FROM Opcoes_declividade_' + str(id)):
        dados.append(linha)

    conexao_bd.close()

    return dados

def Acessar_tabela_Parametros(diretorio, id):
    """
    Função Acessar_tabela_Parametros: Usada para acessar os dados da tabela de parametros.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta.
    :return: Uma tupla contendo os dados obtidos da tabela.
    """
    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    for linha in cursor_bd.execute('SELECT * FROM Parametros'):
        if linha[0] == str(id):
            dados = linha
            break

    conexao_bd.close()

    return dados

def Acessar_tabela_Topo_x_id(diretorio, id, op_decli_margem, op_teo_coord_reg):
    """
    Função Acessar_tabela_Topo_x_id: Usada para acessar os dados das tabelas de topografia.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da tabela a ser acessada.
    :param op_decli_margem: 0 se declividade; 1 se margem.
    :param op_teo_coord_reg: 0 se teodolito; 1 se coordenada; 2 se réguas.
    :return:  Uma matriz na forma [(0), ..., (n)], onde: (0), ..., (n): São os dados obtidos.
    """
    dados = []

    # Declividade
    if op_decli_margem == 0:
        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_decli_teo_id' + str(id)

        # Coordenadas
        elif op_teo_coord_reg == 1:
            nome_tabela = 'Topo_decli_coord_id' + str(id)

        # Réguas
        else:
            nome_tabela = 'Topo_decli_reg_id' + str(id)

    # Margem
    else:
        if op_decli_margem == 1:
            margem = '0'

        else:
            margem = 'n'

        # Teodolito
        if op_teo_coord_reg == 0:
            nome_tabela = 'Topo_margem_'+margem+'_teo_id' + str(id)

        # Coordenadas
        else:
            nome_tabela = 'Topo_margem_'+margem+'_coord_id' + str(id)

    str_comando = 'SELECT * FROM ' + nome_tabela

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    for linha in cursor_bd.execute(str_comando):
        dados.append(linha)

    conexao_bd.close()

    return dados

def Intervalos_decli_rug(diretorio):
    """
    Função Intervalos_decli_rug: Usada para determinar os valors mínimo e máximo de declividade e rugosidade para uma seção.
    :param diretorio: O diretório do banco de dados.
    :return: Uma matriz na forma [[decli_min, decli_max], [rug_min, rug_max]]
    """

    retorno = [['-', '-'], ['-', '-']]

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    for linha in cursor_bd.execute('SELECT * FROM Parametros'):
        for c in range(0, 3):
            try:
                if float(linha[8+c]) < float(retorno[0][0]):
                    retorno[0][0] = linha[8+c]
            except Exception:
                if retorno[0][0] == '-':
                    retorno[0][0] = linha[8+c]

            try:
                if float(linha[8+c]) > float(retorno[0][1]):
                    retorno[0][1] = linha[8+c]
            except Exception:
                if retorno[0][1] == '-':
                    retorno[0][1] = linha[8+c]

            try:
                if float(linha[11+c]) < float(retorno[1][0]):
                    retorno[1][0] = linha[11+c]
            except Exception:
                if retorno[1][0] == '-':
                    retorno[1][0] = linha[11+c]

            try:
                if float(linha[11+c]) > float(retorno[1][1]):
                    retorno[1][1] = linha[11+c]
            except Exception:
                if retorno[1][1] == '-':
                    retorno[1][1] = linha[11+c]

    conexao_bd.close()

    return retorno

def Ordenar_entradas_coletas(data, hora_inicio, hora_termino):
    """
    Função Ordenar_entradas_coletas: Usada para auxiliar na ordenação das entredas de coletas.
    :param data: Uma string contendo a data.
    :param hora_inicio: Uma string contendo a hora de início da coleta.
    :param hora_termino: Uma string contendo a hora de término da coleta.
    :return: Um número inteiro baseado na data.
    """
    p_data = data[6:]+data[3:5]+data[0:2]
    p_h_t = hora_termino[0:2] + hora_termino[3:]
    p_h_i = hora_inicio[0:2] + hora_inicio[3:]

    return int(p_data+p_h_t+p_h_i)

def Pos_x(contador, lista_larguras=[], espacamento=5, origem=5):
    """
    Função Pos_x: Usada para informar a posição x de uma label.
    :param lista_larguras: A lista das larguras das labels.
    :param espacamento: O espaçamento entre as labels.
    :param cont: O contador que representa a posição de um dos n elementos da lista: (0, 1, ..., n-1)
    :param origem: A posição da inserção da primeira label.
    :return: A posição da label.
    """

    pos = origem

    for c in range(0, contador):
        if lista_larguras[c] > 0:
            pos = pos + lista_larguras[c] +espacamento

    return pos

def Validacao_Entradas(tipo, dado, diretorio='', id=''):
    """
    Função Validação de entradas: Realiza a validação de um dado.
    :param tipo: O tipo de validação em forma de string. São válidos:
                    - '.db': Diretório de um banco de dados.
                    - 'ang': Uma string contendo um ângulo (ggg mm ss).
                    - 'data': String com data na forma DD/MM/AAAA.
                    - 'dir': Diretório de uma pasta.
                    - 'float': Um número de ponto flutuante.
                    - 'float+': Um número de ponto flutuante positivo.
                    - 'hora': String com hora na forma HH:MM.
                    - 'int+': Número inteiro positivo.
                    - 'null': Qualquer entrada.
                    - 'str': String não vazia e sem os caracteres '\', '/', ':', '^', '?', '"', '<', '>', '|', '.'.
                    - 'sstr': String não vazia e diferente de '-'.
                    - 't_decli': Tipo do ponto topografia (m, s, j). (Montante, Secao, Jusante).
    :param dado: O dado de entrada na forma de string.
    :param diretorio: O diretório do arquivo carregado.
    :param id: O id da seção carregada.
    :return: A validade do dado True ou False.
    """
    validade = True

    if tipo == 'str':
        caracteres = [('\ ').strip(), '/', ':', '^', '?', '"', '<', '>', '|', '.']
        if dado == '':
            validade = False
        for c in range(0, len(caracteres)):
            if caracteres[c] in dado:
                validade = False
                break

    elif tipo == 'ang':
        if len(dado) == 9 and dado[3] == ' ' and dado[6] == ' ':
            try:
                grau = int(dado[:3])
                min = int(dado[4:6])
                seg = int(dado[7:])

                if grau >= 0 and grau < 360 and min >= 0 and min < 60 and seg >= 0 and seg < 60:
                    validade = True
                else:
                    validade = False

            except Exception:
                validade = False
        else:
            validade = False

    elif tipo == 'data':
        if len(dado) == 10 and dado[2] == '/' and dado [5] == '/':
            try:
                d = int(dado[0:2])
                m = int(dado[3:5])
                a = int(dado[6:])

                data_inexistente = ['30/02', '31/02', '31/04', '31/06', '31/09', '31/11']
                if (a - 2020) / 4 != int((a - 2020) / 4):
                    data_inexistente.append('29/02')

                if d > 0 and d < 32 and m > 0 and m < 13 and a > 1000 and dado[:5] not in data_inexistente:
                    validade = True
                else:
                    validade = False

            except Exception:
                validade = False

        else:
            validade = False

    elif tipo == 'dir':
        if not os.path.exists(dado) or '.' in dado:
            validade = False
        else:
            validade = True

    elif tipo == 'float':
        try:
            n = float(dado)
            validade = True

        except Exception:
            validade = False

    elif tipo == 'float+':
        try:
            n = float(dado)
            if n >= 0:
                validade = True
            else:
                validade = False

        except Exception:
            validade = False

    elif tipo == 'hora':
        if len(dado) == 5 and dado[2] == ':':
            try:
                h = int(dado[0:2])
                m = int(dado[3:])

                if h >= 0 and h <= 23 and m >= 0 and m <= 59:
                    validade = True
                else:
                    validade = False

            except Exception:
                validade = False

        else:
            validade = False

    elif tipo == 'int+':
        try:
            d = int(dado)
            if d >= 0:
                validade = True
            else:
                validade = False
        except Exception:
            validade = False

    elif tipo == '.db':
        if dado != '' and dado[len(dado) - 3] + dado[len(dado) - 2] + dado[len(dado) - 1] == '.db':

            if not os.path.exists(dado):
                validade = False
            else:
                validade = True

        else:
            validade = False

    elif tipo == 'sstr':
        if dado != '' and dado != '-':
            validade = True
        else:
            validade = False

    elif tipo == 't_decli':
        if dado == 'm' or dado == 's' or dado == 'j':
            validade = True
        else:
            validade = False

    return validade

def Verificar_hidrometria(diretorio, id):
    """
    Função Verificar_hidrometria: Usada para verificar se a hidrometria foi alterada.
    :param diretorio: O diretório do banco de dados.
    :param id: O id da coleta carregada.
    :return: True em caso positivo,  False em caso negativo.
    """
    edicao = True

    if id != -1:
        conexao_bd = sqlite3.connect(diretorio)
        cursor_bd = conexao_bd.cursor()

        for linha in cursor_bd.execute('SELECT * FROM Hidrometria_id' + str(id)):
            if 'Editar' in linha:
                edicao = False

        conexao_bd.close()

    else:
        edicao = False

    return edicao

# Funções auxiliares para os cálculos ----------------------------------------------------------------------------------
def Coord_teo(fi, fm, fs, ang_z, ang_h, h_equip):
    """
    Função Coord_teo: Usada para calcular as coordenadas a partir dos dados de um teodolito.
    :param fi: Valor do fio inferior.
    :param fm: Valor do fio médio.
    :param fs: Valor do fio superior.
    :param ang_z: Ângulo zênital.
    :param ang_h: Ângulo horizontal
    :param h_equip: Altura do equipamento.
    :return: Um vetor na forma [x, y, z, validade] contendo as coordenadas x, y e z respectivamente e a validade dos
             pontos True/False.
    """
    validade = True
    x = 0
    y = 0
    z = 0

    angulo_zenital = math.radians(float(ang_z[:3])+float(ang_z[4:6])/60+float(ang_z[7:])/(60**2))

    if angulo_zenital > math.radians(180):
        return [x, y, z, False]

    angulo_horizontal = math.radians(float(ang_h[:3]) + float(ang_h[4:6]) / 60 + float(ang_h[7:]) / (60 ** 2))

    alpha = math.radians(90)-angulo_zenital

    fs = float(fs)
    fm = float(fm)
    fi = float(fi)

    i = fs-fi

    if fi >= fm or fi >= fs or fm >= fs or f'{fm - fi:.3f}' != f'{fs - fm:.3f}':
        return [x, y, z, False]

    v = 50*i*math.sin(2*alpha)

    z = float(h_equip) + v - fm

    h = 100*i*((math.cos(alpha))**2)

    x = h*math.sin(angulo_horizontal)
    y = h * math.cos(angulo_horizontal)

    return [x, y, z, validade]

def Distancia(x0, x1, y0, y1, z0=0, z1=0):
    """
    Função Distância: Usada para calcular a distância entre dois pontos.
    :param x0: Coordenada x do ponto 0.
    :param x1: Coordenada x do ponto 1.
    :param y0: Coordenada y do ponto 0.
    :param y1: Coordenada y do ponto 1.
    :param z0: Coordenada z do ponto 0.
    :param z1: Coordenada z do ponto 1.
    :return: A distância entre os pontos
    """
    return math.sqrt(((float(x1)-float(x0))**2)+((float(y1)-float(y0))**2)+((float(z1)-float(z0))**2))

def Rug_manning(diretorio, id, declividade):
    """
    Função Rug_manning: Usada para calcular a rugosidade de Manning.
    :param diretorio: O diretorio do arquivo carregado.
    :param id: O id da coleta.
    :param declividade: A declividade estimada.
    :return: O valor da rugosidade.
    """

    conexao_bd = sqlite3.connect(diretorio)
    cursor_bd = conexao_bd.cursor()

    for linha in cursor_bd.execute('SELECT * FROM Parametros WHERE id = ?', (id, )):
        dados = linha

    conexao_bd.close()

    if linha[1] == '-':
        rug = '-'

    else:
        try:
            rug = (float(dados[3])*(float(dados[4])**(2/3))*(declividade**(1/2)))/float(dados[6])
        except Exception:
            rug = 'Erro'

    return rug
