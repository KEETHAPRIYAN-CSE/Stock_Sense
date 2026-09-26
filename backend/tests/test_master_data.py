import pytest


@pytest.fixture
def auth_client(client):
    res = client.post(
        "/api/auth/register",
        json={
            "email": "manager@test.com",
            "full_name": "Test Manager",
            "password": "password123",
            "role": "INVENTORY_MANAGER",
        },
    )
    token = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


def test_master_data_crud(auth_client):
    # 1. Category
    cat_res = auth_client.post(
        "/api/categories", json={"name": "Raw Materials", "description": "Metals"}
    )
    assert cat_res.status_code == 201
    cat_id = cat_res.json()["id"]

    # 2. UOM
    uom_res = auth_client.post("/api/uoms", json={"name": "Kilogram", "code": "kg"})
    assert uom_res.status_code == 201
    uom_id = uom_res.json()["id"]

    # 3. Warehouse
    wh_res = auth_client.post(
        "/api/warehouses",
        json={"name": "Central Hub", "code": "WH-01", "address": "123 Warehouse Rd"},
    )
    assert wh_res.status_code == 201
    wh_id = wh_res.json()["id"]

    # 4. Location
    loc_res = auth_client.post(
        "/api/locations",
        json={
            "warehouse_id": wh_id,
            "name": "Main Store",
            "code": "LOC-MS",
            "location_type": "STORAGE",
        },
    )
    assert loc_res.status_code == 201
    loc_id = loc_res.json()["id"]

    # 5. Supplier
    sup_res = auth_client.post(
        "/api/suppliers",
        json={"name": "Apex Supplies", "email": "apex@supplies.com", "phone": "1234567890"},
    )
    assert sup_res.status_code == 201

    # 6. Customer
    cust_res = auth_client.post(
        "/api/customers",
        json={"name": "BuildCorp", "email": "contact@buildcorp.com", "phone": "9876543210"},
    )
    assert cust_res.status_code == 201

    # 7. Product
    prod_res = auth_client.post(
        "/api/products",
        json={
            "name": "Steel Rods",
            "sku": "ROD-STEEL-01",
            "category_id": cat_id,
            "uom_id": uom_id,
            "initial_stock": 50.0,
            "reorder_level": 10.0,
            "initial_warehouse_id": wh_id,
            "initial_location_id": loc_id,
        },
    )
    assert prod_res.status_code == 201
    prod_data = prod_res.json()
    assert prod_data["sku"] == "ROD-STEEL-01"
    assert prod_data["total_stock"] == 50.0
    prod_id = prod_data["id"]

    # 8. Duplicate SKU rejection
    dup_res = auth_client.post(
        "/api/products",
        json={
            "name": "Another Steel Rod",
            "sku": "ROD-STEEL-01",
            "category_id": cat_id,
            "uom_id": uom_id,
            "initial_stock": 10.0,
            "reorder_level": 5.0,
        },
    )
    assert dup_res.status_code == 400

    # 9. Product List and Search
    list_res = auth_client.get("/api/products?search=Steel")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 10. Product Detail
    detail_res = auth_client.get(f"/api/products/{prod_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["name"] == "Steel Rods"
    assert len(detail_res.json()["location_stocks"]) == 1
    assert detail_res.json()["location_stocks"][0]["quantity"] == 50.0
