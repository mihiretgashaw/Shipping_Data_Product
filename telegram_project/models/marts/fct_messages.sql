SELECT m.message_id,
    c.channel_id,
    d.date,
    m.sender_id,
    m.message_length,
    m.has_image
FROM {{ ref('stg_telegram_messages')}} m
    JOIN {{ ref('dim_channels')}} c ON m.channel_name = c.channel_name
    JOIN {{ ref('dim_dates')}} d ON m.message_date::date = d.date