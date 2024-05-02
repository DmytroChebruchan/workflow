## Project Information
- **Repository**: [GitHub - DmytroChebruchan/workflow](https://codeclimate.com/github/DmytroChebruchan/workflow)
- **Maintainability Badge**: [![Maintainability](https://api.codeclimate.com/v1/badges/02724330d63a34a5fc21/maintainability)](https://codeclimate.com/github/DmytroChebruchan/workflow/maintainability)

This project was done as test case. Main task it can perform is to manage workflows with
tasks as nodes inside. With this app you can create, read, update and delete workflows and nodes of workflows.
Main feature is checking if workflow has a path from Start Node to End Node.

## Getting Started

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Make migration

2. Make mifration with alembic
    ```bash
    alembic upgrade head
    ```
### Running the App

3. Start the app:
   ```bash
   python -m main
   ```

### Documentation

- Access the FastAPI documentation page at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- On this page you can not only read about API views available, but also test them manually.

---

## Testing

Most tests are unit tests.
- Run tests using pytest:
  ```bash
  pytest
  ```

---
