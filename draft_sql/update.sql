SELECT * FROM classicmodels.orders_copy;

SET SQL_SAFE_UPDATES = 0;
update classicmodels.orders_copy join classicmodels.customers
set classicmodels.orders_copy.status='EMBARGOED'
where (classicmodels.orders_copy.status<>'SHIPPED' and classicmodels.orders_copy.status<>'CANCELLED') and 
classicmodels.customers.country='Australia';
SET SQL_SAFE_UPDATES = 1;

select
	customers.customerNumber, customers.country, orders_copy.orderNumber, orders_copy.status from
    customers join orders_copy
    using (customerNumber)
    where country = 'Australia'
order by status;

