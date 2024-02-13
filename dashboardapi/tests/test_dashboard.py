from django.test import TestCase, Client
from dashboardapi.models import Category, Item, Tag
import json
import uuid

class FullDashboardTest (TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def setUp(self) -> None:
        # Populate the database with items
        Client().post("/dashboard/init/")
        self.unimportant = Category.objects.get(name="Unimportant")
    
    def test_items(self):
        client = Client()
        
        # Try logging in with non existant user
        response = client.post("/dashboard/login/", content_type="application/json", data=json.dumps({
            "username": "hello",
            "password": "world"
        }))
        self.assertEquals(response.status_code, 400, "Was able to login non existant user")
        
        # Try to access all item api without being logged in
        response = client.get("/dashboard/item/all/")
        self.assertEquals(response.status_code, 403, "Was able to see items without login")
        
        # Register (add) a new user
        response = client.post("/dashboard/register/", content_type="application/json", data=json.dumps({
            "username": "johndoe",
            "password": "johndoe123",
            "email": "johndoe@example.com"
        }))
        self.assertEquals(response.status_code, 200, "Unable to register new user")
        
        # Log in with the newly added user
        response = client.post("/dashboard/login/", content_type="application/json", data=json.dumps({
            "username": "johndoe",
            "password": "johndoe123"
        }))
        self.assertEquals(response.status_code, 200, "Was unable to login existant user")
        
        # Use the get all items api
        response = client.get("/dashboard/item/all/")
        self.assertEquals(response.status_code, 200, "Was unable to see items with proper login")
        
        expected_response = {
            'items': [
                {'sku': '', 'name': 'Item 1', 'category': 'Important', 'in_stock': '20.400', 'available_stock': '5.340', 'tags': ['Tag 1', 'Tag 2']}, 
                {'sku': '', 'name': 'Item 2', 'category': 'Important', 'in_stock': '200.400', 'available_stock': '5.770', 'tags': []}, 
                {'sku': '', 'name': 'Item 3', 'category': 'Unimportant', 'in_stock': '203.788', 'available_stock': '50.550', 'tags': []}, 
                {'sku': '', 'name': 'Item 4', 'category': 'Important', 'in_stock': '500.000', 'available_stock': '25.340', 'tags': []}
            ]
        }
        actual_response = response.json()
        next_uuid = actual_response["items"][0]["id"]
        
        for item in actual_response["items"]:
            item["tags"].sort()
            del item["id"]
        
        for item in expected_response["items"]:
            self.assertIn(item, actual_response["items"])
            
        # Use the get all items with filter
        response = client.get(f"/dashboard/item/all/?category={self.unimportant.id}")
        response_json = response.json()
        self.assertEquals(len(response_json["items"]), 1)
        del response_json["items"][0]["id"]
        self.assertEquals(response_json["items"][0], expected_response["items"][2])
        
        # Use the get single item api
        response = client.get(f"/dashboard/item/{next_uuid}/")
        self.assertEquals(response.status_code, 200, "Was unable to see item with proper login")
        response_json = response.json()
        self.assertEquals(len(response_json["items"]), 1)
        response_json["items"][0]["tags"].sort()
        del response_json["items"][0]["id"]
        self.assertEquals(response_json["items"][0], actual_response["items"][0])
        
        # Try to get a non existant item
        response = client.get(f"/dashboard/item/{uuid.uuid4()}/")
        self.assertEquals(response.status_code, 200, "Was unable to see item with proper login")
        self.assertEquals(len(response.json()["items"]), 0)
