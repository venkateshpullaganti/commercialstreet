# Testing Notes: Fixtures and Model Baker

## Overview
This guide explains how to use pytest fixtures and model_bakery for testing Django applications, using examples from the commercialstreet project.

## What are Fixtures?

Fixtures are reusable pieces of code that set up test data or test environment. They help avoid code duplication and make tests more maintainable.

### Basic Fixture Structure
```python
@pytest.fixture
def fixture_name():
    # Setup code
    return something_useful
```

## Fixtures in Our Codebase

### 1. API Client Fixture (`conftest.py`)

```python
@pytest.fixture
def api_client():
    return APIClient()
```

**What it does:**
- Creates a Django REST Framework API client for making HTTP requests
- Available to all tests in the same directory and subdirectories
- Returns a fresh client instance for each test

**Usage Example:**
```python
def test_something(api_client):
    response = api_client.get("/store/collections/")
    assert response.status_code == 200
```

### 2. Authentication Fixture (`conftest.py`)

```python
@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate
```

**What it does:**
- Returns a function that can authenticate users
- Takes `is_staff` parameter to create admin or regular users
- Uses `force_authenticate` to bypass actual login process

**Usage Examples:**
```python
# Authenticate as regular user
def test_regular_user(authenticate):
    authenticate()  # is_staff=False by default
    # Now api_client is authenticated as regular user

# Authenticate as admin user
def test_admin_user(authenticate):
    authenticate(is_staff=True)
    # Now api_client is authenticated as admin user
```

### 3. Custom Action Fixture (`test_collections.py`)

```python
@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)
    return do_create_collection
```

**What it does:**
- Creates a reusable function for creating collections
- Encapsulates the POST request logic
- Makes tests more readable and maintainable

**Usage Example:**
```python
def test_create_collection(create_collection):
    response = create_collection({"title": "Electronics"})
    assert response.status_code == 201
```

## Model Baker (formerly Model Mommy)

Model Baker automatically creates model instances with realistic fake data.

### Basic Usage

```python
from model_bakery import baker
from store.models import Collection, Product

# Create a single instance
collection = baker.make(Collection)

# Create multiple instances
collections = baker.make(Collection, _quantity=5)

# Create with specific values
collection = baker.make(Collection, title="Electronics")
```

### Example from Our Code

```python
def test_if_collection_exists_returns_200(self, api_client):
    # Arrange - Create test data
    collection = baker.make(Collection)
    
    # Act - Make the request
    response = api_client.get(f"/store/collections/{collection.id}/")
    
    # Assert - Check the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': collection.id,
        'title': collection.title,
        'products_count': 0
    }
```

## Step-by-Step Testing Examples

### Example 1: Testing Anonymous User Access

```python
def test_if_user_is_anonymous_returns_401(self, create_collection):
    # Step 1: No authentication (user is anonymous)
    
    # Step 2: Try to create a collection
    response = create_collection({"title": "a"})
    
    # Step 3: Verify access is denied
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

**What happens:**
1. No authentication is set up
2. API client tries to create a collection
3. Server returns 401 (Unauthorized) because user is not logged in

### Example 2: Testing Non-Admin User Access

```python
def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
    # Step 1: Authenticate as regular user (not admin)
    authenticate()  # is_staff=False by default
    
    # Step 2: Try to create a collection
    response = create_collection({"title": "a"})
    
    # Step 3: Verify access is forbidden
    assert response.status_code == status.HTTP_403_FORBIDDEN
```

**What happens:**
1. User is authenticated but not as admin
2. API client tries to create a collection
3. Server returns 403 (Forbidden) because user lacks admin privileges

### Example 3: Testing Valid Data with Admin User

```python
def test_if_valid_data_returns_201(self, create_collection, authenticate):
    # Step 1: Authenticate as admin user
    authenticate(is_staff=True)
    
    # Step 2: Create collection with valid data
    response = create_collection({"title": "a"})
    
    # Step 3: Verify successful creation
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] > 0
```

**What happens:**
1. User is authenticated as admin (has permissions)
2. API client creates a collection with valid data
3. Server returns 201 (Created) and assigns an ID

## Advanced Baker Examples

### Creating Related Models

```python
# Create a product with a collection
product = baker.make(Product)  # Baker automatically creates related Collection

