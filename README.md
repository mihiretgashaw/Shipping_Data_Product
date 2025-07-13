Shipping Data Product – Telegram Medical Marketplace Analytics

This project transforms messy Telegram e-commerce data into structured, trusted insights using a modern data stack.
Task 1 - Scraping and Loading Telegram Messages
Extract messages from public Telegram channels using the Telegram API.
Save messages in JSON format.
Load the JSON into the raw.telegram_messages table in PostgreSQL.

    Task 2 - Data Modeling and Transformation with DBT
        Create staging models to clean and normalize raw data.
        Build data mart models using star schema:
             dim_channels, dim_dates, fct_messages
             Validate with tests (unique, not_null, and one custom test).
             Use dbt docs to generate documentation.
