# Projeto Silflores

Bem-vindo ao repositório do projeto **Silflores**.

## Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Linguagens**: Python, JavaScript, HTML, CSS
- **Framework**: Django
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis
- **Containerização**: Docker

## Executando o Projeto Localmente

Para executar o projeto localmente, siga os passos abaixo:

1. Certifique-se de que o Docker está instalado na sua máquina.
2. No terminal, navegue até o diretório raiz do projeto.
3. Execute o comando abaixo:

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

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob os termos da [licença MIT](LICENSE).