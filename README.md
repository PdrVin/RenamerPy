# Automação para Renomeação e Organização de Arquivos

Este projeto foi desenvolvido durante meu estágio no Departamento de TI do UNIAENE com o objetivo de automatizar a renomeação e organização de arquivos com base em uma tabela de dados (CSV).

## Funcionalidades 🛠️

### Renomeação de Arquivos
- **Identificação automática** do arquivo CSV mais recente com dados dos usuários.
- **Padronização de nomes** de usuários e códigos de registro, garantindo a correspondência correta.
- **Renomeação das fotos** com base no código de registro.
- **Separar automaticamente** as fotos sem correspondência em uma pasta específica.
- Geração de **relatórios detalhados** ao final do processo.

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
- `Fotos_Sistema/`: Pasta contendo as fotos a serem renomeadas.
- `Fotos_Isoladas/`: Pasta que irá armazenar fotos sem correspondência.
- `Fotos_Falhas/`: Pasta que irá armazenar fotos que geraram erros.

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

---
Espero que este projeto seja útil para automatizar suas tarefas e inspirar novas soluções práticas no dia a dia! 😄
