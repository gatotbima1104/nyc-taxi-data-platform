{% macro filter_trip_month(column_name) %}

{{ column_name }} >= to_date('{{ var("trip_month") }}', 'YYYY-MM')
and
{{ column_name }} < (
    to_date('{{ var("trip_month") }}', 'YYYY-MM')
    + interval '1 month'
)

{% endmacro %}