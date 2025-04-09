# demo_dbt_airflow

A Docker-based setup integrating Apache Airflow, DBT (Data Build Tool), and PostgreSQL for managing data pipelines and transformations. This project serves as a demo environment for ETL processes, orchestration, and data modeling.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Docker**: Download and install from [docker.com](https://www.docker.com/get-started).
- **Docker Compose**: Included with Docker Desktop on Windows.
- **Git**: Install from [git-scm.com](https://git-scm.com/downloads) to clone the repository.
- **pgAdmin** (optional): For visualizing the PostgreSQL database. Get it from [pgadmin.org](https://www.pgadmin.org/).

---

## Project Structure

```
demo_dbt_airflow/
├── airbyte/              # (Optional) Airbyte configuration (if used)
├── dags/                 # Airflow Directed Acyclic Graphs (DAGs)
├── dbt_debug.log         # DBT debug log file
├── dbt_project/          # DBT project files (models, profiles.yml, etc.)
├── docker-compose.yml    # Docker Compose configuration
├── logs/                 # Log files (ignored by Git)
├── scripts/              # Custom scripts (if any)
├── .gitignore            # Git ignore file
├── .gitattributes        # Git attributes for line endings
└── README.md             # This file
```

---

## Setup Instructions

### 1. Clone the Repository
Clone the repository and initialize submodules (if any):
```bash
git clone https://github.com/Steevaeen/demo_dbt_airflow.git
cd demo_dbt_airflow
git submodule update --init --recursive
```

### 2. Configure the Environment
- Ensure your `docker-compose.yml` includes the following services. Edit as needed:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres
    container_name: demo_dbt_airflow-postgres-1
    environment:
      - POSTGRES_USER=steev
      - POSTGRES_PASSWORD=Sugukumar@0101
      - POSTGRES_DB=mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
  airflow-webserver:
    image: apache/airflow:2.5.0
    container_name: demo_dbt_airflow-airflow-webserver-1
    depends_on:
      - postgres
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://steev:Sugukumar@0101@postgres:5432/mydb
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
  airflow-scheduler:
    image: apache/airflow:2.5.0
    container_name: demo_dbt_airflow-airflow-scheduler-1
    depends_on:
      - postgres
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://steev:Sugukumar@0101@postgres:5432/mydb
    volumes:
      - ./dags:/opt/airflow/dags
  dbt:
    image: ghcr.io/dbt-labs/dbt-postgres:1.5.0
    container_name: demo_dbt_airflow-dbt-1
    depends_on:
      - postgres
    volumes:
      - ./dbt_project:/dbt
    entrypoint: dbt
    command: run --profiles-dir /dbt --project-dir /dbt
volumes:
  pgdata:
```

- **DBT Configuration**: Create or update `dbt_project/profiles.yml`:
```yaml
demo_dbt_airflow:
  target: dev
  outputs:
    dev:
      type: postgres
      host: postgres
      user: steev
      pass: Sugukumar@0101
      port: 5432
      dbname: mydb
      schema: public
```

### 3. Start the Services
Launch all services in detached mode:
```bash
docker-compose up -d
```

### 4. Initialize Airflow (First Time Only)
Run the Airflow initialization:
```bash
docker-compose up airflow-init
```

### 5. Verify Containers
Check that all containers are running:
```bash
docker ps
```
- Expected containers: `demo_dbt_airflow-postgres-1`, `demo_dbt_airflow-airflow-webserver-1`, `demo_dbt_airflow-airflow-scheduler-1`, `demo_dbt_airflow-dbt-1`.

---

## Usage

### Access Services
- **PostgreSQL**: Connect via pgAdmin:
  - Host: `localhost`
  - Port: `5432`
  - Database: `mydb`
  - Username: `steev`
  - Password: ``
- **Airflow Webserver**: Open `http://localhost:8080` (default username: `airflow`, password: `airflow`—change it in the UI).
- **DBT**: Run DBT commands inside the `dbt` container:
  ```bash
  docker exec -it demo_dbt_airflow-dbt-1 dbt run
  ```

### Add Sample Data
Create a sample table in PostgreSQL:
```sql
CREATE TABLE public.final_sales (sale_date DATE, total_sales NUMERIC, unique_customers INTEGER);
INSERT INTO public.final_sales (sale_date, total_sales, unique_customers) VALUES 
('2025-04-01', 100.50, 1), ('2025-04-02', 200.75, 1), ('2025-04-03', 150.25, 1);
```
Verify in pgAdmin or with:
```bash
docker exec demo_dbt_airflow-postgres-1 psql -U steev -d mydb -c "SELECT * FROM public.final_sales LIMIT 5;"
```

---

## Troubleshooting

- **Git Issues**:
  - Ensure `.gitignore` excludes `logs/`, `target/`, and `.env`. Move or delete `logs/` if indexing fails (e.g., `move logs logs_backup`).
  - Use `.gitattributes` for consistent line endings.
- **Container Conflicts**:
  - Remove old containers with `docker rm <container_id>` and re-run `docker-compose up -d`.
- **Authentication Issues**:
  - Verify `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` in `docker-compose.yml` match your setup.
- **Logs**:
  - Check container logs with `docker logs <container_name>` for errors.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-branch`.
3. Commit changes: `git commit -m "Describe your changes"`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a Pull Request on GitHub.

---

## License

[MIT License] (or specify your preferred license). Add a `LICENSE` file if needed.
