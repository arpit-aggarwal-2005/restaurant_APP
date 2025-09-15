# 🍽️ Restaurant App

A Flask-based backend api for  restaurant management and recommendation system with **JWT authentication**, **MySQL integration**, and personalized menu handling.  
This project manages customers, menus, and orders while supporting secure authentication and future recommendation features.

---

## 🚀 Features
- 🔑 Customer Authentication with JWT (JSON Web Tokens)  
- 🗂️ CRUD operations for customers and menus  
- 📋 Menu system with cuisine types (`title` → e.g., Italian, Indian, Chinese)  
- 📦 Order management (extendable)  
- 🔒 Secure MySQL database integration  
- 🌐 REST API structure (ready for frontend integration)  

---

## 🛠️ Tech Stack
- **Backend**: Python (Flask)  
- **Database**: MySQL (`restaurant_db`)  
- **Authentication**: JWT  
 

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/arpit_aggarwal_2005/restaurant_app.git
cd restaurant_app
```

### 2. Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### 3. Configure MySQL
- Create database:
```sql
CREATE DATABASE restaurant_db;
```
- Update your DB credentials in `config.py` (or `.env` file if you use one).

### 4. Run the app
```bash
run this start_env.ps1
```

App will run at 👉 `http://127.0.0.1:5000/`

---

## 📌 API Endpoints (Examples)

### 🔑 Authentication
- `POST /login` → JWT login for customers  

### 👤 Customers
- `POST /customers` → Create new customer  
- `GET /customers/<id>` → Get customer details  
- `PUT /customers/<id>` → Update customer  
- `DELETE /customers/<id>` → Delete customer  

### 🍴 Menus
- `POST /menus` → Add new menu  
- `GET /menus` → Get all menus  
- `PUT /menus/<id>` → Update menu  
- `DELETE /menus/<id>` → Remove menu  

---

## 🧾 Folder Structure
```
restaurant_app/
│── app.py                # Main Flask app
│── customer_model.py     # Customer model + CRUD
│── menu_model.py         # Menu model + CRUD
│── controllers/          # Route controllers
│── static/               # Static files (CSS, JS)
│── templates/            # HTML templates (if any)
│── requirements.txt      # Dependencies
│── config.py             # DB and app configuration
```

---

## 🚀 Future Improvements
- ✅ Personalized menu recommendations  
- ✅ Order system integration  
- ✅ Admin panel for restaurant owners  
- ✅ Deployment on cloud (Heroku/Render/Docker)  

---

## 🤝 Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to improve.

---

