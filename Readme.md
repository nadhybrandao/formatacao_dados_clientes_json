# 💻Resolução do Teste💻 #

## 💡LÓGICA DA RESOLUÇÃO:💡 ##
Dividi a resolução em partes:
1. Precisava estruturas os dados no formato json, com isso utilizei o exemplo enviado para isso;
2. Validar todas as informações e também colocar as informações de erro, caso as informações estivessem incorretas;
3. Padronizar as informações, pois vieram de formas diferentes, com isso daria erro diferentes;
4. Criar chamada de API para validação de CEP (teste bônus).

## 💻PASSO A PASSO:💻 ##
- Requisitos:
    - Python 3.12.4;
    - pandas;
    - re;
    - json;
    - datetime;
    - requests.
-   Comando de execução:
```
python ./app.py
```

### IMPORT: ###
Comecei adicionando o import para incluir bibliotecas e módulos. Utilizei a biblioteca do **pandas** para manipulação e análise de dados, o **re** para expressões regulares, **JSON** para trabalhar dados no formato, **datetime** para manipular datas e horários, e **requests** para fazer requisições HTTP.

### VARIÁVEIS: ###
Criei variáveis para o caminho das pastas que serão utilizadas, para ficar mais limpo os códigos.
```
caminho_dados = './dados.xlsx'
caminho_erro = './erro.xlsx'
caminho_saida_json = './dados_saida.json'
caminho_sistema = './sistema.xlsx'
```

### PRINT INICIAL E FINAL: ###
Adicionei um print inicial para informar que o código começou a rodar:
```
print("INFO: Inciando execução.")
```

No final pode correr Sucesso:
```
print("INFO: Execução concluída com sucesso! Json salvo em "+caminho_saida_json+".")
```
ou Falha:
```
print("ERRO: Falha na preparação do Json.")
```

### FUNÇÃO PRINCIPAL: ###
Iniciei chamando as principais váriaveis com os arquivos que serão abertos no decorrer da função *main*. Primeiro ponto é abrir os arquivos xlsx, todos os dados que tiverem corretores estará em *lista_sucesso*. Utilizei o exemplo enviado para começar a formatar o json que será enviado, precisei condicionar o formato do ID, CPF, data de nascimento, tipo, cep, ddd e telefone. Após isso, criei um print de informação que os ID's foram válidados, até para testar se estavam corretos, criei as mensagem de erro para mostar quais o motivo do erro. Inserido comandos aonde essas informações deveriam ficar, converter para umna lista de sucesso em json, salvar o arquivo e informar que execução foi concluída ou não.

### CONVERTER DATA DE NASCIMENTO: ###
Criei uma função *formatar_data* onde as datas receberão um formato padrão "dd/mm/yyyy". Primeiro verifiquei se *data* é uma instância de *date* (se é um objeto de data), caso seja receberá a função *formatar_data*, caso contrário é convertido para um objeto *datetime* usando *datetime.strptime*. Para formartar a data, utilizei *data_formatada.strftime('%d/%m/%Y')* ára converter *data_formatada* de volta para uma string no formato "dd/mm/yyyy".

Fiquei quebrando um pouco a cabeça pois não sabia se em dados estava como dd/mm/yyyy ou mm/dd/yyyy, mas tomei como parâmetro o dd/mm/yyyy após abrir o excel converter tudo para data. Tentei por bastante tempo utlizar vários tipos de códigos, mas estava voltando algumas datas com hora (exemplo: 02/08/2000 00:00:00), mas consegui achar este formato em uma aula e deu certo.

### LIMPAR ARQUIVO ERRO.XLSX: ###
Toda vez que rodava o código, os dados era adicionados de forma acumulativa no arquivo *erro.xlsx*. Com isso criei essa função para limpar os dados do *erro,xlsx*, mantendo apenas o cabeçalho, e salvar o arquivo modificado de volta no mesmo caminho.

## 📝VALIDAR INFORMAÇÕES:📝 ##
⚠️ Se ocorrer qualquer exceção durante a execução do *try*, o *except* será executado, com isso é retornado *False*, pois falhou a validação.

### VALIDAR CEP: ###
Defini uma função *validar_cep* onde receberá dois parâmetros (*cep* e *endereco*). Em seguida construi uma chamada para acessar a API ViaCEP, incorporando o CEP fornecido pelo JSON, fiz uma requisição GET a API. Extrai as informações logradouro e depois realizei a comparação se o endereço é igual ou diferente ao endereço informado. 

