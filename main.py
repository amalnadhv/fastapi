from fastapi import FastAPI
import pyodbc

app = FastAPI()

def get_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=BSERVER\\PBSERVER;"
        "Database=COM_JSF;"
        "UID=sa;"
        "PWD=SVVsvv@999;"
    )

@app.get("/sales_today")
def get_sales_today():
    conn = get_connection()
    cursor = conn.cursor()

    # Query 1: Sales
    cursor.execute("""
        SELECT SUM(ISNULL(amount, 0)) AS sales
        FROM astran
        WHERE LEFT(account, 4) BETWEEN '4000' AND '4999'
          AND type = 'C'
          AND CONVERT(date, jvdate) = CONVERT(date, GETDATE())
    """)
    sales = cursor.fetchone()[0] or 0

    # Query 2: Sales Return
    cursor.execute("""
        SELECT SUM(ISNULL(amount, 0)) AS salesReturn
        FROM astran
        WHERE LEFT(account, 4) BETWEEN '4000' AND '4999'
          AND type = 'D'
          AND CONVERT(date, jvdate) = CONVERT(date, GETDATE())
    """)
    sales_return = cursor.fetchone()[0] or 0

    conn.close()

    # Calculate actual sales
    actual_sales = float(sales) - float(sales_return)

    return {
        "sales": float(sales),
        "sales_return": float(sales_return),
        "actual_sales": actual_sales
    }
