SELECT
    CAST(message_id AS INTEGER) AS message_id,
    object_class,
    confidence_score
FROM {{ source('raw', 'image_detections')}}
