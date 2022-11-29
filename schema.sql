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

-- arc_item is a table that functions as a materialized view andd stores the result of joining the arc and item tables using the arc_featured_in table
-- this is done as MySQL doesn't support materialized view
-- the triggers below the table are used to dynamically update the table as needed
-- only situations that can actually arise from the system have associated triggers
-- identical "views" and triggers could be made for all the many-many relation in the system
-- but this serves as a demo of what it would look like
-- the items shown on the bottom of the arc page are retrieved from this view

create table arc_item as 
    select a.id as arc_id, i.id as item_id, a.name as arc_name, i.name as item_name, a.description as arc_description, i.description as item_description, i.rarity as item_rarity, i.category as item_category, author_id 
    from arc a inner join (item_featured_in ai inner join item i on ai.item_id=i.id) on ai.arc_id=a.id;

delimiter //

create trigger insert_arc_item_mv
after insert on item_featured_in
for each row
begin
	insert into arc_item (select a.id, i.id, a.name, i.name, a.description, i.description, i.rarity, i.category, author_id from arc a inner join (item_featured_in ai inner join item i on ai.item_id=i.id) on ai.arc_id=a.id where a.id=new.arc_id and i.id=new.item_id);
end; //

create trigger delete_arc_item_mv
after delete on item_featured_in
for each row
begin
	delete from arc_item where arc_id=old.arc_id and item_id=old.item_id;
end; //

create trigger arc_update
after update on arc
for each row
begin
	update arc_item set arc_name=new.name, arc_description=new.description where arc_id=new.id;
end; //

create trigger item_update
after update on item
for each row
begin
	update arc_item 
	set item_name=new.name, item_description=new.description, item_rarity=new.rarity, item_category=new.category
	where item_id=new.id;
end; //




