# Dashboard-de-log-stica-feito-em-Python


Dashboard de Logística - Loggi

Este repositório contém um dashboard interativo desenvolvido em Python com o framework Dash e a biblioteca Plotly, destinado à análise exploratória de dados de logística. O dashboard foi criado para auxiliar na visualização e interpretação de dados referentes às operações de entrega e distribuição da empresa Loggi, sendo parte de uma análise de dados aplicada à logística.

Sumário

Descrição

Funcionalidades

Arquitetura e Fluxo de Dados

Instalação

Uso

Estrutura do Código

Contribuição

Licença


Descrição

O dashboard analisa dados armazenados em um arquivo JSON (deliveries.json) que contém informações sobre hubs (centros de distribuição), capacidade dos veículos e entregas realizadas. O código implementa:

Download e carregamento dos dados: Caso o arquivo JSON não esteja presente, o script tenta baixá-lo de um repositório remoto. Se o download falhar, um conjunto de dados de exemplo é criado.

Processamento dos dados: Os dados são processados e transformados usando Pandas, incluindo extração de dados aninhados (ex.: informações do hub) e cálculo de métricas como número de entregas, densidade de entregas e taxa de utilização da capacidade dos veículos.

Visualizações interativas: O dashboard exibe:

Um mapa interativo (usando Plotly e Mapbox) que permite alternar entre a visualização dos hubs e das entregas.

Um gráfico de barras com o número de entregas por hub, com opções de ordenação.

Um gráfico de utilização de capacidade que mostra a taxa de utilização de cada hub.

Uma análise comparativa por região, permitindo comparar hubs de uma região específica ou visualizar métricas agregadas por região.


Filtros e métricas dinâmicas: É possível filtrar os dados por região e ordenar os hubs de acordo com diferentes critérios. O dashboard também apresenta cards com métricas como total de hubs, total de entregas, capacidade total e média de entregas por hub.


Funcionalidades

Download automático do dataset: Se o arquivo deliveries.json não for encontrado localmente, o script fará o download do arquivo do repositório oficial.

Tratamento de erros: Caso o download ou o carregamento dos dados falhe, o sistema cria um conjunto de dados mínimo para garantir que o dashboard funcione.

Interatividade: Filtros por região, ordenação dos hubs e seletor de visualização do mapa (entre hubs e entregas).

Visualizações interativas e responsivas: Mapa, gráficos de barras e de utilização que se adaptam a diferentes dispositivos e tamanhos de tela.

Estilo profissional: Layout e estilos customizados utilizando CSS embutido para melhorar a experiência do usuário.


Arquitetura e Fluxo de Dados

1. Carregamento dos Dados:

Função load_data(): Verifica se o arquivo JSON existe. Caso contrário, tenta baixá-lo ou gera um dataset de exemplo.



2. Processamento dos Dados:

Função process_data(data): Cria um DataFrame, extrai informações aninhadas, calcula métricas (número de entregas, densidade, utilização) e gera um DataFrame adicional com os destinos das entregas.



3. Dashboard e Visualizações:

O layout do dashboard é definido com seções para cabeçalho, filtros, cards de métricas, mapa interativo, gráficos e rodapé.

Callbacks do Dash atualizam as visualizações com base nos filtros selecionados e nos dados processados.




Instalação

Certifique-se de ter o Python (3.7+) instalado e instale as dependências necessárias usando pip:

pip install dash pandas plotly requests numpy

Uso

1. Clone o repositório:

git clone https://github.com/Lelolima/Dashboard-de-log-stica-feito-em-Python

2. Execute o dashboard:

python dashboard.py


3. Abra o navegador e acesse http://127.0.0.1:8050 para interagir com o dashboard.



Estrutura do Código

dashboard.py:
Arquivo principal que contém a lógica para:

Carregamento e processamento dos dados;

Definição do layout do dashboard;

Callbacks para interatividade (atualização dos gráficos, métricas, e mapas).


deliveries.json:
Arquivo com os dados das entregas. Caso não esteja presente, o código tentará baixá-lo automaticamente ou criará um dataset de exemplo.

README.md:
Este arquivo, com as instruções e documentação do projeto.


Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar o código, adicionar novas funcionalidades ou corrigir eventuais bugs.

Licença

Este projeto está licenciado sob a MIT License.


