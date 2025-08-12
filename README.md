# DevOps Project Implementation

This repository contains a DevOps pipeline implementation following the requirements specified in the DevOps Task document. The project demonstrates containerization, CI/CD, monitoring, and logging capabilities.

## Project Structure

```
my-devops-project/
├── app/                    # Application source code directory
├── grafana/                # Grafana configuration directory
├── logstash/               # Logstash configuration directory
├── prometheus/             # Prometheus configuration directory
├── tests/                  # Test cases directory
├── .env                    # Environment variables (68 bytes)
├── .gitlab-ci.yml          # CI/CD pipeline configuration (1 KB)
├── docker-compose.yml      # Docker services orchestration (4 KB)
└── README.md               # This documentation
```

## Getting Started

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/devops-project.git
   cd devops-project
   ```

2. Create your environment file:
   ```bash
   cp .env.example .env
   ```

3. Start the services:
   ```bash
   docker-compose up -d --build
   ```

4. Verify all services are running:
   ```bash
   docker-compose ps
   ```

## Service Access Information

### Main Application
- **URL**: http://localhost:5000
- **Endpoints**:
  - `GET /health` - Health check endpoint
  - `GET /data` - Sample data endpoint

### Monitoring Stack
| Service | Port | Access URL |
|---------|------|------------|
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3000 | http://localhost:3000 |

### Logging Stack
| Service | Port | Access URL |
|---------|------|------------|
| Kibana | 5601 | http://localhost:5601 |
| Elasticsearch | 9200 | http://localhost:9200 |
| Logstash | 5044 | Internal service |

### Database
- **PostgreSQL**
  - Host: `postgres` (within Docker network)
  - Port: 5432
  - Username/Password: Defined in `.env` file
  - Database: `devops_db`

## Environment Configuration

The `.env` file (68 bytes) contains environment variables for the application. This file is not committed to version control for security reasons. A sample `.env.example` file should be provided with placeholder values.

Example content:
```
# Application Configuration
FLASK_ENV=production
PORT=5000

# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_NAME=devops_db
DB_USER=devops_user
DB_PASSWORD=devops_password

# Monitoring Configuration
PROMETHEUS_URL=http://prometheus:9090
```

## CI/CD Pipeline

The `.gitlab-ci.yml` file (1 KB) implements a basic CI/CD pipeline with the following stages:
- Build: Docker image creation
- Test: Basic validation tests
- Deploy: Deployment using docker-compose

To trigger the pipeline:
1. Commit and push changes to the repository
2. View pipeline status in GitLab's CI/CD section

## Important Notes

1. **Credentials**: All sensitive information is stored in the `.env` file which is not committed to version control. You must create your own `.env` file with appropriate values.

2. **Grafana Default Credentials**: 
   - Username: `admin`
   - Password: `admin` (you'll be prompted to change this on first login)

3. **Project Limitations**:
   - The actual implementation details of the application code, monitoring dashboards, and logging configuration cannot be verified from the repository structure alone
   - You'll need to examine the contents of each directory for specific implementation details

## Verification

To verify the project meets the DevOps Task requirements:

1. Check that all required directories exist (app/, grafana/, logstash/, prometheus/)
2. Confirm the presence of required files (.env, .gitlab-ci.yml, docker-compose.yml)
3. Validate that the application has at least two endpoints (/health and /data)
4. Ensure Prometheus is configured to scrape application metrics
5. Verify Grafana has at least one working dashboard
6. Confirm logs are being processed through the ELK stack

## Troubleshooting

If services fail to start:
1. Check logs with `docker-compose logs [service-name]`
2. Verify your `.env` file has correct values
3. Ensure all required ports are available on your system

## Contributing

Contributions are welcome. Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request