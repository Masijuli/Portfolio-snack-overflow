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
# API ROUTES
# ------------------------

@app.route("/api/items", methods=["GET"])
def get_items():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, quantity
            FROM inventory
            ORDER BY id DESC
        """)

        rows = cur.fetchall()

    conn.close()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "name": row[1],
            "quantity": row[2]
        })

    return jsonify(items)


@app.route("/api/items", methods=["POST"])
def add_item():

    data = request.json

    name = data["name"]
    quantity = data["quantity"]

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute("""
            INSERT INTO inventory (name, quantity)
            VALUES (%s, %s)
        """, (name, quantity))

    conn.commit()
    conn.close()

    return jsonify({"message": "Item added"})



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
            FROM recipes
        """)
        recipes_count = cur.fetchall()[0]

    conn.close()

    items = {"inventory_count": inventory_count,
             "expired_count":   expired_count,
             "expiring_7_count":expiring_7_count,
             "open_count":      open_count,
             "recipes_count":   recipes_count}

    return jsonify(items)


@app.route("/api/dashboard/expired-list", methods=["GET"])
def get_dashbaord_expired_list():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT food_name, expiration_date
            FROM inventory
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


@app.route("/api/dashboard/expiring-7-list", methods=["GET"])
def get_dashbaord_expiring_7_list():

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT food_name, expiration_date
            FROM inventory
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



if __name__ == "__main__":
    app.run(debug=True)