-- 动态表单配置扩展：添加 group_name 和 display_inline 字段
-- 执行时间: 2024-xx-xx
-- 说明: 支持表单字段分组显示和行内布局配置

-- 添加分组名称字段
ALTER TABLE project_options 
ADD COLUMN IF NOT EXISTS group_name VARCHAR(100) COMMENT '分组名称（如：样品信息、测试参数、服务选项）';

-- 添加行内显示配置字段
ALTER TABLE project_options 
ADD COLUMN IF NOT EXISTS display_inline BOOLEAN DEFAULT FALSE COMMENT '是否行内显示（标签+控件同行）';

-- 更新已有记录的默认值
UPDATE project_options SET display_inline = FALSE WHERE display_inline IS NULL;

-- 创建索引优化按分组查询
CREATE INDEX IF NOT EXISTS idx_project_options_group_name ON project_options(group_name);
