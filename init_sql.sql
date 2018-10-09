

-- ----------------------------
-- Table structure for t_target_mark
-- ----------------------------
DROP TABLE IF EXISTS `t_target_mark`;
CREATE TABLE `t_target_mark` (
  `id` bigint(15) NOT NULL AUTO_INCREMENT,
  `u_id` bigint(15) NOT NULL,
  `t_id` bigint(15) NOT NULL,
  `count` int(11) DEFAULT '0',
  `mark_date` varchar(32) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_user_device
-- ----------------------------
DROP TABLE IF EXISTS `t_user_device`;
CREATE TABLE `t_user_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` bigint(15) NOT NULL,
  `mac` varchar(64) DEFAULT NULL,
  `imei` varchar(64) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_user_info
-- ----------------------------
DROP TABLE IF EXISTS `t_user_info`;
CREATE TABLE `t_user_info` (
  `id` bigint(15) NOT NULL AUTO_INCREMENT,
  `account` varchar(45) NOT NULL,
  `username` varchar(45) DEFAULT NULL,
  `passwd` varchar(64) DEFAULT NULL,
  `mail` varchar(64) DEFAULT NULL,
  `wechat` varchar(64) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `can_update` tinyint(1) DEFAULT '1',
  `send_flag` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_UNIQUE` (`account`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_user_target
-- ----------------------------
DROP TABLE IF EXISTS `t_user_target`;
CREATE TABLE `t_user_target` (
  `id` bigint(15) NOT NULL AUTO_INCREMENT,
  `u_id` bigint(15) DEFAULT NULL,
  `target_type` int(11) NOT NULL,
  `target_content` varchar(128) DEFAULT NULL,
  `target_count` int(11) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_vtarget_dict
-- ----------------------------
DROP TABLE IF EXISTS `t_vtarget_dict`;
CREATE TABLE `t_vtarget_dict` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `value` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `pic_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_type_value` (`value`,`type`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;



insert into vtarget.t_vtarget_dict  (name,value,type) values('读书',1,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('写作',2,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('运动',3,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('唱歌',4,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('摄影',5,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('学习',6,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('娱乐',7,1);
insert into vtarget.t_vtarget_dict  (name,value,type) values('生活',8,1);
