# Automação do processo "Extrair CNAE IBGE"

Navega pelo site do IBGE e busca dados de CNAE das seções A, B e C. Insere informações em planilha e depois higieniza dados.

## Funcionamento

Esta automação foi desenvolvida tendo como base o REFramework para se aproveitar de todos os benefícios já conhecidos do projeto, como padronização do código, robustez e logs. Seria possível também adaptar facilmente para uso de Queues para processar ainda mais rápido.

Robustez é especialmente importante neste processo pois o site é muito instável, apresentando erros frequentes no carregamento das muitas páginas visitadas pelo robô.

Por se tratar do REFramework, o funcionamento da automação será detalhados considerando os estados do projeto.

Esta automação é passível de rodar em *background*, já que as interações com a tela podem ser feitas com propriedade `Simulate` habilitada.

### Initialization

No estado **Initilization** é carregado as configurações do projeto, bem como iniciado os sistemas, que neste caso é o site do IBGE.

É neste estado também que o robô identifica quais são as seções que devem ser extraídas. A automação foi desenvolvida de forma que se fosse desejado processar outras além das A, B e C, seria muito simples, bastando apenas informar no arquivo `Config`.

Aqui também é criado o arquivo do Excel onde os dados extraídos do site do IBGE serão armazenados.

### Get Transaction Data

Estado sem muitas modificações em relação ao REFramework padrão, com exceção da alteração para obter o `TransactionItem` de uma tabela.

### Process

O robô acessa a página da seção referente à transação atual utilizando seletores dinâmicos, para depois iniciar o processo de extração de informações até o último nível hierárquico, que é a Subclasse.

Foi criado o *workflow* **ExtrairDadosHierarquiaFinal.xaml** que faz a extração das informações independente de qual das páginas está carregada. Este fluxo retorna uma tabela com todas as informações necessárias para que o robô faça a navegação, além do nome referentes aos códigos. Para que a extração ficasse flexível desta maneira, a propriedade `ExtractMetadata` foi customizada para extrair informações apenas do último nível de hierarquia presente na página, independente de qual dos níveis de hierarquia esteja carregado. 

Outras alterações nesta atividade de extração foram habilitar para que seja lançado exceção em casos de falha, a fim de tratar erros adequadamente, além de configurar para que aguarde a página carregar completamente. Mesmo com a instabilidade do sistema, que muitas vezes falha em carregar páginas, o robô aguarda o tempo definido no *timeout* antes de lançar uma exceção e este comportamento por si só já evita encerramentos desnecessários, já que o navegador consegue recarregar a página automaticamente depois de alguns segundos, contornando a instabilidade de forma elegante. Caso o carregamento correto da página não ocorra dentro do tempo estipulado, então uma exceção é lançada e o robô pode tentar processar a seção novamente, dependendo do que for configurado no parâmetro da planilha `Config`. 

Laços de repetição foram utilizados para que o robô percorra todas as páginas com informações dinamicamente, garantindo que independente da quantidade de links que surgirem, a extração ocorrerá conforme desejado.

Ao extrair as informações referentes ao último nível hirárquico (Subclasse), o robô insere os dados na tabela interna dele de controle, que no fim do processamento de cada transação é persistido na planilha do Excel e posteriormente limpa, preparando para a próxima transação ou até mesmo para uma retentativa de processar a seção em caso de falha.

As transições de exceções possuem uma ação que é chamar o *workflow* que navega para a página inicial do site, a fim de conseguir realizar novas tentativas de processamento para aquela seção.

As planilhas geradas pelo robô possuem o timestamp do início da execução no nome do arquivo e ficam armazenadas na pasta `Data\Output` por padrão (caminho relativo ao projeto).

### End Process

Neste estado é feito o processamento dos dados extraídos pelo robô utilizando Python. Para esta tarefa foi escolhido utilizar a biblioteca Pandas por ser excelente para trabalhar com dados, sendo bastante performática.

O script em Python foi desenvolvido para aproveitar das vantagens oferecidas pelo Pandas, entre elas a possibilidade de processar lotes de dados de uma só vez. Isto é utilizado para remover acentuação, deixar textos em minúsculo e remover caracteres não dígitos de colunas de códigos específicas.

## Gravação da execução

Uma demonstração de execução deste processo pelo robô está disponível através deste [link](https://1drv.ms/u/s!AiGNcL-XaP2nh-VWW8-xU_9JSnc7_A?e=xRU6bb).

## Pré-requisitos para execução

- Python 3 (x64) com libs 'pandas' e 'openpyxl' instaladas na máquina;
- No arquivo Config do framework, definir o valor do parâmetro "PathPython" de acordo com o caminho do executável Python instalado na máquina.