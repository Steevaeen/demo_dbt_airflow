
  create view "mydb"."public"."stg_sales__dbt_tmp"
    
    
  as (
    

SELECT 
    id,
    sale_date,
    amount,
    customer_id
FROM raw_sales
  );