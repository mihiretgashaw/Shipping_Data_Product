-- SELECT det.message_id,
--     det.file_name,
--     det.detected_object_class,
--     det.confidence_score,
--     msg.channel_name,
--     msg.message_timestamp
-- FROM {{ ref('stg_image_detections')}} AS det
--     LEFT JOIN {{ ref('stg_telegram_messages')}} AS msg
--     ON CAST(det.message_id AS INTEGER) = msg.message_id

WITH valid_detections AS (
    SELECT *
    FROM {{ ref('stg_image_detections') }}
    WHERE message_id IS NOT NULL AND message_id ~ '^\d+$'
)

SELECT 
    det.message_id,
    det.file_name,
    det.detected_object_class,
    det.confidence_score,
    msg.channel_name,
    msg.message_timestamp
FROM valid_detections AS det
LEFT JOIN {{ ref('stg_telegram_messages') }} AS msg
    ON CAST(det.message_id AS INTEGER) = msg.message_id
