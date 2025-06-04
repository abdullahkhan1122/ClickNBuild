-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 04, 2025 at 05:57 PM
-- Server version: 8.0.42-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ClickNBuild`
--

-- --------------------------------------------------------

--
-- Table structure for table `BIDS`
--

CREATE TABLE `BIDS` (
  `bid_id` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `builder_id` int DEFAULT NULL,
  `estimated_cost` decimal(15,2) DEFAULT NULL,
  `timeline` varchar(50) DEFAULT NULL,
  `proposal` varchar(500) DEFAULT NULL,
  `status` enum('Pending','Accepted','Rejected','Completed') DEFAULT NULL,
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `BIDS`
--

INSERT INTO `BIDS` (`bid_id`, `project_id`, `builder_id`, `estimated_cost`, `timeline`, `proposal`, `status`, `submitted_at`, `user_id`) VALUES
(21, 36, 4, '980000000.00', '49', 'I ll complete the project much quicker and you will be satisfied.', 'Accepted', '2025-06-04 11:58:49', NULL),
(22, 37, 4, '480000.00', '30', 'I ll complete the project in 30 weeks and you will be absolutely satisfied with my work.', 'Completed', '2025-06-04 12:03:42', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `BUILDERS`
--

CREATE TABLE `BUILDERS` (
  `builder_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `active_bids` int DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT NULL,
  `total_projects` int DEFAULT NULL,
  `total_earning` decimal(15,2) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `experience` varchar(255) DEFAULT NULL,
  `about` text,
  `profile_picture` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `BUILDERS`
--

