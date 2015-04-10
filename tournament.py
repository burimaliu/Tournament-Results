#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys

db_name = 'tournament'

def connect(database):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect('dbname=' + database)

def deleteMatches():
    """Remove all the match records from the database."""
    database = connect(db_name)
    cursor = database.cursor()
    cursor.execute(" DELETE FROM matches; ")
    database.commit()
    database.close()
    
    return database


def deletePlayers():
    """Remove all the player records from the database."""
    database = connect(db_name)
    cursor = database.cursor()
    cursor.execute(" DELETE FROM players; ")
    database.commit()
    database.close()

    return database


def countPlayers():
    """Returns the number of players currently registered."""
   
    database = connect(db_name)
    cursor = database.cursor()
    cursor.execute(" SELECT COUNT(id) from players; ")
    data = cursor.fetchall()
    database.close()

    assert len(data) == 1
    return int(data[0][0])



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    database = connect(db_name)
    cursor = database.cursor()
    query =  "INSERT INTO players (name) values (%s);"
    data = [name]
    cursor.execute(query,data)
    database.commit()
    database.close()

    return database
    


def playerStandings():
    """ Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    selector = """
    select players.id, name, count(matches.id) as {group}
        from players left join matches
            on players.id = {name}
        group by players.id
        order by {group} desc 
    """

    wins = selector.format(name='winner', group='wins')
    losses = selector.format(name='loser', group='losses')

    join = """
    select winners.id, winners.name, wins, wins+losses as matches
        from ({wins}) as winners left join ({losses}) as losers
            on winners.id = losers.id;
    """.format(wins=wins, losses=losses)

    database = connect(db_name)
    cursor = database.cursor()
    cursor.execute(join + ';')
    results = cursor.fetchall()

    database.close()
    return results


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = " INSERT INTO matches (winner,loser) VALUES (%s, %s); "
    data = [winner, loser]
    
    database = connect(db_name)
    cursor = database.cursor()
    cursor.execute(query,data)
    database.commit()
    database.close()
    return database
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = [(data[0], data[1]) for data in playerStandings()]
    if len(standings) < 2:
        raise KeyError("Looks like we dont have enough players, bring someone on board.")
    left = standings[0::2]
    right = standings[1::2]
    pairings = zip(left, right)

    # flatten the pairings and convert back to a tuple
    results = [tuple(list(sum(pairing, ()))) for pairing in pairings]

    return results
