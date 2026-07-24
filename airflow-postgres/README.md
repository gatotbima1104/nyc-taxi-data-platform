# NYC Taxi Data Platform

This project is an end-to-end data engineering pipeline for the NYC Yellow Taxi dataset. It demonstrates a Medallion Architecture using Python, PostgreSQL, dbt, Apache Airflow, and Docker.

The pipeline performs data extraction, validation, loading, transformation, quality checks, and documentation generation.

---

# Features

- Extract NYC Yellow Taxi datasets
- Validate downloaded files
- Load raw data into PostgreSQL (Bronze)
- Transform data using dbt (Staging, Silver, Gold)
- Perform data quality checks
- Export cleaned Silver data to Parquet
- Generate dbt documentation
- Orchestrate the pipeline with Apache Airflow

---

# Tech Stack

- Python
- PostgreSQL
- dbt
- Apache Airflow 3
- Docker & Docker Compose
- Pandas
- PyArrow

---

# Project Structure

```text
nyc-taxi-data-platform/
│
├── airflow-postgres/
│   ├── airflow/
│   ├── data/
│   ├── dbt_project/
│   ├── scripts/
│   ├── sql/
│   ├── utils/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
├── LICENSE
└── README.md
```

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/gatotbima1104/nyc-taxi-data-platform.git

cd nyc-taxi-data-platform/airflow-postgres
```

---

## Prerequisites

Install the following software:

- Docker Desktop (or Docker Engine)
- Docker Compose
- Git

Check the installation:

```bash
docker --version
docker compose version
git --version
```

---

## Configuration

Copy the example environment file.

```bash
cp .env.example .env
```

The `.env` file contains:

- PostgreSQL configuration
- Airflow configuration
- Docker environment variables
- Pipeline configuration

Fill this values
```bash
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

---

## Start the Project

Build and start all containers.

```bash
docker compose up airflow-init -d
```

```bash
docker compose up -d
```

The first build may take a few minutes.

---

# Airflow

Open Airflow in your browser.

```
http://localhost:8080
```

Default login:

| Username | Password |
|----------|----------|
| airflow | airflow |

---

# Running the Pipeline

Enable the DAG named **taxi_pipeline**.

Click **Trigger DAG**.

The pipeline runs the following steps:

```text
Validate Database
        │
        ▼
Extract Files
        │
        ▼
Validate Files
        │
        ▼
Load Bronze
        │
        ▼
Validate Bronze
        │
        ▼
dbt Build
        │
        ▼
Export Silver Dataset
        │
        ▼
Validate Silver
        │
        ▼
Validate Gold
        │
        ▼
Generate dbt Documentation
```

---

# Database Layers

## Bronze

Stores the raw datasets loaded into PostgreSQL.

Tables:

- bronze.raw_taxi_trips
- bronze.raw_taxi_lookup

---

## Silver

Contains cleaned and transformed data.

Some transformations include:

- Data type conversion
- Lookup joins
- Derived columns
- Data cleaning

Tables:

- silver.fact_taxi_trips
- silver.dim_taxi_zone
- silver.data_quality_issues

The Silver dataset is also exported to:

```text
data/processed/processed_taxi_trips.parquet
```

---

## Gold

Contains business-ready tables for analytics and reporting.

Examples:

- Daily Summary
- Hourly Demand
- Zone Performance
- Payment Behavior
- Route Performance

---

# Data Quality Checks

The pipeline validates data during execution.

### File Validation

- File exists
- File is not empty
- Required columns exist

### Bronze Validation

- Table exists
- Row count is greater than zero
- Required columns are not NULL
- Numeric values are not negative

### Silver Validation

- Table exists
- Row count is greater than zero
- Required columns are not NULL
- Numeric values are not negative

### Gold Validation

- Gold tables exist
- Gold tables contain data

---

# Output

Raw files:

```text
data/raw/
```

Processed files:

```text
data/processed/
```

Generated documentation:

```text
dbt_project/taxi_dbt/target/
```

---

# dbt Documentation

The pipeline automatically runs
Open:

```
http://localhost:8081
```

---

# Available Services

| Service | URL |
|----------|-----|
| Airflow | http://localhost:8080 |
| PostgreSQL | localhost:5433 |
| dbt Docs | http://localhost:8081 (optional) |

---

# Future Improvements

- Incremental dbt models
- CI/CD pipeline
- Data freshness monitoring
- Cloud deployment
- Great Expectations integration

---