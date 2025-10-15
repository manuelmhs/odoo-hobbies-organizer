# Hobbies Organizer

This is a **custom Odoo 19 application** developed as a learning project.\
It involves topics like setting up a new Odoo's app, using some of Odoo's ORM features, models, XML views, actions and menus, permissions, data seeding, configuring a Docker/Odoo environment.

## Description
The idea of this project was to learn Odoo developing a minimal application module example, using a simple base concept, involving all Odoo's fundamentals.

**The module allows the user to:**

- Register hobbies, categories and people.

- Manage a schedule for each person-hobby relationship.

- Visualization and CRUD in different views (list, form, calendar) and support for custom filters and groupings.

**Technical features involved like:**

- Basic module's architecture and manifest.

- Definition of custom models and extension of Odoo's core ones.

- Odoo's environment, context, domain.

- Usage of Odoo's ORM: fields, api decorators, constrains, ordering, groups, relationships.

- XML views, menus, window and server actions.

- Security rules.

- Basic and demo data seeding for module installation.

- Easy to use Docker/Docker Compose setup for development in Odoo 19 and PostgreSQL 15.

## Requirements
- Linux (tested on Ubuntu x86-64)
- Docker (28.4.0) and Docker Compose (2.39.4)

Alternatively, you can install and setup Odoo 19 manually, handling Python and Postgres dependencies.

## Usage

Clone the [repository](https://github.com/manuelmhs/odoo-hobbies-organizer.git) and enter the directory.\
Within the root folder using bash:
- ```sudo docker compose up -d``` to create and run the docker containers for postgres 15 and odoo 19 (it will download both images if needed)
- To initialize the Odoo database in Postgres and install the Hobbies Organizer module:
  - ```sudo docker compose exec web odoo -d hobbies_db -i hobbies_organizer --with-demo --stop-after-init``` to initialize the database **with** demo data
  - ```sudo docker compose exec web odoo -d hobbies_db -i hobbies_organizer --stop-after-init``` to initialize the database **without** demo data
- Enter **localhost:8069** to use the Odoo web client. Default user credentials are admin, admin