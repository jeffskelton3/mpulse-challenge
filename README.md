### Requirements

- docker
- docker-compose

### Starting the application

open a terminal at the root of the project and run `docker-compose up`. Everything will get handled in that one command including spinning up the server.

After the boot sequence completes visit `http://localhost:8000/docs` you should see a swagger ui interface and all the available endpoints.

### Notable technology choices

Full disclosure: Richie recommended fast api and kafka. I am glad he did. They're great.

- [FastAPI](https://fastapi.tiangolo.com/)
- [postgres](https://www.postgresql.org/) + [sqlalchemy](https://www.sqlalchemy.org/)
- [kafka](https://kafka.apache.org/) + [aiokafka](https://aiokafka.readthedocs.io/en/stable/index.html#)
- [docker](https://www.docker.com/)

I also set up quality of life things like pydantic and black. I found poetry for package management which was close enough to tech I am familiar with like npm and maven to be useful.
