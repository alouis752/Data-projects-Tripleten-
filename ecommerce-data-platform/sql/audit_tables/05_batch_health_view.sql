CREATE OR REPLACE VIEW
    ECOMMERCE_DATA_PLATFORM.AUDIT.BATCH_HEALTH AS

SELECT
    run_date,
    COUNT(*) AS datasets_loaded,
    SUM(records_loaded) AS total_records_loaded,

    COUNT_IF(
        validation_status = 'valid'
    ) AS datasets_valid,

    COUNT_IF(
        load_status = 'success'
    ) AS datasets_successful,

    COUNT_IF(
        error_message IS NOT NULL
    ) AS datasets_with_errors,

    CASE
        WHEN COUNT(*) = 9
            AND COUNT_IF(validation_status = 'valid') = 9
            AND COUNT_IF(load_status = 'success') = 9
        THEN 'SUCCESS'
        ELSE 'INCOMPLETE'
    END AS batch_status,

    MAX(load_completed_at) AS batch_completed_at

FROM
    ECOMMERCE_DATA_PLATFORM.AUDIT.PIPELINE_LOAD_AUDIT

GROUP BY
    run_date;