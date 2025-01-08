import os
import re
from typing import Literal
import pandas as pd
import shutil

# Caminho Pasta Atual
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Caminhos Pastas Fotos
FOTOS = os.path.join(ROOT_PATH, "Fotos_Sistema") 
FOTOS_ISOLAD = os.path.join(ROOT_PATH, "Fotos_Isoladas") # Pasta Fotos s/ Registro
FOTOS_FALHAS = os.path.join(ROOT_PATH, "Fotos_Falhas") # Pasta Fotos c/ Erro

# Função - Encontrar o arquivo CSV mais recente
def find_recent_csv(padrao: Literal['']) -> str | None:
    csv_files = [file for file in os.listdir(ROOT_PATH) if re.match(padrao, file)]
    csv_files.sort(reverse=True)
    return os.path.join(ROOT_PATH, csv_files[0]) if csv_files else None

# Padrão do nome dos arquivos CSV
PADRAO_CSV = r"Pessoas_\d{6}_\d{4}.csv"

# Encontra o arquivo CSV mais recente
recent_csv_file = find_recent_csv(PADRAO_CSV)

# Verificação de Existência de CSV
if recent_csv_file is None:
    raise FileNotFoundError(
        "Nenhum arquivo CSV encontrado com o padrão especificado.")

# Leitura da tabela CSV definindo "Registro" como string
df = pd.read_csv(recent_csv_file, dtype={"Registro": str})

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
    