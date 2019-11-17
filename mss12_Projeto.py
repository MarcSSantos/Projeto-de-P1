
def eliminarBarraN(string):
    """
    Essa função elimina os /n dos conteúdos que as variáveis recebem.
    """ 
    stringNova = ""
    for caractere in string:
        if caractere != "\n": 
            stringNova += caractere
    return stringNova

def lerArquivo():
    """
    Essa fução ler o arquivo usuarios.txt já fazendo a descriptografia
    e retorna o dicionário de usuários.
    """
    arquivoChaves = open("chavePrivada.txt", "r")
    linhasChaves = arquivoChaves.readlines()
    arquivoChaves.close()

    num = ""
    listaChaves = []
    for x in linhasChaves:
        for y in x:
            if y != "\n":
                num += y
            if len(num) == 4:
                num = int(num)
                listaChaves.append(num)
                num = ""
         
    d = listaChaves[0]
    n = listaChaves[1]


    arquivo = open("usuarios.txt", "r")
    linhas = arquivo.readlines()
    arquivo.close()

    usuarios = {}
    listaLetras = []
    listaDesCrip = []
    letra = ""
    palavra = ""
    for x in linhas:

        for  y in x:
            
            if y != " ":
                letra += y
            if y == " ":
                letraCrip = int(letra)
                letraDesCrip = chr(letraCrip ** d % n)
                listaLetras.append(letraDesCrip)
            
                letra = ""
            if y == "\t" or y == "\n":
                listaLetras.append(" ")

            if y == "\n":
                for x in listaLetras:
                    if x != " ":
                        palavra += x
                    if x == " ":
                        listaDesCrip.append(palavra)
                        palavra = ""
                        listaLetras = []

                usuarios[listaDesCrip[0]] = (listaDesCrip[1], listaDesCrip[2])
                listaDesCrip = []
                
    return usuarios

def escreveArq(usuarios):
    """
    Essa função recebe como parâmentro usuarios que tem nele um conjunto de dicionários que serão escritos
    no arquivo usuarios.txt.
    """
    arquivo = open("usuarios.txt", "w")
    lista = usuarios.items()
    
    for x in lista:
        arquivo.write(x[0]+"\t")
        arquivo.write(x[1][0]+"\t")
        arquivo.write(x[1][1]+ "\n")
        #arquivo.write("\n")
        
        
    arquivo.close()
    
    return usuarios

def criptografarUsuarios(usuarios):
    """
    Essa função criptografa todos os usuários, primeiro ela ler o arquivo que contem a chave publica e com essas chaves
    é possível efetuar a criptografia por meio de cáuculos, após criptografar todos usuários é chamada a função esreverArq
    e assim todos usuarios são escritos no arquivo usuarios.txt.
    """
    arquivo = open("chavePublica.txt","r")
    linhas = arquivo.readlines()
    arquivo.close()
    e = int(eliminarBarraN(linhas[0]))
    n = int(linhas[1])

    
    userEncriptado = {}
    listaValores = []

    for chave in usuarios:
        stringChave = ""
        
        for letra in chave:
            letraCifrada = str(ord (letra) ** e % n)
            stringChave += str(letraCifrada) + " "
        userEncriptado[stringChave]=""        

        listaValores = []
        for valores in usuarios[chave]:
            stringValor = ""
            

            for valor in valores:
                letraCifrada = str(ord (valor) ** e % n)
                stringValor += str(letraCifrada) + " "
            listaValores.append(stringValor)

        userEncriptado[stringChave] = (listaValores[0],listaValores[1])

    escreveArq(userEncriptado)
    
    return userEncriptado

def checarNivelAcesso(login):
    """
    Essa função tem como finalidade checar o nível de acesso do usuário cadastrado no sistema
    para que assim ele posso ser conduzido para o menu de acordo com o seu nível de acesso.
    Além disso, ela lê todos os usuários cadastrados (no arquivo) e verifica o login e o nível de acesso para saber 
    se eles estão no mesmo dicionário
    """
    usuarios = lerArquivo() #chama a função lerArquivo para que o conteudo seja armazenado em uma váriavel
    nivel = usuarios.items()
    lista = []
    for x in nivel:
        lista.append(x)
    for y in nivel:
        if y[0] == login:
            nivel = eliminarBarraN((y[1][1]))
    
    return nivel,login

