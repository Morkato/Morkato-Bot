# MorkatoStorage (Object Storage)
MorkatoStorage é um **serviço de armazenamento eficiente e de alta performance** para dados binários (como imagens). Ele é programado em C++ para fornecer controle de memória e velocidade. Este documento descreve a estrutura e os principais componentes do serviço.
1. Estrutura de Armazenamento e UUID
  1. Arquivos de Armazenamento
    Os dados binários serão armazenados em arquivos grandes. Cada arquivo tem duas partes principais:
      ###### Headers (Metadados):
      1. **Assinatura** (7 BYTES - CHAR[7]): Validação do servidor com o valor fixo MORKATO. Todas as requisições precisam incluir essa assinatura.
      2. **Length** (4 BYTES - UINT): Número total de objetos no arquivo.
      ###### Body (Conteúdo):
      1. **Objeto:** Dados binários armazenados, precedidos pelo tamanho (4 BYTES - UINT).
  2. Gerenciamento de Arquivos
    * Cada arquivo pode conter até **2³² - 1 objetos**.
    * Ao exceder o limite, um novo arquivo será criado automaticamente.
    * O nome do arquivo é gerado dinamicamente e vinculado aos IDs dos objetos.
  3. UUID de Objetos
    Os IDs dos objetos são gerados como uma concatenação:
    * Data de criação.
    * Local da memória no arquivo.
    * Identificação do arquivo.
    O UUID é criptografado para garantir que apenas o MorkatoStorage saiba interpretá-lo.
2. Comunicação com o Serviço