# unlucky-strike

A tech blog project built with Django

## About The Project

Developers grow up struggling with various problems. This project aims to write a narrative about the process of solving these difficulties and learning through them.

Here's why:
* To test and apply various new technologies
* For constant growth
* To share my knowledge

### Features

- **Blog App**: Post articles, categorize content, and manage blog entries with Django models and templates.
- **Gallery App**: Upload and display photos, with forms for photo management.
- **Home App**: Static pages like About, Contact, and Home index.
- **Projects App**: Showcase projects, including ETF tracking, exchange rates, and technical demos (e.g., Raspberry Pi, image processing).
- **Database Backup**: Automated scripts for backing up SQLite database.
- **Containerized Deployment**: Docker and Docker Compose for easy development and production setup.
- **Web Server Integration**: nginx for static file serving and reverse proxy, uWSGI for application serving.
- **SSL Support**: Let's Encrypt integration for secure HTTPS.

### Built With

* Django
* SQLite
* Nginx
* Docker
* Bootstrap

## Architecture

The project follows a standard Django web application architecture, containerized with Docker for portability. The system is designed for scalability and ease of deployment.

### System Architecture Diagram

```mermaid
graph TD;
    A[Client (Browser)] --> B[nginx (Web Server)];
    B --> C[uWSGI (Application Server)];
    C --> D[Django Application];
    D --> E[SQLite Database];
    D --> F[Static Files (CSS/JS/Images)];
    D --> G[Templates (HTML)];
    
    subgraph "Docker Containers"
        B
        C
        D
    end
    
    subgraph "Host System"
        E
        F
        G
    end