def acesso():
    
    """
    Essa é a funão Main, ele serve para iniciar o programa, e para que o usuário consiga acessar o sitema pelo
    seu login e senha de acesso, caso o usuário não tenha cadastro ele pode efetuar o cadastro e depois acessar o programa
    Observavação: Todos usuários cadastrados recebem o nível 3 de acesso.
    Dentro da função é feita a checagem se o usuario já possui cadastro ou não chamando a função checarAcesso se o 
    usuário tiver devidamente cadastro ele irá acessar o programa de acordo com o seu nível de acesso, pois logo após a 
    chacagem do acesso é feita a verificação do nível de acesso para que o usuário seja encaminhado para a sua aba especifica.
    """


    usuarios = lerArquivo()
    sair = False
    while sair == False:
        
        print("***Bem Vindo ao Escambo***""\n")
        acesso = input(str("Se já possui uma conta digite 'Y' se não, digite 'C' "
                           "para criar uma conta ou 'S' para sair: "))
        print("")
        acesso = acesso.upper()

        if acesso == "Y":
            login = str(input("Login: "))
            senha = str(input("Senha: "))
            login = login.upper()
            checar = checarAcesso(login,senha)
            print("")
            
            if checar == True:
                print("")
                return menu(checarNivelAcesso(login))
            
            else:
                print("Login ou Senha incorretos, tente novamente""\n")
                
            
        elif acesso == "C":
            
            return cadastrar(usuarios)
            
        elif acesso == "S":
            print("Programa encerrado.")
            
            sair = True
        
        elif acesso != "Y" and  acesso != "C" and acesso != "S":
            print("Opção inválida, tente novamente.""\n")
                
def checarAcesso(login,senha): 
    """
    Essa função verifica se o login e a senha do usuário estão corretas, ou seja, se as chave(login)
    e o valor(senha) estão dentro do mesmo dicionário e também se estão corretas.
    """
    usuarios = lerArquivo()
    for keys,values in usuarios.items():
        if keys == login and values[0] == senha:
            return True
    return False
         
def cadastrar(usuarios):
    """
    Essa função é chamada dentro da função acesso quando o usuario digita a letra "C" para dar início ao cadastro
    ela solicita o login e um senha para que o usuário seja registrado no sistema e após o resgistro todas as informações
    são criptografadas e armazendas no arquivo usuario.txt
    """

    print("")
    print("***Criação do login de acesso***""\n")
    
    flag = False
    while flag == False:
        login = str(input("Crie seu login: "))
        senha = str(input("Crie sua senha: "))
        login = login.strip(" ")
        login = login.upper()
        print("")
        nivelDeAcesso = "3"
        for x in login:
            if x == " ":
                login = True

        if login == True:
            print(print("O login não pode conter espaços, tente novamente. EX: Maria, João""\n"))
            flag = False
                    
        else:
            flag = True
            igual = login in usuarios.keys()#checa se o longin já existe
            if igual == False:


                if len(senha) < 1:
                    print("Senha menor do que o tamanho desejado, digite novamente.""\n")
                    
                else:
                    usuarios[login] =(senha,nivelDeAcesso)
                    
                    flag = True
            else:
                print("Login",login,"já cadastrado. Crie um login diferente.")

            print("Conta Criada com sucesso.""\n")
    
    usuariosCrip =  criptografarUsuarios(usuarios)
    escreveArq(usuariosCrip)

    return acesso()

def ordenarUsuarios(dicionario):
    """
    Essa função ordena o dicionário de usuários pelo nome de "A" a "Z" 
    e retonrar o dicionário ordenado
    """
    listao = dicionario.items()
    lista = []
    dicionarioOrdenado = {}
    for x in listao:
        lista.append(x)
        
    for x in lista:
        atual = 0
        while atual < len(lista) - 1:
            if (lista[atual] > lista[atual+1]):
                temp = lista[atual]
                lista[atual] = lista[atual+1]
                lista[atual+1] = temp
            atual = atual + 1
            
    for x in lista:
        dicionarioOrdenado[x[0]] = x[1]
    
    return dicionarioOrdenado

def buscarUsuario(login): 
    """
    Essa função busca os usuários que estão cadastrados de duas formas:
    Primeira forma ele busca todos usuários que estão no sistema e printa 
    todas as informções de forma ordenada.
    Segunda forma efetua a busca pelo login do usuário e se encontrado 
    as informações são printadas na tela
    """

    sair = False
    while sair == False:
        print(">>>Buca de usuário<<<""\n")
        forma = int(input("1 - Buscar todos usuários""\n"
                          "2 - Busca pelo login""\n"))

        if forma < 1 or forma > 2:
            print("Valor digitado inválido, tente novamente.""\n")
            sair = True

        elif forma == 1:       
            dicUsuarios = lerArquivo()
            dicionarioOrdenado = ordenarUsuarios(dicUsuarios)
    
            for x in dicionarioOrdenado.items():
                print(" Login:",x[0],"\n","Senha:",x[1][0],"\n","Nível de acesso:",x[1][1],"\n")
                acao = " buscou pelo usuário " + x[0] + "."
                logSystem(login,acao)
                sair = True 

        elif forma == 2:
            buscar = str(input("Digite o login do usuário a ser buscado: "))
            print("")
            buscar = buscar.upper()
            dicionario = lerArquivo()
            listao = dicionario.items()

            achou = False
            for x in listao:
                for y in x:
                    if y == buscar:
                        print(" Login:",x[0],"\n","Senha:",x[1][0],"\n","Nível de acesso:",x[1][1],"\n")
                        acao = " buscou pelo usuário " + x[0] + "."
                        logSystem(login,acao)
                        achou = True
                        sair = True

            if achou == False:
                acao = " buscou pelo usuário " + buscar + " Usuário não encontrado."
                logSystem(login,acao)
                print("Usuário",buscar,"não encontrado.""\n")
                sair = True

        flag_2 = False
        while flag_2 == False:

            continuar = str(input("Deseja fazer uma nova busca ? Se sim digite 'Y'"
                                    "se não digite 'N': "))
            print("")

            continuar = continuar.upper()
            if continuar == "N":
                print("Você saiu da aba de busca de usuários""\n")
                flag_2 = True
            elif continuar == "Y":
                sair = False
                flag_2 = True
            elif continuar != "Y" or continuar != "N":
                print("Opção inválida, tente novamente""\n")
                flag_2 = False

