SELECT title
FROM films
WHERE 1=1
{% if start_date is not none %}
AND release_date >= :start_date
{% endif %}
{% if end_date is not none %}
AND release_date <= :end_date
{% endif %}