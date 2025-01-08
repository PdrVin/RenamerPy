import os
import pandas as pd
import shutil

# Caminho Pasta Atual
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Caminhos Pastas Fotos
FOTOS = os.path.join(ROOT_PATH, "FotosSistema") 
FOTOS_ISOLAD = os.path.join(ROOT_PATH, "FotosIsoladas") # Pasta Fotos s/ Registro
FOTOS_FALHAS = os.path.join(ROOT_PATH, "FotosFalhas") # Pasta Fotos c/ Erro
EXCEL = os.path.join(ROOT_PATH, "UsuáriosSistema.xlsx")

# Leitura da tabela Excel definindo "Registro" como string
df = pd.read_excel(EXCEL, dtype={"Registro": str})

# Preparação dos dados no DataFrame
df["Registro"] = df["Registro"].str.zfill(6)  # Garante zeros à esquerda
df["Usuário"] = df["Usuário"].str.strip()

# Criação de dicionário para mapear Registros para Usuários
register_user = dict(zip(df["Registro"], df["Usuário"]))

# Inicialização de contadores e lista de erros
transfered_rows, affected_rows, none_rows = 0, 0, 0
list_falhas = []

# Iteração dos arquivos de foto na Pasta
for arquivo in os.listdir(FOTOS):
    try:
        if arquivo.lower().endswith(".jfif"):
            # Extrai o Nome da Foto e a Extensão
            register_foto, extensao = os.path.splitext(arquivo)
            
            # Extrai o Código de Registro
            name_user = register_user.get(register_foto)
            
            # Caminho Original de cada foto
            path_original = os.path.join(FOTOS, arquivo)
            
            # Verificar Matricula Vazia
            if name_user in [None, 'None']:
                new_path = os.path.join(FOTOS_FALHAS, arquivo)
                shutil.move(path_original, new_path)
                none_rows += 1
            else:
                new_name = f"{name_user}{extensao}"
                new_path = os.path.join(FOTOS, new_name)
                os.rename(path_original, new_path)
                affected_rows += 1
    except Exception as e:
        # Adiciona o nome do arquivo e a mensagem de erro
        list_falhas.append((arquivo, str(e)))

# Relatório
print("Processo concluído.")
print(f"Fotos Renomeadas: {affected_rows}")
print(f"Fotos Falhas: {none_rows}")

# Relatório Erros
print("Erros:", end=" ")
print(0) if not list_falhas else print("\n")
for file, error in list_falhas:
    print(f"Arquivo: {file} - Erro: {error}")
    