# Create product with specific collection
collection = baker.make(Collection, title="Electronics")
product = baker.make(Product, collection=collection)

# Create multiple products for one collection
collection = baker.make(Collection)
products = baker.make(Product, collection=collection, _quantity=3)
```

### Creating Complex Relationships

```python
# Create a customer with user
customer = baker.make(Customer)  # Baker creates related User automatically

# Create an order with items
customer = baker.make(Customer)
order = baker.make(Order, customer=customer)
products = baker.make(Product, _quantity=3)

# Create order items
for product in products:
    baker.make(OrderItem, order=order, product=product, quantity=2)
```

### Using Baker with Specific Values

```python
# Create collection with specific title
collection = baker.make(Collection, title="Electronics")

# Create product with specific price range
product = baker.make(Product, unit_price=99.99, inventory=50)

# Create user with specific attributes
user = baker.make(User, is_staff=True, username="admin")
```

## Best Practices

### 1. Use Descriptive Test Names
```python
# Good
def test_if_user_is_anonymous_returns_401(self):
    pass

# Bad
def test_create_collection(self):
    pass
```

### 2. Follow Arrange-Act-Assert Pattern
```python
def test_retrieve_existing_collection(self, api_client):
    # Arrange - Set up test data
    collection = baker.make(Collection, title="Electronics")
    
    # Act - Perform the action
    response = api_client.get(f"/store/collections/{collection.id}/")
    
    # Assert - Check the results
    assert response.status_code == 200
    assert response.data['title'] == "Electronics"
```

### 3. Use Fixtures for Common Setup
```python
# Instead of repeating this in every test:
def test_something():
    client = APIClient()
    user = User.objects.create(username="test")
    client.force_authenticate(user=user)
    # ... test code

# Create a fixture:
@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = baker.make(User)
    client.force_authenticate(user=user)
    return client

def test_something(authenticated_client):
    # ... test code using authenticated_client
```

### 4. Keep Tests Independent
Each test should be able to run independently without relying on other tests.

```python
# Good - each test creates its own data
def test_create_collection(self, create_collection, authenticate):
    authenticate(is_staff=True)
    response = create_collection({"title": "Test"})
    assert response.status_code == 201

def test_update_collection(self, api_client, authenticate):
    authenticate(is_staff=True)
    collection = baker.make(Collection)  # Create fresh data
    response = api_client.patch(f"/store/collections/{collection.id}/", {"title": "Updated"})
    assert response.status_code == 200
```

## Common Patterns in Our Tests

### 1. Permission Testing Pattern
```python
# Test anonymous user
def test_anonymous_user_denied(self, action_fixture):
    response = action_fixture(data)
    assert response.status_code == 401

# Test regular user
def test_regular_user_forbidden(self, action_fixture, authenticate):
    authenticate()
    response = action_fixture(data)
    assert response.status_code == 403

# Test admin user
def test_admin_user_allowed(self, action_fixture, authenticate):
    authenticate(is_staff=True)
    response = action_fixture(data)
    assert response.status_code == 200  # or 201, depending on action
```

### 2. Data Validation Testing Pattern
```python
# Test invalid data
def test_invalid_data_returns_400(self, create_collection, authenticate):
    authenticate(is_staff=True)
    response = create_collection({"title": ""})  # Invalid: empty title
    assert response.status_code == 400
    assert 'title' in response.data  # Check error message

# Test valid data
def test_valid_data_returns_201(self, create_collection, authenticate):
    authenticate(is_staff=True)
    response = create_collection({"title": "Valid Title"})
    assert response.status_code == 201
    assert response.data['id'] > 0
```

This testing approach ensures your Django REST API is robust, secure, and handles all edge cases properly!
