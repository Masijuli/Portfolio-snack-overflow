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


@app.route("/api/expired-list", methods=["GET"])
def get_dashbaord_expired_list():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT food.food_name, inventory.expiration_date
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
            "expiration": row[1]
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

@app.route("/api/inventory", methods=["GET"])
def get_inventory():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT inventory.inventory_id, food.food_name, inventory.quantity, units.unit_name, storage.location, grocery_runs.bought_date, inventory.opened_date, inventory.expiration_date
            FROM inventory JOIN food
                ON inventory.food_id = food.food_id
            JOIN storage
                ON inventory.storage_id = storage.storage_id
            JOIN units
                ON inventory.unit_id = units.unit_id
            JOIN grocery_runs
                ON inventory.run_id = grocery_runs.run_id
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
            "expiration_date": row[7]
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

if __name__ == "__main__":
    app.run(debug=True)