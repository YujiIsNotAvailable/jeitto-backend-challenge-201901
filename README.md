# Desafio Backend do Jeitto

## Pré-requisitos
- Python3
- MySQL

## Rodar o projeto
__Testes__
```sh
  python -m pytest .
```

__Sem docker__
```sh
  pip install -r ./requirements.txt
  python ./server.py
```

__Com Docker__
```sh
  docker build . -t jeitto-backend-challenge
  docker run -p5000:5000 jeitto-backend-challenge
```

## Perguntas que devem ser respondidas
- Quais foram os principais desafios durante o desenvolvimento?
  - Obter conhecimentos detalhados sobre a linguagem, e as tecnologias que a envolve.
- O que você escolheu como arquitetura/framework/banco e por que?
  - aiohttp (web) Framework simples para utilizar, de fácil implementação e boa documentação.
  - mysql (db) Familiaridade com o sgdb, com modelos/estruturas bem definidas. 
- O que falta desenvolver / como poderiamos melhorar o que você entregou?
  [ ] Melhoria em validações
  [ ] Automatização do deploy

- Python é a melhor escolha para esta atividade? Por que?
  - Sim. Uma linguagem facil de desenvolver, de alto nível, e principalmente alta performance.