def editarUsuario(login):
    """
    Essa função edita o nível de acesso e a senha dos usuários cadastrados, a edição só pode ser
    feita pelo ADM ou por algum usuário que possui nível 2 de acesso.
    Para que a edição seja iniciada é preciso saber o login do usuário assim que o login for encontrado
    no sistema a aba de edição ira aparecer na tela.
    """
    recebeUsuarios = lerArquivo()
    sair = False
    while sair == False:
        encontrarUser = str(input("Digite o login do usuário para editar alguma informação: "))
        encontrarUser = encontrarUser.upper()
        if encontrarUser == "ADM":
            print("Administrador não pode ser removido, tente novamente.""\n")
        else:
            verificar = encontrarUser in recebeUsuarios.keys()
            if verificar == True:
                opcao = int(input("1 - Editar senha""\n""2 - Editar nível de acesso""\n"))
                if opcao == 1:
                    nivel = recebeUsuarios[encontrarUser][1]
                    novaSenha = str(input("Digite a nova senha: "))
                    recebeUsuarios[encontrarUser] = (novaSenha,nivel)
                    print("Senha alterada com sucesso.""\n")
                    acao = " alterou a senha do usuário " + encontrarUser + "."
                    logSystem(login,acao)
                    usuariosCrip =  criptografarUsuarios(recebeUsuarios)
                    escreveArq(usuariosCrip)
                    sair = True

                elif opcao == 2:
                    senha = recebeUsuarios[encontrarUser][0]
                    novoNivel = int(input("Digite o novo nível de acesso: "))
                    if  novoNivel >= 1 and novoNivel <= 3:
                        novoNivel = str(novoNivel)
                        recebeUsuarios[encontrarUser] = (senha, novoNivel)
                        print("Nível de acesso alterado com sucesso.""\n")
                        acao = " alterou o nível de acesso do usuário " + encontrarUser + "."
                        logSystem(login,acao)
                        usuariosCrip =  criptografarUsuarios(recebeUsuarios)
                        escreveArq(usuariosCrip)
                        sair = True
                    else:
                        print("Nível de acesso inválido, tente novamente.""\n") 
            else:
                print("Usuário",encontrarUser,"não encontrado, tente novamente.""\n")
                acao = " tentou editar informações do usuário " + encontrarUser + " Usuário não encontrado."
                logSystem(login,acao)
                sair = True
        
        sair_2 = False
        while sair_2 == False:
            sair = False
            fechar = str(input("Deseja EDITAR mais algum usuário? Se sim digite 'Y' se não digite 'N': "))
            fechar = fechar.upper()
            if fechar != "Y" and fechar != "N":
                print("Opção inválida, tente novamente.""\n")
            else:
                sair_2 = True
                print("")
        
        if fechar == "N":
            print("Você saiu da aba de edição de usuários.""\n")
            sair = True
            sair_2 = True
        elif fechar == "Y":
            sair_2 = True
             
def removerUsuarios(login):
    """
    Essa função remove os usuários do sistema e apenas o ADM pode remover usuários.
    Para remover é preciso saber o login do usuário após digitar o login e apertar enter
    o usuário selecionado será removido.
    """
    recebeUsuarios = lerArquivo()
    sair = False
    while sair == False:
        encontrarUser = str(input("Digite o login do usuário para removelo: "))
        encontrarUser = encontrarUser.upper()
        if encontrarUser == "ADM":
            print("Administrador não pode ser removido, tente novamente.""\n")
            
        else:
            verificar = encontrarUser in recebeUsuarios.keys()
            if verificar == True:
                recebeUsuarios.pop(encontrarUser)
                usuariosCrip =  criptografarUsuarios(recebeUsuarios)
                escreveArq(usuariosCrip)
                print("Usuário",encontrarUser,"removido com sucesso.""\n")
                acao = " removeu o usuário " + encontrarUser + "."
                logSystem(login,acao)
                sair = True

            else:
                print("Usuário",encontrarUser,"não encontrado, tente novamente.""\n")
                acao = " tentou remover o usuário " + encontrarUser + "." + "Usuário não encontrado."
                logSystem(login,acao)
                sair = True

        sair_2 = False
        while sair_2 == False:
            sair = False    
            fechar = str(input("Deseja REMOVER mais algum usuário? Se sim digite 'Y' se não digite 'N': "))
            fechar = fechar.upper()
            if fechar != "Y" and fechar != "N":
                print("Opção inválida, tente novamente.""\n")
            else:
                sair_2 = True
                print("")
        
        if fechar == "N":
            print("Você saiu da aba de remoção de usuários.""\n")
            sair = True
            sair_2 = True
        elif fechar == "Y":
            sair_2 = True

