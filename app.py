# Iniciar o código e importar algumas bibliotecas e módulos que serão utilizados
import pandas as pd
import re
import json
from datetime import datetime, date
import requests

# Informar que iniciou a rodar o código
print("INFO: Inciando execução.")

# Criar váriaveis para trazer os caminhos para os arquivos que serão utilizados
caminho_dados = './dados.xlsx'
caminho_erro = './erro.xlsx'
caminho_saida_json = './dados_saida.json'
caminho_sistema = './sistema.xlsx'

# Iniciar a função principal do app, chamando as váriaveis que serão utilizadas
def main(caminho_dados, caminho_erro, caminho_saida_json, caminho_sistema):
    try:
        # Leitura dos dados do arquivo XLSX
        limpar_dados_excel(caminho_erro)
        df = pd.read_excel(caminho_dados)
        
        # Lista para armazenar os dados que estão ok
        lista_sucesso = []

        # Estruturar os dados no formato Json que será enviado ao arquivo dados_saída.json se estiver ok
        for index, row in df.iterrows():
            dados_cliente = {
                "id": str(row['Faculdade']+"-"+re.sub(r'\D', '', row['CPF'])).lower(),
                "agrupador": row['Faculdade'],
                "tipoPessoa": row['Curso'],
                "nome": row['NOME'],
                "cpf": re.sub(r'\D', '', row['CPF']),
                "dataNascimento": formatar_data(row['Data de Nascimento']),
                "Tipo": validar_tipo(row['CPF'],caminho_sistema),
                "enderecos": [
                    {
                        "cep": row['CEP'].replace("-",""),
                        "logradouro": row['Endereço'],
                        "bairro": row['Bairro'],
                        "cidade": row['Cidade'],
                        "numero": str(row['Numero']),
                        "uf": row['Estado']
                    }
                ],
                "emails": [
                    {
                        "email": row['Email']
                    }
                ],
                "telefones": [
                    {
                        "tipo": "CELULAR",
                        "ddd": row["Telefone"].replace("(","")[:2],
                        "telefone": re.sub(r'\D', '', row['Telefone'])[2:]
                    }
                ],
                "informacoesAdicionais": [
                    {
                        "campo": "cpf_aluno",
                        "linha": index + 1,
                        "coluna": 1,
                        "valor": re.sub(r'\D', '', row['CPF'])
                    },
                    {
                        "campo": "registro_aluno",
                        "linha": index + 1,
                        "coluna": 1,
                        "valor": row['RA']
                    },
                    {
                        "campo": "nome_aluno",
                        "linha": index + 1,
                        "coluna": 1,
                        "valor": row['NOME']
                    }
                ]
            }
            
            print("INFO: Validando dados ID: "+str(row['Faculdade']+"-"+re.sub(r'\D', '', row['CPF'])).lower()+"...")
            
            # Criar lista para armazenar mensagens de inválidos e iniciar funções de validação dos dados. 
            mensagens_erro = []

            if not validar_nome_completo(row['NOME']):
                mensagens_erro.append("Nome inválido")
                
            if not validar_cep(row['CEP'].replace("-",""),row['Endereço']):
                mensagens_erro.append("CEP inválido")
            
            if not validar_data_nascimento(formatar_data(row['Data de Nascimento'])):
                mensagens_erro.append("Data de Nascimento inválida")
            
            if not validar_email(row['Email']):
                mensagens_erro.append("Email inválido")

            if not validar_telefone(row['Telefone']):
                mensagens_erro.append("Telefone inválido")
                        
            if not validar_cpf(row['CPF']):
                mensagens_erro.append("CPF inválido")
                        
            if mensagens_erro:
                dados_cliente_erro = {
                    'NOME': row['NOME'],
                    'CPF': row['CPF'],
                    'Data de Nascimento': formatar_data(row['Data de Nascimento']),
                    'Email': row['Email'],
                    'CEP': row['CEP'],
                    'Endereço': row['Endereço'],
                    'Numero': str(row['Numero']),
                    'Bairro': row['Bairro'],
                    'Cidade': row['Cidade'],
                    'Estado': row['Estado'],
                    'Telefone': row['Telefone'],
                    'RA': row['RA'],
                    'Curso': row['Curso'],
                    'Faculdade': row['Faculdade'],
                    'Motivo': '; '.join(mensagens_erro)
                }
                
                lista_erro = pd.DataFrame(dados_cliente_erro, index=[index])
                df_erro = pd.read_excel(caminho_erro)
                gravar_erro = pd.ExcelWriter(caminho_erro, mode='a',if_sheet_exists='overlay')
                lista_erro.to_excel(gravar_erro,index = False, header = False, startrow = len(df_erro) + 1)
                gravar_erro.close()
            
            else:
                lista_sucesso.append(dados_cliente)

        # Converter a lista_sucesso para JSON
        dados_json = json.dumps(lista_sucesso, ensure_ascii=False, indent=4)

        # Salvar a lista_sucesso em um arquivo JSON
        with open(caminho_saida_json, 'w', encoding='utf-8') as f:
            f.write(dados_json)

        print("INFO: Execução concluída com sucesso! Json salvo em "+caminho_saida_json+".")
    except:
        print("ERRO: Falha na preparação do Json.")
        
