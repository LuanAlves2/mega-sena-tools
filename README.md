# 🎲 Mega-Sena Tools V2.0

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0-orange)

</div>

## 📋 Descrição

Ferramenta avançada para análise e geração de apostas da Mega-Sena, Lotofácil e Quina, utilizando padrões históricos e estatísticas para otimizar suas chances de ganho. O sistema analisa milhares de sorteios para identificar padrões e gerar apostas mais inteligentes.

## 🗂️ Estrutura de Diretórios

```
📦 Mega-Sena Tools
 ┣ 📂 database/     # Base de dados de sorteios
 ┣ 📂 logs/         # Registros de execução
 ┣ 📂 sorteios/     # Apostas geradas
 ┣ 📜 main.py       # Ponto de entrada
 ┣ 📜 cli.py        # Interface do usuário
 ┣ 📜 utils.py      # Funções auxiliares
 ┣ 📜 downloader.py # Download de dados
 ┣ 📜 analyzer.py   # Análise Mega-Sena
 ┣ 📜 lotofacil_analyzer.py # Análise Lotofácil
 ┣ 📜 quina_analyzer.py     # Análise Quina
 ┣ 📜 validator.py  # Validação Mega-Sena
 ┣ 📜 lotofacil_validator.py # Validação Lotofácil
 ┗ 📜 quina_validator.py     # Validação Quina
```

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/mega-sena-tools.git
cd mega-sena-tools
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Uso

Execute o programa principal:
```bash
python main.py
```

### ✨ Funcionalidades

1. **🎯 Gerar Apostas**
   - Gera apostas baseadas em padrões históricos
   - Suporta apostas com quantidade de dezenas variável conforme o jogo
   - Validação automática de padrões

2. **🔍 Validar Apostas**
   - Verifica apostas em arquivos Excel
   - Análise de conformidade com padrões
   - Relatório detalhado de validação

3. **📊 Checar Resultados**
   - Verifica acertos de apostas
   - Relatório de acertos por aposta
   - Estatísticas de performance

4. **📥 Atualizar Dados**
   - Download automático de resultados
   - Atualização da base histórica
   - Processamento de novos dados

## 🛠️ Módulos

- **`main.py`**: Ponto de entrada do programa
- **`cli.py`**: Interface de linha de comando interativa
- **`utils.py`**: Funções auxiliares e utilitários
- **`downloader.py`**: Download e processamento de dados
- **`analyzer.py`**, **`lotofacil_analyzer.py`**, **`quina_analyzer.py`**: análises dos jogos
- **`validator.py`**, **`lotofacil_validator.py`**, **`quina_validator.py`**: validação e geração de apostas

## 📦 Requisitos

- Python 3.7 ou superior
- Dependências listadas em `requirements.txt`:
  - pandas >= 1.5.0
  - requests >= 2.28.0
  - beautifulsoup4 >= 4.11.0
  - openpyxl >= 3.0.10
  - tqdm >= 4.64.0
  - unidecode >= 1.3.0

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 💝 Apoie o Projeto

Se você gostou do projeto e quer ajudar no seu desenvolvimento, considere fazer uma doação em SOL (Solana)!

<div align="center">

![Solana](https://img.shields.io/badge/Solana-000000?style=for-the-badge&logo=solana&logoColor=white)

### 🎁 Faça uma Doação

Seu apoio ajuda a manter o projeto ativo e a implementar novas funcionalidades!

```
3hsQ1SWGQBwZHzpqdQuMyRjemthKpgKspWBsfi27YhJX
```

</div>

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ⚠️ Aviso Legal

Este software é apenas uma ferramenta de análise e não garante resultados em jogos de loteria. Use por sua conta e risco. 