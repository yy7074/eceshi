"""
Ensure project_options has the columns required by dynamic option management.

This script is intentionally compatible with MySQL 5.7, where
`ALTER TABLE ... ADD COLUMN IF NOT EXISTS` is not available.
"""
from sqlalchemy import text

from app.core.database import engine


TABLE_NAME = "project_options"

REQUIRED_COLUMNS = {
    "allow_children": "ADD COLUMN allow_children TINYINT(1) DEFAULT 1 COMMENT '是否需要/允许展开子选项'",
    "requires_input": "ADD COLUMN requires_input TINYINT(1) DEFAULT 0 COMMENT '选中后是否需要填写输入内容'",
    "input_mode": "ADD COLUMN input_mode VARCHAR(20) DEFAULT 'single' COMMENT '输入模式: single/multiple'",
    "group_name": "ADD COLUMN group_name VARCHAR(100) NULL COMMENT '分组名称（如：样品信息、测试参数、服务选项）'",
    "display_inline": "ADD COLUMN display_inline TINYINT(1) DEFAULT 0 COMMENT '是否行内显示（标签+控件同行）'",
}


def existing_columns(connection):
    rows = connection.execute(text(f"SHOW COLUMNS FROM {TABLE_NAME}")).fetchall()
    return {row[0] for row in rows}


def main():
    with engine.begin() as connection:
        columns = existing_columns(connection)
        added = []

        for column_name, ddl in REQUIRED_COLUMNS.items():
            if column_name not in columns:
                connection.execute(text(f"ALTER TABLE {TABLE_NAME} {ddl}"))
                added.append(column_name)

        connection.execute(text(
            """
            UPDATE project_options
            SET
              allow_children = CASE
                WHEN option_type = 'input' THEN 0
                ELSE COALESCE(allow_children, 1)
              END,
              requires_input = CASE
                WHEN option_type = 'input' THEN 1
                ELSE COALESCE(requires_input, 0)
              END,
              input_mode = COALESCE(input_mode, 'single'),
              display_inline = COALESCE(display_inline, 0)
            """
        ))

    if added:
        print(f"Added columns: {', '.join(added)}")
    else:
        print("project_options columns already up to date")


if __name__ == "__main__":
    main()
