"""Apply 2026-05-28 finance trace fields idempotently.

Run from backend directory on the server:
    python3 migrations/apply_0528_finance_trace.py
"""
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import pymysql


def load_database_url() -> str:
    env_path = Path(".env")
    if not env_path.exists():
        raise RuntimeError(".env not found")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key == "DATABASE_URL":
            return value.strip().strip('"').strip("'")
    raise RuntimeError("DATABASE_URL not found in .env")


def connect():
    url = urlparse(load_database_url())
    if not url.scheme.startswith("mysql"):
        raise RuntimeError(f"Unsupported database URL scheme: {url.scheme}")

    query = parse_qs(url.query)
    charset = query.get("charset", ["utf8mb4"])[0]
    database = url.path.lstrip("/")
    if not database:
        raise RuntimeError("Database name is empty")

    return database, pymysql.connect(
        host=url.hostname or "127.0.0.1",
        port=url.port or 3306,
        user=unquote(url.username or ""),
        password=unquote(url.password or ""),
        database=database,
        charset=charset,
        autocommit=False,
    )


def existing_columns(cursor, database: str, table: str) -> set:
    cursor.execute(
        """
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        """,
        (database, table),
    )
    return {row[0] for row in cursor.fetchall()}


def ensure_columns(cursor, database: str, table: str, specs: list) -> list:
    columns = existing_columns(cursor, database, table)
    added = []
    for name, ddl in specs:
        if name in columns:
            continue
        cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{name}` {ddl}")
        columns.add(name)
        added.append(f"{table}.{name}")
    return added


def ensure_index(cursor, database: str, table: str, index_name: str, ddl: str) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND INDEX_NAME = %s
        """,
        (database, table, index_name),
    )
    if cursor.fetchone()[0]:
        return False
    cursor.execute(ddl)
    return True


def main():
    database, conn = connect()
    added = []
    with conn.cursor() as cursor:
        added.extend(ensure_columns(cursor, database, "orders", [
            ("payment_source", "VARCHAR(30) NULL COMMENT '资金来源: prepaid/credit/mixed/wechat/alipay'"),
            ("repayment_status", "VARCHAR(20) DEFAULT 'not_required' COMMENT '还款状态: not_required/pending/partial/paid'"),
            ("repayment_method", "VARCHAR(30) NULL COMMENT '还款方式: wechat/alipay/transfer/prepaid/other'"),
            ("repayment_amount", "DECIMAL(10,2) DEFAULT 0 COMMENT '已登记还款金额'"),
            ("repayment_time", "DATETIME NULL COMMENT '最近还款登记时间'"),
            ("repayment_records", "JSON NULL COMMENT '还款记录明细'"),
            ("sales_id", "BIGINT NULL COMMENT '对接销售/老师ID'"),
            ("sales_name", "VARCHAR(50) NULL COMMENT '对接销售/老师姓名'"),
            ("sales_phone", "VARCHAR(20) NULL COMMENT '对接销售/老师电话'"),
            ("report_url", "VARCHAR(500) NULL COMMENT '测试报告文件链接'"),
            ("checklist_url", "VARCHAR(500) NULL COMMENT '测试清单文件链接'"),
            ("invoice_file_url", "VARCHAR(500) NULL COMMENT '订单发票文件链接'"),
        ]))
        added.extend(ensure_columns(cursor, database, "users", [
            ("advisor_name", "VARCHAR(50) DEFAULT NULL COMMENT '专属顾问姓名'"),
            ("advisor_phone", "VARCHAR(20) DEFAULT NULL COMMENT '专属顾问电话'"),
        ]))

        if ensure_index(
            cursor,
            database,
            "orders",
            "idx_orders_repayment_status",
            "CREATE INDEX idx_orders_repayment_status ON orders (repayment_status)",
        ):
            added.append("index.orders.idx_orders_repayment_status")

        cursor.execute("UPDATE orders SET repayment_status = 'not_required' WHERE repayment_status IS NULL")
        cursor.execute(
            """
            UPDATE orders
            SET payment_source = CASE
                WHEN payment_method IN ('balance', 'prepaid') THEN 'prepaid'
                WHEN payment_method = 'credit' THEN 'credit'
                WHEN payment_method = 'mixed' THEN 'mixed'
                WHEN payment_method = 'wechat' THEN 'wechat'
                WHEN payment_method = 'alipay' THEN 'alipay'
                ELSE payment_source
            END
            WHERE payment_source IS NULL
            """
        )
        cursor.execute(
            """
            UPDATE orders
            SET repayment_status = 'pending'
            WHERE COALESCE(credit_amount, 0) > 0
              AND COALESCE(repayment_status, 'not_required') = 'not_required'
              AND status <> 'cancelled'
            """
        )

    conn.commit()
    conn.close()
    print("added=" + (",".join(added) if added else "none"))
    print("migration=ok")


if __name__ == "__main__":
    main()
