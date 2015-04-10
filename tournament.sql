-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Table representing players

CREATE TABLE players (id serial primary key,
                        name varchar (255) not null,
                        created_at timestamp default current_timestamp);


-- Table representing matches played
CREATE TABLE matches (id serial primary key,
                         winner int,
                         loser int,
                         foreign key (winner) references players(id),
                         foreign key (loser) references players(id));

