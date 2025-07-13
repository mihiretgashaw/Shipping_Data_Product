SELECT DISTINCT message_date::date AS date,
    EXTRACT(
        DAY
        FROM message_date
    ) AS day,
    EXTRACT(
        MONTH
        FROM message_date
    ) AS month,
    EXTRACT(
        YEAR
        FROM message_date
    ) AS year
FROM {{ ref('stg_telegram_messages')}}