def lerArquivoElementos():
    """
    Essa função lê todos os elementos(informações dos livros) que estão salvos no arquivo elementos.txt
    faz a descriptografia e retorna um dicionário para que outras funções usem esse dicionário.
    """
    arquivoChaves = open("chavePrivada.txt", "r")
    linhasChaves = arquivoChaves.readlines()
    arquivoChaves.close()

    num = ""
    listaChaves = []
    for x in linhasChaves:
        for y in x:
            if y != "\n":
                num += y
            if len(num) == 4:
                num = int(num)
                listaChaves.append(num)
                num = ""
         
    d = listaChaves[0]
    n = listaChaves[1]


    arquivo = open("elementos.txt", "r")
    linhas = arquivo.readlines()
    arquivo.close()

    elementos = {}
    listaLetras = []
    listaDesCrip = []
    letra = ""
    palavra = ""
    listaDesCrip2 = []
    
    for x in linhas:

        for  y in x:
            
            if y != " ":
                letra += y
            if y == " ":
                letraCrip = int(letra)
                letraDesCrip = chr(letraCrip ** d % n)
                listaLetras.append(letraDesCrip)
                letra = ""
                
            if y == "\t" or y == "\n":
                listaLetras.append("+")
                
            if y == "\n":
                
                for x in listaLetras:
                    for y in x:
                        if y != "+":
                            palavra += y
                        if y == " ":
                            palavra += " "
                        if y == "+":
                            listaDesCrip.append(palavra)
                            palavra = ""
                
                elementos[listaDesCrip[0]] = (listaDesCrip[1],listaDesCrip[2],listaDesCrip[3],listaDesCrip[4],
                                              listaDesCrip[5],listaDesCrip[6],listaDesCrip[7])
                listaDesCrip2.append(listaDesCrip)
                listaDesCrip = [] 
                listaLetras = []




    return elementos

def criptografarElementos(elementos):
    """
    Essa função criptografa todos os elementos, primeiro ela ler o arquivo que contem a chave privada e com essas chaves
    é possível efetuar a descriptografia por meio de cáuculos, após descriptografar todos os elementos os mesmos
    são retornados em forma de dicionário para que outras funções possam utilizar esse dicionánario.
    """
    arquivo = open("chavePublica.txt","r")
    linhas = arquivo.readlines()
    arquivo.close()
    e = int(eliminarBarraN(linhas[0]))
    n = int(linhas[1])

    elementosEncriptado = {}
    listaValores = []

    for chave in elementos:
        stringChave = ""

        for letra in chave:
            letraCifrada = str(ord (letra) ** e % n)
            stringChave += str(letraCifrada) + " "
        elementosEncriptado[stringChave]=""  

        listaValores = []
        for valores in elementos[chave]:
            stringValor = ""

            for valor in valores:
                letraCifrada = str(ord (valor) ** e % n)
                stringValor += str(letraCifrada) + " "
            listaValores.append(stringValor)

        elementosEncriptado[stringChave] = (listaValores[0],listaValores[1],listaValores[2],listaValores[3],listaValores[4],listaValores[5],listaValores[6])

    return elementosEncriptado

def ordenarElementos(dicionario):
    """
    Essa função ordena o dicionário de elementos pelo nome de "A" a "Z" 
    e retonrar o dicionário ordenado
    """
    listao = dicionario.items()
    lista = []
    dicionarioOrdenado = {}
    for x in listao:
        lista.append(x)
        
    for x in lista:
        atual = 0
        while atual < len(lista) - 1:
            if (lista[atual][1][0] > lista[atual+1][1][0]):
                temp = lista[atual]
                lista[atual] = lista[atual+1]
                lista[atual+1] = temp
            atual = atual + 1
            
    for x in lista:
        dicionarioOrdenado[x[0]] = x[1]
    
    return dicionarioOrdenado

def escreveArqElementos(elementos):
    """
    Essa função recebe como parâmentro elementos que tem nele um conjunto de dicionários que serão escritos
    no arquivo elementos.txt.
    """
    arquivo = open("elementos.txt", "w")
    lista = elementos.items()
    
    for x in lista:
        arquivo.write(x[0]+"\t")
        arquivo.write(x[1][0]+"\t")
        arquivo.write(x[1][1]+"\t")
        arquivo.write(x[1][2]+"\t")
        arquivo.write(x[1][3]+"\t")
        arquivo.write(x[1][4]+"\t")
        arquivo.write(x[1][5]+"\t")
        arquivo.write(x[1][6]+"\n")
        
        
    arquivo.close()
    return elementos

