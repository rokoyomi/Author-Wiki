CREATE TABLE author (
    id int primary key auto_increment,
    first_name  varchar(30),
    last_name varchar(30),
    email varchar(50) unique not null,
    password_hash int not null default(0),
    pen_name varchar(30) not null
);
CREATE TABLE story (
    id int primary key auto_increment,
    author_id int not null,
    name varchar(50) not null,
    status varchar(20) not null default('not started'),
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE arc( 
    id int primary key auto_increment,
    story_id int not null,
    name varchar(50) not null,
    description text,
    FOREIGN KEY (story_id) REFERENCES story(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE race(
    id int primary key auto_increment,
    author_id int not null,
    name varchar(30) not null,
    category varchar(30) not null,
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE characters(
    id int primary key auto_increment,
    author_id int not null,
    name varchar(50) not null,
    race_id int,
    gender varchar(7) not null,
    status varchar(10) not null,
    height int not null,
    weight int not null,
    age int not null,
    alignment varchar(20) not null,
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (race_id) REFERENCES race(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE traits(
    character_id int not null,
    name varchar(20) not null,
    description text,
    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(character_id, name)
);
CREATE TABLE world(
    id int primary key auto_increment,
    author_id int not null,
    name varchar(20) not null,
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE location(
    id int primary key auto_increment,
    author_id int not null,
    world_id int not null,
    location_id int,
    category varchar(20) not null,
    name varchar(30) not null,
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE item(
    id int primary key auto_increment,
    author_id int not null,
    name varchar(20) not null,
    rarity varchar(20) not null,
    category varchar(20) not null,
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE organization(
    id int primary key auto_increment,
    author_id int not null,
    leader_id int not null,
    base_location_id int not null,
    name varchar(30) not null,
    description text,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE,FOREIGN KEY (leader_id) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (base_location_id) REFERENCES location(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE appearance(
    character_id int not null,
    arc_id int not null,
    role varchar(40),
    description text,
    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (arc_id) REFERENCES arc(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(character_id, arc_id)
);
CREATE TABLE item_featured_in (
    item_id int not null,
    arc_id int not null,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (arc_id) REFERENCES arc(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(item_id, arc_id)
);
CREATE TABLE arc_occurs_in (
    arc_id int not null,
    location_id int not null,
    FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (arc_id) REFERENCES arc(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(arc_id, location_id)
);
CREATE TABLE race_lives_in (
    race_id int not null,
    world_id int not null,
    FOREIGN KEY (race_id) REFERENCES race(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (world_id) REFERENCES world(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(race_id, world_id)
);
CREATE TABLE item_found_in_world (
    item_id int not null,
    world_id int not null,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (world_id) REFERENCES world(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(item_id, world_id)
);