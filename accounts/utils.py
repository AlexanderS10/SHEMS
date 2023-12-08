from django.db import connection
def get_energy_usage_device_24(customer_id):
    with connection.cursor() as cursor:
        query = """
        SELECT D.device_id, D.device_name, SUM(E."Energy") as energy_use
        FROM accounts_servicelocations AS SL
        JOIN accounts_devices AS D ON (SL.id = D.location_id)
        JOIN accounts_energyusage AS E ON (E.device_id = D.device_id)
        WHERE SL.customer_id = %s AND E."EnergyTimestamp" >= NOW() - Interval '24 hours'
        GROUP BY D.device_id, D.device_name
        """
        cursor.execute(query, [customer_id])
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return data
        else:
            return []
        
def get_energy_usage_location_24(customer_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT l.id, l."streetName", SUM(e."Energy") AS total_energy_consumption
            FROM accounts_customers AS c 
            JOIN accounts_servicelocations AS l ON (c.id = l.customer_id)
            JOIN accounts_devices AS d ON (l.id = d.location_id)
            JOIN accounts_energyusage AS e ON (d.device_id = e.device_id)
            WHERE l.customer_id = %s AND e."EnergyTimestamp" >= NOW() - Interval '24 hours'
            GROUP BY l.id, l."streetName"
        ''', [customer_id])
        if cursor.description is not None:
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        else:
            results = []
    return results