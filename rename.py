import os
import re
import shutil
from typing import Literal
import pandas as pd
from unidecode import unidecode

# Caminho Pasta Atual
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Caminhos Pastas Fotos
FOTOS = os.path.join(ROOT_PATH, "FotosSistema") 
FOTOS_ISOLAD = os.path.join(ROOT_PATH, "FotosIsoladas") # Pasta Fotos s/ Registro
FOTOS_FALHAS = os.path.join(ROOT_PATH, "FotosFalhas") # Pasta Fotos c/ Erro

# Certifica-se que as pastas de destino existem
for folder in [FOTOS_ISOLAD, FOTOS_FALHAS]:
    os.makedirs(folder, exist_ok=True)

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
df["Usuário"] = df["Usuário"].str.strip().str.lower().apply(unidecode)

# Criação de dicionário para mapear Nomes de Usuários para Matrículas
nome_p_registro = dict(zip(df["Usuário"], df["Registro"]))

# Inicialização de contadores e lista de erros
transfered_rows, affected_rows, fail_rows = 0, 0, 0
list_falhas = []

# Iteração dos arquivos de foto na Pasta
for arquivo in os.listdir(FOTOS):
    try:
        if arquivo.lower().endswith(".jfif"):
            # Extrai o Nome da Foto e a Extensão
            nome_foto, extensao = os.path.splitext(arquivo)
            nome_foto = unidecode(nome_foto.lower()) # Remove acentuação
            
            # Extrai o Código de Registro
            registro = nome_p_registro.get(nome_foto)
            
            # Caminho Original de cada foto
            path_original = os.path.join(FOTOS, arquivo)
            
            # Verificar Registro Vazio
            if registro in ['000nan']:
                new_path = os.path.join(FOTOS_ISOLAD, arquivo)
                shutil.move(path_original, new_path)
                transfered_rows += 1
            elif registro in [None, 'None']:
                new_path = os.path.join(FOTOS_FALHAS, arquivo)
                shutil.move(path_original, new_path)
                fail_rows += 1
            else:
                new_name = f"{registro}{extensao}"
                new_path = os.path.join(FOTOS, new_name)
                os.rename(path_original, new_path)
                affected_rows += 1
    except Exception as e:
        # Adiciona o nome do arquivo e a mensagem de erro
        list_falhas.append((arquivo, str(e)))

# Relatório
print("Processo concluído.")
print(f"Fotos Renomeadas: {affected_rows}")
print(f"Fotos Isoladas: {transfered_rows}")
print(f"Fotos Falhas: {fail_rows}")

# Relatório Erros
print("Erros:", end=" ")
print(0) if not list_falhas else print("\n")
for arquivo, erro in list_falhas:
    print(f"Arquivo: {arquivo} - Erro: {erro}")
