from store.models import Collection, Product
from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

""" 
Testing Philosophy: Test the behavior not the implementation
"""

"""
Common Cases while testing apis:
1. Permissions
    - Anonymous user 
    - Normal User
    - Admin User
2. Existing data
3. New data
4. Invalid data
"""


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)
    return do_create_collection


@pytest.fixture
def delete_collection(api_client):
    def do_delete_collection(collection_id):
        return api_client.delete(f"/store/collections/{collection_id}/")
    return do_delete_collection

@pytest.fixture
def patch_collection(api_client):
    def do_patch_collection(collection_id, data):
        return api_client.patch(f"/store/collections/{collection_id}/",data)
    return do_patch_collection

@pytest.mark.django_db
class TestCreateCollection:

    # @pytest.mark.skip(reason="skipping test for now")
    def test_if_user_is_anonymous_returns_401(self,create_collection):
        response = create_collection({"title":"a"})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self,create_collection,authenticate):
        authenticate()

        response = create_collection({"title":"a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_invalid_data_returns_400(self, create_collection,authenticate):
        authenticate(is_staff=True)

        response = create_collection({"title":""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_valid_data_returns_201(self,create_collection,authenticate):
        authenticate(is_staff=True)
        
        response = create_collection({"title":"a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
    

@pytest.mark.django_db
class TestRetrieveCollection:

    def test_if_collection_exists_returns_200(self,api_client):
        # Arrange
        collection = baker.make(Collection)

        # Act
        response = api_client.get(f"/store/collections/{collection.id}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    def test_if_collection_does_not_exist_returns_404(self,api_client):
        response = api_client.get("/store/collections/999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
@pytest.mark.django_db
class TestDeleteCollection:

    def test_if_collection_deletes_returns_204(self,delete_collection,authenticate):
        authenticate(True)
        collection = baker.make(Collection)

        response = delete_collection(collection.id)

        print(response)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
    
    def test_if_normal_user_deletes_returns_403(self, delete_collection, authenticate):
        authenticate()
        
        collection = baker.make(Collection)
        
        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data is not None
    
    def test_anonymous_user_deletes_returns_401(self, delete_collection):
        
        collection = baker.make(Collection)
        
        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateCollection:
    
    def test_if_anonymous_user_updates_return_401(self,patch_collection):

        collection = baker.make(Collection)

        response = patch_collection(collection.id, {"title":"New collection1"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_normal_user_updates_return_403(self, patch_collection, authenticate):
        authenticate()
        collection = baker.make(Collection)

        response = patch_collection(collection.id, {"title":"New collection2"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_updates_collection_returns_200(self, patch_collection,authenticate):
        authenticate(True)
        collection = baker.make(Collection)
        title = "New collection2"
        

        response = patch_collection(collection.id, {"title":title})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == title
        assert response.data['id'] == collection.id
    