def cadastroLivro(elementos):
    """
    Essa função cadastra as informações dos livros e escreve
    no arquibo elementos.txt as informações criptografadas
    """
    sair = False
    while sair == False :
        
        sair_3 = False
        
        while sair_3 == False:
            print(">>>Cadastro do livro<<<""\n")
            nome = str(input("Digite o nome do livro: "))
            nome = nome.upper()
            autor = str(input("Digite o nome do autor do livro: "))
            autor = autor.upper()
            ano = int(input("Digite o ano de lançamento do livro: "))
            edicao = str(input("Digite a edição do livro: "))
            edicao =edicao.upper()
            isbn = int(input("Digite o ISBN do livro: "))
            quantidade = int(input("Digite a quantidade de livros que será adicionada: "))
            estado = str(input("Descreva da melhor maneira o estado de qualidade do livro: "))
            login = str(input("Digite o seu login para confirmar o cadastro do livro: "))
            senha = str(input("Digite a sua senha para confirmar o cadastro do livro: "))
            print("")
            estado = estado.upper()
            login = login.upper()                                     
            ano = str(ano)
            isbn = str(isbn)
            quantidade = str(quantidade)
            confirmacao = checarAcesso(login,senha)
        
            if nome == "" or autor == "" or edicao == "" or edicao == "" or quantidade == "":
                print("Algum campo está vazio, digite novamente.""\n")
                
            elif confirmacao == False:
                print("Login ou Senha inválido, tente novamente.""\n")
                
            else:

                elementos[isbn] = (nome, autor, ano, edicao, quantidade, estado, login)
                elementosCrip =  criptografarElementos(elementos)
                escreveArqElementos(elementosCrip)
                
                print("Livro",nome,"cadastrado com sucesso""\n")
                acao = " cadastrou o livro " + nome + "."
                logSystem(login,acao)
                sair_3 = True
                
 
    
        sair_3 = False
        while sair_3 == False:
            
            fechar = str(input("Deseja ADICIONAR mais um livro? Se sim digite 'Y' se não digite 'N': "))
            
            if fechar != "y" and fechar != "n":
                print("Opção inválida, tente novamente.""\n")
            else:
                sair_3 = True
        print("")
    
        if fechar == "n":
            print("Você saiu da aba de cadastro de livros.""\n")
            sair = True
        elif fechar == "y":
            sair = False

def buscaLivros(login):
    """
    Essa função busca os livros que estão cadastrados de duas formas:
    Primeira forma ele busca todos livros que estão no sistema e printa 
    todas as informções de forma ordenada.
    Segunda forma efetua a busca pelo nome do autor e se encontrado 
    as informações são printadas na tela
    """
    sair = False
    while sair == False:
        dicElementos = lerArquivoElementos()
        formaBusca = int(input(">>>Opção de busca<<""\n""\n"
                            "1 - Buscar todos os livros""\n"
                            "2 - Buscar por nome do livro""\n"))

        if dicElementos == {}:
            print("Lista de livros se encontra vazia""\n")
            acao = " buscou por todos os livros. Lista de livros vazia. "
            logSystem(login,acao)
            sair = True
        elif formaBusca < 1 or formaBusca > 2:
            print("Valor digitado incorreto, tente novamente.""\n")
            sair = True

        elif formaBusca == 1:
            dicionarioOrdenado = ordenarElementos(dicElementos)
            for x in dicionarioOrdenado.values():
                print("Nome do Livro:",x[0],"\n""Nome do autor:",x[1],"\n""Ano de lançamento:",x[2],"\n"
                                "Edição:",x[3],"\n""Quantidade:",x[4],"\n""Estado do livro:",x[5],"\n"
                                "Usuário que adicionou o(s) livro(s):",x[6],"\n")

                acao = " buscou por todos os livros de forma ordenada. "
                logSystem(login,acao)
                sair = True

        elif formaBusca == 2:
            nomeLivro = str(input("Digite o nome do livro: "))
            nomeLivro = nomeLivro.upper()
            print("")
            achou = False
            for x in dicElementos.values():
                if x[0] == nomeLivro:
                    for x in dicElementos.values():
                        if x[0] == nomeLivro:
                            print("Nome do Livro:",x[0],"\n""Nome do autor:",x[1],"\n""Ano de lançamento:",x[2],"\n"
                                "Edição:",x[3],"\n""Quantidade:",x[4],"\n""Estado do livro:",x[5],"\n"
                                "Usuário que adicionou o(s) livro(s):",x[6],"\n")
                            achou = True
                            acao = " buscou pelo livro " + nomeLivro + "."
                            logSystem(login,acao)   
                            sair = True
                           
            if achou == False:
                acao = " buscou pelo livro " + nomeLivro + ". Livro não encontrado."
                logSystem(login,acao) 
                print("Livro",nomeLivro,"não encontrado ou nome do livro foi digitado incorretamente.""\n")
                sair = True

        else:
            print("Digito inválido, tente novamente.")

        sair_2 = False
        while sair_2 == False:
            sair = False    
            fechar = str(input("Deseja efetuar mais alguma busca? Se sim digite 'Y' se não digite 'N': "))
            fechar = fechar.upper()
            if fechar != "Y" and fechar != "N":
                print("Opção inválida, tente novamente.""\n")
            else:
                sair_2 = True
                print("")
        
        if fechar == "N":
            print("Você saiu da aba de busca de livros.""\n")
            sair = True
            sair_2 = True
        elif fechar == "Y":
            sair_2 = True

