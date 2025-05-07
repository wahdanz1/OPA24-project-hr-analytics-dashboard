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
-- script does this: 
-- 1. Get all columns from the relation.
-- 2. Loop through each column and check if it is in the list of columns to format.
-- 3. If it is, apply the `capitalize_first_letter` macro to that column and append it to the result list.
-- 4. If it is not, simply append the column name to the result list.
-- 5. Finally, return the result list as a comma-separated string.

