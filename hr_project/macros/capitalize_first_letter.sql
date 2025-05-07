-- macros/capitalize_first_letter.sql
{% macro capitalize_first_letter(column_name) %}
    upper(left({{ column_name }}, 1)) || lower(substring({{ column_name }}, 2))
{% endmacro %}

--  1 This macro capitalizes the first letter of a given column name and converts the rest to lowercase.
--  2 It is useful for normalizing string data in a consistent format.
--  3 The macro takes a single argument, `column_name`, which is the name of the column to be formatted.