from django.db import connection
def get_service_locations(customer_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT * 
            FROM accounts_servicelocations
            WHERE customer_id = %s
        ''', [customer_id])
        if cursor.description is not None:    
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return rows
        else:
            return []

def get_energy_usage_device_24(customer_id):
    with connection.cursor() as cursor:
        query = """
        SELECT D.device_id, D.device_name, SUM(E."Energy") as energy_use
        FROM accounts_servicelocations AS SL
        JOIN accounts_devices AS D ON (SL.id = D.location_id)
        JOIN accounts_energyusage AS E ON (E.device_id = D.device_id)
        WHERE SL.customer_id = %s AND E."EnergyTimestamp" >= NOW() - Interval '24 hours' AND D.is_active = TRUE
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
            WHERE l.customer_id = %s AND e."EnergyTimestamp" >= NOW() - Interval '24 hours' AND d.is_active = TRUE
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

def get_location_history_comparison(location_id, date):
    sql_query = """
    WITH LocationsConsumption AS (
    SELECT SL.customer_id, SL.id as location_id, SL."squareFootage" as squarefootage,
	(SL."squareFootage" * 1.05) as footageUpper, (SL."squareFootage" * 0.95) as footageLower, 
	SUM(E."Energy") as energy_consumption
    FROM accounts_ServiceLocations AS SL 
    JOIN accounts_Devices AS D ON (SL.id = D.location_id)
    JOIN accounts_EnergyUsage AS E ON (E.device_id = D.device_id)
    WHERE DATE_TRUNC('month', E."EnergyTimestamp") = %s::DATE
    GROUP BY SL.customer_id, SL.id, SL."squareFootage"
    ),
    LocationsRelated AS (
        SELECT L1.location_id,AVG(L2.energy_consumption) as similarLocationsAvg
        FROM LocationsConsumption AS L1 
        JOIN LocationsConsumption AS L2 ON (
            L1.squareFootage >= L2.footageLower 
            AND L1.squareFootage <= L2.footageUpper 
            AND L1.location_id != L2.location_id
        )
        GROUP BY L1.location_id
    )
    SELECT LR.location_id, 
    LC.energy_consumption,
    ROUND(LR.similarLocationsAvg, 2) as similar_avg,
    ROUND((LC.energy_consumption / LR.similarLocationsAvg) * 100, 2) as energy_as_percentage
    FROM LocationsRelated AS LR
    JOIN LocationsConsumption AS LC USING (location_id)
    WHERE LR.location_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [f'{date}',location_id])
        if cursor.description is not None:
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results

    return []




def get_peak_power_data(customer_id):
   with connection.cursor() as cursor:
       query = """
       WITH SummedEnergy AS (
    SELECT D.location_id, EU."EnergyTimestamp" as energytimestamp, SUM(EU."Energy") AS summed_energy
    FROM accounts_devices AS D
    JOIN accounts_energyusage AS EU ON D.device_id = EU.device_id
    GROUP BY D.location_id, EU."EnergyTimestamp"
    ),
    MaxEnergyPerYear AS (
        SELECT location_id, EXTRACT(YEAR FROM EnergyTimestamp) AS year, MAX(summed_energy) AS max_summed_energy
        FROM SummedEnergy
        GROUP BY location_id, EXTRACT(YEAR FROM EnergyTimestamp)
    )
    SELECT distinct on (sl.id, m.year) SL.id AS location_id, SL."streetName",M.year, M.max_summed_energy * 6 AS peak_power
    FROM accounts_servicelocations AS SL
    JOIN MaxEnergyPerYear AS M ON SL.id = M.location_id
    JOIN SummedEnergy AS SE ON SL.id = SE.location_id AND M.max_summed_energy = SE.summed_energy
    WHERE SL.customer_id = %s
    GROUP BY SL.id, SL."streetName", M.year, M.max_summed_energy, SE.EnergyTimestamp
       """
       cursor.execute(query, [customer_id])
       if cursor.description:
           columns = [col[0] for col in cursor.description]
           data = [dict(zip(columns, row)) for row in cursor.fetchall()]
           return data
       else:
           return []