INSERT INTO `BUILDERS` (`builder_id`, `user_id`, `location`, `active_bids`, `rating`, `total_projects`, `total_earning`, `company_name`, `specialization`, `experience`, `about`, `profile_picture`) VALUES
(1, 18, NULL, 0, '0.00', 0, '0.00', NULL, NULL, NULL, NULL, NULL),
(2, 19, NULL, 0, '0.00', 0, '0.00', NULL, NULL, NULL, NULL, NULL),
(3, 22, NULL, 0, '5.00', 0, '0.00', NULL, NULL, NULL, NULL, NULL),
(4, 25, NULL, 0, '5.00', 0, '0.00', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `CLIENT`
--

CREATE TABLE `CLIENT` (
  `client_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `total_posted_projeccts` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `profile_picture` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `about` text,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `CLIENT`
--

INSERT INTO `CLIENT` (`client_id`, `user_id`, `total_posted_projeccts`, `created_at`, `profile_picture`, `location`, `company_name`, `about`, `updated_at`) VALUES
(1, 13, NULL, '2025-04-26 19:47:02', 'uploads/blue-teal-sand-paper.jpg', 'Japan', 'hhhh', 'sddasdafor first', '2025-04-28 00:32:23'),
(2, 21, NULL, '2025-04-28 11:19:17', NULL, 'My locatuon', ' Abdullah', 'I am testing things here', '2025-05-01 16:55:14'),
(3, 23, NULL, '2025-06-04 11:44:07', NULL, NULL, NULL, NULL, '2025-06-04 16:44:07'),
(4, 24, NULL, '2025-06-04 11:56:04', 'uploads/3d-view-house-model.jpg', 'Pakistan', 'TEST', 'I am a client', '2025-06-04 17:06:06');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `FEEDBACK`
--

CREATE TABLE `FEEDBACK` (
  `feedback_id` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `client_id` int DEFAULT NULL,
  `builder_id` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `MILESTONES`
--

CREATE TABLE `MILESTONES` (
  `milestone_id` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `status` enum('in_progress','completed') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ORDERS`
--

CREATE TABLE `ORDERS` (
  `order_id` int NOT NULL,
  `builder_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `total_price` decimal(15,2) DEFAULT NULL,
  `status` enum('pending','shipped','delivered') DEFAULT NULL,
  `ordered_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `PAYMENTS`
--

CREATE TABLE `PAYMENTS` (
  `payment_id` int NOT NULL,
  `project_id` int NOT NULL,
  `client_id` int NOT NULL,
  `amount_due` int NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `PAYMENTS`
--

INSERT INTO `PAYMENTS` (`payment_id`, `project_id`, `client_id`, `amount_due`, `status`, `created_at`) VALUES
(5, 36, 4, 980000000, 'Pending', '2025-06-04 11:59:12'),
(6, 37, 4, 480000, 'Paid', '2025-06-04 12:04:12');

-- --------------------------------------------------------

--
-- Table structure for table `PROJECTS`
--

CREATE TABLE `PROJECTS` (
  `project_id` int NOT NULL,
  `client_id` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `project_type` varchar(50) DEFAULT NULL,
  `budget` decimal(15,2) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `timeline` varchar(50) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `assigned_to` int DEFAULT NULL,
  `client_completed` tinyint(1) DEFAULT '0',
  `builder_completed` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `PROJECTS`
--

INSERT INTO `PROJECTS` (`project_id`, `client_id`, `title`, `description`, `project_type`, `budget`, `location`, `timeline`, `image_path`, `status`, `created_at`, `assigned_to`, `client_completed`, `builder_completed`) VALUES
(36, 4, 'New House', 'I want to build a lavish house with modern architecture in islamabad.', 'Residential Construction', '10000000.00', 'Islamabad', '50', NULL, 'Active', '2025-06-04 11:57:25', 4, 0, 1),
(37, 4, 'House construction', 'i want to build a 30 story building in islamabad.', 'Commercial Construction', '500000.00', 'Islamabad , Pakistan', '40', NULL, 'Completed', '2025-06-04 12:02:40', 4, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `project_images`
--

CREATE TABLE `project_images` (
  `image_id` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `project_images`
--

INSERT INTO `project_images` (`image_id`, `project_id`, `image_path`) VALUES
(38, 36, 'uploads/3d-view-house-model.jpg'),
(39, 37, 'uploads/3d-view-house-model.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `REVIEWS`
--

CREATE TABLE `REVIEWS` (
  `review_id` int NOT NULL,
  `project_id` int NOT NULL,
  `reviewer_id` int NOT NULL,
  `reviewee_id` int NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `rating` int NOT NULL,
  `comment` text NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `REVIEWS`
--

INSERT INTO `REVIEWS` (`review_id`, `project_id`, `reviewer_id`, `reviewee_id`, `role`, `rating`, `comment`, `created_at`) VALUES
(3, 37, 24, 25, 'client', 5, 'This builder is great he completed the project as promised.', '2025-06-04 12:05:18'),
(4, 37, 25, 24, 'builder', 5, 'This client is great .', '2025-06-04 12:05:36');

-- --------------------------------------------------------

--
-- Table structure for table `USER`
--

CREATE TABLE `USER` (
  `user_id` int NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(600) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `USER`
--

INSERT INTO `USER` (`user_id`, `username`, `password`, `email`, `phone`, `created_at`, `role`) VALUES
(13, 'root', 'scrypt:32768:8:1$R5yQMvcvkWdjAd2t$ba0a7a25e918c2595a6c30de258e9df627ceadaf2748d1399707891b78304e1f5e2cd4f08709fa99244f4af1f1d4c6a050589a83cbd048d81b53cd4dfef382a7', 'a@gmail.com', '03379672148', '2025-04-26 19:47:02', 'Client'),
(18, 'root', 'scrypt:32768:8:1$JmMYTYX5kBB5roUY$7e13ee34bb0c8e136d15e489f05a531ff15a01f37c3a7dc2479cc99978ead295c95d4d24666d6b3006f676e5a027078aba02ccd7f3ee3f7b5ca7e3f76a2a8c86', 'l@gmail.com', '12312', '2025-04-26 20:29:45', 'Builder'),
(19, 'root', 'scrypt:32768:8:1$xqLekr2Bm9n8DgEG$7bf2a18a1d77a47c2c3df8ac889ba027ac721191e85bb1a1e9696c6c3f84e6c96a0d23f90d3ea0ca7aa95da2fabb48ec2101150d75ea8e4728eccfcc6a93482c', 'l@gmail.com', '12312', '2025-04-27 09:49:30', 'Builder'),
(20, 'root', 'scrypt:32768:8:1$A4J5i37OdgAX32gf$d2f1ee618463d1250c37f8895cbcb15eddcaba1712ea0cd10bf4c1dcb0c3249cab71af27a21895d47c555377cdc099f102512af48110ff3f661b179b1854bb33', 'l@gmail.com', '1222', '2025-04-27 09:49:52', 'Client'),
(21, 'test', 'scrypt:32768:8:1$mEHTWQs7EmGDix74$2d6872375685b98ed1f759d7dfb8f7b3b098c17b1d77031a1d7676c268fcfd869a8dc9b9937ea719f24e25ac83852feddc604560589e5462010df1f6faec50fe', 'test@gmail.com', '03379672148', '2025-04-28 11:19:17', 'Client'),
(22, 'abdullah', 'scrypt:32768:8:1$LBW89aTwDD0yqJrE$b734fdb4a48d3563f7e27ad7eca109b2f2dc9970e4c515ec0cc5ad11e050c0beb991f7a22943653b52386fc2556c198f9617fed4551642c71260883aebe4a99d', 'ab@gmail.com', '03379672148', '2025-04-28 11:21:18', 'Builder'),
(23, 'new_test', 'scrypt:32768:8:1$I2Eyym8QY5SW1tOb$a14b8866baef4370684eb2306206c5f316c73262a2bf9a5002bad4384bf9db64472f92f6d53133f5ae5c2ad5712f089ab434359ca8468c3c7ab339e43b696817', 'test@hotmail.com', '0337111111', '2025-06-04 11:44:07', 'Client'),
(24, 'testing', 'scrypt:32768:8:1$wovFyGxVK9qhftHu$687439ee3aefacb4dfa600bbf4f9ff2f5c4345e4a81d84589a404b98ead325bcf2d850df9e5e97c31dfb6567a69e81bf4992b35278f654f2720660cdec9da0d0', 'client@hotmail.com', '0331234567', '2025-06-04 11:56:04', 'Client'),
(25, 'builder', 'scrypt:32768:8:1$HQaAvFLqEkwSW2A4$003da6c141ee00d3211092997cad63206441cfd189e65f1ab34c304318b7873a68bd768787f7b123f77188576b19f71b197ee400758ec43438b990eeacad1ff7', 'builder@hotmail.com', '0337123456', '2025-06-04 11:58:02', 'Builder');

-- --------------------------------------------------------

--
-- Table structure for table `VENDOR_MARKETPLACE`
--

CREATE TABLE `VENDOR_MARKETPLACE` (
  `product_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `price` decimal(15,2) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `vendor_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vendor_marketplace`
--

CREATE TABLE `vendor_marketplace` (
  `product_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `price_pkr` float NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `vendor_name` varchar(100) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `vendor_marketplace`
--

INSERT INTO `vendor_marketplace` (`product_id`, `name`, `description`, `price_pkr`, `category`, `vendor_name`, `contact_number`, `created_at`, `image`) VALUES
(1, 'Premium Cement', 'High-quality cement for construction projects.', 126000, 'Materials', 'BuildPro Ltd.', '+92-300-1234567', '2025-04-25 14:32:00', '/static/images/cement.webp'),
(2, 'Steel Rods - 12mm', 'High tensile strength steel rods.', 322140, 'Materials', 'IronBuilds', '+92-321-9876543', '2025-04-27 10:12:00', '/static/images/steel.webp'),
(3, 'Red Bricks', 'Standard red clay bricks for masonry work.', 15000, 'Materials', 'BrickWorks', '+92-333-4567890', '2025-04-28 09:15:00', '/static/images/brick.jpeg'),
(4, 'Concrete Blocks', 'Precast concrete blocks for quick construction.', 28000, 'Materials', 'StoneTech', '+92-301-2345678', '2025-04-29 11:45:00', '/static/images/blocks.jpg'),
(5, 'Construction Sand', 'Fine river sand for plastering and mixing.', 5000, 'Materials', 'SandCo', '+92-302-3456789', '2025-04-29 13:20:00', '/static/images/sand.jpeg'),
(6, 'PVC Pipes - 4 inch', 'Durable PVC pipes for plumbing and drainage.', 12000, 'Plumbing', 'PipeMasters', '+92-304-5678901', '2025-04-29 15:30:00', '/static/images/pvc_pipes.jpg'),
(7, 'Ceramic Floor Tiles', 'High-quality ceramic tiles for flooring, 12x12 inches.', 45000, 'Finishing', 'TileTrendz', '+92-305-6789012', '2025-04-29 16:45:00', '/static/images/tiles.jpg'),
(8, 'Waterproof Paint', 'Exterior waterproof paint, 10L bucket.', 35000, 'Finishing', 'ColorShield', '+92-306-7890123', '2025-04-29 17:10:00', '/static/images/paint.jpg'),
(9, 'Electrical Cables - 3mm', 'Copper-core electrical cables for wiring.', 25000, 'Electrical', 'PowerLine', '+92-307-8901234', '2025-04-29 18:00:00', '/static/images/cables.jpg'),
(10, 'Ready-Mix Concrete', 'Pre-mixed concrete for foundations and slabs.', 200000, 'Materials', 'ConcreteCo', '+92-308-9012345', '2025-04-29 19:20:00', '/static/images/concrete.webp');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `BIDS`
--
ALTER TABLE `BIDS`
  ADD PRIMARY KEY (`bid_id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `builder_id` (`builder_id`),
  ADD KEY `fk_bids_user` (`user_id`);

--
-- Indexes for table `BUILDERS`
--
ALTER TABLE `BUILDERS`
  ADD PRIMARY KEY (`builder_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `CLIENT`
--
ALTER TABLE `CLIENT`
  ADD PRIMARY KEY (`client_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `FEEDBACK`
--
ALTER TABLE `FEEDBACK`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `builder_id` (`builder_id`);

--
-- Indexes for table `MILESTONES`
--
ALTER TABLE `MILESTONES`
  ADD PRIMARY KEY (`milestone_id`),
  ADD KEY `project_id` (`project_id`);

--
-- Indexes for table `ORDERS`
--
ALTER TABLE `ORDERS`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `builder_id` (`builder_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `PAYMENTS`
--
ALTER TABLE `PAYMENTS`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `PROJECTS`
--
ALTER TABLE `PROJECTS`
  ADD PRIMARY KEY (`project_id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `assigned_to` (`assigned_to`);

--
-- Indexes for table `project_images`
--
ALTER TABLE `project_images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `project_id` (`project_id`);

--
-- Indexes for table `REVIEWS`
--
ALTER TABLE `REVIEWS`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `reviewer_id` (`reviewer_id`),
  ADD KEY `reviewee_id` (`reviewee_id`);

--
-- Indexes for table `USER`
--
ALTER TABLE `USER`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `VENDOR_MARKETPLACE`
--
ALTER TABLE `VENDOR_MARKETPLACE`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `vendor_marketplace`
--
ALTER TABLE `vendor_marketplace`
  ADD PRIMARY KEY (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `BIDS`
--
ALTER TABLE `BIDS`
  MODIFY `bid_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `BUILDERS`
--
ALTER TABLE `BUILDERS`
  MODIFY `builder_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `CLIENT`
--
ALTER TABLE `CLIENT`
  MODIFY `client_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `FEEDBACK`
--
ALTER TABLE `FEEDBACK`
  MODIFY `feedback_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `MILESTONES`
--
ALTER TABLE `MILESTONES`
  MODIFY `milestone_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ORDERS`
--
ALTER TABLE `ORDERS`
  MODIFY `order_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `PAYMENTS`
--
ALTER TABLE `PAYMENTS`
  MODIFY `payment_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `PROJECTS`
--
ALTER TABLE `PROJECTS`
  MODIFY `project_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `project_images`
--
ALTER TABLE `project_images`
  MODIFY `image_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `REVIEWS`
--
ALTER TABLE `REVIEWS`
  MODIFY `review_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `USER`
--
ALTER TABLE `USER`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `VENDOR_MARKETPLACE`
--
ALTER TABLE `VENDOR_MARKETPLACE`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vendor_marketplace`
--
ALTER TABLE `vendor_marketplace`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `BIDS`
--
ALTER TABLE `BIDS`
  ADD CONSTRAINT `BIDS_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `PROJECTS` (`project_id`),
  ADD CONSTRAINT `BIDS_ibfk_2` FOREIGN KEY (`builder_id`) REFERENCES `BUILDERS` (`builder_id`),
  ADD CONSTRAINT `fk_bids_user` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`);

--
-- Constraints for table `BUILDERS`
--
ALTER TABLE `BUILDERS`
  ADD CONSTRAINT `BUILDERS_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`);

--
-- Constraints for table `CLIENT`
--
ALTER TABLE `CLIENT`
  ADD CONSTRAINT `CLIENT_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`);

--
-- Constraints for table `FEEDBACK`
--
ALTER TABLE `FEEDBACK`
  ADD CONSTRAINT `FEEDBACK_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `PROJECTS` (`project_id`),
  ADD CONSTRAINT `FEEDBACK_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `CLIENT` (`client_id`),
  ADD CONSTRAINT `FEEDBACK_ibfk_3` FOREIGN KEY (`builder_id`) REFERENCES `BUILDERS` (`builder_id`);

--
-- Constraints for table `MILESTONES`
--
ALTER TABLE `MILESTONES`
  ADD CONSTRAINT `MILESTONES_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `PROJECTS` (`project_id`);

--
-- Constraints for table `ORDERS`
--
ALTER TABLE `ORDERS`
  ADD CONSTRAINT `ORDERS_ibfk_1` FOREIGN KEY (`builder_id`) REFERENCES `BUILDERS` (`builder_id`),
  ADD CONSTRAINT `ORDERS_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `VENDOR_MARKETPLACE` (`product_id`);

--
-- Constraints for table `PAYMENTS`
--
ALTER TABLE `PAYMENTS`
  ADD CONSTRAINT `PAYMENTS_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `PROJECTS` (`project_id`),
  ADD CONSTRAINT `PAYMENTS_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `CLIENT` (`client_id`);

--
-- Constraints for table `PROJECTS`
--
ALTER TABLE `PROJECTS`
  ADD CONSTRAINT `PROJECTS_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `CLIENT` (`client_id`),
  ADD CONSTRAINT `PROJECTS_ibfk_2` FOREIGN KEY (`assigned_to`) REFERENCES `BUILDERS` (`builder_id`);

--
-- Constraints for table `project_images`
--
ALTER TABLE `project_images`
  ADD CONSTRAINT `project_images_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `PROJECTS` (`project_id`);

--
-- Constraints for table `REVIEWS`
--
ALTER TABLE `REVIEWS`
  ADD CONSTRAINT `REVIEWS_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `PROJECTS` (`project_id`),
  ADD CONSTRAINT `REVIEWS_ibfk_2` FOREIGN KEY (`reviewer_id`) REFERENCES `USER` (`user_id`),
  ADD CONSTRAINT `REVIEWS_ibfk_3` FOREIGN KEY (`reviewee_id`) REFERENCES `USER` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
