-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: dbspecifique
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

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
-- Table structure for table `Affectation`
--

DROP TABLE IF EXISTS `Affectation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Affectation` (
  `CodeEnseignantfk` varchar(50) NOT NULL,
  `CodeCoursfk` varchar(50) NOT NULL,
  PRIMARY KEY (`CodeEnseignantfk`,`CodeCoursfk`),
  KEY `CodeCoursfk` (`CodeCoursfk`),
  CONSTRAINT `Affectation_ibfk_1` FOREIGN KEY (`CodeCoursfk`) REFERENCES `Cours` (`CodeCours`),
  CONSTRAINT `Affectation_ibfk_2` FOREIGN KEY (`CodeEnseignantfk`) REFERENCES `Enseignant` (`CodeEnseignant`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Affectation`
--

LOCK TABLES `Affectation` WRITE;
/*!40000 ALTER TABLE `Affectation` DISABLE KEYS */;
/*!40000 ALTER TABLE `Affectation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Classe`
--

DROP TABLE IF EXISTS `Classe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Classe` (
  `CodeClasse` varchar(50) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `CodeEtablissementfk` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodeClasse`),
  KEY `CodeEtablissementfk` (`CodeEtablissementfk`),
  CONSTRAINT `Classe_ibfk_1` FOREIGN KEY (`CodeEtablissementfk`) REFERENCES `Etablissement` (`CodeEtablissement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Classe`
--

LOCK TABLES `Classe` WRITE;
/*!40000 ALTER TABLE `Classe` DISABLE KEYS */;
INSERT INTO `Classe` VALUES ('ESI1','Premiere annee','ESI'),('ESI2','Deuxieme annee','ESI'),('ESI3','Troisieme  annee','ESI');
/*!40000 ALTER TABLE `Classe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Competence`
--

DROP TABLE IF EXISTS `Competence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Competence` (
  `CodeCompetence` varchar(50) NOT NULL,
  `Description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CodeCompetence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Competence`
--

LOCK TABLES `Competence` WRITE;
/*!40000 ALTER TABLE `Competence` DISABLE KEYS */;
INSERT INTO `Competence` VALUES ('D1INF1100cm','Utilisation des systèmes d\'exploitation les plus courants'),('D1INF1100tp','Utilisation des systèmes d\'exploitation les plus courants tp'),('D1INF1101cm','Algorithmique et structures de données statiques cm'),('D1INF1101td','Algorithmique et structures de données statiques td'),('D1INF1102cm','Programmation cm'),('D1INF1102tp','Programmation tp'),('D1INF1103cm','Logique et raisonnement cm'),('D1INF1103td','Logique et raisonnement td'),('D1INF1104cm','Analyse 1 cm'),('D1INF1104td','Analyse 1 td'),('D1INF1105cm','Statistiques descriptives cm'),('D1INF1105td','Statistiques descriptives td'),('D1INF1106cm','Électrocinétique cm'),('D1INF1106td','Électrocinétique td'),('D1INF1106tp','Électrocinétique tp'),('D1INF1107cm','Comptabilité Générale cm'),('D1INF1107td','Comptabilité Générale td'),('D1INF1108cm','Anglais 1 cm'),('D1INF1108td','Anglais 1 td'),('D1INF1600cm','Algorithmique et structures de données dynamiques cm'),('D1INF1600td','Algorithmique et structures de données dynamiques td'),('D1INF1600tp','Algorithmique et structures de données dynamiques tp'),('D1INF1601cm','Électronique numérique cm'),('D1INF1601td','Électronique numérique td'),('D1INF1601tp','Électronique numérique tp'),('D1INF1602cm','Architecture et fonctionnement des ordinateurs cm'),('D1INF1602td','Architecture et fonctionnement des ordinateurs td'),('D1INF1602tp','Architecture et fonctionnement des ordinateurs tp'),('D1INF1603cm','Algèbre générale cm'),('D1INF1603td','Algèbre générale td'),('D1INF1604cm','Analyse 2 cm'),('D1INF1604td','Analyse 2 td'),('D1INF1605cm','Électronique analogique cm'),('D1INF1605td','Électronique analogique td'),('D1INF1606cm','Économie générale cm'),('D1INF1607cm','Anglais 2 cm'),('D1INF1607td','Anglais 2 td'),('D2INF1100cm','Bureautique td'),('D2INF1100td','Bureautique cm'),('D2INF1106cm','Électrostatique cm'),('D2INF1106td','Électrostatique td'),('D2INF1108cm','Techniques d\'expression 1 cm'),('D2INF1108td','Techniques d\'expression 1 td'),('D2INF1600cm','Introduction à la programmation web cm'),('D2INF1600tp','Introduction à la programmation web tp'),('D2INF1603cm','Algèbre linéaire 1 cm'),('D2INF1603td','Algèbre linéaire 1 td'),('D2INF1605cm','Électromagnétisme cm'),('D2INF1605td','Électromagnétisme td'),('D2INF1607cm','Techniques d\'expression 2 cm'),('D2INF1607td','Techniques d\'expression 2 td'),('N1INF1100cm','Utilisation des systèmes d\'exploitation les plus courants'),('N1INF1100tp','Utilisation des systèmes d\'exploitation les plus courants tp'),('N1INF1101cm','Algorithmique et structures de données statiques cm'),('N1INF1101td','Algorithmique et structures de données statiques td'),('N1INF1102cm','Programmation cm'),('N1INF1102tp','Programmation tp'),('N1INF1103cm','Logique et raisonnement cm'),('N1INF1103td','Logique et raisonnement td'),('N1INF1104cm','Analyse 1 cm'),('N1INF1104td','Analyse 1 td'),('N1INF1105cm','Statistiques descriptives cm'),('N1INF1105td','Statistiques descriptives td'),('N1INF1106cm','Électrocinétique cm'),('N1INF1106td','Électrocinétique td'),('N1INF1106tp','Électrocinétique tp'),('N1INF1107cm','Comptabilité Générale cm'),('N1INF1107td','Comptabilité Générale td'),('N1INF1108cm','Anglais 1 cm'),('N1INF1108td','Anglais 1 td'),('N1INF1600cm','Algorithmique et structures de données dynamiques cm'),('N1INF1600td','Algorithmique et structures de données dynamiques td'),('N1INF1600tp','Algorithmique et structures de données dynamiques tp'),('N1INF1601cm','Électronique numérique cm'),('N1INF1601td','Électronique numérique td'),('N1INF1601tp','Électronique numérique tp'),('N1INF1602cm','Architecture et fonctionnement des ordinateurs cm'),('N1INF1602td','Architecture et fonctionnement des ordinateurs td'),('N1INF1602tp','Architecture et fonctionnement des ordinateurs tp'),('N1INF1603cm','Algèbre générale cm'),('N1INF1603td','Algèbre générale td'),('N1INF1604cm','Analyse 2 cm'),('N1INF1604td','Analyse 2 td'),('N1INF1605cm','Électronique analogique cm'),('N1INF1605td','Électronique analogique td'),('N1INF1606cm','Économie générale cm'),('N1INF1607cm','Anglais 2 cm'),('N1INF1607td','Anglais 2 td'),('N2INF1100cm','Bureautique td'),('N2INF1100td','Bureautique cm'),('N2INF1106cm','Électrostatique cm'),('N2INF1106td','Électrostatique td'),('N2INF1108cm','Techniques d\'expression 1 cm'),('N2INF1108td','Techniques d\'expression 1 td'),('N2INF1600cm','Introduction à la programmation web cm'),('N2INF1600tp','Introduction à la programmation web tp'),('N2INF1603cm','Algèbre linéaire 1 cm'),('N2INF1603td','Algèbre linéaire 1 td'),('N2INF1605cm','Électromagnétisme cm'),('N2INF1605td','Électromagnétisme td'),('N2INF1607cm','Techniques d\'expression 2 cm'),('N2INF1607td','Techniques d\'expression 2 td');
/*!40000 ALTER TABLE `Competence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CompetencePossede`
--

DROP TABLE IF EXISTS `CompetencePossede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CompetencePossede` (
  `CodeCompetencefk` varchar(50) NOT NULL,
  `CodeEnseignantfk` varchar(50) NOT NULL,
  PRIMARY KEY (`CodeCompetencefk`,`CodeEnseignantfk`),
  KEY `CodeEnseignantfk` (`CodeEnseignantfk`),
  CONSTRAINT `CompetencePossede_ibfk_1` FOREIGN KEY (`CodeEnseignantfk`) REFERENCES `Enseignant` (`CodeEnseignant`),
  CONSTRAINT `CompetencePossede_ibfk_2` FOREIGN KEY (`CodeCompetencefk`) REFERENCES `Competence` (`CodeCompetence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CompetencePossede`
--

LOCK TABLES `CompetencePossede` WRITE;
/*!40000 ALTER TABLE `CompetencePossede` DISABLE KEYS */;
INSERT INTO `CompetencePossede` VALUES ('D2INF1100td','10'),('N1INF1100tp','10'),('N1INF1101td','10'),('N1INF1102tp','10'),('N1INF1101cm','102 929 F'),('N1INF1101td','102 929 F'),('N1INF1102cm','102 929 F'),('N1INF1102tp','102 929 F'),('D1INF1101cm','13'),('D1INF1101td','13'),('D1INF1102cm','13'),('D1INF1102tp','13'),('N1INF1100cm','13'),('N1INF1100tp','13'),('N2INF1100cm','13'),('N2INF1100td','13'),('D2INF1106cm','2'),('D2INF1106td','2'),('D1INF1104td','20'),('D1INF1105cm','20'),('D1INF1105td','20'),('N1INF1103td','20'),('D1INF1106cm','22'),('D1INF1106td','22'),('D1INF1106tp','22'),('D1INF1100tp','241865 R'),('D1INF1101td','241865 R'),('N1INF1101cm','241865 R'),('N1INF1102tp','241865 R'),('N1INF1103td','241865 R'),('N2INF1100cm','241865 R'),('D1INF1101td','257259 J'),('D1INF1102tp','257270 G'),('D1INF1108cm','27'),('D1INF1108td','27'),('N1INF1100tp','271381 U'),('N1INF1101cm','271381 U'),('N1INF1101td','271381 U'),('N2INF1100td','271381 U'),('D2INF1108cm','28'),('D2INF1108td','28'),('D1INF1100cm','3'),('D1INF1100tp','3'),('D1INF1101td','3'),('D1INF1102tp','3'),('D2INF1100cm','3'),('D2INF1100td','3'),('D1INF1107cm','31'),('D1INF1107td','31'),('D1INF1101cm','45763 D'),('N1INF1103cm','50'),('N1INF1103td','50'),('N2INF1108cm','50'),('N2INF1108td','50'),('N1INF1104cm','59'),('N1INF1104td','59'),('N1INF1105cm','59'),('N1INF1105td','59'),('N1INF1105cm','60'),('N1INF1105td','60'),('N1INF1107cm','61'),('N1INF1104cm','62'),('N1INF1104td','62'),('N1INF1105cm','62'),('N1INF1105td','62'),('N1INF1103cm','63'),('N1INF1105cm','63'),('N1INF1104cm','64'),('N1INF1104td','64'),('N1INF1105cm','64'),('N1INF1105td','64'),('D2INF1100cm','8'),('D2INF1100td','8'),('N1INF1101td','8'),('N1INF1102cm','8'),('N1INF1102tp','8');
/*!40000 ALTER TABLE `CompetencePossede` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cours`
--

DROP TABLE IF EXISTS `Cours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cours` (
  `CodeCours` varchar(50) NOT NULL,
  `Description` varchar(100) DEFAULT NULL,
  `VolumeHoraire` float DEFAULT NULL,
  `DateAuPlusTard` date DEFAULT NULL,
  `Statut` enum('NonAffecte','Affecte','EnCours','Termine') DEFAULT NULL,
  `Semestrefk` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`CodeCours`),
  KEY `Semestrefk` (`Semestrefk`),
  CONSTRAINT `Semestrefk` FOREIGN KEY (`Semestrefk`) REFERENCES `Semestre` (`CodeSemestre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cours`
--

LOCK TABLES `Cours` WRITE;
/*!40000 ALTER TABLE `Cours` DISABLE KEYS */;
INSERT INTO `Cours` VALUES ('1INF1100cm','Utilisation des systèmes d\'exploitation les plus courants',10,NULL,'NonAffecte','S1'),('1INF1100tp','Utilisation des systèmes d\'exploitation les plus courants tp',20,NULL,'NonAffecte','S1'),('1INF1101cm','Algorithmique et structures de données statiques cm',30,NULL,'NonAffecte','S1'),('1INF1101td','Algorithmique et structures de données statiques td',30,NULL,'NonAffecte','S1'),('1INF1102cm','Programmation cm',15,NULL,'NonAffecte','S1'),('1INF1102tp','Programmation tp',45,NULL,'NonAffecte','S1'),('1INF1103cm','Logique et raisonnement cm',15,NULL,'NonAffecte','S1'),('1INF1103td','Logique et raisonnement td',15,NULL,'NonAffecte','S1'),('1INF1104cm','Analyse 1 cm',23,NULL,'NonAffecte','S1'),('1INF1104td','Analyse 1 td',22,NULL,'NonAffecte','S1'),('1INF1105cm','Statistiques descriptives cm',15,NULL,'NonAffecte','S1'),('1INF1105td','Statistiques descriptives td',15,NULL,'NonAffecte','S1'),('1INF1106cm','Électrocinétique cm',23,NULL,'NonAffecte','S1'),('1INF1106td','Électrocinétique td',15,NULL,'NonAffecte','S1'),('1INF1106tp','Électrocinétique tp',7,NULL,'NonAffecte','S1'),('1INF1107cm','Comptabilité Générale cm',25,NULL,'NonAffecte','S1'),('1INF1107td','Comptabilité Générale td',20,NULL,'NonAffecte','S1'),('1INF1108cm','Anglais 1 cm',15,NULL,'NonAffecte','S1'),('1INF1108td','Anglais 1 td',15,NULL,'NonAffecte','S1'),('2INF1100cm','Bureautique td',10,NULL,'NonAffecte','S1'),('2INF1100td','Bureautique cm',20,NULL,'NonAffecte','S1'),('2INF1106cm','Électrostatique cm',8,NULL,'NonAffecte','S1'),('2INF1106td','Électrostatique td',7,NULL,'NonAffecte','S1'),('2INF1108cm','Techniques d\'expression 1 cm',13,NULL,'NonAffecte','S1'),('2INF1108td','Techniques d\'expression 1 td',17,NULL,'NonAffecte','S1');
/*!40000 ALTER TABLE `Cours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Enseignant`
--

DROP TABLE IF EXISTS `Enseignant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Enseignant` (
  `CodeEnseignant` varchar(50) NOT NULL,
  `Nom` varchar(100) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `CodeGradefk` varchar(50) DEFAULT NULL,
  `Statut` int DEFAULT NULL,
  `Abattement` int DEFAULT NULL,
  PRIMARY KEY (`CodeEnseignant`),
  UNIQUE KEY `Email` (`Email`),
  KEY `CodeGradefk` (`CodeGradefk`),
  CONSTRAINT `Enseignant_ibfk_1` FOREIGN KEY (`CodeGradefk`) REFERENCES `Grade` (`CodeGrade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Enseignant`
--

LOCK TABLES `Enseignant` WRITE;
/*!40000 ALTER TABLE `Enseignant` DISABLE KEYS */;
INSERT INTO `Enseignant` VALUES ('1','YELEMOU Tiguiane ',NULL,'PT',1,0),('10','SANOU François d\'Assise',NULL,'Master',0,0),('102 929 F','SOME Borlli Michel Jonas',NULL,'MC',1,0),('11','COULIBALY Dramane',NULL,'Master',1,0),('110980A','MALO Sadouanouan',NULL,'PT',1,0),('12','SANOU Affoussatou Rolande',NULL,'Doctorat',1,0),('13','TRAORE Go Issa',NULL,'Master',0,0),('15','SOULAMA Zidama',NULL,'Master',1,0),('16','TAPSOBA Théodore M. Y.',NULL,'PT',1,0),('17','BARRO Moussa',NULL,'MA',0,0),('18','KABORE Idrissa',NULL,'PT',0,0),('2','Kiélem Wilfried Albert Duniwangda',NULL,'Master',1,0),('20','SANKARA Karim',NULL,'Doctorat',0,0),('21','TRAORE Bakary',NULL,'MC',0,0),('22','KABORE M\'Bi',NULL,'MC',1,0),('23','SAWADOGO Gaël',NULL,'Doctorat',0,0),('24','OUEDRAOGO Drissa',NULL,'Doctorat',0,0),('241865 R','OUATTARA Anasthasie',NULL,'MA',1,0),('25','GOUNKAOU Yomi Woro',NULL,'Doctorat',0,0),('257259 J','BELEM Mahamadou',NULL,'MC',1,0),('257270 G','ZOUMORE Téeg-wendé Gildas',NULL,'A',1,0),('26','GNANOU Aboubacar',NULL,'Doctorat',0,0),('27','COULIBALY Samadou',NULL,'MC',0,0),('271381 U','KINDO Abdoul Azize',NULL,'A',1,0),('28','SANOU Abel',NULL,'MC',0,0),('29','KPODA Gabin',NULL,'MC',0,0),('3','KAFANDO Patrice',NULL,'Master',1,0),('30','ROMBA Christian',NULL,'A',0,0),('31','GNOUMOU GNOUMOU',NULL,'A',0,0),('32','PORGO Inoussa',NULL,'A',0,0),('33','AGBEZOUTSI Edem Kodjo',NULL,'A',1,0),('34','SORE Herman',NULL,'MA',0,0),('348101 V','TALL Hamadoun',NULL,'MA',1,0),('35','COULIBALY Siaka',NULL,'MA',0,0),('36','NANA Mahamadi',NULL,'MA',0,0),('37','KAM Grégoire',NULL,'MA',0,0),('38','NYANQUINI Ismaël',NULL,'MA',0,0),('39','OUEDRAOGO Seydou',NULL,'MC',0,0),('4','PODA Ives Emile',NULL,'Master',1,0),('40','KAM Dieudonné',NULL,'MA',0,0),('41','COULIBALY Soungalo ',NULL,'MA',0,0),('42','MASSAMBA Ange',NULL,'Doctorat',0,0),('43','PODA Joseph',NULL,'MA',0,0),('44','YATABARE Abdoulaye',NULL,'MA',0,0),('45','ZONGO Gilbert',NULL,'Doctorat',0,0),('45763 D','DANDJINOU Toundé Mesmin',NULL,'MC',1,0),('46','ZERBO Abdoulaye',NULL,'Doctorat',0,0),('47','TRAORE Abdoulaye',NULL,'Doctorat',0,0),('48','DIALLO Abdoul Karim D.',NULL,'Master',1,0),('49','BEYI Boukari',NULL,'MA',0,0),('5','SIEBA Idriss',NULL,'Master',1,0),('50','COULIBALY Dieudonné',NULL,'MA',0,0),('51','SAWADOGO Issaka',NULL,'Doctorat',0,0),('52','OUEDRAOGO Moutawakilou',NULL,'Doctorat',0,0),('53','BARRA Ousmane',NULL,'Doctorat',0,0),('54','OUEDRAOGO Boris',NULL,'MC',0,0),('55','SAWADOGO Marc',NULL,'Doctorat',0,0),('56','SAWADOGO Moumouni',NULL,'Doctorat',0,0),('57','THIOMBIANO Aristide',NULL,'Doctorat',0,0),('58','DRABO Constantin',NULL,'Doctorat',0,0),('59','Yoda',NULL,'Doctorat',0,0),('6','BOULOU Mahamadi',NULL,'Doctorat',1,0),('60','TRAORE Issouf',NULL,'Master',0,0),('61','Yameogo w Blaise ',NULL,'A',1,0),('62','OUEDRAOGO Bèbyada Thomas',NULL,'A',0,0),('63','Joseph Bayara ',NULL,'MC',1,0),('64','Zongo',NULL,'A',1,0),('7','KONFE Abdoul Hadi',NULL,'Doctorat',1,0),('8','ILLY Amado',NULL,'Master',0,0),('9','KINDA Zakaria',NULL,'Master',1,0),('91621 A','PODA Pasteur',NULL,'MC',1,0);
/*!40000 ALTER TABLE `Enseignant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Etablissement`
--

DROP TABLE IF EXISTS `Etablissement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Etablissement` (
  `CodeEtablissement` varchar(50) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodeEtablissement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Etablissement`
--

LOCK TABLES `Etablissement` WRITE;
/*!40000 ALTER TABLE `Etablissement` DISABLE KEYS */;
INSERT INTO `Etablissement` VALUES ('ESI','Ecole informatique');
/*!40000 ALTER TABLE `Etablissement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Grade`
--

DROP TABLE IF EXISTS `Grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Grade` (
  `CodeGrade` varchar(50) NOT NULL,
  `Nom` varchar(50) DEFAULT NULL,
  `VolumeHoraireStatuitaire` int DEFAULT NULL,
  `Abatement` int DEFAULT NULL,
  PRIMARY KEY (`CodeGrade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Grade`
--

LOCK TABLES `Grade` WRITE;
/*!40000 ALTER TABLE `Grade` DISABLE KEYS */;
INSERT INTO `Grade` VALUES ('A','Assistant',260,0),('Doctorat','Doctorat',270,0),('MA','Maitre Assistant',240,0),('Master','Master',280,0),('MC','Maitre de Ceremonie',220,0),('PT','Professeur Titulaire',200,0);
/*!40000 ALTER TABLE `Grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Preference`
--

DROP TABLE IF EXISTS `Preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Preference` (
  `CodeCoursfk` varchar(50) NOT NULL,
  `CodeEnseignantfk` varchar(50) NOT NULL,
  `disponibilite` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`CodeCoursfk`,`CodeEnseignantfk`),
  KEY `CodeEnseignantfk` (`CodeEnseignantfk`),
  CONSTRAINT `Preference_ibfk_1` FOREIGN KEY (`CodeEnseignantfk`) REFERENCES `Enseignant` (`CodeEnseignant`),
  CONSTRAINT `Preference_ibfk_2` FOREIGN KEY (`CodeCoursfk`) REFERENCES `Cours` (`CodeCours`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Preference`
--

LOCK TABLES `Preference` WRITE;
/*!40000 ALTER TABLE `Preference` DISABLE KEYS */;
INSERT INTO `Preference` VALUES ('1INF1100cm','13',1,4),('1INF1100cm','3',1,5),('1INF1100tp','10',1,5),('1INF1100tp','102 929 F',1,1),('1INF1100tp','13',1,4),('1INF1100tp','241865 R',1,2),('1INF1100tp','271381 U',1,3),('1INF1100tp','3',1,5),('1INF1101cm','102 929 F',1,2),('1INF1101cm','13',1,5),('1INF1101cm','241865 R',1,5),('1INF1101cm','271381 U',1,3),('1INF1101cm','45763 D',1,1),('1INF1101td','10',1,2),('1INF1101td','102 929 F',1,2),('1INF1101td','13',1,5),('1INF1101td','241865 R',1,5),('1INF1101td','257259 J',1,5),('1INF1101td','271381 U',1,3),('1INF1101td','3',1,3),('1INF1101td','8',1,5),('1INF1102cm','102 929 F',1,2),('1INF1102cm','13',1,5),('1INF1102cm','8',1,5),('1INF1102tp','10',1,5),('1INF1102tp','102 929 F',1,2),('1INF1102tp','13',1,5),('1INF1102tp','241865 R',1,4),('1INF1102tp','257270 G',1,5),('1INF1102tp','3',1,3),('1INF1102tp','8',1,5),('1INF1103cm','50',1,3),('1INF1103cm','63',1,3),('1INF1103td','20',1,5),('1INF1103td','241865 R',1,2),('1INF1103td','50',1,3),('1INF1104cm','59',1,3),('1INF1104cm','62',1,3),('1INF1104cm','64',1,3),('1INF1104td','20',1,5),('1INF1104td','59',1,3),('1INF1104td','62',1,3),('1INF1104td','64',1,3),('1INF1105cm','20',1,5),('1INF1105cm','59',1,3),('1INF1105cm','60',1,5),('1INF1105cm','62',1,5),('1INF1105cm','63',1,3),('1INF1105cm','64',1,3),('1INF1105td','20',1,5),('1INF1105td','59',1,3),('1INF1105td','60',1,5),('1INF1105td','62',1,5),('1INF1105td','64',1,3),('1INF1106cm','22',1,5),('1INF1106td','22',1,5),('1INF1106tp','22',1,3),('1INF1107cm','31',1,3),('1INF1107cm','61',1,5),('1INF1107td','31',1,3),('1INF1108cm','27',1,3),('1INF1108td','27',1,3),('2INF1100cm','13',1,5),('2INF1100cm','241865 R',1,2),('2INF1100cm','3',1,5),('2INF1100cm','8',1,4),('2INF1100td','10',1,5),('2INF1100td','13',1,5),('2INF1100td','271381 U',1,3),('2INF1100td','3',1,5),('2INF1100td','8',1,4),('2INF1106cm','2',1,5),('2INF1106td','2',1,5),('2INF1108cm','28',1,3),('2INF1108cm','50',1,3),('2INF1108td','28',1,3),('2INF1108td','50',1,3);
/*!40000 ALTER TABLE `Preference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prerequis`
--

DROP TABLE IF EXISTS `Prerequis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prerequis` (
  `CodeCoursfk` varchar(50) NOT NULL,
  `CodePrerequis` varchar(50) NOT NULL,
  PRIMARY KEY (`CodeCoursfk`,`CodePrerequis`),
  KEY `CodePrerequis` (`CodePrerequis`),
  CONSTRAINT `Prerequis_ibfk_1` FOREIGN KEY (`CodeCoursfk`) REFERENCES `Cours` (`CodeCours`),
  CONSTRAINT `Prerequis_ibfk_2` FOREIGN KEY (`CodePrerequis`) REFERENCES `Cours` (`CodeCours`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prerequis`
--

LOCK TABLES `Prerequis` WRITE;
/*!40000 ALTER TABLE `Prerequis` DISABLE KEYS */;
/*!40000 ALTER TABLE `Prerequis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ScoreCompetence`
--

DROP TABLE IF EXISTS `ScoreCompetence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ScoreCompetence` (
  `CodeCompetencefk` varchar(50) NOT NULL,
  `CodeCoursfk` varchar(50) NOT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`CodeCompetencefk`,`CodeCoursfk`),
  KEY `CodeCoursfk` (`CodeCoursfk`),
  CONSTRAINT `ScoreCompetence_ibfk_1` FOREIGN KEY (`CodeCompetencefk`) REFERENCES `Competence` (`CodeCompetence`),
  CONSTRAINT `ScoreCompetence_ibfk_2` FOREIGN KEY (`CodeCoursfk`) REFERENCES `Cours` (`CodeCours`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ScoreCompetence`
--

LOCK TABLES `ScoreCompetence` WRITE;
/*!40000 ALTER TABLE `ScoreCompetence` DISABLE KEYS */;
INSERT INTO `ScoreCompetence` VALUES ('D1INF1100cm','1INF1100cm',100),('D1INF1100tp','1INF1100tp',100),('D1INF1101cm','1INF1101cm',100),('D1INF1101td','1INF1101td',100),('D1INF1102cm','1INF1102cm',100),('D1INF1102tp','1INF1102tp',100),('D1INF1103cm','1INF1103cm',100),('D1INF1103td','1INF1103td',100),('D1INF1104cm','1INF1104cm',100),('D1INF1104td','1INF1104td',100),('D1INF1105cm','1INF1105cm',100),('D1INF1105td','1INF1105td',100),('D1INF1106cm','1INF1106cm',100),('D1INF1106td','1INF1106td',100),('D1INF1106tp','1INF1106tp',100),('D1INF1107cm','1INF1107cm',100),('D1INF1107td','1INF1107td',100),('D1INF1108cm','1INF1108cm',100),('D1INF1108td','1INF1108td',100),('D2INF1100cm','2INF1100cm',100),('D2INF1100td','2INF1100td',100),('D2INF1106cm','2INF1106cm',100),('D2INF1106td','2INF1106td',100),('D2INF1108cm','2INF1108cm',100),('D2INF1108td','2INF1108td',100),('N1INF1100cm','1INF1100cm',30),('N1INF1100tp','1INF1100tp',30),('N1INF1101cm','1INF1101cm',30),('N1INF1101td','1INF1101td',30),('N1INF1102cm','1INF1102cm',30),('N1INF1102tp','1INF1102tp',30),('N1INF1103cm','1INF1103cm',30),('N1INF1103td','1INF1103td',30),('N1INF1104cm','1INF1104cm',30),('N1INF1104td','1INF1104td',30),('N1INF1105cm','1INF1105cm',30),('N1INF1105td','1INF1105td',30),('N1INF1106cm','1INF1106cm',30),('N1INF1106td','1INF1106td',30),('N1INF1106tp','1INF1106tp',30),('N1INF1107cm','1INF1107cm',30),('N1INF1107td','1INF1107td',30),('N1INF1108cm','1INF1108cm',30),('N1INF1108td','1INF1108td',30),('N2INF1100cm','2INF1100cm',30),('N2INF1100td','2INF1100td',30),('N2INF1106cm','2INF1106cm',30),('N2INF1106td','2INF1106td',30),('N2INF1108cm','2INF1108cm',30),('N2INF1108td','2INF1108td',30);
/*!40000 ALTER TABLE `ScoreCompetence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Semestre`
--

DROP TABLE IF EXISTS `Semestre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Semestre` (
  `CodeSemestre` varchar(50) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `CodeClassefk` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodeSemestre`),
  KEY `CodeClassefk` (`CodeClassefk`),
  CONSTRAINT `Semestre_ibfk_1` FOREIGN KEY (`CodeClassefk`) REFERENCES `Classe` (`CodeClasse`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Semestre`
--

LOCK TABLES `Semestre` WRITE;
/*!40000 ALTER TABLE `Semestre` DISABLE KEYS */;
INSERT INTO `Semestre` VALUES ('S1','Premier semestre','ESI1'),('S2','Deuxieme semestre','ESI1'),('S3','Troisieme semestre','ESI2'),('S4','Quatrieme semestre','ESI2'),('S5RS','Semestre RS','ESI3'),('S5SI','Semestre SI','ESI3');
/*!40000 ALTER TABLE `Semestre` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-03 18:45:48
