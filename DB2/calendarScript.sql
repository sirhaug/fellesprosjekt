CREATE database calendardb;

CREATE TABLE people(
  id int NOT NULL AUTO_INCREMENT,
  first_name varchar(256) NOT NULL,
  last_name varchar(256) NOT NULL,
  username varchar(20) NOT NULL,
  hash varchar(256) NOT NULL,
  PRIMARY KEY(id),
  UNIQUE(username)
);

CREATE TABLE events(
  id int NOT NULL AUTO_INCREMENT,
  description varchar(50) NOT NULL,
  start_time datetime NOT NULL, 
  end_time datetime NOT NULL,
  place varchar(20) DEFAULT NULL,
  owner int NOT NULL, 
  PRIMARY KEY(id),
  FOREIGN KEY(owner)
    REFERENCES people(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE groups(
  id int NOT NULL AUTO_INCREMENT,
  name varchar(256) NOT NULL,
  event_id NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(event_id)
    REFERENCES events(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE group_people(
  id int NOT NULL AUTO_INCREMENT,
  group_id NOT NULL,
  person_id NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(group_id)
    REFERENCES groups(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY(person_id)
    REFERENCES people(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE rooms(
  id int NOT NULL AUTO_INCREMENT,
  name varchar(256) NOT NULL,
  capacity int NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE event_participants(
  id int NOT NULL AUTO_INCREMENT,
  invite_status int NOT NULL,
  person_id int NOT NULL,
  event_id int NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(person_id)
    REFERENCES people(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY(event_id)
    REFERENCES events(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE event_groups(
  id int NOT NULL AUTO_INCREMENT,
  group_id int NOT NULL,
  event_id int NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(event_id)
    REFERENCES events(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY(group_id)
    REFERENCES groups(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE event_rooms(
  id int NOT NULL AUTO_INCREMENT,
  room_id int NOT NULL,
  event_id int NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(event_id)
    REFERENCES events(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY(room_id)
    REFERENCES rooms(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE notifications(
  id int NOT NULL AUTO_INCREMENT,
  event_id int NOT NULL,
  person_id int NOT NULL,
  type varchar(256) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(event_id)
    REFERENCES events(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY(person_id)
    REFERENCES people(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE alarms(
  id int NOT NULL AUTO_INCREMENT,
  time datetime NOT NULL,
  event_id int NOT NULL,
  person_id int NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(event_id)
    REFERENCES events(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY(person_id)
    REFERENCES people(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);
