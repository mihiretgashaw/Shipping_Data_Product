WITH messages AS (
    SELECT *
    FROM {{ ref('stg_telegram_messages')}}
),
channels AS (
    SELECT DISTINCT channel_name
    FROM messages
)
SELECT channel_name,
    'Channel ' || channel_name AS channel_display_name
FROM channels