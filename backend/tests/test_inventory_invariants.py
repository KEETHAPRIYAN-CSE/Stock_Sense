import pytest


@pytest.fixture
def auth_client(client):
    reg = client.post(
        "/api/auth/register",
        json={
            "email": "manager@inventory.com",
            "full_name": "Inventory Manager",
            "password": "managerpassword",
            "role": "INVENTORY_MANAGER",
        },
    )
    token = reg.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def base_inventory_setup(auth_client):
    cat = auth_client.post("/api/categories", json={"name": "Metals"}).json()
    uom = auth_client.post("/api/uoms", json={"name": "Kilogram", "code": "kg"}).json()
    wh = auth_client.post("/api/warehouses", json={"name": "Central Hub", "code": "WH-01"}).json()
    loc1 = auth_client.post(
        "/api/locations",
        json={"warehouse_id": wh["id"], "name": "Main Store", "code": "LOC-MS", "location_type": "STORAGE"},
    ).json()
    loc2 = auth_client.post(
        "/api/locations",
        json={"warehouse_id": wh["id"], "name": "Production Rack", "code": "LOC-PR", "location_type": "PRODUCTION"},
    ).json()
    sup = auth_client.post("/api/suppliers", json={"name": "Steel Provider Ltd"}).json()
    cust = auth_client.post("/api/customers", json={"name": "Heavy Machinery Inc"}).json()

    prod = auth_client.post(
        "/api/products",
        json={
            "name": "Steel Rods",
            "sku": "ROD-001",
            "category_id": cat["id"],
            "uom_id": uom["id"],
            "initial_stock": 0.0,
            "reorder_level": 15.0,
        },
    ).json()

    return {
        "cat": cat,
        "uom": uom,
        "wh": wh,
        "loc1": loc1,
        "loc2": loc2,
        "sup": sup,
        "cust": cust,
        "prod": prod,
    }


