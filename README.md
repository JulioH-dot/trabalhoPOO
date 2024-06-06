# Projeto de Agendamento de Laboratórios

Este projeto é uma aplicação web para agendar horários em laboratórios de uma instituição educacional. Ele permite que professores e funcionários reservem horários específicos em laboratórios disponíveis para diversas atividades, como aulas práticas, pesquisas e workshops.

## Funcionalidades Principais

- Login de usuários: Professores e funcionários podem fazer login em suas contas para acessar o sistema.
- Agendamento de Laboratórios: Usuários autenticados podem agendar horários em laboratórios disponíveis.
- Visualização de Agendamentos: Os usuários podem visualizar seus próprios agendamentos e os horários disponíveis nos laboratórios.
- Cadastro de Usuários: Novos usuários podem se cadastrar no sistema.

## Tecnologias Utilizadas

- **Frontend:** HTML, CSS, JavaScript (utilizando o framework Vue.js)
- **Backend:** Python (utilizando o framework Flask)
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JSON Web Tokens (JWT)
- **Integração Frontend-Backend:** Requisições HTTP (fetch API)
- **Segurança:** CORS (Cross-Origin Resource Sharing)
- **Controle de Versão:** Git e GitHub

## Configuração do Ambiente de Desenvolvimento

1. Clone este repositório: `git clone https://github.com/seu-usuario/nome-do-repositorio.git`
2. Instale as dependências do frontend: `cd frontend && npm install`
3. Instale as dependências do backend: `cd backend && pip install -r requirements.txt`
4. Configure o banco de dados PostgreSQL e atualize as informações de conexão no arquivo `config.py`.
5. Inicie o servidor Flask: `flask run`
6. Inicie o servidor de desenvolvimento do frontend: `npm run serve`

## Estrutura de Pastas

- **frontend:** Contém os arquivos do frontend da aplicação, incluindo HTML, CSS, JavaScript e assets.
- **backend:** Contém os arquivos do backend da aplicação, incluindo código Python, configurações e o arquivo requirements.txt.
- **docs:** Documentação do projeto, incluindo este arquivo README.md.

## Contribuição

Contribuições são bem-vindas! Para sugestões, melhorias ou correções, por favor abra uma issue ou envie um pull request.

---

Esse README.md é um exemplo básico e pode ser adaptado conforme necessário para seu projeto específico. Certifique-se de incluir informações relevantes sobre o projeto, como instruções de instalação, uso e contribuição, além de detalhes sobre tecnologias utilizadas e estrutura de pastas.
