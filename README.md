# 🛒 NEWKALA

**NEWKALA** is a full-stack e-commerce website built with **Python, Django, JavaScript, and PostgreSQL**.

The project focuses on building a complete and practical online shopping experience with product management, categories, brands, filtering, search, shopping cart, wishlist, reviews, authentication, AJAX interactions, and location-based data.

The project is developed as a real-world Django application with a modular structure and Docker support.

---

## ✨ Features

### 🛍️ Product Management

* Product listing and details
* Product categories and subcategories
* Brand management
* Product colors
* Product specifications and attributes
* Product galleries
* Product discounts
* Amazing products
* Product search
* Product filtering
* Product sorting
* Pagination

### 👤 User Features

* User authentication
* User profile
* User interactions with products
* Wishlist / Favorites
* Product comments
* Product ratings

### 🛒 Shopping

* Shopping cart
* Product quantity management
* Discount support
* Order management

### ⚡ AJAX Interactions

AJAX is used throughout the project to provide smoother interactions without unnecessary full-page reloads.

Examples include:

* Cart operations
* Product interactions
* Wishlist actions
* Filtering and dynamic requests
* Other asynchronous user interactions

---

## 🛠️ Technologies

### Backend

* Python
* Django
* Django ORM

### Frontend

* HTML5
* CSS3
* JavaScript
* Tailwind CSS
* AJAX

### Database

* PostgreSQL

### DevOps

* Docker
* Docker Compose

### Development Tools

* Git
* GitHub

---

## 🏗️ Project Structure

```text
newkala/
│
├── account_module/
├── contact_us_module/
├── home_module/
├── order_module/
├── polls/
├── product_module/
├── profile_module/
├── settings_site_module/
│
├── new_kala/
│   └── Django project configuration
│
├── data/
│   └── provinces.json
│
├── static/
├── templates/
├── utils/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/Amirmhdp/newkala.git
cd newkala
```

---

## 2. Create Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then configure your environment variables according to your local setup.

> Never commit your `.env` file or sensitive credentials to GitHub.

---

# 🐳 Running with Docker

Make sure **Docker Desktop** is installed and running.

Build and start the containers:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View Django logs:

```bash
docker compose logs -f django
```

The application should then be available at:

```text
http://localhost:8000/
```

---

## 🗃️ Database Migrations

After starting the containers, run:

```bash
docker compose exec django python manage.py migrate
```

To create an admin user:

```bash
docker compose exec django python manage.py createsuperuser
```

---

# 🌱 Seed Data

NEWKALA includes a custom Django management command for generating realistic sample data for development and testing.

The seed command can create sample data such as:

* Users
* Categories
* Subcategories
* Brands
* Colors
* Discounts
* Products
* Product specifications
* Product attributes
* Comments
* Ratings
* Favorites

Run:

```bash
docker compose exec django python manage.py seed_data
```

To clear existing seeded data before generating it again:

```bash
docker compose exec django python manage.py seed_data --clear
```

This makes it easier to quickly prepare the database with sample e-commerce data during development.

---

# 📍 Location Data

The project also includes management commands for importing Iranian province and city data.

## Import Provinces

Province data is loaded from:

```text
data/provinces.json
```

The import command reads the JSON file and creates the corresponding `Province` records.

Run:

```bash
docker compose exec django python manage.py import_provinces
```

---

## Import Cities

The city import command retrieves city data from the configured JSON source and associates each city with its corresponding province.

Run:

```bash
docker compose exec django python manage.py import_cities
```

> Make sure the province data has been imported before importing cities because cities are associated with existing `Province` records.

---

# 🔄 Recommended Setup Order

For a fresh installation, the recommended order is:

```bash
docker compose up -d --build
```

Then:

```bash
docker compose exec django python manage.py migrate
```

Import provinces:

```bash
docker compose exec django python manage.py import_provinces
```

Import cities:

```bash
docker compose exec django python manage.py import_cities
```

Finally, populate the database with sample e-commerce data:

```bash
docker compose exec django python manage.py seed_data
```

Create an admin account if needed:

```bash
docker compose exec django python manage.py createsuperuser
```

---

# 🧹 Useful Docker Commands

### Start containers

```bash
docker compose up -d
```

### Rebuild containers

```bash
docker compose up -d --build
```

### Stop containers

```bash
docker compose down
```

### View logs

```bash
docker compose logs -f django
```

### Open Django shell

```bash
docker compose exec django python manage.py shell
```

### Run migrations

```bash
docker compose exec django python manage.py migrate
```

---

# 📸 Screenshots

Screenshots and visual previews of the project can be added here to demonstrate the main pages and user experience.

Suggested screenshots:

* Home page
* Product listing
* Product detail
* Shopping cart
* User profile
* Wishlist
* Authentication
* Order page
* Admin panel

---

# 🎯 Project Goals

The main goals of NEWKALA are:

* Build a complete Django-based e-commerce application
* Practice real-world Django architecture
* Work with PostgreSQL in a production-oriented project
* Implement dynamic frontend interactions with JavaScript and AJAX
* Build reusable and maintainable Django modules
* Implement product filtering and shopping functionality
* Work with relational data and complex model relationships
* Use Docker for a consistent development environment

---

# 🔮 Future Improvements

Potential future improvements include:

* Online payment gateway
* More advanced order management
* Advanced product recommendation system
* Improved search functionality
* SEO optimization
* Performance optimization
* Automated testing
* Production deployment
* CI/CD pipeline
* Nginx configuration
* REST API
* Advanced admin dashboard

---

# 👨‍💻 Developer

**Amir**

Python & Django Developer

Main technologies:

```text
Python
Django
JavaScript
PostgreSQL
Tailwind CSS
Docker
```

---

# 📄 License

This project is a personal development and portfolio project.

The source code is available for learning, development, and portfolio demonstration purposes.
