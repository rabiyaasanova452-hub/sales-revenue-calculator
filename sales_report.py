
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="sales.log",
    encoding="utf-8"
)

logging.info("Анализ продаж начат")

try:
    df = pd.read_csv("sales.csv")
    logging.info("Данные успешно загружены")

    # Проверяем наличие обязательных столбцов
    required_columns = ["product", "sales"]
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Отсутствуют столбцы: {', '.join(missing_columns)}"
        )

    # Проверяем, что продажи представлены числами
    sales_numeric = pd.to_numeric(df["sales"], errors="coerce")
    invalid_sales = sales_numeric.isna() & df["sales"].notna()

    if invalid_sales.any() or sales_numeric.isna().any():
        logging.error("В столбце sales обнаружены некорректные или пустые значения")
        print("Ошибка: проверьте столбец sales — есть пустые или нечисловые значения")
    else:
        df["sales"] = sales_numeric

        # Проверяем отрицательные продажи
        if (df["sales"] < 0).any():
            logging.error("Обнаружены отрицательные значения в sales")
            print("Ошибка: обнаружены отрицательные продажи. Отчёт не сформирован")
        elif df.empty:
            logging.warning("Файл не содержит строк с данными")
            print("Ошибка: файл не содержит данных")
        else:
            # Анализ продаж
            total_sales = df["sales"].sum()
            sales_by_product = df.groupby("product")["sales"].sum()

            best_product = sales_by_product.idxmax()
            best_sales = sales_by_product.max()

            print(f"Общая сумма продаж: {total_sales} тенге")
            print(f"Товар с наибольшими продажами: {best_product}")
            print(f"Сумма продаж этого товара: {best_sales} тенге")

            logging.info("Анализ продаж успешно завершён")

except FileNotFoundError:
    logging.error("Файл sales.csv не найден")
    print("Ошибка: файл sales.csv не найден")

except KeyError as error:
    logging.error("Ошибка структуры данных: %s", error)
    print(f"Ошибка: {error}")

except pd.errors.EmptyDataError:
    logging.error("Файл sales.csv пуст")
    print("Ошибка: файл sales.csv пуст или не содержит заголовков")



