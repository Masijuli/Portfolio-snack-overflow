from flask import Flask, render_template, request, jsonify
from db import get_connection

app = Flask(__name__)

# ------------------------
# PAGE ROUTES
# ------------------------

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/expiration")
def expiration():
    return render_template("expiration.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/grocery-list")
def grocery_list():
    return render_template("grocery-list.html")




# ------------------------
# DASHBOARD
# ------------------------

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM inventory
        """)
        inventory_count = cur.fetchall()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM inventory
            WHERE expiration_date < CURRENT_DATE
            AND quantity > 0
        """)
        expired_count = cur.fetchall()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM inventory
            WHERE expiration_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
            AND quantity > 0
        """)
        expiring_7_count = cur.fetchall()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM inventory
            WHERE opened_date IS NOT NULL
        """)
        open_count = cur.fetchall()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM recipe
        """)
        recipes_count = cur.fetchall()[0]

    conn.close()

    items = {"inventory_count": inventory_count,
             "expired_count":   expired_count,
             "expiring_7_count":expiring_7_count,
             "open_count":      open_count,
             "recipes_count":   recipes_count}

    return jsonify(items)


# ------------------------
# EXPIRED
# ------------------------

@app.route("/api/expired-list", methods=["GET"])
def get_dashbaord_expired_list():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT food.food_name, inventory.expiration_date, inventory.inventory_id
            FROM inventory JOIN food
                ON inventory.food_id = food.food_id
            WHERE expiration_date < CURRENT_DATE
            AND quantity > 0
        """)

        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "name": row[0],
            "expiration": row[1],
            "inventory_id": row[2]
        })

    return jsonify(items)

@app.route("/api/expiring-7-list", methods=["GET"])
def get_dashbaord_expiring_7_list():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT food.food_name, inventory.expiration_date
            FROM inventory JOIN food
                ON inventory.food_id = food.food_id
            WHERE expiration_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
            AND quantity > 0
        """)

        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "name": row[0],
            "expiration": row[1]
        })

    return jsonify(items)

@app.route("/api/inventory/<int:id>", methods=["DELETE"])
def delete_inventory(id):

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute("""
            DELETE FROM inventory
            WHERE inventory_id = %s
        """, (id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

# ------------------------
# INVENTORY
# ------------------------

@app.route("/api/inventory", methods=["GET"])
def get_inventory():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT inventory.inventory_id, food.food_name, inventory.quantity, units.unit_name, storage.location, grocery_runs.bought_date, inventory.opened_date, inventory.expiration_date, grocery_stores.store_name
            FROM inventory JOIN food
                ON inventory.food_id = food.food_id
            JOIN storage
                ON inventory.storage_id = storage.storage_id
            JOIN units
                ON inventory.unit_id = units.unit_id
            JOIN grocery_runs
                ON inventory.run_id = grocery_runs.run_id
            JOIN grocery_stores
                ON grocery_runs.store_id = grocery_stores.store_id
            WHERE inventory.quantity > 0
            ORDER BY inventory.expiration_date DESC
        """)

        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "inventory_id": row[0],
            "name": row[1],
            "quantity": row[2],
            "unit": row[3],
            "storage": row[4],
            "purchase_date": row[5],
            "opened_date": row[6],
            "expiration_date": row[7],
            "store": row[8]
        })

    return jsonify(items)

@app.route("/api/inventory/<int:inventory_id>/open", methods=["POST"])
def open_inventory_item(inventory_id):

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute("""
            UPDATE inventory
            SET opened_date = CURRENT_DATE
            WHERE inventory_id = %s
        """, (inventory_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Item opened"
    })

