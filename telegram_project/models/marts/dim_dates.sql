-- models/marts/dim_dates.sql

WITH dates AS (
    SELECT DISTINCT DATE(message_timestamp) AS date_day
    FROM {{ ref('stg_telegram_messages') }}
)

SELECT
    date_day,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(WEEK FROM date_day) AS week,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(YEAR FROM date_day) AS year
FROM dates
