# Radiant Forecast

## Descrição
Este projeto visa integrar dados meteorológicos do INMET (Instituto Nacional de Meteorologia) com dados de geração de energia solar da ONS (Operador Nacional do Sistema Elétrico) para criar uma base de dados unificada. O objetivo é utilizar essas informações para analisar e prever a geração de energia solar em Minas Gerais.

## Estrutura do Repositório
Descreva aqui a organização do repositório, facilitando a navegação e entendimento para novos colaboradores. Por exemplo:

```
├── data # Dados utilizados nas análises
    ├── external # Dados externos ao projeto
    ├── processed # Dados processados para análise
    └── raw # Dados brutos coletados
├── docs # Documentação relevante ao projeto
    ├── presentation.pptx # Apresentação do projeto
    └── references.md # Referências e fontes utilizadas
├── notebooks # Notebooks Jupyter para análise e modelagem
    ├── 01_data_collection.ipynb # Notebook para coleta de dados
    ├── 02_data_manipulation_and_merging.ipynb # Notebook para manipulação e cruzamento de dados
    ├── 03_data_preprocessing.ipynb # Notebook para pré-processamento de dados
    └── 04_modeling.ipynb # Notebook para modelagem de dados
├── src # Código-fonte para scripts e módulos
    ├── data_collection.py # Script para coleta de dados
    ├── data_manipulation_and_merging.py # Script para manipulação e cruzamento de dados
    ├── data_preprocessing.py # Script para pré-processamento de dados
    ├── database.py # Script para operações com banco de dados
    ├── modelling.py # Script para modelagem de dados
    └── utils.py # Funções utilitárias
├── .gitignore # Arquivo para especificar quais arquivos devem ser ignorados pelo Git
├── README.md # Descrição e instruções para o projeto
└── requirements.txt # Lista de dependências e bibliotecas necessárias para o projeto
```

## Configuração
Instruções sobre como preparar o ambiente para executar o projeto, incluindo a instalação de dependências:

```
# Adicione comandos para instalar dependências, por exemplo:
pip install -r requirements.txt
```

Versão do Python: 3.x

## Uso
### Executando os Notebooks

Os notebooks devem ser utilizados na seguinte ordem para garantir que todas as etapas do processo sejam concluídas corretamente:

1. **01_data_collection.ipynb**: Este notebook realiza a coleta dos dados brutos do INMET e da ONS.
2. **02_data_manipulation_and_merging.ipynb**: Este notebook manipula e cruza os dados meteorológicos com os dados de geração de energia solar, integrando-os em uma única base de dados.
3. **03_data_preprocessing.ipynb**: Este notebook pré-processa os dados, preparando-os para a modelagem.
4. **04_modeling.ipynb**: Este notebook realiza a modelagem dos dados para análise e previsão da geração de energia solar.


## Contato
Para mais informações ou caso necessite falar com os responsáveis pelo projeto, entre em contato:

**Amanda Ferreira de Azevedo**  
Email: [afazevedo29@gmail.com](mailto:afazevedo29@gmail.com)