### VALIDAR NOME COMPLETO: ###
Defini uma função *validar_nome_completo* para verificar se o *nome* fornecido consiste em pelo menos dois componentes (Nome e Sobrenome). O *nome.split()* divide o *nome* em uma lista usando o espaço como delimitadores, em seguinda é contado quanto componentes existem em cada lista e verifica se estes componentes são maior que 2.

### VALIDAR DATA DE NASCIMENTO: ###
Defini uma função *validar_data_nascimento* que receberá *data_nascimento* caso indique que o cliente tem mais que 17 anos. Converti *data_nascimento* em um objeto *datetime* usando o formato (dd/mm/yyyy), criei uma variável com data e hora atuais, para calcular a idadel da pessoa (*data_agora.year - data_nascimento.year*). Precisei ajustar caso o aniversário do cliente ainda não ocorreu este ano.

### VALIDAR E-MAIL e TELEFONE: ###
Defini uma função *validar_email* e *validar_telefone* que reberá o e-mail e o outro receberá o telefone do cliente, caso esteja no formato correto. O *re.match...* é uma expressão regular para verificar se o e-mail ou telefone corresponde ao padrão báscio.

### VALIDAR CPF: ###
Defini uma função *validar_cpf* que reberá o cpf fornecido, caso esteja no formato correto e é válido de acordo com as regras brasileiras. Retirei todos os caracteres não uméricos (". " e "-"), verifiquei se o CPF é diferente de 11 dígitos e se este dígitos são iguais, caso a condição fosse verdeira, retorna *False*. Em seguinda um calculo e verificação da regra do CPF.

Essa parte achei interresante, pois estava pesquisando como validar um CPF e verifiquei que existe uma regra:

>"A validação de CPF é baseada na verificação dos nove primeiros dígitos do CPF, e comparada com os dois últimos dígitos:
>
>Multiplicamos os nove primeiros dígitos do CPF um a um pelos valores decrescentes de 10 até 2, conforme o exemplo a seguir para o CPF 123.456.789-10, onde multiplicamos:
>
>1 X 10 = 10 - 2 X 9 = 18 - 3 X 8 = 24
>
>e assim sucessivamente, ao final pegamos o total da soma destes nove resultados e dividimos por 11.
>
>Se o resto desta soma for menor ou igual a 1 e o penúltimo dígito do CPF deve ser igual ao numeral zero... Entretanto se o resto for maior de 2, então o penúltimo dígito do CPF deve ser igual a diferença entre o numero 11 menos o valor do resto obtido."

### VERIFICAR INFORMAÇÕES "I" OU "A": ###
Defini uma função *validar_tipo* que verificará se o CPF fornecido está presente na váriavel *caminho_sistema*. Utilizei a biblioteca *pandas* para ler o arquivo localizado no *caminho_sistema* e armazena o conteúdo em um DataFrame *df*, verifique se o CPF está presente na coluna cpf do *df*, caso estiver presente, retorna ¨A¨, caso contrário, retorna ¨I¨.
 
## 🔳SAÍDAS DE TELA:🔳 ##
```
INFO: Inciando execução.
INFO: Validando dados ID: usp-14538854042...
INFO: Validando dados ID: unicamp-56479804652...
INFO: Validando dados ID: ufba-74686320909...
INFO: Validando dados ID: ufrj-97206364873...
INFO: Validando dados ID: usp-91450681603...
INFO: Validando dados ID: unicamp-18055390193...
INFO: Validando dados ID: usp-54231533601...
INFO: Validando dados ID: ufpr-56862426745...
INFO: Validando dados ID: usp-46652259400...
INFO: Validando dados ID: ufba-67261458104...
INFO: Validando dados ID: unicamp-76213854991...
INFO: Validando dados ID: unicamp-41402042906...
INFO: Validando dados ID: unicamp-58367221028...
INFO: Validando dados ID: unicamp-74154779109...
INFO: Validando dados ID: ufrj-6692225183...
INFO: Validando dados ID: ufba-4892321249...
INFO: Validando dados ID: ufrj-47401084961...
INFO: Validando dados ID: ufrj-29173074390...
INFO: Validando dados ID: ufrj-04012272195...
INFO: Validando dados ID: ufrj-46547901360...
INFO: Validando dados ID: usp-91450681603...
INFO: Validando dados ID: usp-03011616150...
INFO: Execução concluída com sucesso! Json salvo em ./dados_saida.json.
```

## 📚REFERÊNCIAS: ##

- [Python Docs](https://docs.python.org/pt-br/3/)
- [pandas Docs](https://pandas.pydata.org/docs/)
- [GitHub Docs](https://docs.github.com/pt)
- [Tutoriais do Youtube](https://www.youtube.com/)
- [Stack overflow](https://stackoverflow.com/)