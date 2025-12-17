from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from rest_framework import status

""" 
Testing Philosophy: Test the behavior not the implementation

"""

@pytest.mark.django_db
class TestCreateCollection:

    # @pytest.mark.skip(reason="skipping test for now")
    def test_if_user_is_anonymous_returns_401(self):

        client = APIClient()
        response = client.post("/store/collections/",{"title":"a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

    def test_if_user_is_not_admin_returns_403(self):

        client = APIClient()
        client.force_authenticate(user={})
        response = client.post("/store/collections/",{"title":"a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_invalid_data_returns_400(self):

        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post("/store/collections/",{"title":""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_valid_data_returns_201(self):

        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post("/store/collections/",{"title":"a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
    
