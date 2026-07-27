SELECT *
FROM orders
WHERE 1=1
{% if start_date is not none %}
AND order_date >= :start_date
{% endif %}
{% if end_date is not none %}
AND order_date <= :end_date
{% endif %}