def editarLivros():
    """
    Essa função edita todas informações do livro, e cada usuário só pode editar os livros que o mesmo cadastrou.
    Para que a edição seja iniciada é preciso saber o ISBN do livro 
    assim que o ISBN  for encontrado no sistema a aba de edição ira aparecer na tela.

    """
    print(">>>Edição de Livro(s)<<<""\n")
    print("Confirme seu login e senha para alterar informações.""\n")
    login = str(input("Digite o seu login: "))
    senha = str(input("Digite sua senha: "))
    login = login.upper()
    verificar = checarAcesso(login,senha)
    print("")
    if verificar == True:

        sair = False
        while sair == False:
            opcao = int(input("1 - Visualizar todos os seus livros cadastrados (É possível visualizar o ISBN dos seus livros).""\n"
                              "2 - Editar""\n""Observação: Para editar as informações do(s) livro(s) é preciso usar o ISBN""\n"))
            if opcao < 1 or opcao > 2:
                    print("Opção inválida, tente novamente.") 
                    sair = True
            else:
                receberLivros = lerArquivoElementos()
                listaLivros = receberLivros.items()
                
                if receberLivros == {}:
                    print("Lista de livros se encontra vazia""\n")
                    acao = " tentou editar algum livro. Lista de livros vazia. "
                    logSystem(login,acao)
                    sair = True
                    

                elif opcao == 1:
                    for x in listaLivros:
                        if x[1][6] == login:
                            print("ISBN:",x[0],"\n""Nome do Livro:",x[1][0],"\n""Nome do autor:",x[1][1],"\n"
                                "Ano de lançamento:",x[1][2],"\n""Edição:",x[1][3],"\n""Quantidade:",x[1][4],"\n"
                                "Estado do livro:",x[1][5],"\n""Usuário que adicionou o(s) livro(s):",x[1][6],"\n")
                            sair = True
                            

                elif opcao == 2:
            
                    flag = False
                    while flag == False:
                        isbn = int(input("Digite o ISBN para altetar alguma informação:"))
                        isbn = str(isbn)
                        print("")
                        achou = isbn in receberLivros
    
                        if achou == True:

                            pegarValores = receberLivros[isbn]
                            validarLogin = pegarValores[6] == login

                            if login == "ADM":
                                validarLogin = True

                            if validarLogin == True:
                                chave = False
                                for procura in listaLivros:
                                    if procura[0] == isbn:
                                        chave = procura                                 
                                   
                                if chave != False:

                                    print("*A edição será feita neste livro*""\n""\n"
                                        "ISBN:",chave[0],"\n""Nome do Livro:",chave[1][0],"\n""Nome do autor:",chave[1][1],"\n"
                                        "Ano de lançamento:",chave[1][2],"\n""Edição:",chave[1][3],"\n""Quantidade:",chave[1][4],"\n"
                                        "Estado do livro:",chave[1][5],"\n""Usuário que adicionou o(s) livro(s):",chave[1][6],"\n")

                                    info = int(input("Escolha uma opção de edição""\n""\n""1 - Nome do Livro""\n""2 - Nome do autor""\n"
                                                    "3 - Ano de lançamento""\n""4 - Edição""\n""5 - Quantidade""\n""6 - Estado do Livro""\n"))
                                    if info < 1 or info > 7:
                                        print("Opção inválida,tente novamente.""\n")
                                        flag = True

                                    else:

                                        if info == 1:
                                            nome = str(input("Digite o novo nome do livro:"))
                                            nome = nome.upper()
                                            valores =  receberLivros[isbn]
                                            receberLivros[isbn] = (nome,valores[1],valores[2],valores[3],valores[4],valores[5],valores[6])
                                            print("Edição efetuada com sucesso.""\n""Novo nome do lvro:",nome,"\n")
                                            acao = " editou o nome do livro " + chave[1][0] + "."
                                            logSystem(login,acao)    
                                            flag = True

                                        elif info == 2:
                                            autor = str(input("Digite o novo nome do autor:"))
                                            autor = autor.upper()
                                            valores =  receberLivros[isbn]
                                            receberLivros[isbn] = (valores[0],autor,valores[2],valores[3],valores[4],valores[5],valores[6])
                                            acao = " editou o nome do autor do livro " + chave[1][1] + "."
                                            logSystem(login,acao)
                                            print("Edição efetuada com sucesso.""\n""Novo nome do autor:",autor,"\n")
                                            flag = True

                                        elif info == 3:
                                            ano = int(input("Digite o novo ano de lançamento:"))
                                            ano = str(ano)
                                            valores =  receberLivros[isbn]
                                            receberLivros[isbn] = (valores[0],valores[1],ano,valores[3],valores[4],valores[5],valores[6])
                                            acao = " editou o ano de lançamento do livro " + chave[1][2] + "."
                                            logSystem(login,acao)                
                                            print("Edição efetuada com sucesso.""\n""Novo ano do livro:",ano,"\n")
                                            flag = True

                                        elif info == 4:
                                            edicao = str(input("Digite a nova edição do livro:"))
                                            edicao = edicao.upper()
                                            valores =  receberLivros[isbn]
                                            receberLivros[isbn] = (valores[0],valores[1],valores[2],edicao,valores[4],valores[5],valores[6])
                                            acao = " editou a edição do livro " + chave[1][3] + "."
                                            logSystem(login,acao)
                                            print("Edição efetuada com sucesso.""\n""Nova edição do livro:",edicao,"\n")
                                            flag = True

                                        elif info == 5:
                                            quantidade = int(input("Digite a nova quantidade de livros:"))
                                            quantidade = str(quantidade)
                                            valores =  receberLivros[isbn]
                                            receberLivros[isbn] = (valores[0],valores[1],valores[2],valores[3],quantidade,valores[5],valores[6])
                                            acao = " editou a quantidade de livro(s) " + chave[1][4] + "."
                                            logSystem(login,acao)
                                            print("Edição efetuada com sucesso.""\n""Nova quantidade:",quantidade,"\n")
                                            flag = True

                                        elif info == 6:
                                            estado = str(input("Digite o novo estado do livro:"))
                                            estado = estado.upper()
                                            valores =  receberLivros[isbn]
                                            receberLivros[isbn] = (valores[0],valores[1],valores[2],valores[3],valores[4],estado,valores[6])
                                            acao = " editou o estado do livro " + chave[1][5] + "."
                                            logSystem(login,acao)
                                            print("Edição efetuada com sucesso.""\n""Novo estado:",estado,"\n")
                                            flag = True
                                        criptografarEdicao = criptografarElementos(receberLivros)
                                        escreveArqElementos(criptografarEdicao)

                        else:
                            print("ISBN inválido, tente novamente.""\n")
                            acao = " tentou editar alguma informação " + isbn + " Não encontrado."
                            logSystem(login,acao)
                            flag = True


            sair_2 = False
            while sair_2 == False:
                sair = False
                fechar = str(input("Deseja EDITAR mais algum livro? Se sim digite 'Y' se não digite 'N': "))
                fechar = fechar.upper()
                if fechar != "Y" and fechar != "N":
                    print("Opção inválida, tente novamente.""\n")
                else:
                    sair_2 = True
                    sair = False
                    print("")
                
            if fechar == "N":
                print("Você saiu da aba de edição de livros.""\n")
                sair = True
                sair_2 = True
            elif fechar == "Y":
                flag = False
                sair = False
                sair_2 = True      
    else:
        print("Login ou senha incorretos, tente novamente.")            

