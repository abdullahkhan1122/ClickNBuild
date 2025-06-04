# 🏗️ ClickNBuild

**ClickNBuild** is a construction project bidding platform built with **Flask**, **HTML**, **CSS**, and **Python**. It connects clients looking for construction services with builders who can bid on their projects. The platform also includes a material price marketplace to help clients make informed bidding decisions.

---

## 📌 Features

- 📝 **Post Projects** – Clients can create and post construction project listings.
- 💰 **Bid on Projects** – Builders submit bids with pricing and estimated timelines.
- ✔️ **Accept Bids** – Clients choose the best bid and initiate work with the builder.
- 🛠️ **Project Workflow** – Builders mark projects as complete, and clients confirm with payment.
- 🌟 **Mutual Reviews** – Both builders and clients can review each other after project completion.
- 🛒 **Material Marketplace** – Shows current prices of construction materials.
- 🧑‍💼 **User Profiles** – Clients and builders can update their profile information.
- 🔍 **Builder Reviews** – Clients can choose builders based on past reviews and ratings.

---

## 🛠️ Built With

- **Backend**: [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/)
- **Frontend**: HTML5, CSS3
- **Database**: *(Specify the database used – SQLite, PostgreSQL, etc.)*
- *(Optional)* **Authentication**: Flask-Login or custom auth logic


---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv *(recommended)*

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ClickNBuild.git
cd ClickNBuild

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run

```
## 🛠️ Database Setup (MySQL)

You can import the entire database (tables + sample data) using :
NOTE : the database must be in the project directory or at the place where you are making your database.
```bash
mysql -u root -p -e "CREATE DATABASE ClickNBuild; USE ClickNBuild; SOURCE ClickNBuild.sql;"
