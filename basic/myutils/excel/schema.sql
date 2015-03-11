-- 用户表
DROP TABLE IF EXISTS t_user;
CREATE TABLE t_user (
  id                BIGINT PRIMARY KEY COMMENT '主键ID',
  username          VARCHAR(32)  NOT NULL COMMENT '用户名',
  password          VARCHAR(32) NOT NULL COMMENT '密码',
  fullname          VARCHAR(10) COMMENT '中文名',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户表';

-- 角色表
DROP TABLE IF EXISTS t_role;
CREATE TABLE t_role (
  id                BIGINT PRIMARY KEY COMMENT '主键ID',
  name              VARCHAR(30)  NOT NULL COMMENT '角色名',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '角色表';

-- 用户角色表
DROP TABLE IF EXISTS t_user_role;
CREATE TABLE t_user_role (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  user_id            BIGINT  NOT NULL COMMENT '用户ID',
  role_id            BIGINT  NOT NULL COMMENT '角色ID',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户角色表';

-- 权限表
DROP TABLE IF EXISTS t_privilege;
CREATE TABLE t_privilege (
  id                BIGINT PRIMARY KEY COMMENT '主键ID',
  name              VARCHAR(30)  NOT NULL COMMENT '权限名',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '权限表';

-- 角色权限表
DROP TABLE IF EXISTS t_role_privilege;
CREATE TABLE t_role_privilege (
  id                BIGINT PRIMARY KEY COMMENT '主键ID',
  role_id           BIGINT  NOT NULL COMMENT '角色ID',
  privilege_id      BIGINT  NOT NULL COMMENT '权限ID',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '角色权限表';

-- 企业基本资料表
DROP TABLE IF EXISTS t_company;
CREATE TABLE t_company (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  name               VARCHAR(80)  NOT NULL COMMENT '企业名称',
  taxno              VARCHAR(60)  NOT NULL COMMENT '税号',
  reg_location      VARCHAR(80)  COMMENT '注册地',
  reg_time           DATETIME COMMENT '注册时间',
  business_years    INT COMMENT '经营时间，以年为单位',
  core_flag          VARCHAR(2) COMMENT '是否核心企业：是/否',
  account_bank       VARCHAR(30) COMMENT '开户银行',
  tax_amount         INT COMMENT '该企业近一年的纳税额，以万为单位',
  comp_location      VARCHAR(100) COMMENT '企业地址',
  area                VARCHAR(30) COMMENT '所属片区',
  status              VARCHAR(20) COMMENT '业务状态',
  created_time       DATETIME COMMENT '创建时间',
  updated_time       DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '企业基本资料表';

-- 企业联系方式表
DROP TABLE IF EXISTS t_company_contact;
CREATE TABLE t_company_contact (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  company_id        BIGINT NOT NULL COMMENT '企业ID',
  name               VARCHAR(10) COMMENT '联系人姓名',
  mobile_number     VARCHAR(20) COMMENT '联系人电话',
  position           VARCHAR(30) COMMENT '联系人职位',
  remark             VARCHAR(100) COMMENT '备注',
  created_time       DATETIME COMMENT '创建时间',
  updated_time       DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '企业联系方式表';

-- 供应关系表
DROP TABLE IF EXISTS t_supply_relation;
CREATE TABLE t_supply_relation (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  company_id        BIGINT NOT NULL COMMENT '企业ID',
  corecomp_id       BIGINT NOT NULL COMMENT '所属核心企业ID',
  supply_years      INT COMMENT '供应时间，以年为单位',
  start_time        DATETIME COMMENT '供应开始时间',
  end_time          DATETIME COMMENT '最近供应时间',
  year_amount       INT COMMENT '年开票金额，以万为单位',
  total_amount      INT COMMENT '历史开票总额，以万为单位',
  created_time       DATETIME COMMENT '创建时间',
  updated_time       DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '供应关系表';

-- 拜访记录表
DROP TABLE IF EXISTS t_visit_record;
CREATE TABLE t_visit_record (
  id                  BIGINT PRIMARY KEY COMMENT '主键ID',
  company_id         BIGINT NOT NULL COMMENT '企业ID',
  corecomp_id        BIGINT NOT NULL COMMENT '所属核心企业ID',
  status              VARCHAR(10) COMMENT '拜访状态：未分配、已分配、接触中、有意向、没意向、已取数据。',
  customer_manager   VARCHAR(10) COMMENT '客户经理名称',
  contact_phone      VARCHAR(16) COMMENT '客户经理联系电话',
  no_intent_reason   VARCHAR(120) COMMENT '没意向原因',
  created_time       DATETIME COMMENT '创建时间',
  updated_time       DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '拜访记录表';

-- 企业意向表
DROP TABLE IF EXISTS t_company_intention;
CREATE TABLE t_company_intention (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  company_id        BIGINT NOT NULL COMMENT '企业ID',
  corecomp_id       BIGINT NOT NULL COMMENT '所属核心企业ID',
  loan_usage        VARCHAR(80) COMMENT '贷款用途',
  loan_amount       INT COMMENT '贷款金额，以万为单位',
  loan_cycle        VARCHAR(30) COMMENT '贷款周期，格式为年-月~年-月',
  repay_method      VARCHAR(30) COMMENT '还款方式',
  suggest_amount    INT COMMENT '建议额度，以万为单位',
  recommend_level   VARCHAR(2) COMMENT '推荐等级，字段值为A、B、C、D',
  evaluation         VARCHAR(120) COMMENT '评价',
  customer_manager   VARCHAR(10) COMMENT '客户经理名称',
  contact_phone      VARCHAR(16) COMMENT '客户经理联系电话',
  created_time       DATETIME COMMENT '创建时间',
  updated_time       DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '企业意向表';

-- 银行推荐表
DROP TABLE IF EXISTS t_bank_recommend;
CREATE TABLE t_bank_recommend (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  company_id        BIGINT NOT NULL COMMENT '企业ID',
  corecomp_id       BIGINT NOT NULL COMMENT '所属核心企业ID',
  accept_bank       VARCHAR(30) COMMENT '受理银行',
  recommend_status  VARCHAR(10) COMMENT '推荐状态',
  recommend_time    DATETIME COMMENT '推荐时间',
  failure_reason    VARCHAR(120) COMMENT '失败原因',
  credit_line       INT COMMENT '授信额度，以万为单位',
  finish_time       DATETIME COMMENT '完成时间',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '银行推荐表';

-- 银行认可表
DROP TABLE IF EXISTS t_bank_recognize;
CREATE TABLE t_bank_recognize (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  company_id        BIGINT NOT NULL COMMENT '企业ID',
  recognize_bank    VARCHAR(30) COMMENT '认可银行',
  created_time      DATETIME COMMENT '创建时间',
  updated_time      DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '银行认可表';

-- 上传文件记录表
DROP TABLE IF EXISTS t_upload_record;
CREATE TABLE t_upload_record (
  id                 BIGINT PRIMARY KEY COMMENT '主键ID',
  file_name         VARCHAR(60) COMMENT '上传文件名称',
  store_location    VARCHAR(80) COMMENT '上传文件的备份地址',
  uploader           VARCHAR(10) COMMENT '上传者',
  upload_time        DATETIME COMMENT '上传时间',
  created_time       DATETIME COMMENT '创建时间',
  updated_time       DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '上传文件记录表';

