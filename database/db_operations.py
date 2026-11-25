from database.db_connection import get_connection
from datetime import datetime

def normalize_quantity_and_unit(quantity, unit):
    """Quantity ni base unit (kg, L, piece) ki convert chesthundi"""
    unit = unit.strip()
    if unit == "g":
        return quantity / 1000.0, "kg"
    elif unit == "kg":
        return quantity, "kg"
    elif unit == "ml":
        return quantity / 1000.0, "L"
    elif unit == "L":
        return quantity, "L"
    else:
        return quantity, "piece"

def add_purchase_to_db(product_name, category, shop_name, total_price, quantity, unit, purchase_date):
    """Product & Purchase ni SQLite lo save chesthundi"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Normalized Unit Price calculate cheyadam
        norm_qty, base_unit = normalize_quantity_and_unit(quantity, unit)
        normalized_price = round(total_price / norm_qty, 2)

        # 2. Product already unda leda check cheyadam (Case-Insensitive)
        cursor.execute("SELECT product_id FROM products WHERE LOWER(name) = LOWER(?)", (product_name,))
        row = cursor.fetchone()

        if row:
            product_id = row[0]
        else:
            # Kotha product ayithe products table lo insert cheyadam
            cursor.execute(
                "INSERT INTO products (name, category, base_unit) VALUES (?, ?, ?)",
                (product_name, category, base_unit)
            )
            product_id = cursor.lastrowid

        # 3. Purchases table lo record insert cheyadam
        cursor.execute("""
            INSERT INTO purchases (product_id, shop_name, total_price, quantity, unit, normalized_price, purchase_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (product_id, shop_name, total_price, quantity, unit, normalized_price, purchase_date))

        conn.commit()
        return True, f"Saved! Normalized Price: ₹{normalized_price} / {base_unit}"

    except Exception as e:
        conn.rollback()
        return False, f"Database Error: {str(e)}"
    finally:
        conn.close()

def get_all_products(search_query=""):
    """Products list + prathi product enni sarlu konnamo count thesthundi (Case-Insensitive)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT p.product_id, p.name, p.category, p.base_unit, COUNT(pu.purchase_id) as times_purchased
        FROM products p
        LEFT JOIN purchases pu ON p.product_id = pu.product_id
        WHERE LOWER(p.name) LIKE ?
        GROUP BY p.product_id
        ORDER BY p.product_id DESC
    """
    cursor.execute(query, (f"%{search_query.lower()}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_product_from_db(product_id):
    """Product ni delete chesthundi (ON DELETE CASCADE valla history kuda delete avuthundi)"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        conn.commit()
        return True, "Product and its purchase history deleted successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"Delete Error: {str(e)}"
    finally:
        conn.close()

def get_purchase_history(product_query="", shop_query=""):
    """Purchase history ni Product & Shop filters tho thesthundi (Case-Insensitive)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT pu.purchase_date, p.name, pu.shop_name, pu.total_price, 
               pu.quantity, pu.unit, pu.normalized_price, p.base_unit
        FROM purchases pu
        JOIN products p ON pu.product_id = p.product_id
        WHERE LOWER(p.name) LIKE ? AND LOWER(pu.shop_name) LIKE ?
        ORDER BY pu.purchase_date DESC, pu.purchase_id DESC
    """
    cursor.execute(query, (f"%{product_query.lower()}%", f"%{shop_query.lower()}%"))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_product_names():
    """Dropdown kosam database lo unna anni product names thesthundi"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products ORDER BY name ASC")
    rows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return rows

def get_price_comparison(product_name):
    """Selected product ki anni shops nundi normalized price ascending order lo thesthundi"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT pu.shop_name, pu.quantity, pu.unit, pu.total_price, pu.normalized_price, p.base_unit
        FROM purchases pu
        JOIN products p ON pu.product_id = p.product_id
        WHERE LOWER(p.name) = LOWER(?)
        ORDER BY pu.normalized_price ASC
    """
    cursor.execute(query, (product_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_dashboard_stats():
    """Dashboard cards kosam Total Products, Total Purchases, Total Spent, & Monthly Spend thesthundi"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(total_price), 0) FROM purchases")
    total_purchases, total_spent = cursor.fetchone()

    # Current month (YYYY-MM) spend calculation
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute(
        "SELECT COALESCE(SUM(total_price), 0) FROM purchases WHERE purchase_date LIKE ?",
        (f"{current_month}%",)
    )
    monthly_spent = cursor.fetchone()[0] or 0

    conn.close()
    return total_products, total_purchases, round(total_spent, 2), round(monthly_spent, 2)

def get_recent_purchases(limit=8):
    """Dashboard table kosam recent purchases thesthundi"""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT pu.purchase_date, p.name, pu.shop_name, pu.total_price,
               pu.quantity, pu.unit, pu.normalized_price, p.base_unit
        FROM purchases pu
        JOIN products p ON pu.product_id = p.product_id
        ORDER BY pu.purchase_date DESC, pu.purchase_id DESC
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows