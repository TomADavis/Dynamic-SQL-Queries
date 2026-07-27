SELECT *
FROM orders
{% if FILTERS %}
WHERE {{ FILTERS }}
{% endif %}