def removerLivros():
    """
    Essa função remove oslivros do sistema e cada usuário só pode remover os livros que o mesmo cadastrou.
    OBS: o ADM pode remover qualquer livro.
    Para remover é preciso saber o ISBN após digitar o login e apertar enter o livro selecionado será removido.
    """
    print("Confirme seu login e senha para remover livro(s).""\n")
    login = str(input("Digite o seu login: "))
    senha = str(input("Digite sua senha: "))
    login = login.upper()
    verificar = checarAcesso(login,senha)
    print("")
    if verificar == True:    

        recebeLivros = lerArquivoElementos()

        if recebeLivros == {}:
            print("Lista de livros se encontra vazia""\n")
            acao = " tentou remover algum livro. Lista de livros vazia. "
            logSystem(login,acao)

        else:            
            sair = False
            while sair == False:
                print(">>>Remoção de livro<<<""\n")
                encontrarLivro = int(input("Digite o ISBN: "))
                encontrarLivro = str(encontrarLivro)
                print("")
                verificar = encontrarLivro in recebeLivros.keys()
                if verificar == True:
                    achou = encontrarLivro in recebeLivros
                    pegarValores = recebeLivros[encontrarLivro]
                    validarLogin = pegarValores[6] == login
                    if login == "ADM":
                        validarLogin = True
                    
                    if achou == True and validarLogin == True:
                        recebeLivros.pop(encontrarLivro)
                        encriptarRemocao = criptografarElementos(recebeLivros)
                        escreveArqElementos(encriptarRemocao)
                        acao = " removeu o livro " + encontrarLivro + "."
                        logSystem(login,acao)  
                        print("Livro",pegarValores[0],"removido com sucesso.""\n")
                        sair = True

                        if recebeLivros == {}:
                            print("Lista de livros se encontra vazia.""\n")
                            sair = True

                    elif validarLogin == False:
                        print("Usuário sem permição para remover o livro desejado, tente novamente.""\n")
                        acao = "tentou remover um livro. Usuário sem permissão."
                        logSystem(login,acao)  
                        sair = True
                else:
                    print("ISBN inválido, tente novamente.""\n")
                    
                sair_2 = False
                while sair_2 == False:
                    sair = False
                    sair = False    
                    fechar = str(input("Deseja REMOVER mais algum livro? Se sim digite 'Y' se não digite 'N': "))
                    fechar = fechar.upper()

                    if fechar != "Y" and fechar != "N":
                        print("Opção inválida, tente novamente.""\n")
                    else:
                        sair_2 = True
                        print("")
                
                if fechar == "N":
                    print("Você saiu da aba de remoção de livros.""\n")
                    sair = True
                    sair_2 = True

                elif fechar == "Y":
                    sair_2 = True
            
    else:
        print("Login ou senha incorreto, tente novamente.""\n")

