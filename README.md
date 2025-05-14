## 🛠️ Admin Panel (Admin Branch)

The **Admin Panel** of PawPromise is a dedicated interface for managing and moderating all aspects of the platform, including users, organizations, pets, events, fundraisers, and analytics. It is separated from the main user application for security and modularity.

📌 **Note:** The Main project Source code is in  `master` branch.

🔗 [Go to master Branch](https://github.com/kalp26/PawPromise-eAdoption/tree/master)

---

## 📁 Folder Structure

The admin-side project is organized as follows:

```plaintext
admin/
│
├── .idea/                       # IDE configurations
├── .venv/                       # Virtual environment
├── static/                      # Static assets (CSS, JS, etc.)
├── templates/                   # HTML templates for admin views
│   ├── dashboard.html           # Admin dashboard (overview of platform metrics)
│   ├── fundraiser-detail.html   # Detailed view of a specific fundraiser
│   ├── fundraiser-Listings.html # List of all fundraisers
│   ├── meetup-detail.html       # Details of specific pet meetup events
│   ├── message.html             # Contact or query messages from users
│   ├── nav.html                 # Navigation bar shared across admin pages
│   ├── organization.html        # View and manage registered organizations
│   ├── pending_org.html         # List and verify pending organization accounts
│   ├── pet-detail.html          # Details of a listed pet
│   ├── pet-meetups.html         # Overview of all pet meetup requests
│   ├── pet-selling.html         # Section for managing selling requests
│   ├── pet-statistics.html      # View pet-related statistics (adopted, pending, etc.)
│   ├── pets.html                # Master list of pets on the platform
│   ├── user.html                # Manage user accounts
│   ├── verified_org.html        # Verified organization accounts
├── app.py                       # Main admin Flask application
```
# 🧩 Admin Features

✅ **Dashboard Overview**: Platform metrics like active users, adoptions, and fundraisers.

🐾 **Pet Management**: Approve, reject, or remove pet listings.

🏥 **Organization Verification**: Manage pending and verified organizations.

💌 **Contact Messages**: View and respond to user-submitted messages.

🧑‍🤝‍🧑 **User Controls**: View, delete, or verify user accounts.

💸 **Fundraiser Oversight**: View detailed fundraiser data and manage listings.

📅 **Event Moderation**: Approve or decline meetup events created by users/organizations.

📊 **Analytics Section**: Visual pet statistics for better platform monitoring.

This admin panel ensures that only valid users and organizations operate on PawPromise, while enabling streamlined moderation of adoptions, events, and donations.

## 🗄️ Database Setup

SQL files are available for database initialization:

- [schema.sql](https://github.com/kalp26/PawPromise-eAdoption/blob/admin/pawpromise_without_data.sql) - Empty database structure


Use the empty schema for production environments and the populated schema for development and testing purposes.