@app.route("/api/inventory", methods=["POST"])
def add_inventory():

    data = request.json

    conn = get_connection()

    with conn.cursor() as cur:
        # this should be done using GENERATED ALWAYS AS IDENTITY in the sql but it was not included in the original table generation
        cur.execute("""
            SELECT MAX(inventory_id) 
            FROM inventory
        """)
        id = cur.fetchone()[0] + 1

        cur.execute("""
            INSERT INTO inventory (
                inventory_id,
                food_id,
                storage_id,
                run_id,
                purchase_price,
                expiration_date,
                opened_date,
                quantity,
                unit_id
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id,
            data["food_id"],
            data["storage_id"],
            data["run_id"],
            None,
            data["expiration_date"],
            None,
            data["quantity"],
            data["unit_id"]
        ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Inventory item added"})

@app.route("/api/inventory/<string:search>/search", methods=["GET"])
def search_inventory(search):
    
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT inventory.inventory_id, food.food_name, inventory.quantity, units.unit_name, storage.location, grocery_runs.bought_date, inventory.opened_date, inventory.expiration_date, grocery_stores.store_name
            FROM inventory JOIN food
                ON inventory.food_id = food.food_id
            JOIN storage
                ON inventory.storage_id = storage.storage_id
            JOIN units
                ON inventory.unit_id = units.unit_id
            JOIN grocery_runs
                ON inventory.run_id = grocery_runs.run_id
            JOIN grocery_stores
                ON grocery_runs.store_id = grocery_stores.store_id
            WHERE inventory.quantity > 0
            AND food.food_name = %s
            ORDER BY inventory.expiration_date DESC
        """, (search,))

        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "inventory_id": row[0],
            "name": row[1],
            "quantity": row[2],
            "unit": row[3],
            "storage": row[4],
            "purchase_date": row[5],
            "opened_date": row[6],
            "expiration_date": row[7],
            "store": row[8]
        })

    return jsonify(items)

# INVENTORY HELPERS
@app.route("/api/foods", methods=["GET"])
def get_foods():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT food_id, food_name
            FROM food
            ORDER BY food_name
        """)
        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "value": row[1]
        })

    return jsonify(items)

@app.route("/api/stores", methods=["GET"])
def get_stores():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT grocery_runs.run_id, grocery_runs.store_id, grocery_runs.bought_date, grocery_stores.store_name
            FROM grocery_runs JOIN grocery_stores
                ON grocery_runs.store_id = grocery_stores.store_id
            ORDER BY bought_date
        """)
        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "value": str(row[2])+' ' + row[3]
        })

    return jsonify(items)

@app.route("/api/storage", methods=["GET"])
def get_storage():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT storage_id, location
            FROM storage
            ORDER BY location
        """)
        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "value": row[1]
        })

    return jsonify(items)

@app.route("/api/units", methods=["GET"])
def get_units():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT unit_id, unit_name
            FROM units
            ORDER BY unit_name
        """)
        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "value": row[1]
        })

    return jsonify(items)


# ------------------------
# GROCERY LIST
# ------------------------
@app.route("/api/grocery-lists", methods=["GET"])
def get_grocery_lists():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT grocery_list_id, list_name
            FROM grocery_list
            ORDER BY list_name
        """)
        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "value": row[1]
        })

    return jsonify(items)

@app.route("/api/grocery-lists/<int:list_id>/search", methods=["GET"])
def get_grocery_list_items(list_id):
    
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT grocery_list_items.grocery_list_item_id, food.food_name, grocery_list_items.notes, grocery_list_items.quantity, grocery_list_items.purchased, units.unit_name
            FROM grocery_list_items JOIN food
                ON grocery_list_items.food_id = food.food_id
            JOIN units
                ON grocery_list_items.unit_id = units.unit_id
            WHERE grocery_list_items.grocery_list_id = %s
        """, (list_id,))

        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "item_id": row[0],
            "food": row[1],
            "notes": row[2],
            "quantity": row[3],
            "purchased": row[4],
            "units": row[5]
        })

    return jsonify(items)

@app.route("/api/grocery-lists/<int:list_id>/mark", methods=["POST"])
def mark_grocery_list(list_id):

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute("""
            UPDATE grocery_list_items
            SET purchased = TRUE
            WHERE grocery_list_item_id = %s
        """, (list_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Item opened"
    })

if __name__ == "__main__":
    app.run(debug=True)