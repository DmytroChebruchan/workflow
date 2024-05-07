## Project Information
- **Repository**: [GitHub - DmytroChebruchan/workflow](https://codeclimate.com/github/DmytroChebruchan/workflow)
- **Maintainability Badge**: [![Maintainability](https://api.codeclimate.com/v1/badges/02724330d63a34a5fc21/maintainability)](https://codeclimate.com/github/DmytroChebruchan/workflow/maintainability)

This project was done as test case. Main task it can perform is to manage workflows with
tasks as nodes inside. With this app you can create, read, update and delete workflows and nodes of workflows.
Main feature is checking if workflow has a path from Start Node to End Node.

## Getting Started

### Installation and run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make migration with alembic
    ```bash
    alembic upgrade head
    ```
3. Start the app:
   ```bash
   python -m main
   ```

## General description of project.

The project manages workflows, nodes, and edges. It utilizes the graph library networkX to determine if there is a path from the start node to the end node of the project.

To ensure data integrity, the project includes validations. For instance, nodes can only be added to existing workflows.

Also, to make usage easier from the box, scripts are used instead of small process instructions.
For example, if workflow is deleted by user, nodes and edges of workflow are deleted automatically as well.

Users have comprehensive functionality, including creating, reading, updating, deleting, and executing (run option) workflows. When a workflow is executed, the path from the start node to the end node
is provided.

Furthermore, users can perform operations on nodes such as creation, viewing, updating, and deletion.

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
