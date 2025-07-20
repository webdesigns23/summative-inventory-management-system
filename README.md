## Inventory Management System
This system will allow employees to add, edit, view, and delete inventory items. Additionally, the system will fetch real-time product data from an external API (OpenFoodFacts API) to supplement additional product details.

## Features
- View products in inventory
- Add new products
- Edit product stock level
- Delete a product from inventory
- View additional details about product from OpenFoodFacts API

## Setup Instructions
1. Clone the Repository
git clone <repo-url>
cd course-8-module-6-connect-client-server-lab
2. Create Your Environment
Using Pipenv:
pipenv install
pipenv shell

## Running the App
python server.py
Then open client/index.html in your browser to view the frontend.

## Running the Tests
To check your work, run:
pytest