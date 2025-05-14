-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 30, 2025 at 10:40 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pawpromise`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat_messages`
--

CREATE TABLE `chat_messages` (
  `id` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `is_bot` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_messages`
--

INSERT INTO `chat_messages` (`id`, `session_id`, `message`, `is_bot`, `timestamp`) VALUES
(23, 13, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-03-29 18:38:43'),
(24, 13, 'How to train a puppy?', 0, '2025-03-29 18:43:00'),
(25, 13, 'Puppy training is a rewarding experience!  Start early with socialization, introducing your pup to new people, places, and sounds.  Keep training sessions short and fun, using positive reinforcement like treats and praise.  Focus on basic commands like sit, stay, come, and down.  House training requires consistency – take your puppy outside frequently, especially after waking up and eating.  Crate training can help with housebreaking and provide a safe space.  Remember, patience and consistency are key to a well-trained pup!  If you encounter specific challenges, consider consulting a professional dog trainer.  They can offer personalized guidance.\n', 1, '2025-03-29 18:43:05'),
(26, 14, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-03-29 18:43:06'),
(27, 14, 'Best cat food for kittens?', 0, '2025-03-29 18:44:09'),
(28, 14, 'For kittens, choosing a food formulated specifically for growth is key!  Look for \"kitten\" food, as it has higher protein and calorie content than adult cat food.  Some good brands to consider are Royal Canin Kitten, Purina Pro Plan Kitten, and Hill\'s Science Diet Kitten.  Wet food is generally more palatable and hydrating for kittens, but dry food can be good for dental health.  A mix of both is often ideal.  Always check the ingredient list and choose a food with real meat or poultry as the first ingredient.  If your kitten has any special dietary needs, it\'s best to consult with your veterinarian.\n', 1, '2025-03-29 18:44:12'),
(29, 14, 'what is sun', 0, '2025-03-29 18:44:28'),
(30, 14, 'While the sun is important for all living things, I\'m a pet assistant chatbot, PawPromise, and I focus on helping with your furry, feathered, or scaled friends.  I can answer questions about dogs, cats, and other pets.  Do you have any pet-related questions I can help with today?\n', 1, '2025-03-29 18:44:30'),
(31, 14, 'my cat is not eating what should i do', 0, '2025-03-29 18:44:58'),
(32, 14, 'Oh no, a cat not eating can be worrying!  There are several reasons why your kitty might have lost their appetite. It could be something simple like they don\'t like their current food, or their bowl is dirty.  Sometimes stress, like a new pet or a change in routine, can also affect their appetite. \n\nMore serious reasons include dental problems, an upset tummy, or other illnesses.  If your cat hasn\'t eaten anything for 24 hours, or is showing other symptoms like vomiting, lethargy, or hiding, please take them to the vet right away.  For less urgent situations, try enticing them with a tasty treat like warmed-up wet food or a little bit of cooked chicken.  Make sure their water bowl is fresh and clean too.  If you\'re still concerned, a vet check-up is always a good idea.\n', 1, '2025-03-29 18:45:02'),
(33, 14, 'any near pet hospitals here ?', 0, '2025-03-29 18:45:28'),
(34, 14, 'I can help you find a pet hospital!  To give you the best recommendations, I need a little more information. Could you tell me your current location?  Knowing your city and state (or zip code) will allow me to search for nearby pet hospitals and emergency veterinary clinics.\n', 1, '2025-03-29 18:45:30'),
(35, 14, '380050', 0, '2025-03-29 18:45:41'),
(36, 14, 'That doesn\'t look like a question about pets!  I\'m PawPromise, your friendly pet assistant chatbot. I can help you with questions about dogs, cats, and other common household pets.  Ask me about pet care, behavior, health, or anything pet-related and I\'ll do my best to help!  Just rephrase your question about pets.\n', 1, '2025-03-29 18:45:43'),
(37, 14, 'any near pet hospitals here ? my zipcode is 380050', 0, '2025-03-29 18:46:16'),
(38, 14, 'I can\'t directly help you find pet hospitals near your zip code because I don\'t have real-time access to location data.  However, I recommend searching online using a phrase like \"pet hospitals near 380050\" or checking online directories specifically for veterinary services.  You can also ask your neighbors or local pet stores for recommendations.  I hope you find a great vet near you!\n', 1, '2025-03-29 18:46:18'),
(39, 14, 'How to train a puppy?', 0, '2025-03-30 16:26:05'),
(40, 14, 'Training a puppy takes patience and consistency!  Start with basic commands like \"sit,\" \"stay,\" and \"come\" using positive reinforcement like treats and praise. Keep training sessions short and fun, and be sure to socialize your puppy with other dogs and people early on.  Crate training can also be helpful for housebreaking and providing a safe space.  Consider enrolling in a puppy obedience class for professional guidance and socialization opportunities.  Remember to be patient, as every puppy learns at their own pace.\n', 1, '2025-03-30 16:26:08'),
(41, 14, 'who are you broo ?', 0, '2025-03-30 16:26:19'),
(42, 14, 'Hey there! I\'m PawPromise, your friendly pet assistant chatbot.  I\'m here to help with any questions you have about dogs, cats, and other pets.  Your question wasn\'t about pets, so I can\'t really answer it.  But if you have anything you\'d like to know about caring for your furry, feathered, or scaled friends, just ask!\n', 1, '2025-03-30 16:26:21'),
(43, 14, 'my parrot is not eating', 0, '2025-03-30 16:26:39'),
(44, 14, 'I can help with that!  A parrot not eating can be serious.  There are several possible reasons, including illness, changes in environment, or even boredom with their food.  \n\nFirst, double-check their food is fresh and appealing.  Sometimes parrots get picky!  Try offering a variety of healthy options like fresh fruits and vegetables in addition to their regular pellets.  \n\nMake sure their environment is comfortable and stress-free.  Changes in their cage, routine, or household can upset a parrot\'s appetite.\n\nIf they continue to refuse food, it\'s crucial to consult an avian veterinarian as soon as possible.  They can diagnose any underlying health problems and provide appropriate treatment.\n', 1, '2025-03-30 16:26:42'),
(73, 26, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-08 17:52:52'),
(74, 26, 'Give some useful tips for the first time pet adopters', 0, '2025-04-08 18:00:06'),
(75, 26, 'Congrats on your new furry friend!  Bringing a pet home is exciting. Here are a few tips to make it smoother.  First, pet-proof your home. Tuck away anything potentially dangerous like electrical cords and toxic cleaning supplies.  Set up a comfy space just for them with food, water, a bed, and toys.  Patience is key, especially during the first few days. Let them adjust at their own pace.  Start with short training sessions and use positive reinforcement like treats and praise.  Establish a routine for feeding, walks, and playtime to help them feel secure.  And don\'t forget to schedule a vet checkup soon after adoption for a health assessment and to discuss preventative care.\n', 1, '2025-04-08 18:00:10'),
(86, 28, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-12 13:09:44'),
(87, 28, 'How to train a puppy?', 0, '2025-04-12 13:10:51'),
(88, 28, 'Puppy training is a rewarding journey!  Start early with socialization, introducing your puppy to new sights, sounds, and friendly people and animals.  Basic obedience training can begin as soon as you bring your puppy home.  Keep training sessions short and fun, using positive reinforcement like treats and praise.  Focus on key commands like sit, stay, come, and leave it.  Consistency is key, so make sure everyone in the family uses the same commands.  House training requires patience and a regular schedule.  Crate training can be a helpful tool.  If you encounter challenges, consider enrolling in a puppy training class for professional guidance. Remember to be patient and enjoy this special time with your new furry friend.\n', 1, '2025-04-12 13:10:55'),
(89, 29, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-12 13:14:15'),
(90, 29, 'How to train a puppy?', 0, '2025-04-12 13:14:17'),
(91, 29, 'Puppy training is a rewarding experience!  It\'s all about positive reinforcement.  Start early, keep training sessions short and fun, and use treats and praise. Focus on basic commands like sit, stay, come, and down.  House training involves a consistent schedule, rewarding potty breaks outside, and cleaning up accidents thoroughly to eliminate odors.  Socialization is crucial, so expose your puppy to different sights, sounds, and friendly people and dogs early on.  Consider enrolling in a puppy kindergarten class for professional guidance and a chance for your pup to socialize with other puppies.  Remember, patience and consistency are key!  Let me know if you have other puppy questions!\n', 1, '2025-04-12 13:14:20'),
(92, 30, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-17 20:34:43'),
(98, 32, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-21 21:27:32'),
(99, 32, 'How to train a puppy?', 0, '2025-04-21 21:27:38'),
(100, 32, 'Training a puppy takes patience and consistency!  Start with basic obedience like sit, stay, and come.  Use positive reinforcement like treats and praise. Keep training sessions short and fun, especially when they\'re young.  Socialization is key, so expose your puppy to different sights, sounds, and friendly people and dogs.  Crate training can help with housebreaking and provide a safe space.  If you\'re having trouble, consider puppy classes – they\'re a great way to get professional guidance and socialize your pup!\n', 1, '2025-04-21 21:27:44'),
(101, 32, 'Why does my cat knead?', 0, '2025-04-21 21:27:49'),
(102, 32, 'It\'s adorable when your cat kneads, isn\'t it?  This behavior, sometimes called \"making biscuits,\" usually traces back to kittenhood.  When kittens nurse, they knead their mother\'s belly to stimulate milk flow.  As adults, cats often continue this behavior when they feel content and comfortable.  It\'s a sign of happiness and relaxation.  They might knead on soft blankets, your lap, or even other pets!  Sometimes, kneading can also be a way for your cat to mark territory, as they have scent glands in their paws.\n', 1, '2025-04-21 21:27:53'),
(103, 33, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-21 21:27:53'),
(104, 34, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-21 21:27:54'),
(109, 37, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-24 23:39:02'),
(110, 37, 'How to train a puppy?', 0, '2025-04-24 23:39:03'),
(111, 37, 'Training a puppy takes patience and consistency!  Start with basic obedience like sit, stay, and come.  Use positive reinforcement like treats and praise. Keep training sessions short and fun, especially when they\'re young.  Socialization is key, so expose your puppy to different sights, sounds, and people early on.  Crate training can help with housebreaking and provide a safe space.  If you\'re having trouble, consider puppy classes – they\'re a great way to get professional guidance and socialize your pup!  Remember, every puppy learns at their own pace, so be patient and celebrate the small victories.\n', 1, '2025-04-24 23:39:09'),
(112, 38, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-24 23:53:30'),
(113, 39, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-24 23:53:31'),
(114, 38, 'Best cat food for kittens?', 0, '2025-04-24 23:53:35'),
(115, 38, 'Finding the best kitten food can be tricky!  Look for foods specifically formulated for kittens, as they have higher protein and calorie content for growth.  Wet food is a great option, as it helps with hydration.  Some good brands to consider are Royal Canin Kitten, Purina Pro Plan Kitten, and Hill\'s Science Diet Kitten. Always check the ingredient list and choose a food with real meat or fish as the first ingredient.  Chat with your vet too – they can recommend the perfect diet based on your kitten\'s specific needs.\n', 1, '2025-04-24 23:53:38'),
(116, 40, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-25 00:00:04'),
(117, 41, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-25 00:00:06'),
(118, 41, 'Best cat food for kittens?', 0, '2025-04-25 00:00:08'),
(119, 41, 'Finding the perfect kitten food can be a paw-some adventure!  Look for foods specifically formulated for kittens, as they need higher levels of protein and calories for growth.  Brands like Royal Canin, Purina Pro Plan, and Hill\'s Science Diet offer excellent kitten formulas.  Wet food is a great option for hydration, while dry food helps with dental health.  Always check the ingredient list, prioritizing meat-based protein sources.  And remember, transitioning to a new food should be gradual. If you have any other kitten questions, I\'m here to help!\n', 1, '2025-04-25 00:00:13'),
(120, 41, 'How often should I walk my dog?', 0, '2025-04-25 00:00:16'),
(121, 41, 'Walking your dog depends on their breed, age, and energy level.  Generally, most dogs benefit from at least one walk a day.  Energetic breeds like Huskies or Border Collies might need two or even three walks or longer outings to burn off energy.  Senior dogs or smaller breeds may be content with shorter, gentler strolls.  Puppies need shorter, more frequent walks to avoid overexertion.  Observe your dog for signs of fatigue like excessive panting or lagging behind.  Adjust your walking schedule based on their individual needs.  Always remember to bring poop bags and fresh water, especially on longer walks!\n', 1, '2025-04-25 00:00:19'),
(127, 45, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-30 11:50:35'),
(128, 45, 'Signs of healthy pets', 0, '2025-04-30 11:50:45'),
(129, 45, 'A healthy pet is a happy pet!  Here are some general signs to look for:  A shiny coat, bright eyes, and a wet nose (except in some breeds like pugs).  Your pet should be active and playful, with a good appetite and regular bowel movements. They should also be alert and responsive to you.  Regular vet checkups are key to catching any potential problems early.  Remember, each pet is unique, so if you have any concerns about your furry friend, it\'s always best to chat with your vet.\n', 1, '2025-04-30 11:50:48'),
(130, 45, 'why my cat is craying all night', 0, '2025-04-30 11:51:07'),
(131, 45, 'It sounds like your cat is keeping you up all night!  There are a few reasons why your cat might be crying.  They could be hungry, thirsty, or bored.  Sometimes, older cats can get confused at night and cry due to cognitive decline.  If your cat is normally quiet at night and this is a new behavior, it\'s a good idea to schedule a vet visit to rule out any medical problems.  Make sure they have fresh food and water available, and try playing with them before bedtime to tire them out.  A little extra attention and enrichment can go a long way!\n', 1, '2025-04-30 11:51:10'),
(132, 46, 'Hi there! I\'m your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?', 1, '2025-04-30 13:44:11');

-- --------------------------------------------------------

--
-- Table structure for table `chat_sessions`
--

CREATE TABLE `chat_sessions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `session_name` varchar(255) DEFAULT 'New Chat',
  `created_at` datetime DEFAULT current_timestamp(),
  `last_updated` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_sessions`
--

INSERT INTO `chat_sessions` (`id`, `user_id`, `org_id`, `session_name`, `created_at`, `last_updated`) VALUES
(13, NULL, 6, 'New Chat', '2025-03-29 18:38:43', '2025-03-29 18:43:00'),
(14, NULL, 6, 'New Chat', '2025-03-29 18:43:06', '2025-03-30 16:26:39'),
(26, 12, NULL, 'New Chat', '2025-04-08 17:52:52', '2025-04-08 18:00:06'),
(28, 13, NULL, 'New Chat', '2025-04-12 13:09:44', '2025-04-12 13:10:51'),
(29, 13, NULL, 'New Chat', '2025-04-12 13:14:15', '2025-04-12 13:14:17'),
(30, 13, NULL, 'New Chat', '2025-04-17 20:34:43', '2025-04-17 20:34:43'),
(32, 13, NULL, 'New Chat', '2025-04-21 21:27:32', '2025-04-21 21:27:49'),
(33, 13, NULL, 'New Chat', '2025-04-21 21:27:53', '2025-04-21 21:27:53'),
(34, 13, NULL, 'New Chat', '2025-04-21 21:27:54', '2025-04-21 21:27:54'),
(37, 13, NULL, 'New Chat', '2025-04-24 23:39:02', '2025-04-24 23:39:03'),
(38, 13, NULL, 'New Chat', '2025-04-24 23:53:30', '2025-04-24 23:53:35'),
(39, 13, NULL, 'New Chat', '2025-04-24 23:53:31', '2025-04-24 23:53:31'),
(40, 13, NULL, 'New Chat', '2025-04-25 00:00:04', '2025-04-25 00:00:04'),
(41, 13, NULL, 'New Chat', '2025-04-25 00:00:06', '2025-04-25 00:00:16'),
(45, 12, NULL, 'New Chat', '2025-04-30 11:50:35', '2025-04-30 11:51:07'),
(46, NULL, 6, 'New Chat', '2025-04-30 13:44:11', '2025-04-30 13:44:11');

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `post_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id`, `user_id`, `org_id`, `post_id`, `text`, `created_at`) VALUES
(26, 12, NULL, 20, 'hii', '2025-04-29 07:52:34'),
(27, 12, NULL, 21, 'woww', '2025-04-29 07:52:51'),
(41, NULL, 6, 22, 'hiii', '2025-04-29 13:39:28');

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `email`, `phone`, `message`, `created_at`) VALUES
(0, 'PANDYA KALP', 'kalppandya1511@gmail.com', '917378723', 'i want to buy other pats is there any other pet here ?', '2025-03-15 12:34:51');

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `organizer_id` int(11) NOT NULL,
  `event_name` varchar(255) NOT NULL,
  `event_description` text NOT NULL,
  `event_datetime` datetime NOT NULL,
  `event_duration` varchar(50) NOT NULL,
  `event_location` varchar(255) NOT NULL,
  `google_maps_link` varchar(255) DEFAULT NULL,
  `event_type` varchar(50) NOT NULL,
  `allowed_pet_types` varchar(255) NOT NULL,
  `pet_limit` int(11) NOT NULL,
  `max_participants` int(11) NOT NULL,
  `event_poster` varchar(255) DEFAULT NULL,
  `organizer_name` varchar(255) NOT NULL,
  `organizer_type` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `sponsors` text DEFAULT NULL,
  `rules` text DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `user_type` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`id`, `organizer_id`, `event_name`, `event_description`, `event_datetime`, `event_duration`, `event_location`, `google_maps_link`, `event_type`, `allowed_pet_types`, `pet_limit`, `max_participants`, `event_poster`, `organizer_name`, `organizer_type`, `email`, `phone`, `address`, `sponsors`, `rules`, `status`, `user_type`) VALUES
(4, 10, 'Cat meetup for everyone', 'Playfull date with cat', '2025-04-09 09:00:00', '1 hrs', 'Maninagar', 'https://maps.app.goo.gl/15N2dvbNNvSmBDMD7', 'Playdate', 'Cats only', 1, 50, 'static\\uploads\\20250407215308_Pet_meetup.png', 'SafePaws Alliance', 'Individual', 'kalppandya1511@gmail.com', '9173784275', 'Ghodasar,380050,Ahmedabad', 'Pedigree', 'If your cat damage anything you will be responsible', 'approved', 'organization'),
(12, 10, 'Pet Playdate in the Park', 'Join us for a fun-filled pet playdate! Meet fellow pet lovers, socialize your pets, and enjoy games, treats, and giveaways.', '2025-04-30 18:36:00', '3 hours', 'Central Bark Dog Park, Main Street, Springfield', 'https://maps.google.com/?q=Central+Bark+Dog+Park+Springfield', 'Playdate', 'Dogs, Cats', 2, 50, 'static\\uploads\\20250408184323_Pet_PlayDate.png', 'SafePaws Alliance', 'Individual', 'kalppandya26@gmail.com', '01234567891', 'Springfield, IL', ' PetSmart, Paws & Treats Bakery', 'All pets must be leashed unless in designated play zones.\r\nAggressive pets will be asked to leave.\r\nOwners must clean up after their pets.\r\nVaccinations must be up to date.', 'approved', 'organization'),
(17, 12, 'Wag & Walk – Dog Meetup Mumbai', 'An exclusive dog meetup event where pet parents can socialize, join fun activities, and let their dogs play freely in a secure, open space. Perfect for friendly pooches and their humans!\r\n', '2025-05-10 16:08:00', '4 hours', 'Shivaji Park, Dadar West, Mumbai, Maharashtra', 'https://goo.gl/maps/mumbai-shivaji-park', 'Playdate', 'Dogs only', 2, 100, 'static\\uploads\\20250418160843_ChatGPT_Image_Apr_18_2025_03_39_24_PM.png', 'Paw Haven', 'Individual', 'vishwapatel.21.cs@iite.indusuni.ac.in', '‪+91-9090123456‬', 'Bandra East, Mumbai, Maharashtra', 'Heads Up For Tails, Drools, PetChum Club', 'Only vaccinated and non-aggressive dogs allowed.\r\n\r\nAll dogs must be leashed until inside the play zone.\r\n\r\nOwners must clean up after their pets.\r\n\r\nWater and treats will be provided.', 'approved', 'organization'),
(18, 12, 'The Purrfect Hangout – Cat Lovers Meetup Delhi', 'Join fellow cat parents and feline friends for an exclusive indoor cat meetup featuring enrichment activities, vet Q&A, grooming tips, and a cozy chill zone for our furry companions.\r\n\r\n', '2025-05-13 16:09:00', '3 hours', 'Meow Town Café, Greater Kailash 2, New Delhi', ' https://goo.gl/maps/meowtown-delhi', 'Awareness', 'Cats only', 1, 40, 'static\\uploads\\20250418161116_ChatGPT_Image_Apr_18_2025_03_42_39_PM.png', 'Paw Haven', 'Pet Club', 'vishwapatel.21.cs@iite.indusuni.ac.in', '+91-9876543210‬', 'Lajpat Nagar, New Delhi, Delhi', 'Whiskas India, Catsvilla Grooming Studio, The Feline Foundation', 'Cats must be in carriers or harnesses when entering.\r\nOnly vaccinated and neutered/spayed cats allowed.\r\nPlease avoid bringing aggressive or anxious cats.\r\nTreats and litter trays will be provided.', 'approved', 'organization');

-- --------------------------------------------------------

--
-- Table structure for table `fundraisers`
--

CREATE TABLE `fundraisers` (
  `id` int(11) NOT NULL,
  `creator_id` int(11) NOT NULL,
  `creator_type` enum('user','organization') NOT NULL,
  `title` varchar(255) NOT NULL,
  `brief_description` text NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `funds_usage` text NOT NULL,
  `beneficiaries` text NOT NULL,
  `animals_helped` int(11) NOT NULL,
  `previous_efforts` text NOT NULL,
  `proof_document` varchar(255) NOT NULL,
  `donation_qr` varchar(255) NOT NULL,
  `upi_id` varchar(100) NOT NULL,
  `donor_message` text DEFAULT NULL,
  `social_media` varchar(255) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `endorsements` text DEFAULT NULL,
  `volunteer_info` text DEFAULT NULL,
  `emergency_contact` varchar(255) DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fundraisers`
--

INSERT INTO `fundraisers` (`id`, `creator_id`, `creator_type`, `title`, `brief_description`, `start_date`, `end_date`, `funds_usage`, `beneficiaries`, `animals_helped`, `previous_efforts`, `proof_document`, `donation_qr`, `upi_id`, `donor_message`, `social_media`, `website`, `endorsements`, `volunteer_info`, `emergency_contact`, `status`, `created_at`) VALUES
(1, 10, 'organization', 'Wants the fund to feeds the cat', 'We are organization which feeds the street cats we need support join us by donating us', '2025-04-07', '2025-04-14', 'We will feed the cats around streets in the city', 'Street and homeless cats', 100, 'We are trying this for the first time', 'need_of_proof.jpg', 'Donation_QR.png', 'SafePaws@okicici', 'Support us to help kittens ', '', '', '', '10', '9173784275', 'approved', '2025-04-07 11:02:12'),
(6, 11, 'organization', 'Hope for Paws: Emergency Rescue Support', 'We are raising funds to rescue, treat, and shelter injured and abandoned animals across the city. Every contribution brings them one step closer to safety and care.', '2025-04-18', '2025-04-20', 'Veterinary care (40%), food & nutrition (20%), temporary shelter upgrades (25%), vaccinations & medication (15%).', 'Injured street dogs, abandoned kittens, and rescued animals from illegal breeders.', 60, 'Yes – Last year’s “Paws First” campaign raised ₹1.2L, aiding 45 rescues with successful rehoming for 30 pets.', '141710fe-c2ad-4844-bdac-68a79b845fcf_pet_registration.jpg', 'Donation_QR.png', 'hopeforpaws@upi', 'Your kindness gives voiceless lives a second chance. Every rupee counts toward hope, healing, and happiness.', '', '', '', 'Yes – 20 active volunteers manage rescues, feeding drives, and shelter support on weekends.', 'Ram Patel – +91 123456789', 'approved', '2025-04-18 08:26:53'),
(7, 11, 'organization', 'Feeding Tails: Monsoon Relief for Strays', 'Monsoons leave hundreds of stray animals without shelter or food. Help us set up feeding stations and dry shelters to keep them safe and nourished.', '2025-04-24', '2025-04-30', 'Temporary waterproof shelters (30%), food supplies (50%), rain gear & bedding (10%), outreach & transport (10%).', 'Stray dogs and cats in flood-prone urban areas, especially elderly and injured animals.', 100, 'No – this is our first large-scale seasonal relief campaign.', '141710fe-c2ad-4844-bdac-68a79b845fcf_pet_registration.jpg', 'Donation_QR.png', 'feedingtails@oksbi', 'A warm meal and dry shelter can save a life. Join us in protecting these animals this rainy season.', '', '', 'Supported by RainSafe NGO and local pet store chain PawKart.', 'Over 30 volunteers will operate food stations and monitor animal safety zones during heavy rainfalls.', 'Ravi Sharma – +91 91234 56789', 'pending', '2025-04-18 08:30:25'),
(8, 11, 'organization', 'Feeding Tails: Monsoon Relief for Strays', 'Monsoons leave hundreds of stray animals without shelter or food. Help us set up feeding stations and dry shelters to keep them safe and nourished.', '2025-04-18', '2025-04-29', 'Temporary waterproof shelters (30%), food supplies (50%), rain gear & bedding (10%), outreach & transport (10%).', 'Stray dogs and cats in flood-prone urban areas, especially elderly and injured animals.', 100, 'No – this is our first large-scale seasonal relief campaign.', '141710fe-c2ad-4844-bdac-68a79b845fcf_pet_registration.jpg', 'Donation_QR.png', 'feedingtails@oksbi', 'A warm meal and dry shelter can save a life. Join us in protecting these animals this rainy season.', '', '', 'Supported by RainSafe NGO and local pet store chain PawKart.', 'Over 30 volunteers will operate food stations and monitor animal safety zones during heavy rainfalls.', 'Ravi Sharma – +91 91234 56789', 'approved', '2025-04-18 08:32:45');

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `post_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`id`, `user_id`, `org_id`, `post_id`, `created_at`) VALUES
(98, 12, NULL, 20, '2025-04-08 10:10:41'),
(100, 13, NULL, 20, '2025-04-12 07:44:04'),
(101, 13, NULL, 21, '2025-04-18 10:13:37'),
(107, 12, NULL, 22, '2025-04-28 16:42:23'),
(117, NULL, 6, 20, '2025-04-29 08:11:08'),
(124, NULL, 6, 22, '2025-04-29 13:39:24'),
(125, NULL, 6, 21, '2025-04-30 04:35:21');

-- --------------------------------------------------------

--
-- Table structure for table `meetup_participants`
--

CREATE TABLE `meetup_participants` (
  `id` int(11) NOT NULL,
  `meetup_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `joined_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `meetup_participants`
--

INSERT INTO `meetup_participants` (`id`, `meetup_id`, `user_id`, `joined_at`) VALUES
(2, 3, 1, '2025-04-17 07:02:17'),
(3, 11, 1, '2025-04-17 07:05:17'),
(18, 9, 1, '2025-04-17 11:10:27'),
(20, 12, 13, '2025-04-18 08:20:08'),
(21, 17, 13, '2025-04-18 10:47:20');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `type` varchar(50) NOT NULL,
  `reference_id` int(11) DEFAULT NULL,
  `reference_type` varchar(50) NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `org_id`, `message`, `type`, `reference_id`, `reference_type`, `is_read`, `created_at`) VALUES
(0, NULL, 10, 'Ketul Patel has joined your event: Pet Playdate in the Park', 'join', 12, 'meetup', 1, '2025-04-18 08:19:37'),
(0, NULL, 10, 'Ketul Patel has left your event: Pet Playdate in the Park', 'leave', 12, 'meetup', 1, '2025-04-18 08:20:02'),
(0, NULL, 10, 'Ketul Patel has joined your event: Pet Playdate in the Park', 'join', 12, 'meetup', 1, '2025-04-18 08:20:08'),
(0, NULL, 11, 'Your fundraiser request has been approved', 'status_change', 6, 'fundraiser', 1, '2025-04-18 08:27:21'),
(0, NULL, 11, 'Your fundraiser request has been approved', 'status_change', 7, 'fundraiser', 1, '2025-04-18 08:30:31'),
(0, NULL, 11, 'Your fundraiser request has been pending', 'status_change', 7, 'fundraiser', 1, '2025-04-18 08:30:56'),
(0, NULL, 11, 'Your fundraiser request has been approved', 'status_change', 7, 'fundraiser', 1, '2025-04-18 08:31:03'),
(0, NULL, 11, 'Your fundraiser request has been pending', 'status_change', 7, 'fundraiser', 1, '2025-04-18 08:31:42'),
(0, NULL, 11, 'Your fundraiser request has been approved', 'status_change', 8, 'fundraiser', 1, '2025-04-18 08:32:52'),
(0, 13, NULL, 'Your pet listing status has been approved', 'status_change', 5, 'pet', 1, '2025-04-18 09:52:39'),
(0, 13, NULL, 'Your pet listing status has been approved', 'status_change', 6, 'pet', 1, '2025-04-18 09:57:45'),
(0, NULL, 12, 'Your meet-up event has been approved', 'status_change', 17, 'event', 1, '2025-04-18 10:41:21'),
(0, NULL, 12, 'Your meet-up event has been approved', 'status_change', 18, 'event', 1, '2025-04-18 10:41:22'),
(0, NULL, 12, 'Your organization verification has been verified', 'status_change', 12, 'organization', 1, '2025-04-18 10:45:38'),
(0, NULL, 12, 'Ketul Patel has joined your event: Wag & Walk – Dog Meetup Mumbai', 'join', 17, 'meetup', 1, '2025-04-18 10:47:20'),
(0, NULL, 10, 'kalp pandya has joined your event: Pet Playdate in the Park', 'join', 12, 'meetup', 0, '2025-04-30 05:54:37'),
(0, NULL, 10, 'kalp pandya has left your event: Pet Playdate in the Park', 'leave', 12, 'meetup', 0, '2025-04-30 05:54:56');

-- --------------------------------------------------------

--
-- Table structure for table `organizations`
--

CREATE TABLE `organizations` (
  `id` int(11) NOT NULL,
  `org_name` varchar(255) NOT NULL,
  `org_type` enum('shelter','rescue','ngo','other') NOT NULL,
  `state` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `username` varchar(50) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT 'default.jpg',
  `website` varchar(255) DEFAULT NULL,
  `social_media` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `reg_number` varchar(100) DEFAULT NULL,
  `years_operation` int(11) DEFAULT NULL,
  `emergency_contact` varchar(15) DEFAULT NULL,
  `reg_certificate` varchar(255) DEFAULT NULL,
  `tax_certificate` varchar(255) DEFAULT NULL,
  `rep_name` varchar(255) DEFAULT NULL,
  `rep_id_proof` varchar(255) DEFAULT NULL,
  `mission` text DEFAULT NULL,
  `status` enum('verified','pending','rejected') NOT NULL DEFAULT 'pending',
  `user_type` varchar(100) NOT NULL DEFAULT 'organization',
  `slogan` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `organizations`
--

INSERT INTO `organizations` (`id`, `org_name`, `org_type`, `state`, `city`, `phone`, `email`, `password`, `created_at`, `username`, `profile_pic`, `website`, `social_media`, `address`, `reg_number`, `years_operation`, `emergency_contact`, `reg_certificate`, `tax_certificate`, `rep_name`, `rep_id_proof`, `mission`, `status`, `user_type`, `slogan`) VALUES
(6, 'Doggy hub', '', 'GJ', 'Ahmedabad', '0123456789', 'Doggy@gmail.com', 'K@lp2604', '2025-02-19 13:08:26', 'doggy_hub', 'default.jpg\r\n', '', '', 'dfhgfgfn', '1', 5, '0123456789', 'static/uploads/login.jpeg', 'static/uploads/login.jpeg', 'PANDYA KALP', 'static/uploads/login.jpeg', 'hello ', 'pending', 'organization', 'hello '),
(10, 'SafePaws Alliance', '', 'GJ', 'Ahmedabad', '9173784275', 'kalppandya26@gmail.com', 'K@lp2604', '2025-04-07 10:52:21', 'admin', 'default.jpg\r\n', '', '', 'Ghodasar,380050,Ahmedabad', '1000009', 5, '9173784275', 'static/uploads/need_of_proof.jpg', NULL, 'PANDYA KALP', 'static/uploads/adharcard.webp', 'We are here to help pets around the city', 'verified', 'organization', NULL),
(12, 'Paw Haven', '', 'GJ', 'Ahmedabad', '9874561234', 'vishwapatel.21.cs@iite.indusuni.ac.in', 'V@v123456', '2025-04-18 10:37:52', NULL, 'default.jpg', '', '', 'Bandra East, Mumbai, Maharashtra', '1425525145', 2, '09090123456', 'static/uploads/need_of_proof.jpg', NULL, 'vishwa patel', 'static/uploads/adharcard.webp', 'To promate animal welfare', 'verified', 'organization', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pets`
--

CREATE TABLE `pets` (
  `id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `owner_type` enum('user','doctor','organization') NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `pet_name` varchar(255) NOT NULL,
  `species` enum('Dog','Cat') NOT NULL,
  `breed` varchar(255) DEFAULT NULL,
  `age` int(11) NOT NULL,
  `gender` enum('Male','Female') NOT NULL,
  `reason` text NOT NULL,
  `pet_image` varchar(255) DEFAULT NULL,
  `reg_certificate` varchar(255) DEFAULT NULL,
  `vaccination_records` varchar(255) DEFAULT NULL,
  `climate_suitability` enum('Warm Climates','Cold Climates','Adaptable') NOT NULL,
  `energy_level` enum('Low','Moderate','High') NOT NULL,
  `social_compatibility` enum('Good with Kids','Good with Other Dogs','Good with Cats','Prefers to be the Only Pet') NOT NULL,
  `status` enum('pending','approved','rejected','removed') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pets`
--

INSERT INTO `pets` (`id`, `owner_id`, `owner_type`, `full_name`, `contact_number`, `email`, `location`, `pet_name`, `species`, `breed`, `age`, `gender`, `reason`, `pet_image`, `reg_certificate`, `vaccination_records`, `climate_suitability`, `energy_level`, `social_compatibility`, `status`, `created_at`) VALUES
(1, 12, 'user', 'kalp pandya', '9173784275', 'kalppandya1511@gmail.com', 'Ahmedabad,Gujarat,380050', 'Mousy', 'Cat', 'American Shorthair', 3, 'Female', 'There is no one to take care of her', '6614bd02-233c-465a-88af-1cbfcf853188_kitten_for_rehome.jpg', '141710fe-c2ad-4844-bdac-68a79b845fcf_pet_registration.jpg', '3932b01b-025a-4cbe-8f21-163332c97736_pet_vaccination.jpg', 'Cold Climates', 'Moderate', 'Good with Kids', 'approved', '2025-04-07 11:10:56'),
(5, 13, 'user', 'Sarah Thompson', '+91 9123456788', 'ketul1386@gmail.com', 'Surat', 'Max', 'Dog', 'Golden Retriever', 3, 'Male', 'Due to relocation overseas, I am unable to take Max with me and want to ensure he finds a loving home.\r\n\r\n', '3d05d8df-8d1e-4f34-9878-0654ed19767b_images.jpeg.jpg', '8b5a9ee1-ef8e-4b3b-8466-1c09938b4518_141710fe-c2ad-4844-bdac-68a79b845fcf_pet_registration.jpg', '6925e2fc-a65e-4c6e-a013-7ef503479bc1_pet_vaccination.jpg', 'Adaptable', 'Moderate', 'Good with Kids', 'approved', '2025-04-18 09:52:24'),
(6, 13, 'user', 'Priya Nair', ' ‪+91-9876543210‬', 'ketul1386@gmail.com', 'Andheri East, Mumbai, Maharashtra', 'Miso', 'Cat', 'Persian', 2, 'Female', 'I recently started a job that requires extensive travel, and I am unable to give Miso the attention and care she deserves.', 'bca539a4-1c66-43bf-9109-e609316994a3_persian-cat-breed.avif', '1eddedca-3b09-4c09-8b12-275260c4b75d_pet_registration.jpg', 'e6cb2fcd-6bb7-4908-8d8e-1ef9550530de_pet_vaccination.jpg', 'Warm Climates', 'Low', 'Prefers to be the Only Pet', 'approved', '2025-04-18 09:57:38');

-- --------------------------------------------------------

--
-- Table structure for table `pet_adoption_forms`
--

CREATE TABLE `pet_adoption_forms` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `street_address` varchar(255) NOT NULL,
  `apartment` varchar(100) DEFAULT NULL,
  `country` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `home_ownership` enum('Own','Rent') NOT NULL,
  `landlord_pet_policy` enum('Yes','No','Not Sure') DEFAULT NULL,
  `pet_name_id` varchar(100) NOT NULL,
  `reason_adoption` text NOT NULL,
  `prior_experience` enum('Yes','No') NOT NULL,
  `current_pets` enum('Yes','No') NOT NULL,
  `financial_preparedness` enum('Yes','No') NOT NULL,
  `emergency_plan` text NOT NULL,
  `contact_method` enum('Email','Phone') NOT NULL,
  `visit_pet` enum('Yes','No') NOT NULL,
  `additional_message` text DEFAULT NULL,
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pet_adoption_forms`
--

INSERT INTO `pet_adoption_forms` (`id`, `user_id`, `org_id`, `full_name`, `email`, `phone`, `street_address`, `apartment`, `country`, `state`, `city`, `postal_code`, `home_ownership`, `landlord_pet_policy`, `pet_name_id`, `reason_adoption`, `prior_experience`, `current_pets`, `financial_preparedness`, `emergency_plan`, `contact_method`, `visit_pet`, `additional_message`, `submitted_at`) VALUES
(1, 13, NULL, 'Patel', 'kalppandya26@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', 'ssdsdd', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 11:48:52'),
(2, 13, NULL, 'Patel', 'kalppandya26@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', 'ssdsdd', 'i lave cats', 'Yes', 'No', 'Yes', 'i will go to pet clini', 'Email', 'Yes', '', '2025-04-17 11:49:33'),
(3, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 11:59:23'),
(4, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:00:36'),
(5, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:01:14'),
(6, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:01:18'),
(7, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:02:16'),
(8, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:02:28'),
(9, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:03:06'),
(10, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:03:54'),
(11, 13, NULL, 'Patel Ketul', 'ketul1386@gmail.com', '01234567891', 'Surat, Gujarat', '1233', 'India', 'GJ', 'surat', '394210', 'Own', '', '1', 'i love cats', 'Yes', 'No', 'Yes', 'i will go to pet clinic', 'Email', 'Yes', '', '2025-04-17 12:04:08'),
(12, 12, NULL, 'PANDYA KALP', 'kalppandya26@gmail.com', '09173784275', 'maninagar', '6', 'India', 'Gujarat', 'Ahmedabad', '380050', 'Own', 'Yes', '1', 'none', 'No', 'No', 'Yes', 'ill care', 'Email', 'Yes', '', '2025-04-30 08:18:44'),
(13, 12, NULL, 'PANDYA KALP', 'kalppandya26@gmail.com', '09173784275', 'maninagar', '6', 'India', 'Gujarat', 'Ahmedabad', '380050', 'Own', 'Yes', '5', 'none', 'Yes', 'Yes', 'Yes', 'ill care', 'Phone', 'No', '', '2025-04-30 08:28:41');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `image` varchar(255) NOT NULL,
  `caption` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `user_id`, `org_id`, `image`, `caption`, `created_at`) VALUES
(20, 12, NULL, 'facf06fef71e48138206e108bf5f1fd7.jpg', 'My Cutee Furryy Friend!!', '2025-04-08 10:07:17'),
(21, 13, NULL, 'b70d30930947462e8df7e477488465dd.jpg', '\"Serving royal looks and paw-sitive vibes ????????✨ #CatwalkQueen #PurrfectPrincess #FelineFashionista\"', '2025-04-18 10:13:29'),
(22, 13, NULL, '7b9c0e4f652b4a68a6e9281aad3d5a4e.jpg', '\"Serving royal looks and paw-sitive vibes #CatwalkQueen #PurrfectPrincess #FelineFashionista\"', '2025-04-18 10:22:28');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT 'default.jpg',
  `slogan` text DEFAULT 'Your slogan here',
  `username` varchar(100) DEFAULT 'pawpromise',
  `user_type` varchar(100) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `gender`, `state`, `city`, `phone`, `email`, `password`, `profile_pic`, `slogan`, `username`, `user_type`) VALUES
(11, 'Dhyan', 'bhatt', 'male', 'GJ', 'Ahmedabad', '1234567890', 'bhattdhyan056@gmail.com', 'K@lp2604', 'default.jpg', 'Your slogan here', 'dhyan_bhatt', 'user'),
(12, 'kalp', 'pandya', 'male', 'GJ', 'Ahmedabad', '9173784275', 'kalppandya1511@gmail.com', 'K@lp2604', 'default.jpg', 'In Love With Paws', 'Priyanshi', 'user'),
(13, 'Ketul', 'Patel', 'male', 'GJ', 'Ahmedabad', '987918889', 'ketul1386@gmail.com', 'K@lp2604', 'default.jpg', 'Proud to be a Pet Lover', 'ketulpatel', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`);

--
-- Indexes for table `chat_sessions`
--
ALTER TABLE `chat_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `comments_ibfk_3` (`org_id`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`organizer_id`);

--
-- Indexes for table `fundraisers`
--
ALTER TABLE `fundraisers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`post_id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `likes_ibfk_3` (`org_id`);

--
-- Indexes for table `meetup_participants`
--
ALTER TABLE `meetup_participants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `meetup_user_unique` (`meetup_id`,`user_id`),
  ADD KEY `meetup_id` (`meetup_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `organizations`
--
ALTER TABLE `organizations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `pets`
--
ALTER TABLE `pets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pet_adoption_forms`
--
ALTER TABLE `pet_adoption_forms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_adopt_user` (`user_id`),
  ADD KEY `fk_adopt_org` (`org_id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `posts_ibfk_2` (`org_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chat_messages`
--
ALTER TABLE `chat_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;

--
-- AUTO_INCREMENT for table `chat_sessions`
--
ALTER TABLE `chat_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `fundraisers`
--
ALTER TABLE `fundraisers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT for table `meetup_participants`
--
ALTER TABLE `meetup_participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `organizations`
--
ALTER TABLE `organizations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `pets`
--
ALTER TABLE `pets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `pet_adoption_forms`
--
ALTER TABLE `pet_adoption_forms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `chat_sessions`
--
ALTER TABLE `chat_sessions`
  ADD CONSTRAINT `chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_sessions_ibfk_2` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_3` FOREIGN KEY (`organizer_id`) REFERENCES `organizations` (`id`);

--
-- Constraints for table `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `likes_ibfk_3` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pet_adoption_forms`
--
ALTER TABLE `pet_adoption_forms`
  ADD CONSTRAINT `fk_adopt_org` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_adopt_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `posts_ibfk_2` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
