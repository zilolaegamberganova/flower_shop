from django.db import connection
from contextlib import closing

def dictfetchall(cursor):
    column= [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_order_by_user(id):
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute(""" 
                SELECT core_order.id, core_customer.first_name, core_customer.last_name, 
                       core_order.address, core_order.payment_type, core_order.status, core_order.created_at 
                FROM core_order 
                INNER JOIN core_customer ON core_customer.id = core_order.customer_id 
                WHERE core_order.customer_id = %s
            """, [id])
            return dictfetchall(cursor)
    except Exception:
        return []


def get_product_by_order(id):
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute(""" 
                SELECT core_orderproduct.count, core_orderproduct.price,
                       core_orderproduct.created_at, core_product.title 
                FROM core_orderproduct 
                INNER JOIN core_product ON core_orderproduct.product_id = core_product.id  
                WHERE order_id = %s
            """, [id])
            return dictfetchall(cursor)
    except Exception:
        return []


def get_table():
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute(""" 
                SELECT core_orderproduct.product_id, 
                       COUNT(core_orderproduct.product_id) as count, 
                       core_product.title 
                FROM core_orderproduct 
                INNER JOIN core_product ON core_product.id = core_orderproduct.product_id 
                GROUP BY core_orderproduct.product_id, core_product.title 
                ORDER BY count DESC 
                LIMIT 10
            """)
            return dictfetchall(cursor)
    except Exception:
        return []