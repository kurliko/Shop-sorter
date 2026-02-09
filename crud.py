from database import get_db_connection

def get_all_categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM categories ORDER BY sort_order")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return categories

from database import get_db_connection

def get_all_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        ORDER BY c.sort_order, p.name
    """)
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

def add_product_to_db(name, category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, category_id) VALUES (%s, %s)", (name.lower(), category_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_product_from_db(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_item_priority(item_name):
    conn = get_db_connection()
    cur = conn.cursor()
    item_name = item_name.lower().strip()
    query = """
        SELECT c.sort_order 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        WHERE p.name = %s OR %s LIKE '%%' || p.name || '%%'
        LIMIT 1
    """
    cur.execute(query, (item_name, item_name))
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res['sort_order'] if res else 999