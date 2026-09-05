USE DATABASE ECOMMERCE_DATA_PLATFORM;
USE SCHEMA RAW;

COPY INTO PRODUCTS (
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    PRICE,
    COST,
    ACTIVE_FLAG,
    SOURCE_FILE
)
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/products/run_date={{ params.run_date }}/
)
FILE_FORMAT = CSV_FORMAT;


COPY INTO PAYMENTS (
    PAYMENT_ID,
    ORDER_ID,
    AMOUNT,
    PAYMENT_METHOD,
    PAYMENT_STATUS,
    PAYMENT_TS,
    SOURCE_FILE
)
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/payments/run_date={{ params.run_date }}/
)
FILE_FORMAT = CSV_FORMAT;


COPY INTO SHIPMENTS (
    SHIPMENT_ID,
    ORDER_ID,
    SHIPPED_AT,
    DELIVERED_AT,
    CARRIER,
    SOURCE_FILE
)
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/shipments/run_date={{ params.run_date }}/
)
FILE_FORMAT = CSV_FORMAT;


COPY INTO RETURNS (
    RETURN_ID,
    ORDER_ID,
    RETURNED_AT,
    RETURN_AMOUNT,
    RETURN_REASON,
    SOURCE_FILE
)
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/returns/run_date={{ params.run_date }}/
)
FILE_FORMAT = CSV_FORMAT;


COPY INTO INVENTORY (
    PRODUCT_ID,
    SNAPSHOT_TS,
    QUANTITY_ON_HAND,
    REORDER_POINT,
    SOURCE_FILE
)
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/inventory/run_date={{ params.run_date }}/
)
FILE_FORMAT = CSV_FORMAT;


SELECT
    'PRODUCTS' AS TABLE_NAME,
    COUNT(*) AS ROW_COUNT
FROM PRODUCTS

UNION ALL

SELECT
    'PAYMENTS',
    COUNT(*)
FROM PAYMENTS

UNION ALL

SELECT
    'SHIPMENTS',
    COUNT(*)
FROM SHIPMENTS

UNION ALL

SELECT
    'RETURNS',
    COUNT(*)
FROM RETURNS

UNION ALL

SELECT
    'INVENTORY',
    COUNT(*)
FROM INVENTORY;