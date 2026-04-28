-- 动态树形选项配置扩展
-- 说明：支持节点独立配置是否展开子选项、是否选中后输入、单个/多个输入模式

ALTER TABLE project_options
ADD COLUMN IF NOT EXISTS allow_children BOOLEAN DEFAULT TRUE COMMENT '是否需要/允许展开子选项';

ALTER TABLE project_options
ADD COLUMN IF NOT EXISTS requires_input BOOLEAN DEFAULT FALSE COMMENT '选中后是否需要填写输入内容';

ALTER TABLE project_options
ADD COLUMN IF NOT EXISTS input_mode VARCHAR(20) DEFAULT 'single' COMMENT '输入模式: single/multiple';

UPDATE project_options
SET
  allow_children = CASE WHEN option_type = 'input' THEN FALSE ELSE COALESCE(allow_children, TRUE) END,
  requires_input = CASE WHEN option_type = 'input' THEN TRUE ELSE COALESCE(requires_input, FALSE) END,
  input_mode = COALESCE(input_mode, 'single');
