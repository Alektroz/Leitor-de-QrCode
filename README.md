# Sistema Leitor de QR Code 📷🔳

Este projeto é um sistema desenvolvido em Python para realizar a leitura de QR Codes, consultar informações cadastradas e registrar automaticamente o histórico das leituras.

## 📋 Como funciona

O funcionamento do sistema é dividido em três arquivos principais que se comunicam entre si:

* **`QR_code.py`**: É o script principal e o "cérebro" do projeto. Ele é responsável por executar a lógica de captura e decodificação do QR Code (provavelmente através de uma webcam ou imagens estáticas). Ao ler um código, o script cruza essa informação com a base de dados.
* **`produtos.csv`**: Funciona como o banco de dados local do sistema. É um arquivo de texto separado por vírgulas que armazena a relação dos produtos (como ID, descrição, preço, etc.). O script Python usa esse arquivo para identificar a qual produto o QR Code lido pertence.
* **`historico_leituras.log`**: É o arquivo de auditoria (registro). Toda vez que uma leitura é feita com sucesso, o sistema adiciona uma nova linha neste arquivo registrando a atividade. Isso é ideal para manter um controle do que foi escaneado e quando.

## 🚀 Como executar o projeto

1. Certifique-se de ter o **Python** instalado no seu computador.
2. Caso o projeto utilize bibliotecas externas para ler o QR Code (como `opencv-python` ou `pyzbar`), instale-as via terminal. Exemplo:
   `pip install opencv-python pyzbar`
3. No terminal, navegue até a pasta do projeto e execute o script principal:
   `python QR_code.py`

## 🛠️ Tecnologias e Conceitos Aplicados
* **Python**: Lógica principal e processamento.
* **Manipulação de Arquivos (`.csv` e `.log`)**: Leitura de base de dados e escrita de registros de histórico.
