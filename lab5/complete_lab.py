import great_expectations as gx
import pandas as pd
import os
import shutil

if os.path.exists("gx"):
    shutil.rmtree("gx")
context = gx.get_context(mode="file")

# Подключение источников данных
datasource_csv = context.sources.add_pandas("historical_sales_datasource")
asset_csv = datasource_csv.add_csv_asset(
    name="reference_data", filepath_or_buffer="historical_sales.csv"
)

datasource_sql = context.sources.add_sqlite(
    name="sales_warehouse_datasource", connection_string="sqlite:///sales_warehouse.db"
)
asset_sql = datasource_sql.add_table_asset(
    name="daily_sales_table", table_name="daily_sales"
)

# Автопрофилирование CSV
batch_request_csv = asset_csv.build_batch_request()
data_assistant_result = context.assistants.onboarding.run(
    batch_request=batch_request_csv
)
suite_auto = data_assistant_result.get_expectation_suite()
suite_name_auto = suite_auto.expectation_suite_name
context.add_or_update_expectation_suite(expectation_suite=suite_auto)

# Запуск чекпоинта
checkpoint_auto = context.add_checkpoint(
    name="auto_profiling_checkpoint",
    config_version=1.0,
    class_name="SimpleCheckpoint",
    validations=[
        {"batch_request": batch_request_csv, "expectation_suite_name": suite_name_auto}
    ],
)
context.run_checkpoint(checkpoint_name="auto_profiling_checkpoint")

# Ручные проверки SQL
suite_name_manual = "daily_sales_manual_suite"
context.add_or_update_expectation_suite(suite_name_manual)

batch_request_sql = asset_sql.build_batch_request()
validator_sql = context.get_validator(
    batch_request=batch_request_sql, expectation_suite_name=suite_name_manual
)

validator_sql.expect_column_values_to_not_be_null(column="amount")
validator_sql.expect_column_values_to_be_between(
    column="amount", min_value=0, strict_min=True
)
validator_sql.expect_column_values_to_match_regex(
    column="user_email", regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

# Проверка дрейфа категорий
df_hist = pd.read_csv("historical_sales.csv")
category_dist = df_hist["category"].value_counts(normalize=True).to_dict()
categories = ["Electronics", "Clothing", "Home", "Books"]
partition_object = {
    "values": categories,
    "weights": [category_dist.get(cat, 0.0) for cat in categories],
}
validator_sql.expect_column_kl_divergence_to_be_less_than(
    column="category", partition_object=partition_object, threshold=0.6
)

validator_sql.save_expectation_suite(discard_failed_expectations=False)

# Запуск чекпоинта
checkpoint_name = "daily_sales_checkpoint"
checkpoint = context.add_checkpoint(
    name=checkpoint_name,
    config_version=1.0,
    class_name="SimpleCheckpoint",
    validations=[
        {
            "batch_request": batch_request_sql,
            "expectation_suite_name": suite_name_manual,
        }
    ],
)

result = context.run_checkpoint(checkpoint_name=checkpoint_name)
validation_result = list(result.run_results.values())[0]["validation_result"]
stats = validation_result["statistics"]

print(f"Успешных проверок: {stats['successful_expectations']}")
print(f"Неуспешных проверок: {stats['unsuccessful_expectations']}")

context.build_data_docs()
context.open_data_docs()
