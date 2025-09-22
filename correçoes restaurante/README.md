# Sistema de Reservas - Restaurante Porto Belo

Este projeto é um sistema web simples para gerenciamento de reservas do Restaurante Porto Belo, desenvolvido em Python com Flask.

## Funcionalidades

- Formulário para reservas online
- Validação de dados e horários disponíveis (intervalo mínimo de 30 minutos)
- Armazenamento das reservas em arquivo JSON
- Integração para confirmação via WhatsApp

## Requisitos

- Python 3.8+
- Flask

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd "correçoes restaurante/porto-belo-restaurante"
   ```
3. Instale as dependências:
   ```bash
   pip install flask
   ```

## Como usar

1. Execute o servidor Flask:
   ```bash
   python app.py
   ```
2. Acesse `http://localhost:5000` no navegador.

## Estrutura

- `app.py`: Código principal da aplicação Flask
- `reservas.json`: Arquivo onde as reservas são salvas
- `templates/`: Páginas HTML

## Licença

MIT
