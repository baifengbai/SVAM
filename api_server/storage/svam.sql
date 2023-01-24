-- Adminer 4.8.1 MySQL 5.5.5-10.10.2-MariaDB-1:10.10.2+maria~ubu2204 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `svam`;
CREATE DATABASE `svam` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `svam`;

DROP TABLE IF EXISTS `source_info`;
CREATE TABLE `source_info` (
  `id` mediumint(20) NOT NULL AUTO_INCREMENT COMMENT '数量id',
  `uuid` varchar(255) NOT NULL COMMENT '唯一id(数据源+内部类型+标题)',
  `title` varchar(255) NOT NULL COMMENT '标题',
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除标识',
  `data_type` varchar(255) NOT NULL COMMENT '素材源（抖音）',
  `inner_type` varchar(255) NOT NULL COMMENT '内部类型',
  `style` varchar(255) NOT NULL COMMENT '风格',
  `origin_time` datetime NOT NULL COMMENT '添加时间',
  `used_time` mediumint(20) NOT NULL DEFAULT 0 COMMENT '使用次数',
  `main_file` varchar(255) DEFAULT NULL COMMENT '主文件',
  `link_1` varchar(255) DEFAULT NULL COMMENT '关联1',
  `link_2` varchar(255) DEFAULT NULL COMMENT '关联2',
  `link_3` varchar(255) DEFAULT NULL COMMENT '关联3',
  `link_4` varchar(255) DEFAULT NULL COMMENT '关联4',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

TRUNCATE `source_info`;

-- 2023-01-24 14:51:16