# Validar se o CEP é válido e se o logradouro bate com o endereço. Desafio Bônus
def validar_cep(cep, endereco):
    try:
        url = "https://viacep.com.br/ws/"+cep+"/json/"
        resposta = requests.get(url).json()
        logradouro = resposta["logradouro"]
        
        if endereco == logradouro:
            return True
        else:
            return False
    except:
        print("ERRO: Validação CEP")
        return False

# Validar se o nome é completo. Verificar se possui pelo menos 2 palavras (split)
def validar_nome_completo(nome):
    try:
        return len(nome.split()) >= 2
    except:
        print("ERRO: Validação nome completo")
        return False
    
# Validar se data de nascimento é válido e se é >17 anos
def validar_data_nascimento(data_nascimento):
    try:
        data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y')
        data_agora = datetime.now()
        idade = data_agora.year - data_nascimento.year
        
        if data_agora.month < data_nascimento.month or (data_agora.month == data_nascimento.month and data_agora.day < data_nascimento.day):
            idade -= 1
        
        if idade >17: 
            return True
        else:
            return False
    except:
        print("ERRO: Validação na idade (>17 anos)")
        return False
    
# Validar se email é correto. Dar um padrão e depois verificar se está sendo seguido
def validar_email(email):
    try:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
    except:
        print("ERRO: Validação do e-mail")
        return False
    
# Validar se telefone é correto. Dar um padrão e depois verificar se está sendo seguido
def validar_telefone(telefone):
    try:
        return re.match(r"^\(\d{2}\) \d{4,5}-\d{4}$", telefone) is not None
    except:
        print("ERRO: Validação de telefone")
        return False
    
# Verifica se o CPF é válido. O CPF deve conter 11 dígitos e passar na fórmula de validação
def validar_cpf(cpf):
    try:
        cpf = re.sub(r'\D', '', cpf) 
        if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
            return False
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(cpf[i]):
                return False
        return True
    except:
        print("ERRO: Validação CPF")
        return False
    
# Verificar se as informações precisarão ser inseridas (I) ou atualizadas (A), consultando a base de dados sistema.xlsx
def validar_tipo(cpf, caminho_sistema):
    try:
        df = pd.read_excel(caminho_sistema)
        
        if cpf in df['cpf'].values:
            return 'A'
        else:
            return 'I'
    except:
        print("ERRO: Validação CPF cadastrado no arquivo: "+caminho_sistema)

# Converter data de nascimento para dd/mm/yyyy (padrão brasileiro)   
def formatar_data(data):
    try:
        if isinstance(data, date):
            data_formatada = data
        else:
            data_formatada = datetime.strptime(data, '%d/%m/%Y')
        return data_formatada.strftime('%d/%m/%Y')
    except:
        print("ERRO: Formatação de data de nascimento")
        return False
    
# Limpar informações do arquivo erro.xlsx
def limpar_dados_excel(caminho_erro):
    try:
        df = pd.read_excel(caminho_erro)
        
        df_limpo = df.head(0)
        
        df_limpo.to_excel(caminho_erro, index=False)
    except:
        print("ERRO: Falha limpeza arquivo: "+caminho_erro)

# Iniciar a execução da função principal
if __name__ == "__main__":
    main(caminho_dados, caminho_erro, caminho_saida_json, caminho_sistema)