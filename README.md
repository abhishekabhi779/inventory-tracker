# E-Commerce Inventory Tracker

A robust backend application built with FastAPI to efficiently manage inventory for e-commerce platforms. This API provides comprehensive product management, sophisticated search capabilities, and inventory analytics.

![Inventory API](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red?style=for-the-badge)

## 📋 Features

- **Complete Product Management**: Create, read, update, and delete products with ease
- **Advanced Search**: Filter products by name, minimum and maximum stock levels
- **Stock Management**: Update inventory levels with validation for insufficient stock
- **Analytics Dashboard**: Get insights on total inventory value and low-stock items
- **Reporting**: Generate comprehensive PDF inventory reports

## 🚀 Live Demo

Try the API using the interactive documentation:
[https://inventory-tracker.onrender.com/docs](https://inventory-tracker.onrender.com/docs)

## 📦 Tech Stack

- **FastAPI**: High-performance web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **ReportLab**: PDF generation
- **SQLite**: Default database (can be configured to use other databases)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhishekabhi779/inventory-tracker.git
   cd inventory-tracker
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the application**
   - API: [http://localhost:8000](http://localhost:8000)
   - Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📚 API Documentation

### Products

#### Create a product
```
POST /products/
```
Request body:
```json
{
  "name": "Product Name",
  "description": "Product Description",
  "price": 29.99,
  "stock": 100
}
```

#### Get a product by ID
```
GET /products/{product_id}
```

#### Get all products (with optional filters)
```
GET /products/?name=shirt&min_stock=10&max_stock=100
```
Query parameters:
- `name`: Filter by product name (case-insensitive, partial match)
- `min_stock`: Filter products with stock greater than or equal to this value
- `max_stock`: Filter products with stock less than or equal to this value

#### Update a product
```
PUT /products/{product_id}
```
Request body: Same as create product

#### Delete a product
```
DELETE /products/{product_id}
```

#### Update product stock
```
PATCH /products/{product_id}/stock
```
Request body:
```json
{
  "quantity": 5  // Amount to reduce stock by
}
```

### Analytics

#### Get inventory analytics
```
GET /analytics/
```
Response:
```json
{
  "total_inventory_value": 12345.67,
  "low_stock_items": [
    {"id": 1, "name": "Product Name", "stock": 5}
  ]
}
```

### Reports

#### Generate PDF inventory report
```
GET /inventory-report/
```
Returns a downloadable PDF file with the current inventory.

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
pytest
```

## 🔧 Configuration

The application uses environment variables for configuration:

- `DATABASE_URL`: Connection string for the database (defaults to SQLite if not provided)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Abhishek - [GitHub Profile](https://github.com/abhishekabhi779)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/abhishekabhi779/inventory-tracker/issues).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
