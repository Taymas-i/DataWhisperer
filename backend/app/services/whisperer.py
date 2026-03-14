import os
from groq import Groq
from sqlalchemy import text
from pathlib import Path
from dotenv import load_dotenv
from app.database.session import engine


env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY not loaded")
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SCHEMA_DESCRIPTION = """
You are an expert data analyst writing PostgreSQL queries.

Database schema:

customers
- customer_id (PK)
- customer_city
- customer_state

orders
- order_id (PK)
- customer_id (FK -> customers.customer_id)
- order_status
- order_purchase_timestamp
- order_delivered_customer_date

reviews
- review_id
- order_id (FK -> orders.order_id)
- review_score

order_items
- order_id
- order_item_id
- product_id
- price

products
- product_id
- product_category_name_english

payments
- order_id
- payment_sequential
- payment_type
- payment_value

Relationships:
customers.customer_id -> orders.customer_id
orders.order_id -> reviews.order_id
orders.order_id -> order_items.order_id
orders.order_id -> payments.order_id

Rules:
- CRITICAL: Generate PostgreSQL SQL only.
- CRITICAL: Do NOT include ANY conversational text, greetings, or explanations. 
- CRITICAL: Do NOT wrap the query in markdown blocks (e.g. no ```sql). 
- Return ONLY the exact raw SQL string that can be directly executed against the database.
- Use correct joins when data spans multiple tables.
"""


def generate_sql(question: str) -> str:

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {"role": "system", "content": SCHEMA_DESCRIPTION},
            {"role": "user", "content": question},
        ],
    )

    sql_query = completion.choices[0].message.content

    if sql_query is None:
        raise ValueError("Model returned empty SQL")

    sql_query = sql_query.strip().replace("```sql", "").replace("```", "")

    return sql_query


def run_sql(query: str):

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()

    return [dict(row._mapping) for row in rows]


def explain_result(question: str, data):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Explain the database result to the user clearly.",
            },
            {
                "role": "user",
                "content": f"""
User Question:
{question}

Database Result:
{data}
""",
            },
        ],
    )

    return completion.choices[0].message.content


def ask_whisperer(question: str):

    try:
        print(f"\nUser Question: {question}")

        sql_query = generate_sql(question)
        print(f"\nGenerated SQL:\n{sql_query}")

        # Basic validation to ensure it's a query
        if not sql_query.strip().lower().startswith(("select", "with")):
             print("Invalid SQL detected.")
             return "I'm sorry, I couldn't generate a valid query for that. Please ask about customers, orders, or products."

        data = run_sql(sql_query)
        
        # Prevent huge console dumps if the LLM generated a SELECT * without LIMIT
        if len(data) > 10:
             print(f"\nDatabase Result: Returned {len(data)} rows (truncated for console)")
        else:
             print(f"\nDatabase Result:\n{data}")
             
        # If the result is huge, only pass the first 10 rows to the LLM to explain, 
        # otherwise we might exceed context windows
        data_to_explain = data[:10] if len(data) > 10 else data

        answer = explain_result(question, data_to_explain)
        return answer

    except Exception as e:
        print(f"SQL execution or explanation ERROR: {str(e)}")
        # Return a friendly string instead of raising a 500 error
        return "I'm sorry, I encountered an error querying the database for that question. It might be unrelated to the data or the database schema couldn't answer it."