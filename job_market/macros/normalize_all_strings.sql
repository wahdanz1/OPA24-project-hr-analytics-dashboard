-- Applies formatting to a selected list of string columns in a relation.
-- 1. Gets all columns in the given relation.
-- 2. Capitalizes only those listed in `columns_to_format`.
-- 3. Leaves all other columns unchanged.
-- 4. Returns a comma-separated string of all column expressions.

{% macro normalize_all_strings(relation, columns_to_format=[]) %}
    {% set columns = adapter.get_columns_in_relation(relation) %}
    {% set result = [] %}

    {% for col in columns %}
        {% if col.name in columns_to_format %}
            {% do result.append(capitalize_first_letter(col.name) ~ ' as ' ~ col.name) %}
        {% else %}
            {% do result.append(col.name) %}
        {% endif %}
    {% endfor %}

    {{ return(result | join(', ')) }}
{% endmacro %}
