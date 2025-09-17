
# Catalog Project

[Project GitHub Link](https://github.com/HamzaKiziltoprak/catalog-project)

This project is a Django-based product catalog and order management system. It features media management with Cloudinary, PostgreSQL/SQLite support, and easy deployment with Docker.

## Features
- Product catalog management
- Order creation and tracking
- Admin panel
- Media file management with Cloudinary
- Easy deployment with Docker

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/HamzaKiziltoprak/catalog-project.git
```

### 2. Activate the Virtual Environment
```bash
.\env\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
cd src
python manage.py migrate
```

### 5. Start the Server
```bash
python manage.py runserver
```

## Configuration

### Environment Variables
Project settings are managed using a `.env` file. Example:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

### Cloudinary
To manage media files with Cloudinary, create a [Cloudinary account](https://cloudinary.com/) and add your API credentials to the `.env` file.

### Docker
To run the project with Docker:
```bash
docker build -t catalog-project .
docker run -p 8000:8000 catalog-project
```

## Directory Structure
- `src/` : Django project and app files
- `env/` : Python virtual environment
- `requirements.txt` : Required Python packages
- `Dockerfile` : Docker configuration

## License
MIT License
