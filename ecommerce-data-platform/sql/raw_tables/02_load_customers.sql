USE DATABASE ECOMMERCE_DATA_PLATFORM;

USE SCHEMA RAW;

COPY INTO CUSTOMERS (
    CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    CREATED_AT,
    REGION,
    SEGMENT,
    STATUS,
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
        $7,
        METADATA$FILENAME
    FROM @ECOMMERCE_S3_STAGE/raw/customers/run_date={{ params.run_date }}/
)
FILE_FORMAT = CSV_FORMAT;