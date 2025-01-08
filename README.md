# Automação para Renomeação e Organização de Arquivos

Este projeto foi desenvolvido durante meu estágio no Departamento de TI do UNIAENE com o objetivo de automatizar a renomeação e organização de arquivos com base em uma tabela de dados (CSV). Além disso, inclui a funcionalidade de reverter os arquivos renomeados para seus nomes originais.

## Funcionalidades 🛠️

### Renomeação de Arquivos
- **Identificação automática** do arquivo CSV mais recente com dados dos usuários.
- **Padronização de nomes** de usuários e códigos de registro, garantindo a correspondência correta.
- **Renomeação das fotos** com base no código de registro.
- **Separar automaticamente** as fotos sem correspondência em uma pasta específica.
- Geração de **relatórios detalhados** ao final do processo.

### Reversão de Arquivos
- Reverte os arquivos renomeados para seus nomes originais utilizando o histórico gerado pelo script.

## Benefícios 📈
- Redução significativa do tempo gasto na organização manual.
- Solução robusta e escalável para lidar com grandes volumes de arquivos.
- Tratamento eficaz de inconsistências nos dados.

## Aprendizados 🚀
Durante o desenvolvimento deste projeto, adquiri experiência prática em:
- **Python** para automação de processos.
- Manipulação de arquivos e diretórios.
- Tratamento de exceções e inconsistências em dados.
- Organização e documentação de código.

## Estrutura do Projeto 📂
- `rename.py`: Script principal para renomeação de arquivos.
- `reverse.py`: Script para reverter os nomes dos arquivos para o estado original.
- `Fotos_Sistema/`: Pasta contendo as fotos a serem renomeadas.
- `Fotos_Isoladas/`: Pasta contendo fotos sem correspondência.
- `Fotos_Falhas/`: Pasta contendo fotos com erros.

## Importações Necessárias
```python
import os
import re
import shutil
from typing import Literal
import pandas as pd
from unidecode import unidecode
```

## Como Usar 🚀

### Pré-requisitos
- Python 3.x instalado na sua máquina.
- Bibliotecas pandas e unidecode instaladas:
  ```bash
  pip install pandas unidecode
  ```

### Executando o Script de Renomeação
1. Coloque o arquivo CSV mais recente na pasta que os arquivos  `.py` estão.
2. Adicione as fotos na pasta `Fotos_Sistema/`.
3. Execute o script de renomeação:
   ```bash
   python rename.py
   ```
4. O script criará uma pasta separada para fotos sem correspondência e gerará um relatório em `relatorios/`.

### Executando o Script de Reversão
1. Certifique-se de que o histórico de renomeação está presente na pasta `relatorios/`.
2. Execute o script de reversão:
   ```bash
   python reverse.py
   ```
3. Os arquivos serão revertidos para seus nomes originais com base no histórico.

---
Espero que este projeto seja útil para automatizar suas tarefas e inspirar novas soluções práticas no dia a dia! 😄
