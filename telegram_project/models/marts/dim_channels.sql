SELECT DISTINCT channel_name,
    MD5(channel_name) AS channel_id -- surrogate key
FROM {{ ref('stg_telegram_messages')}}