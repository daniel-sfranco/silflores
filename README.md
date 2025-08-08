# Projeto Silflores

Bem-vindo ao repositório do projeto **Silflores**.

## Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Linguagens**: Python, JavaScript, HTML, CSS
- **Framework**: Django
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis
- **Containerização**: Docker
- **Frontend Tooling**: Vite.js

## Executando o Projeto Localmente

Para executar o projeto localmente, siga os passos abaixo:

1.  Certifique-se de que o Docker está instalado na sua máquina.
2.  No terminal, navegue até o diretório raiz do projeto.
3.  Execute o comando abaixo para iniciar os serviços de backend:

    ```bash
    docker-compose up --build
    ```

    Este comando iniciará o ambiente local do projeto. Caso esteja executando o comando pela primeira vez, o comando irá fazer o pull dos contâineres do Psql e do Redis, além de fazer a build do próprio contâiner do projeto, portanto pode levar alguns minutos para a sua execução.

### Reiniciando o Projeto

Após a configuração inicial, para rodar novamente o projeto, basta executar o comando:

```bash
docker-compose up
```

Em alguns segundos o servidor estará iniciado, e poderá ser acessado no localhost, na porta 8000.

## Desenvolvimento Frontend com Vite

Para o desenvolvimento frontend, utilizamos o Vite.js para um pipeline de assets moderno e rápido. Você precisará ter o Node.js e o npm (ou yarn/pnpm) instalados em sua máquina.

### Instalação das Dependências do Frontend

Na raiz do projeto, instale as dependências do Node.js:

```bash
npm install
```

### Modo de Desenvolvimento (com Hot Module Replacement - HMR)

Para desenvolver o frontend com HMR (atualizações instantâneas no navegador sem recarregar a página), você precisará rodar o servidor de desenvolvimento do Vite em paralelo com o servidor Django.

Abra **dois terminais** na raiz do projeto:

1.  **Terminal 1 (Servidor Django):**
    ```bash
    source venv/bin/activate
    python silfloresapp/manage.py runserver
    ```

2.  **Terminal 2 (Servidor Vite):**
    ```bash
    npm run dev
    ```

    O servidor Vite será iniciado e observará as mudanças nos seus arquivos `silfloresapp/static/src/`. As alterações serão refletidas automaticamente no navegador.

### Build para Produção

Antes de fazer o deploy ou para gerar os arquivos estáticos otimizados para produção, você precisa rodar o build do Vite. Isso criará os arquivos minificados e com hash na pasta `silfloresapp/static/dist/`.

```bash
npm run build
```

Após o build do Vite, você deve coletar os arquivos estáticos do Django:

```bash
source venv/bin/activate
python silfloresapp/manage.py collectstatic
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob os termos da [licença MIT](LICENSE).
