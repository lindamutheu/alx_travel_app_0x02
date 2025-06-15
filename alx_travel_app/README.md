# ALX Travel App 0x00

## 📌 Objective

This project focuses on database modeling and data seeding in Django. The main goals are to define models, create serializers, and populate the database with sample data using a custom management command.

---

## 🛠️ Tasks Completed

### 1. 🔁 Duplicate Project

- Cloned the original `alx_travel_app` repository to a new project named `alx_travel_app_0x00`.

---

### 2. 🗃️ Models

- Defined the following models in `listings/models.py`:
  - `Listing`
  - `Booking`
  - `Review`

Each model includes appropriate:
- Fields (e.g., name, date, rating)
- Relationships (e.g., ForeignKey, OneToMany)
- Constraints (e.g., non-null, unique)

---

### 3. 🔄 Serializers

- Created serializers in `listings/serializers.py` for:
  - `Listing`
  - `Booking`

These serializers convert model instances to JSON for API
