# Dashboard API

The Dashboard API provides endpoints for user authentication, registration, retrieving items, and initializing the database.

**BASE URL** ` https://dashboardapi-910b0a92507e.herokuapp.com/`

## Authentication

### Register
- **URL:** `/dashboard/register/`
- **Method:** POST
- **Parameters:**
  - `username`: Username of the user
  - `password`: Password of the user
  - `email`: Email of the user
- **Response:**
  - Success:
    ```json
    {
        "success": true
    }
    ```
  - Failure:
    ```json
    {
        "success": false,
        "message": "Username not unique"  // or "Email not unique"
    }
    ```

### Login
- **URL:** `/dashboard/login/`
- **Method:** POST
- **Parameters:**
  - `username`: Username of the user
  - `password`: Password of the user
- **Response:**
  - Success:
    ```json
    {
        "success": true
    }
    ```
  - Failure:
    ```json
    {
        "success": false
    }
    ```


## Items

### Get All Items
- **URL:** `/dashboard/item/all/`
- **Method:** GET
- **Response:**
  ```json
  {
      "items": [
          {
              "id": 1,
              "name": "Item 1",
              "category": "Important",
              "in_stock": 20.4,
              "available_stock": 5.34,
              "tags": ["Tag 1", "Tag 2"]
          },
          // Other items...
      ]
  }
  ```

## Get Single Item

- **URL:** `/dashboard/item/<item_id>/`
- **Method:** GET
- **Parameters:**
    - `item_id`: ID of the item
- **Response:**
    ```json
    {
        "items": [
            {
                "id": 1,
                "name": "Item 1",
                "category": "Important",
                "in_stock": 20.4,
                "available_stock": 5.34,
                "tags": ["Tag 1", "Tag 2"]
            }
        ]
    }
    ```

