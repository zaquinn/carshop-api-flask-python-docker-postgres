# carshop-api-flask-python-docker-postgres

Este projeto é uma API em Flask + Python + Postgres + Docker que visa gerenciar um CRUD de pessoas e carros. A documentação da aplicação pode ser obtida ao rodá-la, no endereço de desenvolvimento: http://localhost:5000/

Stacks utilizadas:

<ul>
<li>Flask</li>
<li>Flask JWT Extended</li>
<li>Flask Migrate</li>
<li>Flask Rest X</li>
<li>Flask SQL Alchemy</li>
<li>Postgres</li>
<li>Docker && Docker Compose</li>
</ul>

## Instruções para rodar em servidor local

Clone o repositório do projeto

```
git clone https://github.com/zaquinn/carshop-api-flask-python-docker-postgres.git
```

Entre na pasta do projeto e crie o ambiente virtual

```
$ cd https://github.com/zaquinn/carshop-api-flask-python-docker-postgres.git

$ python -m venv venv
```

Ative o ambiente virtual

```
$ source venv/bin/activate #Linux
```

Instale os requerimentos

```
$ pip install -r requirements.txt
```

Em seguida, inicie o processo de aplicação das migrations e criação das tabelas com:

```
flask db init
```

Gere a primeira migration com:

```
flask db migrate -m "Initial migration."
```

Aplique-as ao banco de dados com:

```
flask db upgrade
```

Rode a aplicação com:

```
python runserver.py
```

Acesse-a em seu localhost no endereço:

```
http://localhost:5000/
```

---

## Instruções para rodar a aplicação pelo Docker

Clone o repositório do projeto

```
git clone https://github.com/zaquinn/carshop-api-flask-python-docker-postgres.git
```

Entre na pasta do projeto e crie o ambiente virtual

```
$ cd https://github.com/zaquinn/carshop-api-flask-python-docker-postgres.git

$ python -m venv venv
```

Ative o ambiente virtual

```
$ source venv/bin/activate #Linux
```

Dentro do projeto, em seu terminal rode:

```
docker compose up --build
```

Em seguida, inicie o processo de aplicação das migrations e criação das tabelas com:

```
flask db init
```

Gere a primeira migration com:

```
flask db migrate -m "Initial migration."
```

Aplique-as ao banco de dados com:

```
flask db upgrade
```

Rode a aplicação com:

```
python runserver.py
```

Acesse-a em seu localhost no endereço:

```
http://localhost:5000/
```