def logSystem(login,acao):
    """
    Essa função recebe como parâmeto o login, ação e importa a data e a hora/m/s 
    para que o login, ação data e hora/m/s sejam registradas no arquivo log.txt.
    """
    from datetime import datetime

    dataHora = datetime.now()
    dataHoraFormat = dataHora.strftime("%d/%m/%y %H:%M:%S")
    log = login + " " + acao + "\t" + dataHoraFormat
    arquivo = open("log.txt","a")
    arquivo.write(log)
    arquivo.write("\n")
    arquivo.close()

def menu(checarNivelAcesso):

    """
    Essa função é chamada após a checagem do acesso e do nível de acesso, se for TRUE o menu
    é printado na tela de acordo com o nível de acesso do usuário e dessa forma o usuário poderá
    utilizar o programa.
    """
    pegarRetorno = checarNivelAcesso
    nivel = pegarRetorno[0]
    login = pegarRetorno[1]

    sair = False
    while sair == False:
        
        sair_2 = False
        while sair_2 == False:
            
            if nivel == "1":

                menu = int(input(">>>MENU<<<""\n""\n"
                                 "1 - Buscar usuário(s)""\n""2 - Editar usuário(s)""\n"
                                 "3 - Remover usuário(s)""\n""4 - Cadastrar livro(s)""\n"
                                 "5 - Buscar Livro(s)""\n""6 - Editar informações do(s) livro(s) cadastrado(s)""\n"
                                 "7 - Remover livro(s)(Via ISBN)""\n""8 - Encerrar o programa""\n"
                                 "9 - Logout""\n"))
                
                if menu < 1 or menu > 9:
                    print("")
                    print("Digito incorrento, tente novamente.""\n")
                
                elif menu == 1:

                  buscarUsuario(login)

                elif menu == 2:

                    editarUsuario(login)
                    
                elif menu == 3:

                    removerUsuarios(login)
                    

                elif menu == 4:

                    elementos = lerArquivoElementos()
                    cadastroLivro(elementos) 
                    

                elif menu == 5:

                    buscaLivros(login)
                    

                elif menu == 6:

                    editarLivros()
                    
                    
                elif menu == 7:

                    removerLivros()
                    

                elif menu == 8:

                    print("Programa encerrado")
                    sair = True
                    sair_2 = True

                elif menu == 9:
                    print("Programa encerrado")
                    return acesso()
                    
            elif nivel == "2":
                
                menu = int(input("Menu""\n""\n"
                                 "1 - Buscar usuários""\n""2 - Cadastrar livro(s)""\n"
                                 "3 - Editar informações do(s) livro(s) cadastrado(s)""\n"
                                 "4 - Bucar livro(s)""\n""5 - Remover livro(s)""\n"
                                 "6 - Editar usuário""\n""7 - Encerrar o programa""\n"
                                 "8 - Logout""\n"))


                if menu < 1 or menu > 8:
                    print("Digito incorrento, tente novamente.""\n")

                elif menu == 1:
                    
                    buscarUsuario(login)
                    
                elif menu == 2:

                    elementos = lerArquivoElementos()
                    cadastroLivro(elementos)
                    

                elif menu == 3:

                    editarLivros()

                elif menu == 4:

                    buscaLivros(login)
                
                elif menu == 5:

                    removerLivros()

                elif menu == 6:
                    
                    editarUsuario(login)
                    
                elif menu == 7:
                    print("Programa encerrado""\n")
                    sair = True
                    sair_2 = True

                elif menu == 8:
                    print("Programa encerrado""\n")
                    return acesso()
                    
            elif nivel == "3":

                menu = int(input("Menu""\n""\n"
                                 "1 - Cadastrar livro(s)""\n"
                                 "2 - Editar informações do(s) livro(s) cadastrado(s)""\n"
                                 "3 - Buscar livro(s)""\n"
                                 "4 - Remover livro(s)""\n"
                                 "5 - Encerrar o programa""\n"
                                 "6 - Logout""\n"))
                
                if menu < 1 or menu > 6:
                    print("Digito incorrento, tente novamente.""\n")
                
                elif menu == 1:
                    
                    elementos = lerArquivoElementos()
                    cadastroLivro(elementos)
                    

                elif menu == 2:

                    editarLivros()
                
                elif menu == 3:

                    buscaLivros(login)
                    
                elif menu == 4:

                    removerLivros()
                    
                    
                elif menu == 5:
                    print("Programa encerrado")
                    sair = True
                    sair_2 = True

                elif menu == 6:
                    print("Programa encerrado""\n")
                    return acesso()

acesso()

###Instrução###
#Para acesar como administrador(ra) 
#Login: adm
#Senha: adm
#Em andamento