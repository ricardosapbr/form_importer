# Scripts de importação dos formulário de inspeção CN/CNJ

## Sequência de execução do script:
1. Solicita o código de inspeção, ou seja, a senha informada para acesso aos formulários de determinada inspeção e.g TJXX@2024;
2. Criação da pasta **Arquivos Formulários de Inspeção** na pastas documentos do usuário;
3. Faz o download do arquivo **links_formularios_inspecao.txt** que contém os links de download das entradas do formulário informado no passo 1;
4. Cria uma pasta de cada formulário em uma pasta de mesmo nome do código de inspeção informado;
5. Baixa todos os formulários, em formato pdf, e seus anexos dentro de cada pasta de formulário;

## Uso do script:
1. Gerar um executável usando o pyinstaller (pip install pyinstaller ou conda install pyinstaller);
2.  


