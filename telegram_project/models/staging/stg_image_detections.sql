SELECT CAST(message_id AS TEXT) AS message_id,
    file_name,
    object_class AS detected_object_class,
    confidence_score
FROM {{ source('raw', 'image_detections')}}