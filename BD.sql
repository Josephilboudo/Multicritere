-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: AffectationCours
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
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodeCompetence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Competence`
--

LOCK TABLES `Competence` WRITE;
/*!40000 ALTER TABLE `Competence` DISABLE KEYS */;
INSERT INTO `Competence` VALUES ('c1','math'),('c2','pc'),('c3','info'),('c4','francais'),('c5','philo'),('c6','eps'),('c7','svt'),('c8','hg');
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
INSERT INTO `CompetencePossede` VALUES ('c1','e1'),('c2','e1'),('c3','e1'),('c4','e1'),('c5','e1'),('c1','e2'),('c2','e2'),('c6','e2');
/*!40000 ALTER TABLE `CompetencePossede` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CompetenceRequise`
--

DROP TABLE IF EXISTS `CompetenceRequise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CompetenceRequise` (
  `CodeCompetencefk` varchar(50) NOT NULL,
  `CodeCoursfk` varchar(50) NOT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`CodeCompetencefk`,`CodeCoursfk`),
  KEY `CodeCoursfk` (`CodeCoursfk`),
  CONSTRAINT `CompetenceRequise_ibfk_1` FOREIGN KEY (`CodeCompetencefk`) REFERENCES `Competence` (`CodeCompetence`),
  CONSTRAINT `CompetenceRequise_ibfk_2` FOREIGN KEY (`CodeCoursfk`) REFERENCES `Cours` (`CodeCours`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CompetenceRequise`
--

LOCK TABLES `CompetenceRequise` WRITE;
/*!40000 ALTER TABLE `CompetenceRequise` DISABLE KEYS */;
/*!40000 ALTER TABLE `CompetenceRequise` ENABLE KEYS */;
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
INSERT INTO `Cours` VALUES ('1INF1100cm','Utilisation des systèmes d\'exploitation les plus courants',10,NULL,'NonAffecte','S1'),('1INF1100tp','Utilisation des systèmes d\'exploitation les plus courants tp',20,NULL,'NonAffecte','S1'),('1INF1101cm','Algorithmique et structures de données statiques cm',30,NULL,'NonAffecte','S1'),('1INF1101td','Algorithmique et structures de données statiques td',30,NULL,'NonAffecte','S1'),('1INF1102cm','Programmation cm',15,NULL,'NonAffecte','S1'),('1INF1102tp','Programmation tp',45,NULL,'NonAffecte','S1'),('1INF1103cm','Logique et raisonnement cm',15,NULL,'NonAffecte','S1'),('1INF1103td','Logique et raisonnement td',15,NULL,'NonAffecte','S1'),('1INF1104cm','Analyse 1 cm',23,NULL,'NonAffecte','S1'),('1INF1104td','Analyse 1 td',22,NULL,'NonAffecte','S1'),('1INF1105cm','Statistiques descriptives cm',15,NULL,'NonAffecte','S1'),('1INF1105td','Statistiques descriptives td',15,NULL,'NonAffecte','S1'),('1INF1106cm','Électrocinétique cm',23,NULL,'NonAffecte','S1'),('1INF1106td','Électrocinétique td',15,NULL,'NonAffecte','S1'),('1INF1106tp','Électrocinétique tp',7,NULL,'NonAffecte','S1'),('1INF1107cm','Comptabilité Générale cm',25,NULL,'NonAffecte','S1'),('1INF1107td','Comptabilité Générale td',20,NULL,'NonAffecte','S1'),('1INF1108cm','Anglais 1 cm',15,NULL,'NonAffecte','S1'),('1INF1108td','Anglais 1 td',15,NULL,'NonAffecte','S1'),('1INF1600cm','Algorithmique et structures de données dynamiques cm',25,NULL,'NonAffecte','S2'),('1INF1600td','Algorithmique et structures de données dynamiques td',15,NULL,'NonAffecte','S2'),('1INF1600tp','Algorithmique et structures de données dynamiques tp',20,NULL,'NonAffecte','S2'),('1INF1601cm','Électronique numérique cm',23,NULL,'NonAffecte','S2'),('1INF1601td','Électronique numérique td',15,NULL,'NonAffecte','S2'),('1INF1601tp','Électronique numérique tp',7,NULL,'NonAffecte','S2'),('1INF1602cm','Architecture et fonctionnement des ordinateurs cm',25,NULL,'NonAffecte','S2'),('1INF1602td','Architecture et fonctionnement des ordinateurs td',15,NULL,'NonAffecte','S2'),('1INF1602tp','Architecture et fonctionnement des ordinateurs tp',20,NULL,'NonAffecte','S2'),('1INF1603cm','Algèbre générale cm',23,NULL,'NonAffecte','S2'),('1INF1603td','Algèbre générale td',22,NULL,'NonAffecte','S2'),('1INF1604cm','Analyse 2 cm',23,NULL,'NonAffecte','S2'),('1INF1604td','Analyse 2 td',22,NULL,'NonAffecte','S2'),('1INF1605cm','Électronique analogique cm',15,NULL,'NonAffecte','S2'),('1INF1605td','Électronique analogique td',7.5,NULL,'NonAffecte','S2'),('1INF1606cm','Économie générale cm',15,NULL,'NonAffecte','S2'),('1INF1607cm','Anglais 2 cm',13,NULL,'NonAffecte','S2'),('1INF1607td','Anglais 2 td',17,NULL,'NonAffecte','S2'),('1INF2100cm','Algorithmiques, structures de données et complexite cm',30,NULL,'NonAffecte','S3'),('1INF2100td','Algorithmiques, structures de données et complexite td',15,NULL,'NonAffecte','S3'),('1INF2100tp','Algorithmiques, structures de données et complexite tp',15,NULL,'NonAffecte','S3'),('1INF2101cm','Programmation orientée objet cm',25,NULL,'NonAffecte','S3'),('1INF2101tp','Programmation orientée objet tp',20,NULL,'NonAffecte','S3'),('1INF2102cm','Utilisation des systèmes d\'exploitation Unix/Linux cm',10,NULL,'NonAffecte','S3'),('1INF2102tp','Utilisation des systèmes d\'exploitation Unix/Linux tp',20,NULL,'NonAffecte','S3'),('1INF2104cm','Probabilités cm',22,NULL,'NonAffecte','S3'),('1INF2104td','Probabilités td',23,NULL,'NonAffecte','S3'),('1INF2105cm','Probabilités cm',15,NULL,'NonAffecte','S3'),('1INF2105td','Probabilités td',15,NULL,'NonAffecte','S3'),('1INF2106cm','Électrotechnique cm',10,NULL,'NonAffecte','S3'),('1INF2106td','Électrotechnique td',12.5,NULL,'NonAffecte','S3'),('1INF2107cm','Droit (travail, sociétés, TIC) cm',15,NULL,'NonAffecte','S3'),('1INF2107td','Droit (travail, sociétés, TIC) td',15,NULL,'NonAffecte','S3'),('1INF2108cm','Anglais 3 cm',13,NULL,'NonAffecte','S3'),('1INF2108td','Anglais 3 td',17,NULL,'NonAffecte','S3'),('1INF2109cm','Comptabilité analytique cm',20,NULL,'NonAffecte','S3'),('1INF2109td','Comptabilité analytique td',25,NULL,'NonAffecte','S3'),('1INF2600cm','Architectures clients / serveurs cm',10,NULL,'NonAffecte','S4'),('1INF2600tp','Architectures clients / serveurs tp',20,NULL,'NonAffecte','S4'),('1INF26012cm','Sécurité informatique cm',15,NULL,'NonAffecte','S4'),('1INF26012td','Sécurité informatique td',10,NULL,'NonAffecte','S4'),('1INF26012tp','Sécurité informatique tp',20,NULL,'NonAffecte','S4'),('1INF26013cm','Modèle relationnel et bases de données cm',30,NULL,'NonAffecte','S4'),('1INF26013td','Modèle relationnel et bases de données td',15,NULL,'NonAffecte','S4'),('1INF26013tp','Modèle relationnel et bases de données tp',15,NULL,'NonAffecte','S4'),('1INF26014cm','Architectures et technologies des réseaux cm',30,NULL,'NonAffecte','S4'),('1INF26014tp','Architectures et technologies des réseaux tp',15,NULL,'NonAffecte','S4'),('1INF26015cm','Modèles OSI et TCP/IP cm',23,NULL,'NonAffecte','S4'),('1INF26015td','Modèles OSI et TCP/IP td',7,NULL,'NonAffecte','S4'),('1INF26015tp','Modèles OSI et TCP/IP tp',15,NULL,'NonAffecte','S4'),('1INF26016cm','Analyse numérique matricielle cm',23,NULL,'NonAffecte','S4'),('1INF26016td','Analyse numérique matricielle td',11,NULL,'NonAffecte','S4'),('1INF26016tp','Analyse numérique matricielle tp',11,NULL,'NonAffecte','S4'),('1INF26017cm','Connaissance de l\'entreprise cm',15,NULL,'NonAffecte','S4'),('1INF26017td','Connaissance de l\'entreprise td',15,NULL,'NonAffecte','S4'),('1INF26018tp','Projet tutoré tp',15,NULL,'NonAffecte','S4'),('1INF2601cm','Statistique inférentielle cm',15,NULL,'NonAffecte','S4'),('1INF2601td','Statistique inférentielle td',8,NULL,'NonAffecte','S4'),('1INF2601tp','Statistique inférentielle tp',7,NULL,'NonAffecte','S4'),('1INF3110cm','Administration réseaux cm',10,NULL,'NonAffecte','S5SI'),('1INF3110tp','Administration réseaux tp',20,NULL,'NonAffecte','S5SI'),('1INF3111cm','Création d\'entreprise cm',15,NULL,'NonAffecte','S5SI'),('1INF3111td','Création d\'entreprise td',15,NULL,'NonAffecte','S5SI'),('1INF3112cm','Anglais 4 cm',13,NULL,'NonAffecte','S5SI'),('1INF3112td','Anglais 4 td',17,NULL,'NonAffecte','S5SI'),('1INF3113cm','Optimisation cm',15,NULL,'NonAffecte','S5SI'),('1INF3113tp','Optimisation tp',15,NULL,'NonAffecte','S5SI'),('1INF3114cm','Conduite de projets informatiques cm',15,NULL,'NonAffecte','S5SI'),('1INF3114td','Conduite de projets informatiques td',10,NULL,'NonAffecte','S5SI'),('1INF3114tp','Conduite de projets informatiques tp',5,NULL,'NonAffecte','S5SI'),('1INF3115cm','Conception des systèmes d\'information cm',20,NULL,'NonAffecte','S5SI'),('1INF3115td','Conception des systèmes d\'information td',20,NULL,'NonAffecte','S5SI'),('1INF3115tp','Conception des systèmes d\'information tp',5,NULL,'NonAffecte','S5SI'),('1INF3116cm','Administration des bases de données cm',20,NULL,'NonAffecte','S5SI'),('1INF3116tp','Administration des bases de données tp',25,NULL,'NonAffecte','S5SI'),('1INF3117cm','Techniques de compilation cm',20,NULL,'NonAffecte','S5SI'),('1INF3117tp','Techniques de compilation tp',10,NULL,'NonAffecte','S5SI'),('1INF3118cm','Programmation orientée objet avancée cm',15,NULL,'NonAffecte','S5SI'),('1INF3118tp','Programmation orientée objet avancée tp',15,NULL,'NonAffecte','S5SI'),('1INF3120cm','Administration réseaux avancé cm',25,NULL,'NonAffecte','S5RS'),('1INF3120tp','Administration réseaux avancé tp',35,NULL,'NonAffecte','S5RS'),('1INF3121cm','Conception de réseaux locaux cm',15,NULL,'NonAffecte','S5RS'),('1INF3121td','Conception de réseaux locaux tp',15,NULL,'NonAffecte','S5RS'),('1INF3122cm','Création d\'entreprise cm',15,NULL,'NonAffecte','S5RS'),('1INF3122tp','Création d\'entreprise tp',15,NULL,'NonAffecte','S5RS'),('1INF3123cm','Anglais 4 cm',13,NULL,'NonAffecte','S5RS'),('1INF3123td','Anglais 4 td',17,NULL,'NonAffecte','S5RS'),('1INF3124cm','Traitement du signal cm',15,NULL,'NonAffecte','S5RS'),('1INF3124td','Traitement du signal td',10,NULL,'NonAffecte','S5RS'),('1INF3124tp','Traitement du signal tp',5,NULL,'NonAffecte','S5RS'),('1INF3125cm','Diagnostic et maintenance materiel cm',15,NULL,'NonAffecte','S5RS'),('1INF3125tp','Diagnostic et maintenance materiel tp',30,NULL,'NonAffecte','S5RS'),('1INF3126cm','Informatique Industrielle (automates programmable et graphcets cm',15,NULL,'NonAffecte','S5RS'),('1INF3126tp','Informatique Industrielle (automates programmable et graphcets tp',30,NULL,'NonAffecte','S5RS'),('1INF3127cm','Technologies émergentes cm',15,NULL,'NonAffecte','S5RS'),('1INF3127tp','Technologies émergentes tp',15,NULL,'NonAffecte','S5RS'),('1INF3128cm','Programmation Système cm',15,NULL,'NonAffecte','S5RS'),('1INF3128tp','Programmation Système tp',30,NULL,'NonAffecte','S5RS'),('1INF3129cm','Déploiement de réseaux locaux et metropolitains cm',15,NULL,'NonAffecte','S5RS'),('1INF3129tp','Déploiement de réseaux locaux et metropolitains tp',15,NULL,'NonAffecte','S5RS'),('2INF1100cm','Bureautique td',10,NULL,'NonAffecte','S1'),('2INF1100td','Bureautique cm',20,NULL,'NonAffecte','S1'),('2INF1106cm','Électrostatique cm',8,NULL,'NonAffecte','S1'),('2INF1106td','Électrostatique td',7,NULL,'NonAffecte','S1'),('2INF1108cm','Techniques d\'expression 1 cm',13,NULL,'NonAffecte','S1'),('2INF1108td','Techniques d\'expression 1 td',17,NULL,'NonAffecte','S1'),('2INF1600cm','Introduction à la programmation web cm',15,NULL,'NonAffecte','S2'),('2INF1600tp','Introduction à la programmation web tp',15,NULL,'NonAffecte','S2'),('2INF1603cm','Algèbre linéaire 1 cm',23,NULL,'NonAffecte','S2'),('2INF1603td','Algèbre linéaire 1 td',22,NULL,'NonAffecte','S2'),('2INF1605cm','Électromagnétisme cm',15,NULL,'NonAffecte','S2'),('2INF1605td','Électromagnétisme td',7.5,NULL,'NonAffecte','S2'),('2INF1607cm','Techniques d\'expression 2 cm',13,NULL,'NonAffecte','S2'),('2INF1607td','Techniques d\'expression 2 td',17,NULL,'NonAffecte','S2'),('2INF2102cm','Conception des systèmes d\'exploitation cm',30,NULL,'NonAffecte','S3'),('2INF2102td','Conception des systèmes d\'exploitation td',30,NULL,'NonAffecte','S3'),('2INF2103cm','Algèbre linéaire 2 cm',15,NULL,'NonAffecte','S3'),('2INF2103td','Algèbre linéaire 2 td',15,NULL,'NonAffecte','S3'),('2INF2106cm','Électronique de puissance cm',10,NULL,'NonAffecte','S3'),('2INF2106td','Électronique de puissance td',12.5,NULL,'NonAffecte','S3'),('2INF2600cm','Administration des systèmes d\'exploitation cm',15,NULL,'NonAffecte','S4'),('2INF2600tp','Administration des systèmes d\'exploitation tp',15,NULL,'NonAffecte','S4'),('2INF26015tp','Routage IP tp',15,NULL,'NonAffecte','S4'),('2INF26017cm','Communication en entreprise cm',15,NULL,'NonAffecte','S4'),('2INF26017td','Communication en entreprise td',15,NULL,'NonAffecte','S4'),('2INF3114','Projet tutoré',15,NULL,'NonAffecte','S5SI'),('2INF3115cm','Analyse et conception orientée objets cm',20,NULL,'NonAffecte','S5SI'),('2INF3115td','Analyse et conception orientée objets td',20,NULL,'NonAffecte','S5SI'),('2INF3115tp','Analyse et conception orientée objets tp',5,NULL,'NonAffecte','S5SI'),('2INF3118cm','Programmation Web avancée cm',15,NULL,'NonAffecte','S5SI'),('2INF3118tp','Programmation Web avancée tp',15,NULL,'NonAffecte','S5SI'),('2INF3120cm','Administration réseaux cm',10,NULL,'NonAffecte','S5RS'),('2INF3120td','Administration réseaux tp',20,NULL,'NonAffecte','S5RS'),('2INF3129cm','Infrastructures des réseaux mobiles cm',15,NULL,'NonAffecte','S5RS'),('2INF3129td','Infrastructures des réseaux mobiles td',15,NULL,'NonAffecte','S5RS'),('3INF26017cm','Analyse financière cm',15,NULL,'NonAffecte','S4'),('3INF26017td','Analyse financière td',15,NULL,'NonAffecte','S4'),('3INF3114cm','IHM cm',15,NULL,'NonAffecte','S5SI'),('3INF3114tp','IHM tp',15,NULL,'NonAffecte','S5SI'),('3INF3118cm','Développement mobile cm',15,NULL,'NonAffecte','S5SI'),('3INF3118tp','Développement mobile tp',15,NULL,'NonAffecte','S5SI'),('3INF3129','Projet tutoré',15,NULL,'NonAffecte','S5RS');
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
  `Disponibilite` date DEFAULT NULL,
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
INSERT INTO `Enseignant` VALUES ('e1','joeseph','joseph.com','1','2025-03-11'),('e2','artur','artue.com','2','2025-03-11'),('e3','alin','alin.com','3','2025-03-11'),('e4','franc','franc.com','3','2025-03-11');
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
INSERT INTO `Grade` VALUES ('1','Pr',12,5),('2','dr',24,2),('3','As',36,1),('5','1',1,1);
/*!40000 ALTER TABLE `Grade` ENABLE KEYS */;
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

-- Dump completed on 2025-03-29  1:22:11
