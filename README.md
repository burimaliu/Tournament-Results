###Tournament Results

###About:

This is a Python project using PostgreSQL database to fulfill a game tournament needs using Swiss pairing system.
It keeps track of players and matches in a game tournament.


###Requirements to run this application:

1. Python with psycopg2
2. PostgreeSQL

###How to run this application:

1. Clone this repository to your working directory
2. Create a PostgreeSQL database named "tournament" if other then update "db_name" on tournament.py file
3. Import SQL file "tournament.sql"
4. From your working directory run: python tournament_test.py

###Results:

When tournament_test.py is executed we should see results like this:

1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.

Success!  All tests pass!
