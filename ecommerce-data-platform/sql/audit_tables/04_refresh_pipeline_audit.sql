USE DATABASE ECOMMERCE_DATA_PLATFORM;
USE SCHEMA AUDIT;

-- Remove the temporary audit records created during development.
TRUNCATE TABLE PIPELINE_LOAD_AUDIT;


MERGE INTO PIPELINE_LOAD_AUDIT AS target

USING (

    WITH load_history AS (

        SELECT
            'customers' AS dataset_name,
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.CUSTOMERS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'products',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.PRODUCTS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'orders',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.ORDERS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'order_items',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.ORDER_ITEMS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'payments',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.PAYMENTS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'shipments',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.SHIPMENTS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'returns',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.RETURNS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'inventory',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.INVENTORY',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )

        UNION ALL

        SELECT
            'web_events',
            file_name,
            status,
            row_count,
            row_parsed,
            first_error_message,
            last_load_time
        FROM TABLE(
            ECOMMERCE_DATA_PLATFORM.INFORMATION_SCHEMA.COPY_HISTORY(
                TABLE_NAME => 'ECOMMERCE_DATA_PLATFORM.RAW.WEB_EVENTS',
                START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())
            )
        )
    )

    SELECT
        SPLIT_PART(
            SPLIT_PART(file_name, 'run_date=', 2),
            '/',
            1
        )::DATE AS run_date,

        dataset_name,

        SPLIT_PART(file_name, '/', -1) AS source_file,

        REGEXP_REPLACE(
            file_name,
            '^s3://[^/]+/',
            ''
        ) AS s3_key,

        row_parsed AS row_count,

        CASE
            WHEN status = 'Loaded' THEN 'success'
            ELSE LOWER(REPLACE(status, ' ', '_'))
        END AS load_status,

        row_count AS records_loaded,

        first_error_message AS error_message,

        last_load_time AS load_completed_at

    FROM load_history

) AS source

ON  target.dataset_name = source.dataset_name
AND target.s3_key = source.s3_key

WHEN MATCHED THEN UPDATE SET

    target.row_count = source.row_count,
    target.load_status = source.load_status,
    target.records_loaded = source.records_loaded,
    target.error_message = source.error_message,
    target.load_completed_at = source.load_completed_at

WHEN NOT MATCHED THEN INSERT (

    run_date,
    dataset_name,
    source_file,
    s3_key,
    file_checksum,
    row_count,
    validation_status,
    load_status,
    records_loaded,
    error_message,
    load_started_at,
    load_completed_at

)
VALUES (

    source.run_date,
    source.dataset_name,
    source.source_file,
    source.s3_key,
    NULL,
    source.row_count,
    'valid',
    source.load_status,
    source.records_loaded,
    source.error_message,
    NULL,
    source.load_completed_at
);


SELECT
    run_date,
    dataset_name,
    source_file,
    row_count,
    records_loaded,
    load_status,
    load_completed_at
FROM PIPELINE_LOAD_AUDIT
ORDER BY dataset_name;