WITH source AS (
    SELECT *
    FROM raw.telegram_messages
)
SELECT message_id,
    channel_name,
    sender_id,
    message_text,
    message_date::timestamp AS message_date,
    LENGTH(message_text) AS message_length,
    FALSE AS has_image
FROM source
WHERE message_text IS NOT NULL
    AND TRIM(message_text) <> ''