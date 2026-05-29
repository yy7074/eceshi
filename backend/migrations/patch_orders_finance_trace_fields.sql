-- 订单支付来源、人工还款、销售归属、订单文件字段
ALTER TABLE orders
  ADD COLUMN payment_source VARCHAR(30) NULL COMMENT '资金来源: prepaid/credit/mixed/wechat/alipay' AFTER credit_amount,
  ADD COLUMN repayment_status VARCHAR(20) DEFAULT 'not_required' COMMENT '还款状态: not_required/pending/partial/paid' AFTER payment_source,
  ADD COLUMN repayment_method VARCHAR(30) NULL COMMENT '还款方式: wechat/alipay/transfer/prepaid/other' AFTER repayment_status,
  ADD COLUMN repayment_amount DECIMAL(10,2) DEFAULT 0 COMMENT '已登记还款金额' AFTER repayment_method,
  ADD COLUMN repayment_time DATETIME NULL COMMENT '最近还款登记时间' AFTER repayment_amount,
  ADD COLUMN repayment_records JSON NULL COMMENT '还款记录明细' AFTER repayment_time,
  ADD COLUMN sales_id BIGINT NULL COMMENT '对接销售/老师ID' AFTER repayment_records,
  ADD COLUMN sales_name VARCHAR(50) NULL COMMENT '对接销售/老师姓名' AFTER sales_id,
  ADD COLUMN sales_phone VARCHAR(20) NULL COMMENT '对接销售/老师电话' AFTER sales_name,
  ADD COLUMN report_url VARCHAR(500) NULL COMMENT '测试报告文件链接' AFTER payment_time,
  ADD COLUMN checklist_url VARCHAR(500) NULL COMMENT '测试清单文件链接' AFTER report_url,
  ADD COLUMN invoice_file_url VARCHAR(500) NULL COMMENT '订单发票文件链接' AFTER checklist_url;

CREATE INDEX idx_orders_repayment_status ON orders (repayment_status);
