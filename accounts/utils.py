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
 
def get_energy_usage_data(customer_id, location_id): #This is just the original function iteration of the one below but in use just in case
    sql_query = """
    SELECT sl.id AS location_id, d.device_id, d.device_name, DATE_TRUNC('day', eu."EnergyTimestamp") AS day_date, ROUND(AVG(eu."Energy"), 2) AS avg_daily_energy
    FROM accounts_customers AS c 
    JOIN accounts_servicelocations AS sl ON c.id = sl.customer_id
    JOIN accounts_devices AS d ON sl.id = d.location_id
    JOIN accounts_energyusage AS eu ON d.device_id = eu.device_id
    WHERE eu."EnergyTimestamp" >= CURRENT_DATE - INTERVAL '7 days' 
    AND eu."EnergyTimestamp" < CURRENT_DATE 
    AND c.id = %s
    AND sl.id = %s
    GROUP BY sl.id, d.device_id, d.device_name, day_date
    ORDER BY sl.id, d.device_id, d.device_name, day_date;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [customer_id, location_id])
        if cursor.description is not None:
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results

    return []

def get_energy_usage_data_custom(customer_id, location_id, days):
    sql_query = """
    SELECT sl.id AS location_id, d.device_id, d.device_name, DATE_TRUNC('day', eu."EnergyTimestamp") AS day_date, ROUND(AVG(eu."Energy"), 2) AS avg_daily_energy
    FROM accounts_customers AS c 
    JOIN accounts_servicelocations AS sl ON c.id = sl.customer_id
    JOIN accounts_devices AS d ON sl.id = d.location_id
    JOIN accounts_energyusage AS eu ON d.device_id = eu.device_id
    WHERE eu."EnergyTimestamp" >= CURRENT_DATE - INTERVAL %s
    AND eu."EnergyTimestamp" < CURRENT_DATE 
    AND c.id = %s
    AND sl.id = %s
    GROUP BY sl.id, d.device_id, d.device_name, day_date
    ORDER BY sl.id, d.device_id, d.device_name, day_date;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [f'{days} days', customer_id, location_id])
        if cursor.description is not None:
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results

    return []

def device_energy_usage_per_date(customer_id, location_id, date):
    sql_query = """
    SELECT l.id, l."streetName", d.device_id, d.device_name, SUM(e."Energy") AS total_energy_consumption
    FROM accounts_customers as c 
    JOIN accounts_servicelocations as l ON (c.id = l.customer_id)
    JOIN accounts_devices as d ON (l.id = d.location_id)
    JOIN accounts_energyusage as e ON (d.device_id = e.device_id)
    WHERE l.customer_id = %s AND l.id=%s AND DATE(e."EnergyTimestamp") = %s
    GROUP BY l.id, l."streetNumber", l."streetName", d.device_id, d.device_name;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [customer_id, location_id, f'{date}'])
        if cursor.description is not None:
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results

    return []