def test_complete_inventory_invariants_and_demo_flow(auth_client, base_inventory_setup):
    ctx = base_inventory_setup
    prod_id = ctx["prod"]["id"]
    loc1_id = ctx["loc1"]["id"]
    loc2_id = ctx["loc2"]["id"]
    wh_id = ctx["wh"]["id"]
    sup_id = ctx["sup"]["id"]
    cust_id = ctx["cust"]["id"]
    uom_id = ctx["uom"]["id"]

    # Invariant 0: Initially stock is 0
    stock_0 = auth_client.get(f"/api/stock/{prod_id}").json()
    assert stock_0["total_quantity"] == 0.0

    # =========================================================================
    # Step 1: Inbound Receipt (100 kg Steel Rods into Main Store)
    # Invariant: after = before + received (0 + 100 = 100)
    # =========================================================================
    rec_res = auth_client.post(
        "/api/receipts",
        json={
            "supplier_id": sup_id,
            "warehouse_id": wh_id,
            "destination_location_id": loc1_id,
            "items": [{"product_id": prod_id, "quantity": 100.0, "uom_id": uom_id}],
        },
    )
    assert rec_res.status_code == 201
    rec_id = rec_res.json()["id"]

    # Validate receipt
    val_rec = auth_client.post(f"/api/receipts/{rec_id}/validate")
    assert val_rec.status_code == 200
    assert val_rec.json()["status"] == "DONE"

    # Verify stock increased by exactly 100
    stock_1 = auth_client.get(f"/api/stock/{prod_id}").json()
    assert stock_1["total_quantity"] == 100.0

    # Cannot validate twice
    double_rec = auth_client.post(f"/api/receipts/{rec_id}/validate")
    assert double_rec.status_code == 400

    # =========================================================================
    # Step 2: Internal Transfer (20 kg Main Store -> Production Rack)
    # Invariant: source_after = source_before - 20 (80)
    #            dest_after = dest_before + 20 (20)
    #            total company stock is UNCHANGED (100 == 100)
    # =========================================================================
    trf_res = auth_client.post(
        "/api/transfers",
        json={
            "warehouse_id": wh_id,
            "source_location_id": loc1_id,
            "destination_location_id": loc2_id,
            "items": [{"product_id": prod_id, "quantity": 20.0, "uom_id": uom_id}],
        },
    )
    assert trf_res.status_code == 201
    trf_id = trf_res.json()["id"]

    val_trf = auth_client.post(f"/api/transfers/{trf_id}/validate")
    assert val_trf.status_code == 200
    assert val_trf.json()["status"] == "DONE"

    # Check locations breakdown
    loc_stocks = auth_client.get(f"/api/stock/{prod_id}/locations").json()
    stock_loc1 = next(l for l in loc_stocks if l["location_id"] == loc1_id)["quantity"]
    stock_loc2 = next(l for l in loc_stocks if l["location_id"] == loc2_id)["quantity"]
    assert stock_loc1 == 80.0
    assert stock_loc2 == 20.0

    # Total company stock strictly unchanged
    stock_2 = auth_client.get(f"/api/stock/{prod_id}").json()
    assert stock_2["total_quantity"] == 100.0

    # Test transfer beyond available stock rejection
    bad_trf = auth_client.post(
        "/api/transfers",
        json={
            "warehouse_id": wh_id,
            "source_location_id": loc2_id,  # has 20
            "destination_location_id": loc1_id,
            "items": [{"product_id": prod_id, "quantity": 50.0, "uom_id": uom_id}],
        },
    )
    bad_val = auth_client.post(f"/api/transfers/{bad_trf.json()['id']}/validate")
    assert bad_val.status_code == 400
    assert "Insufficient" in bad_val.json()["detail"]
    auth_client.post(f"/api/transfers/{bad_trf.json()['id']}/cancel")

    # =========================================================================
    # Step 3: Outbound Delivery (20 kg from Main Store to Customer)
    # Invariant: after = before - delivered (80 - 20 = 60 in Main Store, 80 total)
    #            delivered <= available
    # =========================================================================
    del_res = auth_client.post(
        "/api/deliveries",
        json={
            "customer_id": cust_id,
            "warehouse_id": wh_id,
            "source_location_id": loc1_id,
            "items": [{"product_id": prod_id, "quantity": 20.0, "uom_id": uom_id}],
        },
    )
    assert del_res.status_code == 201
    del_id = del_res.json()["id"]

    # Pick and pack
    auth_client.post(f"/api/deliveries/{del_id}/pick")
    auth_client.post(f"/api/deliveries/{del_id}/pack")

    # Validate
    val_del = auth_client.post(f"/api/deliveries/{del_id}/validate")
    assert val_del.status_code == 200
    assert val_del.json()["status"] == "DONE"

    # Total company stock decreased by 20 (now 80)
    stock_3 = auth_client.get(f"/api/stock/{prod_id}").json()
    assert stock_3["total_quantity"] == 80.0

    # Test delivery exceeding available stock rejection
    excess_del = auth_client.post(
        "/api/deliveries",
        json={
            "customer_id": cust_id,
            "warehouse_id": wh_id,
            "source_location_id": loc1_id,  # has 60
            "items": [{"product_id": prod_id, "quantity": 999.0, "uom_id": uom_id}],
        },
    )
    excess_val = auth_client.post(f"/api/deliveries/{excess_del.json()['id']}/validate")
    assert excess_val.status_code == 400
    assert "Insufficient stock" in excess_val.json()["detail"]
    auth_client.post(f"/api/deliveries/{excess_del.json()['id']}/cancel")

    # =========================================================================
    # Step 4: Inventory Adjustment (-3 kg damaged in Main Store)
    # Invariant: difference = counted - system (57 - 60 = -3)
    #            new_quantity = counted (57)
    #            total stock becomes 57 + 20 = 77 kg
    # =========================================================================
    adj_res = auth_client.post(
        "/api/adjustments",
        json={
            "warehouse_id": wh_id,
            "location_id": loc1_id,
            "reason": "Damaged goods found during cycle count",
            "items": [{"product_id": prod_id, "counted_quantity": 57.0}],
        },
    )
    assert adj_res.status_code == 201
    adj_id = adj_res.json()["id"]

    val_adj = auth_client.post(f"/api/adjustments/{adj_id}/validate")
    assert val_adj.status_code == 200
    assert val_adj.json()["status"] == "DONE"

    stock_4 = auth_client.get(f"/api/stock/{prod_id}").json()
    assert stock_4["total_quantity"] == 77.0

    # =========================================================================
    # Step 5: Immutable Stock Ledger Verification
    # Invariant for EVERY row: quantity_after == quantity_before + quantity_change
    # =========================================================================
    ledger_res = auth_client.get(f"/api/stock/ledger?product_id={prod_id}")
    assert ledger_res.status_code == 200
    ledger_entries = ledger_res.json()

    # 5 operations: RECEIPT, TRANSFER_OUT, TRANSFER_IN, DELIVERY, ADJUSTMENT
    assert len(ledger_entries) == 5

    for entry in ledger_entries:
        expected_after = round(entry["quantity_before"] + entry["quantity_change"], 4)
        actual_after = round(entry["quantity_after"], 4)
        assert actual_after == expected_after, f"Invariant failed for entry: {entry}"

    # =========================================================================
    # Step 6: Dashboard Live Verification
    # =========================================================================
    dash_summary = auth_client.get("/api/dashboard/summary").json()
    assert dash_summary["total_products"] == 1
    assert dash_summary["total_warehouses"] == 1
    assert dash_summary["pending_receipts"] == 0
    assert dash_summary["pending_deliveries"] == 0

    dash_ops = auth_client.get("/api/dashboard/operations").json()
    receipts_stat = next(o for o in dash_ops if o["operation_type"] == "RECEIPTS")
    assert receipts_stat["done"] == 1

    recent_movs = auth_client.get("/api/dashboard/recent-movements").json()
    assert len(recent_movs) == 5
