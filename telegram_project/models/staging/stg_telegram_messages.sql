WITH source AS (
    SELECT *
    FROM {{ source('raw', 'telegram_messages')}}
),
cleaned AS (
    SELECT CAST(message_id AS INTEGER) AS message_id,
        sender_id,
        message_text AS text,
        CAST(message_date AS TIMESTAMP) AS message_timestamp,
        channel_name,
        FALSE AS has_image
    FROM source
)
SELECT *
FROM cleaned