USE DATABASE ECOMMERCE_DATA_PLATFORM;
USE SCHEMA RAW;

COPY INTO ORDERS (
    ORDER_ID,
    CUSTOMER_ID,
    ORDER_TS,
    STATUS,
    CHANNEL,
    SOURCE_FILE
)
FROM (
    SELECT
        $1:order_id::VARCHAR,
        $1:customer_id::VARCHAR,
        $1:order_ts::TIMESTAMP_NTZ,
        $1:status::VARCHAR,
        $1:channel::VARCHAR,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/orders/run_date=2026-08-31/
)
FILE_FORMAT = JSON_FORMAT;

COPY INTO ORDER_ITEMS (
    ORDER_ITEM_ID,
    ORDER_ID,
    PRODUCT_ID,
    QUANTITY,
    UNIT_PRICE,
    DISCOUNT,
    SOURCE_FILE
)
FROM (
    SELECT
        $1:order_item_id::VARCHAR,
        $1:order_id::VARCHAR,
        $1:product_id::VARCHAR,
        $1:quantity::NUMBER,
        $1:unit_price::NUMBER(10,2),
        $1:discount::NUMBER(10,2),
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/order_items/run_date=2026-08-31/
)
FILE_FORMAT = JSON_FORMAT;

COPY INTO WEB_EVENTS (
    EVENT_ID,
    SESSION_ID,
    EVENT_TYPE,
    PRODUCT_ID,
    TRAFFIC_SOURCE,
    EVENT_TS,
    SOURCE_FILE
)
FROM (
    SELECT
        $1:event_id::VARCHAR,
        $1:session_id::VARCHAR,
        $1:event_type::VARCHAR,
        $1:product_id::VARCHAR,
        $1:traffic_source::VARCHAR,
        $1:event_ts::TIMESTAMP_NTZ,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/web_events/run_date=2026-08-31/
)
FILE_FORMAT = JSON_FORMAT;

SELECT 'ORDERS' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM ORDERS
UNION ALL
SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
UNION ALL
SELECT 'WEB_EVENTS', COUNT(*) FROM WEB_EVENTS;