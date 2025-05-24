# 🛡️ Gerador de Senhas Seguro - Backend API 

API backend construída com Python e Flask para gerar senhas seguras e personalizáveis. Este projeto foca em práticas de desenvolvimento web seguro, incluindo validação de entradas, proteção contra ataques de DoS (Denial of Service) através de limitação de taxa e configuração de CORS.

## Status do Projeto

* ✅ **Backend:** Funcional e disponível.
* 🚧 **Frontend:** (Em desenvolvimento / A ser desenvolvido)

## Pré-requisitos

* Python 3.8 ou superior
* `pip` (gerenciador de pacotes Python)
* `venv` (para criar ambientes virtuais, altamente recomendado)

## Tecnologias Utilizadas (Backend)

* Python 3.x
* Flask
* Flask-CORS
* Flask-Limiter

## Estrutura de Pastas do Projeto

A organização do projeto segue uma separação clara entre o frontend e o backend:

```plaintext
gerador_senhas/
├── backend/
│   ├── app.py                 # Arquivo principal da aplicação Flask (API backend)
│   ├── requirements.txt       # Lista de dependências Python para o backend
│   └── venv/                  # Pasta do ambiente virtual Python (geralmente ignorada pelo Git)
│
├── frontend/
│   ├── index.html             # Arquivo HTML principal da interface do usuário
│   ├── css/
│   │   └── style.css          # Arquivos de estilização CSS
│   └── js/
│       └── script.js          # Arquivos JavaScript para interatividade do frontend
│
├── .gitignore                 # Especifica arquivos e pastas a serem ignorados pelo Git
└── README.md                  # Este arquivo de documentação
```

**Descrição dos Principais Componentes:**

* **`backend/`**: Contém toda a lógica do lado do servidor.
    * **`app.py`**: O coração da API Flask, onde os endpoints são definidos, a lógica de geração de senha reside, e as configurações de segurança (CORS, Limiter) são aplicadas.
    * **`requirements.txt`**: Define todas as bibliotecas Python que o backend necessita (ex: Flask, Flask-CORS, Flask-Limiter). Permite uma fácil recriação do ambiente com `pip install -r requirements.txt`.
    * **`venv/`**: Pasta do ambiente virtual Python. É criada localmente e contém as dependências instaladas isoladamente para este projeto. Geralmente é incluída no `.gitignore`.

* **`frontend/`**: Contém todos os arquivos relacionados à interface do usuário que roda no navegador.
    * **`index.html`**: A estrutura da página web que o usuário interage.
    * **`css/style.css`**: Define a aparência visual e o layout da página.
    * **`js/script.js`**: Lida com a interatividade do usuário no frontend, como capturar as opções de senha, fazer requisições AJAX para o backend, exibir a senha gerada e mensagens de erro.

* **`.gitignore`**: Um arquivo crucial para controle de versão com Git. Ele especifica quais arquivos e diretórios não devem ser rastreados pelo Git (por exemplo, a pasta `venv/`, arquivos de cache como `__pycache__/`, arquivos de configuração local, etc.).

* **`README.md`**: Fornece informações essenciais sobre o projeto, como configurá-lo, como usá-lo, sua estrutura e outras documentações relevantes.


## Funcionalidades do Backend

* Geração de senhas com comprimento personalizável (entre 8 e 128 caracteres).
* Opção para incluir letras maiúsculas, minúsculas, números e símbolos.
* Validação robusta de todos os parâmetros de entrada no lado do servidor.
* Limitação de taxa (rate limiting) por IP para proteger contra abuso e ataques de DoS.
* Configuração de CORS para permitir acesso de frontends autorizados.
* Utilização do módulo `secrets` do Python para geração de senhas criptograficamente seguras.
* Logs informativos para rastreamento e depuração.


## Como Configurar e Rodar o Backend

1.  **Clone o repositório** (se ainda não o fez):
    ```bash
    git clone https://github.com/levicarlosz/gerador-senhas.git
    cd gerador-senhas/backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    Certifique-se de que o arquivo `backend/requirements.txt` existe e contém:
    ```txt
    Flask
    Flask-Limiter
    Flask-CORS
    ```
    Então, instale com:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor Flask:**
    ```bash
    python app.py
    ```
    O servidor estará rodando por padrão em `http://127.0.0.1:5000` ou `http://0.0.0.0:5000`. Verifique os logs no console para a URL exata.

## Endpoints da API

### Gerar Senha

* **URL:** `/gerar_senha`
* **Método:** `POST`
* **Proteção:** Limitado a 5 requisições por minuto por IP (além dos limites globais).

* **Corpo da Requisição (JSON):**
    ```json
    {
        "comprimento": 16,
        "maiusculas": true,
        "minusculas": true,
        "numeros": true,
        "simbolos": true
    }
    ```
    * `comprimento` (int): Obrigatório, entre 8 e 128.
    * `maiusculas` (boolean): Opcional, default `false`.
    * `minusculas` (boolean): Opcional, default `false`.
    * `numeros` (boolean): Opcional, default `false`.
    * `simbolos` (boolean): Opcional, default `false`.
    (Pelo menos um dos tipos de caractere deve ser `true`).

* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "senha": "SuaSenhaGeradaSegura!123"
    }
    ```

* **Respostas de Erro:**
    * **400 Bad Request** (Erro de validação):
        ```json
        {
            "erro": "Comprimento inválido. Deve ser um número entre 8 e 128."
        }
        ```
        ou
        ```json
        {
            "erro": "Selecione pelo menos um tipo de caractere."
        }
        ```
        ou
        ```json
        {
            "erro": "Corpo da requisição JSON ausente ou inválido."
        }
        ```
    * **429 Too Many Requests** (Limite de taxa excedido):
        O servidor responderá com um status `429` (a mensagem exata pode variar, podendo ser texto simples ou JSON dependendo da configuração do error handler do Flask-Limiter).
    * **500 Internal Server Error** (Erro inesperado no servidor):
        ```json
        {
            "erro": "Ocorreu um erro interno no servidor ao gerar a senha."
        }
        ```

### Status do Servidor

* **URL:** `/`
* **Método:** `GET`
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "mensagem": "Servidor do Gerador de Senhas está no ar!"
    }
    ```

## Considerações de Segurança Implementadas

* **Geração Criptograficamente Segura:** Utiliza o módulo `secrets` do Python para aleatoriedade adequada a senhas.
* **Validação de Entrada Rigorosa:** Assegura que os parâmetros de entrada estejam dentro dos limites esperados.
* **Limitação de Taxa (Rate Limiting):** Protege contra ataques de força bruta e DoS usando `Flask-Limiter`.
* **CORS Configurado:** Permite que apenas origens autorizadas interajam com a API (em produção, deve-se especificar as origens).

## Como Contribuir

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para discutir novas funcionalidades ou reportar bugs. Pull Requests também são apreciados.

1.  Faça um Fork do projeto.
2.  Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`).
3.  Faça commit de suas alterações (`git commit -m 'Adiciona NovaFeature'`).
4.  Faça push para a branch (`git push origin feature/NovaFeature`).
5.  Abra um Pull Request.
---