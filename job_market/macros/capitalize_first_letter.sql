-- Capitalizes the first letter of the input column and lowercases the rest.
-- Useful for normalizing inconsistent string casing (e.g. 'sTOCKholm' or 'STOCKHOLM' → 'Stockholm').

{% macro capitalize_first_letter(column_name) %}
    upper(left({{ column_name }}, 1)) || lower(substring({{ column_name }}, 2))
{% endmacro %}