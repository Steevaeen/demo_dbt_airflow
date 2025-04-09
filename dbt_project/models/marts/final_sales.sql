{{ config(materialized='table') }}

SELECT 
    s.sale_date,
    SUM(s.amount) as total_sales,
    COUNT(DISTINCT s.customer_id) as unique_customers
FROM {{ ref('stg_sales') }} s
GROUP BY s.sale_date