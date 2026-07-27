SELECT title
FROM films
{% if FILTERS %}
WHERE {{ FILTERS }}
{% endif %}
