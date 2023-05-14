SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema hw2
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `hw2` ;

-- -----------------------------------------------------
-- Schema hw2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hw2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `hw2` ;

-- -----------------------------------------------------
-- Table `hw2`.`administration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`administration` ;

CREATE TABLE IF NOT EXISTS `hw2`.`administration` (
  `administration_id` INT NOT NULL AUTO_INCREMENT,
  `administration_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`administration_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hw2`.`administrator`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`administrator` ;

CREATE TABLE IF NOT EXISTS `hw2`.`administrator` (
  `administrator_id` INT NOT NULL AUTO_INCREMENT,
  `administrator_title` VARCHAR(45) NULL,
  `administration_id` INT NOT NULL,
  `person_id` INT NOT NULL,
  PRIMARY KEY (`administrator_id`),
  CONSTRAINT `administration_id`
    FOREIGN KEY (`administration_id`)
    REFERENCES `hw2`.`administration`(`administration_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `person_id`
    FOREIGN KEY (`person_id`)
    REFERENCES `hw2`.`person`(`person_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hw2`.`assignment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`assignment` ;

CREATE TABLE IF NOT EXISTS `hw2`.`assignment` (
  `assignment_id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NULL,
  `description` VARCHAR(45) NULL,
  `deadline` DATE NOT NULL,
  `max_grade` FLOAT NOT NULL,
  `course_id` INT NULL,
  PRIMARY KEY (`assignment_id`),
  UNIQUE INDEX `assignment_id_UNIQUE` (`assignment_id` ASC) VISIBLE,
  INDEX `fk_course_id_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `hw2`.`course` (`course_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hw2`.`certification`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`certification` ;

CREATE TABLE IF NOT EXISTS `hw2`.`certification` (
  `certification_id` INT NOT NULL AUTO_INCREMENT,
  `certification_name` VARCHAR(60) NOT NULL,
  `instructor_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`certification_id`),
  INDEX `instructor_id` (`instructor_id` ASC) VISIBLE,
  CONSTRAINT `instructor_id_crf_fk`
    FOREIGN KEY (`instructor_id`)
    REFERENCES `hw2`.`instructor` (`instructor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;



-- -----------------------------------------------------
-- Table `hw2`.`course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`course` ;

CREATE TABLE IF NOT EXISTS `hw2`.`course` (
  `course_id` INT NOT NULL AUTO_INCREMENT,
  `course_name` VARCHAR(50) NOT NULL,
  `faculty_id` INT NULL DEFAULT NULL,
  `faculty_member_id` INT NULL DEFAULT NULL,
  `capacity` INT NOT NULL,
  PRIMARY KEY (`course_id`),
  INDEX `faculty_id` (`faculty_id` ASC) VISIBLE,
  INDEX `faculty_member_id` (`faculty_member_id` ASC) VISIBLE,
  CONSTRAINT `faculty_id_crs_fk`
    FOREIGN KEY (`faculty_id`)
    REFERENCES `hw2`.`faculty` (`faculty_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `faculty_member_id_crs_fk`
    FOREIGN KEY (`faculty_member_id`)
    REFERENCES `hw2`.`facultymember` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`curriculum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`curriculum` ;

CREATE TABLE IF NOT EXISTS `hw2`.`curriculum` (
  `curriculum_id` INT NOT NULL AUTO_INCREMENT,
  `credits` INT NULL,
  PRIMARY KEY (`curriculum_id`),
  UNIQUE INDEX `curriculum_id_UNIQUE` (`curriculum_id` ASC) VISIBLE
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hw2`.`curriculumcourse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`curriculumcourse` ;

CREATE TABLE IF NOT EXISTS `hw2`.`curriculumcourse` (
  `curriculum_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  PRIMARY KEY (`curriculum_id`, `course_id`),
  CONSTRAINT `curriculum_id`
    FOREIGN KEY (`curriculum_id`)
    REFERENCES `hw2`.`curriculum` (`curriculum_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `course_id`
    FOREIGN KEY (`curriculum_id`)
    REFERENCES `hw2`.`course` (`course_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hw2`.`department`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`department` ;

CREATE TABLE IF NOT EXISTS `hw2`.`department` (
  `department_id` INT NOT NULL AUTO_INCREMENT,
  `department_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`department_id`),
  UNIQUE INDEX `department_id` (`department_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`faculty`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`faculty` ;

CREATE TABLE IF NOT EXISTS `hw2`.`faculty` (
  `faculty_id` INT NOT NULL AUTO_INCREMENT,
  `department_id` INT NULL DEFAULT NULL,
  `faculty_name` VARCHAR(30) NOT NULL,
  `administration_id` INT NOT NULL,
  PRIMARY KEY (`faculty_id`),
  CONSTRAINT `department_id`
    FOREIGN KEY (`department_id`)
    REFERENCES `hw2`.`department` (`department_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_administration_id`
    FOREIGN KEY (`administration_id`)
    REFERENCES `hw2`.`administration` (`administration_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`facultymember`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`facultymember` ;

CREATE TABLE IF NOT EXISTS `hw2`.`facultymember` (
  `member_id` INT NOT NULL AUTO_INCREMENT,
  `faculty_id` INT NULL DEFAULT NULL,
  `person_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`member_id`),
  INDEX `person_id` (`person_id` ASC) VISIBLE,
  INDEX `faculty_id` (`faculty_id` ASC) VISIBLE,
  CONSTRAINT `faculty_fm_fk`
    FOREIGN KEY (`faculty_id`)
    REFERENCES `hw2`.`faculty` (`faculty_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `person_fm_fk`
    FOREIGN KEY (`person_id`)
    REFERENCES `hw2`.`person` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`instructor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`instructor` ;

CREATE TABLE IF NOT EXISTS `hw2`.`instructor` (
  `instructor_id` INT NOT NULL AUTO_INCREMENT,
  `inductry_experiance` FLOAT NOT NULL,
  `faculty_member_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`instructor_id`),
  INDEX `faculty_member_id` (`faculty_member_id` ASC) VISIBLE,
  CONSTRAINT `faculty_member_in_fk`
    FOREIGN KEY (`faculty_member_id`)
    REFERENCES `hw2`.`facultymember` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`lecturer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`lecturer` ;

CREATE TABLE IF NOT EXISTS `hw2`.`lecturer` (
  `lecturer_id` INT NOT NULL AUTO_INCREMENT,
  `specialization` VARCHAR(60) NOT NULL,
  `faculty_member_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`lecturer_id`),
  INDEX `faculty_member_id` (`faculty_member_id` ASC) VISIBLE,
  CONSTRAINT `faculty_member_lc_fk`
    FOREIGN KEY (`faculty_member_id`)
    REFERENCES `hw2`.`facultymember` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`person` ;

CREATE TABLE IF NOT EXISTS `hw2`.`person` (
  `person_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`person_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`professor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`professor` ;

CREATE TABLE IF NOT EXISTS `hw2`.`professor` (
  `professor_id` INT NOT NULL AUTO_INCREMENT,
  `academic_degree` VARCHAR(50) NOT NULL,
  `faculty_member_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`professor_id`),
  INDEX `faculty_member_id` (`faculty_member_id` ASC) VISIBLE,
  CONSTRAINT `faculty_member_pf_fk`
    FOREIGN KEY (`faculty_member_id`)
    REFERENCES `hw2`.`facultymember` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`program`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`program` ;

CREATE TABLE IF NOT EXISTS `hw2`.`program` (
  `program_code` VARCHAR(5) NOT NULL,
  `department_id` INT NULL DEFAULT NULL, 
  `faculty_id` INT NULL DEFAULT NULL,
  `program_name` VARCHAR(50) NOT NULL,
  `program_description` VARCHAR(200) NULL DEFAULT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `duration` FLOAT GENERATED ALWAYS AS (((year(`end_date`) - year(`start_date`)) + ((dayofyear(`end_date`) - dayofyear(`start_date`)) / 365.25))) VIRTUAL,
  `program_format` VARCHAR(30) NOT NULL,
  `curriculum_id` INT default 0,
  PRIMARY KEY (`program_code`),
  INDEX `faculty_id` (`faculty_id` ASC) VISIBLE,
  INDEX `curriculum_id_fk_idx` (`curriculum_id` ASC) VISIBLE,
  CONSTRAINT `faculty_id_fk`
    FOREIGN KEY (`faculty_id`)
    REFERENCES `hw2`.`faculty` (`faculty_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
CONSTRAINT `department_id_fk`
    FOREIGN KEY (`department_id`)
    REFERENCES `hw2`.`department` (`department_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `curriculum_id_fk`
    FOREIGN KEY (`curriculum_id`)
    REFERENCES `hw2`.`curriculum` (`curriculum_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`publication`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`publication` ;

CREATE TABLE IF NOT EXISTS `hw2`.`publication` (
  `publication_id` INT NOT NULL AUTO_INCREMENT,
  `publication_name` VARCHAR(100) NOT NULL,
  `publication_details` VARCHAR(100) NOT NULL,
  `professor_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`publication_id`),
  INDEX `professor_id` (`professor_id` ASC) VISIBLE,
  CONSTRAINT `professor_id_pb_fk`
    FOREIGN KEY (`professor_id`)
    REFERENCES `hw2`.`professor` (`professor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`registration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`registration` ;

CREATE TABLE IF NOT EXISTS `hw2`.`registration` (
  `course_id` INT NOT NULL,
  `faculty_member_id` INT NOT NULL,
  `student_id` INT NOT NULL,
  PRIMARY KEY (`course_id`, `faculty_member_id`, `student_id`),
  INDEX `course_id` (`course_id` ASC) VISIBLE,
  INDEX `faculty_member_id` (`faculty_member_id` ASC) VISIBLE,
  INDEX `student_id` (`student_id` ASC) VISIBLE,
  CONSTRAINT `course_id_rg_fk`
    FOREIGN KEY (`course_id`)
    REFERENCES `hw2`.`course` (`course_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `member_id_rg_fk`
    FOREIGN KEY (`faculty_member_id`)
    REFERENCES `hw2`.`facultymember` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `student_id_rg_fk`
    FOREIGN KEY (`student_id`)
    REFERENCES `hw2`.`student` (`student_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`student`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`student` ;

CREATE TABLE IF NOT EXISTS `hw2`.`student` (
  `student_id` INT NOT NULL AUTO_INCREMENT,
  `person_id` INT NULL DEFAULT NULL,
  `degree` VARCHAR(5) NULL DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  INDEX `person_id` (`person_id` ASC) VISIBLE,
  CONSTRAINT `person_id_st_fk`
    FOREIGN KEY (`person_id`)
    REFERENCES `hw2`.`person` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`studentprogram`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`studentprogram` ;

CREATE TABLE IF NOT EXISTS `hw2`.`studentprogram` (
  `program_code` VARCHAR(5) NOT NULL,
  `student_id` INT NOT NULL,
  `GPA` FLOAT NOT NULL,
  PRIMARY KEY (`student_id`, `program_code`),
  INDEX `student_id` (`student_id` ASC) VISIBLE,
  INDEX `program_code` (`program_code` ASC) VISIBLE,
  CONSTRAINT `fk_student_program_program`
    FOREIGN KEY (`program_code`)
    REFERENCES `hw2`.`program` (`program_code`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_student_program_student`
    FOREIGN KEY (`student_id`)
    REFERENCES `hw2`.`student` (`student_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hw2`.`submission`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hw2`.`submission` ;

CREATE TABLE IF NOT EXISTS `hw2`.`submission` (
  `submission_id` INT NOT NULL AUTO_INCREMENT,
  `submission_date` DATE NOT NULL,
  `submission_file` BLOB NOT NULL,
  `assignment_id` INT NOT NULL,
  `grade` FLOAT NULL,
  `student_id` INT  NOT NULL,
  PRIMARY KEY (`submission_id`),
  UNIQUE INDEX `submission_id_UNIQUE` (`submission_id` ASC) VISIBLE,
  INDEX `fk_assignment_id_idx` (`assignment_id` ASC) VISIBLE,
  CONSTRAINT `fk_assignment_id`
    FOREIGN KEY (`assignment_id`)
    REFERENCES `hw2`.`assignment` (`assignment_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  INDEX `fk_student_idx` (`student_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_idx`
    FOREIGN KEY (`student_id`)
    REFERENCES `hw2`.`student` (`student_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
