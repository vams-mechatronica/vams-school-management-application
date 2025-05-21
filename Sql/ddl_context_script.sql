-- MySQL dump 10.13  Distrib 9.3.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: vams_sms
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_user_id_2c513194_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_apkversion`
--

DROP TABLE IF EXISTS `api_apkversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_apkversion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `version` varchar(10) NOT NULL,
  `os` varchar(50) NOT NULL,
  `file` varchar(500) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_errorlog`
--

DROP TABLE IF EXISTS `api_errorlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_errorlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `error` varchar(255) NOT NULL,
  `description` longtext,
  `app_type` int NOT NULL,
  `level` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `attendance_staffattendance`
--

DROP TABLE IF EXISTS `attendance_staffattendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_staffattendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `status` int NOT NULL,
  `time_in` time(6) DEFAULT NULL,
  `time_out` time(6) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `staff_id` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `attendance_staffattendance_staff_id_66433418_fk_staffs_staff_id` (`staff_id`),
  CONSTRAINT `attendance_staffattendance_staff_id_66433418_fk_staffs_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staffs_staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `attendance_staffleaverequest`
--

DROP TABLE IF EXISTS `attendance_staffleaverequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_staffleaverequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` longtext NOT NULL,
  `status` int NOT NULL,
  `submitted_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `reviewed_by_id` int DEFAULT NULL,
  `staff_id` int NOT NULL,
  `staff_user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `attendance_staffleav_reviewed_by_id_0e24a0a4_fk_auth_user` (`reviewed_by_id`),
  KEY `attendance_staffleav_staff_id_e3b855a8_fk_staffs_st` (`staff_id`),
  KEY `attendance_staffleav_staff_user_id_4f673ee0_fk_auth_user` (`staff_user_id`),
  CONSTRAINT `attendance_staffleav_reviewed_by_id_0e24a0a4_fk_auth_user` FOREIGN KEY (`reviewed_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `attendance_staffleav_staff_id_e3b855a8_fk_staffs_st` FOREIGN KEY (`staff_id`) REFERENCES `staffs_staff` (`id`),
  CONSTRAINT `attendance_staffleav_staff_user_id_4f673ee0_fk_auth_user` FOREIGN KEY (`staff_user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `attendance_studentattendance`
--

DROP TABLE IF EXISTS `attendance_studentattendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_studentattendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `status` int NOT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `attendance_studentat_student_id_dd381c46_fk_students_` (`student_id`),
  CONSTRAINT `attendance_studentat_student_id_dd381c46_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=218 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_academicsession`
--

DROP TABLE IF EXISTS `corecode_academicsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_academicsession` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `current` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `end_date` date NOT NULL,
  `start_date` date NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_academicterm`
--

DROP TABLE IF EXISTS `corecode_academicterm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_academicterm` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `current` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `end_date` date NOT NULL,
  `start_date` date NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_classsubjectrelation`
--

DROP TABLE IF EXISTS `corecode_classsubjectrelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_classsubjectrelation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class_id_id` int NOT NULL,
  `subject_id` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `corecode_classsubjec_class_id_id_ba1e8c44_fk_corecode_` (`class_id_id`),
  KEY `corecode_classsubjec_subject_id_4f512d7b_fk_corecode_` (`subject_id`),
  CONSTRAINT `corecode_classsubjec_class_id_id_ba1e8c44_fk_corecode_` FOREIGN KEY (`class_id_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `corecode_classsubjec_subject_id_4f512d7b_fk_corecode_` FOREIGN KEY (`subject_id`) REFERENCES `corecode_subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_emailmessageimagelink`
--

DROP TABLE IF EXISTS `corecode_emailmessageimagelink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_emailmessageimagelink` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_1` varchar(100) DEFAULT NULL,
  `image_2` varchar(100) DEFAULT NULL,
  `image_3` varchar(100) DEFAULT NULL,
  `image_4` varchar(100) DEFAULT NULL,
  `image_5` varchar(100) DEFAULT NULL,
  `image_6` varchar(100) DEFAULT NULL,
  `image_7` varchar(100) DEFAULT NULL,
  `image_8` varchar(100) DEFAULT NULL,
  `image_9` varchar(100) DEFAULT NULL,
  `image_10` varchar(100) DEFAULT NULL,
  `image_11` varchar(100) DEFAULT NULL,
  `image_12` varchar(100) DEFAULT NULL,
  `image_13` varchar(100) DEFAULT NULL,
  `image_14` varchar(100) DEFAULT NULL,
  `image_15` varchar(100) DEFAULT NULL,
  `image_16` varchar(100) DEFAULT NULL,
  `image_17` varchar(100) DEFAULT NULL,
  `image_18` varchar(100) DEFAULT NULL,
  `image_19` varchar(100) DEFAULT NULL,
  `image_20` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_holiday`
--

DROP TABLE IF EXISTS `corecode_holiday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_holiday` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_schooldetail`
--

DROP TABLE IF EXISTS `corecode_schooldetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_schooldetail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `short_name` varchar(50) NOT NULL,
  `slogan` varchar(255) DEFAULT NULL,
  `address` longtext NOT NULL,
  `logo_vertical` varchar(100) DEFAULT NULL,
  `logo_horizontal` varchar(100) DEFAULT NULL,
  `favicon` varchar(100) DEFAULT NULL,
  `letterhead` varchar(100) DEFAULT NULL,
  `signature` varchar(100) DEFAULT NULL,
  `background_image` varchar(100) DEFAULT NULL,
  `authorized_signatory` varchar(100) DEFAULT NULL,
  `school_strength` int unsigned NOT NULL,
  `medium` varchar(10) NOT NULL,
  `subdomain` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `fee_collection` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `short_name` (`short_name`),
  UNIQUE KEY `subdomain` (`subdomain`),
  CONSTRAINT `corecode_schooldetail_chk_1` CHECK ((`school_strength` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_siteconfig`
--

DROP TABLE IF EXISTS `corecode_siteconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_siteconfig` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key` varchar(50) NOT NULL,
  `value` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `corecode_siteconfig_key_cede9740` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_studentclass`
--

DROP TABLE IF EXISTS `corecode_studentclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_studentclass` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `tuition_fees` decimal(10,2) NOT NULL,
  `computer_fees` decimal(10,2) NOT NULL,
  `admission_fees` decimal(10,2) NOT NULL,
  `exam_fees` decimal(10,2) NOT NULL,
  `miscellaneous` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corecode_subject`
--

DROP TABLE IF EXISTS `corecode_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corecode_subject` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `test_max_marks` int NOT NULL,
  `exam_max_marks` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `email_module_emailtemplate`
--

DROP TABLE IF EXISTS `email_module_emailtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `email_module_emailtemplate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `finance_invoice`
--

DROP TABLE IF EXISTS `finance_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finance_invoice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `month` varchar(50) DEFAULT NULL,
  `previous_balance` decimal(10,2) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `is_editable` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `class_for_id` int DEFAULT NULL,
  `session_id` int DEFAULT NULL,
  `student_id` int NOT NULL,
  `term_id` int DEFAULT NULL,
  `total_payable` decimal(10,2) NOT NULL,
  `due_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `finance_invoice_class_for_id_7f3077da_fk_corecode_` (`class_for_id`),
  KEY `finance_invoice_session_id_276e9d57_fk_corecode_` (`session_id`),
  KEY `finance_invoice_student_id_c9f27ede_fk_students_student_id` (`student_id`),
  KEY `finance_invoice_term_id_fd04ac73_fk_corecode_academicterm_id` (`term_id`),
  CONSTRAINT `finance_invoice_class_for_id_7f3077da_fk_corecode_` FOREIGN KEY (`class_for_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `finance_invoice_session_id_276e9d57_fk_corecode_` FOREIGN KEY (`session_id`) REFERENCES `corecode_academicsession` (`id`),
  CONSTRAINT `finance_invoice_student_id_c9f27ede_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`),
  CONSTRAINT `finance_invoice_term_id_fd04ac73_fk_corecode_academicterm_id` FOREIGN KEY (`term_id`) REFERENCES `corecode_academicterm` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1179 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `finance_invoicebulkupload`
--

DROP TABLE IF EXISTS `finance_invoicebulkupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finance_invoicebulkupload` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_uploaded` datetime(6) NOT NULL,
  `csv_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `finance_invoiceitem`
--

DROP TABLE IF EXISTS `finance_invoiceitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finance_invoiceitem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `class_for_id` int DEFAULT NULL,
  `invoice_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `finance_invoiceitem_class_for_id_e60d8f6d_fk_corecode_` (`class_for_id`),
  KEY `finance_invoiceitem_invoice_id_41505084_fk_finance_invoice_id` (`invoice_id`),
  CONSTRAINT `finance_invoiceitem_class_for_id_e60d8f6d_fk_corecode_` FOREIGN KEY (`class_for_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `finance_invoiceitem_invoice_id_41505084_fk_finance_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `finance_invoice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2361 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `finance_receipt`
--

DROP TABLE IF EXISTS `finance_receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finance_receipt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount_paid` decimal(10,2) NOT NULL,
  `payment_mode` varchar(50) NOT NULL,
  `date_paid` datetime(6) NOT NULL,
  `comment` longtext,
  `invoice_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `finance_receipt_invoice_id_28cc4014_fk_finance_invoice_id` (`invoice_id`),
  CONSTRAINT `finance_receipt_invoice_id_28cc4014_fk_finance_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `finance_invoice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_announcement`
--

DROP TABLE IF EXISTS `notifications_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_announcement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `delivery_type` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_announcement_recipients`
--

DROP TABLE IF EXISTS `notifications_announcement_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_announcement_recipients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `announcement_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notifications_announceme_announcement_id_user_id_5cf60e74_uniq` (`announcement_id`,`user_id`),
  KEY `notifications_announ_user_id_35c144f4_fk_auth_user` (`user_id`),
  CONSTRAINT `notifications_announ_announcement_id_b29a81da_fk_notificat` FOREIGN KEY (`announcement_id`) REFERENCES `notifications_announcement` (`id`),
  CONSTRAINT `notifications_announ_user_id_35c144f4_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_deliverednotification`
--

DROP TABLE IF EXISTS `notifications_deliverednotification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_deliverednotification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content_type` varchar(50) NOT NULL,
  `object_id` int unsigned NOT NULL,
  `delivered_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `mark_as_read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_delive_user_id_748c2e32_fk_auth_user` (`user_id`),
  CONSTRAINT `notifications_delive_user_id_748c2e32_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `notifications_deliverednotification_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `delivery_type` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_notification_recipients`
--

DROP TABLE IF EXISTS `notifications_notification_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification_recipients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `notification_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notifications_notificati_notification_id_user_id_afce4d82_uniq` (`notification_id`,`user_id`),
  KEY `notifications_notifi_user_id_d8bf565b_fk_auth_user` (`user_id`),
  CONSTRAINT `notifications_notifi_notification_id_89d40b7b_fk_notificat` FOREIGN KEY (`notification_id`) REFERENCES `notifications_notification` (`id`),
  CONSTRAINT `notifications_notifi_user_id_d8bf565b_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_shoutout`
--

DROP TABLE IF EXISTS `notifications_shoutout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_shoutout` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `delivery_type` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `sender_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_shoutout_sender_id_273d40dd_fk_auth_user_id` (`sender_id`),
  CONSTRAINT `notifications_shoutout_sender_id_273d40dd_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications_shoutout_recipients`
--

DROP TABLE IF EXISTS `notifications_shoutout_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_shoutout_recipients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shoutout_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notifications_shoutout_r_shoutout_id_user_id_bc2cbb6a_uniq` (`shoutout_id`,`user_id`),
  KEY `notifications_shouto_user_id_a63b9dec_fk_auth_user` (`user_id`),
  CONSTRAINT `notifications_shouto_shoutout_id_3b35f443_fk_notificat` FOREIGN KEY (`shoutout_id`) REFERENCES `notifications_shoutout` (`id`),
  CONSTRAINT `notifications_shouto_user_id_a63b9dec_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_n_assignments_classassignmentnproject`
--

DROP TABLE IF EXISTS `project_n_assignments_classassignmentnproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_n_assignments_classassignmentnproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(500) NOT NULL,
  `file` varchar(100) NOT NULL,
  `is_assignment_for_all` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `for_class_id` int NOT NULL,
  `user_id` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_n_assignment_for_class_id_08a4f0c4_fk_corecode_` (`for_class_id`),
  KEY `project_n_assignment_user_id_0dd85504_fk_auth_user` (`user_id`),
  CONSTRAINT `project_n_assignment_for_class_id_08a4f0c4_fk_corecode_` FOREIGN KEY (`for_class_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `project_n_assignment_user_id_0dd85504_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_n_assignments_classassignmentnproject_students`
--

DROP TABLE IF EXISTS `project_n_assignments_classassignmentnproject_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_n_assignments_classassignmentnproject_students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `classassignmentnproject_id` bigint NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_n_assignments_cl_classassignmentnproject__6685e504_uniq` (`classassignmentnproject_id`,`student_id`),
  KEY `project_n_assignment_student_id_0ed47f23_fk_students_` (`student_id`),
  CONSTRAINT `project_n_assignment_classassignmentnproj_0d02d85c_fk_project_n` FOREIGN KEY (`classassignmentnproject_id`) REFERENCES `project_n_assignments_classassignmentnproject` (`id`),
  CONSTRAINT `project_n_assignment_student_id_0ed47f23_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `result_result`
--

DROP TABLE IF EXISTS `result_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result_result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_score` int NOT NULL,
  `exam_score` int NOT NULL,
  `current_class_id` int NOT NULL,
  `session_id` int NOT NULL,
  `student_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `term_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `result_result_current_class_id_1504f130_fk_corecode_` (`current_class_id`),
  KEY `result_result_session_id_a3e8f31c_fk_corecode_academicsession_id` (`session_id`),
  KEY `result_result_student_id_59df1edd_fk_students_student_id` (`student_id`),
  KEY `result_result_subject_id_492309bd_fk_corecode_subject_id` (`subject_id`),
  KEY `result_result_term_id_2ed99f1a_fk_corecode_academicterm_id` (`term_id`),
  CONSTRAINT `result_result_current_class_id_1504f130_fk_corecode_` FOREIGN KEY (`current_class_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `result_result_session_id_a3e8f31c_fk_corecode_academicsession_id` FOREIGN KEY (`session_id`) REFERENCES `corecode_academicsession` (`id`),
  CONSTRAINT `result_result_student_id_59df1edd_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`),
  CONSTRAINT `result_result_subject_id_492309bd_fk_corecode_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `corecode_subject` (`id`),
  CONSTRAINT `result_result_term_id_2ed99f1a_fk_corecode_academicterm_id` FOREIGN KEY (`term_id`) REFERENCES `corecode_academicterm` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staffs_staff`
--

DROP TABLE IF EXISTS `staffs_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs_staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `current_status` tinyint(1) NOT NULL,
  `emp_code` varchar(200) NOT NULL,
  `surname` varchar(200) NOT NULL,
  `firstname` varchar(200) NOT NULL,
  `other_name` varchar(200) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `date_of_birth` date NOT NULL,
  `date_of_joining` date NOT NULL,
  `adhar_card_number` varchar(12) DEFAULT NULL,
  `mobile_number` varchar(13) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext NOT NULL,
  `others` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  `subject_expert_id` int DEFAULT NULL,
  `class_incharge_id` int DEFAULT NULL,
  `staff_category_id` int DEFAULT NULL,
  `pancard_number` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `emp_code` (`emp_code`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `staffs_staff_subject_expert_id_7ee997e5_fk_corecode_subject_id` (`subject_expert_id`),
  KEY `staffs_staff_class_incharge_id_abedb78a_fk_corecode_` (`class_incharge_id`),
  KEY `staffs_staff_staff_category_id_72cba59c_fk_staffs_st` (`staff_category_id`),
  CONSTRAINT `staffs_staff_class_incharge_id_abedb78a_fk_corecode_` FOREIGN KEY (`class_incharge_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `staffs_staff_staff_category_id_72cba59c_fk_staffs_st` FOREIGN KEY (`staff_category_id`) REFERENCES `staffs_staffcategory` (`id`),
  CONSTRAINT `staffs_staff_subject_expert_id_7ee997e5_fk_corecode_subject_id` FOREIGN KEY (`subject_expert_id`) REFERENCES `corecode_subject` (`id`),
  CONSTRAINT `staffs_staff_user_id_41ce53bd_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staffs_staff_subject_expert`
--

DROP TABLE IF EXISTS `staffs_staff_subject_expert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs_staff_subject_expert` (
  `id` int NOT NULL AUTO_INCREMENT,
  `staff_id` int NOT NULL,
  `subject_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staffs_staff_subject_expert_staff_id_subject_id_c983cd20_uniq` (`staff_id`,`subject_id`),
  KEY `staffs_staff_subject_subject_id_85dc1746_fk_corecode_` (`subject_id`),
  CONSTRAINT `staffs_staff_subject_expert_staff_id_b7d73ac8_fk_staffs_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staffs_staff` (`id`),
  CONSTRAINT `staffs_staff_subject_subject_id_85dc1746_fk_corecode_` FOREIGN KEY (`subject_id`) REFERENCES `corecode_subject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staffs_staffbulkupload`
--

DROP TABLE IF EXISTS `staffs_staffbulkupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs_staffbulkupload` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_uploaded` datetime(6) NOT NULL,
  `csv_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staffs_staffcategory`
--

DROP TABLE IF EXISTS `staffs_staffcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs_staffcategory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staffs_staffdocument`
--

DROP TABLE IF EXISTS `staffs_staffdocument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs_staffdocument` (
  `id` int NOT NULL AUTO_INCREMENT,
  `document` varchar(100) NOT NULL,
  `title` varchar(255) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `staff_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `staffs_staffdocument_staff_id_4a651d16_fk_staffs_staff_id` (`staff_id`),
  CONSTRAINT `staffs_staffdocument_staff_id_4a651d16_fk_staffs_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staffs_staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_castecategory`
--

DROP TABLE IF EXISTS `students_castecategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_castecategory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(500) NOT NULL,
  `parent_category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `students_castecatego_parent_category_id_c7d20a34_fk_students_` (`parent_category_id`),
  CONSTRAINT `students_castecatego_parent_category_id_c7d20a34_fk_students_` FOREIGN KEY (`parent_category_id`) REFERENCES `students_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_category`
--

DROP TABLE IF EXISTS `students_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_student`
--

DROP TABLE IF EXISTS `students_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `current_status` tinyint(1) NOT NULL,
  `registration_number` varchar(200) NOT NULL,
  `surname` varchar(200) DEFAULT NULL,
  `firstname` varchar(200) NOT NULL,
  `other_name` varchar(200) NOT NULL,
  `father_name` varchar(500) DEFAULT NULL,
  `mother_name` varchar(500) DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `date_of_birth` date NOT NULL,
  `date_of_admission` date NOT NULL,
  `parent_mobile_number` varchar(13) NOT NULL,
  `address` longtext NOT NULL,
  `others` longtext NOT NULL,
  `adharcard_number` varchar(12) NOT NULL,
  `adharcard` varchar(100) NOT NULL,
  `uses_transport` tinyint(1) NOT NULL,
  `pickup_drop_location` varchar(255) NOT NULL,
  `pickup_time` time(6) DEFAULT NULL,
  `drop_time` time(6) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `current_class_id` int DEFAULT NULL,
  `route_id` bigint DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `roll_number` int DEFAULT NULL,
  `student_image` varchar(100) DEFAULT NULL,
  `number_of_siblings` int NOT NULL,
  `pen_number` varchar(100) DEFAULT NULL,
  `sr_number` varchar(100) DEFAULT NULL,
  `caste_category_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registration_number` (`registration_number`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `students_student_current_class_id_cf5f558b_fk_corecode_` (`current_class_id`),
  KEY `students_student_route_id_aa63f523_fk_transport_route_id` (`route_id`),
  KEY `students_student_caste_category_id_2584abd0_fk_students_` (`caste_category_id`),
  KEY `students_student_category_id_972c5ef1_fk_students_category_id` (`category_id`),
  CONSTRAINT `students_student_caste_category_id_2584abd0_fk_students_` FOREIGN KEY (`caste_category_id`) REFERENCES `students_castecategory` (`id`),
  CONSTRAINT `students_student_category_id_972c5ef1_fk_students_category_id` FOREIGN KEY (`category_id`) REFERENCES `students_category` (`id`),
  CONSTRAINT `students_student_current_class_id_cf5f558b_fk_corecode_` FOREIGN KEY (`current_class_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `students_student_route_id_aa63f523_fk_transport_route_id` FOREIGN KEY (`route_id`) REFERENCES `transport_route` (`id`),
  CONSTRAINT `students_student_user_id_56286dbb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=297 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_student_select_siblings`
--

DROP TABLE IF EXISTS `students_student_select_siblings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_student_select_siblings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `from_student_id` int NOT NULL,
  `to_student_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `students_student_select__from_student_id_to_stude_d938ce15_uniq` (`from_student_id`,`to_student_id`),
  KEY `students_student_sel_to_student_id_3c118aa4_fk_students_` (`to_student_id`),
  CONSTRAINT `students_student_sel_from_student_id_d2cec50c_fk_students_` FOREIGN KEY (`from_student_id`) REFERENCES `students_student` (`id`),
  CONSTRAINT `students_student_sel_to_student_id_3c118aa4_fk_students_` FOREIGN KEY (`to_student_id`) REFERENCES `students_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_studentbulkupload`
--

DROP TABLE IF EXISTS `students_studentbulkupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_studentbulkupload` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_uploaded` datetime(6) NOT NULL,
  `csv_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timetable_period`
--

DROP TABLE IF EXISTS `timetable_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable_period` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timetable_periodday`
--

DROP TABLE IF EXISTS `timetable_periodday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable_periodday` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day` int NOT NULL,
  `number_of_periods` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timetable_timetable`
--

DROP TABLE IF EXISTS `timetable_timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable_timetable` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day` int NOT NULL,
  `class_assigned_id` int NOT NULL,
  `period_id` bigint NOT NULL,
  `staff_id` int NOT NULL,
  `subject_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `timetable_timetable_class_assigned_id_4411ec74_fk_corecode_` (`class_assigned_id`),
  KEY `timetable_timetable_period_id_12330ce2_fk_timetable_period_id` (`period_id`),
  KEY `timetable_timetable_staff_id_b1f47677_fk_staffs_staff_id` (`staff_id`),
  KEY `timetable_timetable_subject_id_44bb92e0_fk_corecode_subject_id` (`subject_id`),
  CONSTRAINT `timetable_timetable_class_assigned_id_4411ec74_fk_corecode_` FOREIGN KEY (`class_assigned_id`) REFERENCES `corecode_studentclass` (`id`),
  CONSTRAINT `timetable_timetable_period_id_12330ce2_fk_timetable_period_id` FOREIGN KEY (`period_id`) REFERENCES `timetable_period` (`id`),
  CONSTRAINT `timetable_timetable_staff_id_b1f47677_fk_staffs_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staffs_staff` (`id`),
  CONSTRAINT `timetable_timetable_subject_id_44bb92e0_fk_corecode_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `corecode_subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport_driver`
--

DROP TABLE IF EXISTS `transport_driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport_driver` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `driver_photo` varchar(100) DEFAULT NULL,
  `license_number` varchar(50) NOT NULL,
  `upload_dl` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `joined_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `license_number` (`license_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport_route`
--

DROP TABLE IF EXISTS `transport_route`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport_route` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `start_location` varchar(100) NOT NULL,
  `end_location` varchar(100) NOT NULL,
  `stops` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport_trip`
--

DROP TABLE IF EXISTS `transport_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport_trip` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pickup_time` time(6) NOT NULL,
  `drop_time` time(6) NOT NULL,
  `days_operating` varchar(100) NOT NULL,
  `driver_id` bigint NOT NULL,
  `route_id` bigint NOT NULL,
  `vehicle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transport_trip_driver_id_def4879a_fk_transport_driver_id` (`driver_id`),
  KEY `transport_trip_route_id_d6b67731_fk_transport_route_id` (`route_id`),
  KEY `transport_trip_vehicle_id_1ced30d9_fk_transport_vehicle_id` (`vehicle_id`),
  CONSTRAINT `transport_trip_driver_id_def4879a_fk_transport_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `transport_driver` (`id`),
  CONSTRAINT `transport_trip_route_id_d6b67731_fk_transport_route_id` FOREIGN KEY (`route_id`) REFERENCES `transport_route` (`id`),
  CONSTRAINT `transport_trip_vehicle_id_1ced30d9_fk_transport_vehicle_id` FOREIGN KEY (`vehicle_id`) REFERENCES `transport_vehicle` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport_vehicle`
--

DROP TABLE IF EXISTS `transport_vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport_vehicle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vehicle_number` varchar(20) NOT NULL,
  `vehicle_type` varchar(10) NOT NULL,
  `vehicle_image` varchar(100) DEFAULT NULL,
  `capacity` int unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `driver_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vehicle_number` (`vehicle_number`),
  KEY `transport_vehicle_driver_id_44b3ed9d_fk_transport_driver_id` (`driver_id`),
  CONSTRAINT `transport_vehicle_driver_id_44b3ed9d_fk_transport_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `transport_driver` (`id`),
  CONSTRAINT `transport_vehicle_chk_1` CHECK ((`capacity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-19 19:27:14
