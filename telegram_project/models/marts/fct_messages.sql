with stg as (
  select *
  from {{ ref('stg_telegram_messages')}}
)
select message_id,
  sender_id,
  has_image,
  length(text) as message_length,
  date_trunc('day', message_timestamp) as message_date
from stg