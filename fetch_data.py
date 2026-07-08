#!/usr/bin/env python3
"""
Fetch a real, interconnected film <-> cast graph from Wikidata (SPARQL).
Falls back to an embedded curated dataset if the network/endpoint fails.
Writes data.json: { "films": {filmLabel: [actorLabels...]}, "actors": {actorLabel: [filmLabels...]} }
"""
import json
import urllib.request
import urllib.parse
import sys
import time

SPARQL = "https://query.wikidata.org/sparql"

# Curated list of well-known, cast-interconnected films.
# Many of these share actors deliberately (Tarantino, Scorsese, Nolan, Marvel, etc.)
FILM_TITLES = [
    "The Godfather", "The Godfather Part II", "The Godfather Part III",
    "Pulp Fiction", "Reservoir Dogs", "Jackie Brown", "Kill Bill: Vol. 1",
    "Kill Bill: Vol. 2", "Inglourious Basterds", "Django Unchained",
    "Once Upon a Time in Hollywood", "True Romance", "Natural Born Killers",
    "Heat", "Casino", "GoodFellas", "Raging Bull", "Taxi Driver",
    "The Departed", "The Wolf of Wall Street", "Cape Fear",
    "Mean Streets", "Hugo", "Shutter Island",
    "The Avengers", "Avengers: Endgame", "Iron Man", "Captain America: The First Avenger",
    "Thor", "The Avengers", "Black Panther", "Spider-Man: Homecoming",
    "Captain Marvel", "Ant-Man", "Guardians of the Galaxy",
    "Star Wars", "The Empire Strikes Back", "Return of the Jedi",
    "The Force Awakens", "The Last Jedi", "Rogue One",
    "The Dark Knight", "The Dark Knight Rises", "Batman Begins",
    "Inception", "Interstellar", "Tenet", "Dunkirk", "Memento",
    "Fight Club", "Se7en", "Gone Girl", "The Social Network",
    "Ocean's Eleven", "Ocean's Twelve", "Ocean's Thirteen",
    "The Truman Show", "Eternal Sunshine of the Spotless Mind",
    "Forrest Gump", "Cast Away", "Saving Private Ryan",
    "Catch Me If You Can", "The Terminal",
    "Toy Story", "Toy Story 3", "Up", "WALL-E", "Finding Nemo",
    "Knives Out", "Glass Onion", "No Time to Die",
    "Skyfall", "Spectre", "Casino Royale",
    "Mad Max: Fury Road", "The Matrix", "The Matrix Reloaded",
    "John Wick", "John Wick: Chapter 2", "The Fugitive",
    "A Few Good Men", "The Shawshank Redemption", "The Green Mile",
    "Misery", "Stand by Me",
    "Snatch", "Lock, Stock and Two Smoking Barrels", "Sherlock Holmes",
    "The Hobbit: An Unexpected Journey", "The Lord of the Rings: The Fellowship of the Ring",
    "The Lord of the Rings: The Return of the King",
    "Jurassic Park", "Jurassic World", "Indiana Jones and the Raiders of the Lost Ark",
    "E.T. the Extra-Terrestrial", "Jaws", "Close Encounters of the Third Kind",
    "Lincoln", "Bridge of Spies", "War Horse",
    "No Country for Old Men", "No Country for Old Men", "Fargo",
    "The Big Lebowski", "O Brother, Where Art Thou?", "True Grit",
    "A Serious Man", "Inside Llewyn Davis",
    "There Will Be Blood", "Phantom Thread", "Licorice Pizza",
    "Boogie Nights", "Magnolia", "Hard Eight",
    "The Silence of the Lambs", "The Rock", "Con Air",
    "The Usual Suspects", "L.A. Confidential",
    "Titanic", "Avatar", "Aliens", "Terminator 2: Judgment Day",
    "The Terminator", "True Lies", "Tropic Thunder",
    "Dodgeball: A True Underdog Story", "Anchorman: The Legend of Ron Burgundy",
    "Step Brothers", "Talladega Nights: The Ballad of Ricky Bobby",
    "The Hangover", "Due Date", "Silver Linings Playbook",
    "American Hustle", "American Sniper", "Sully",
]


def run_query(titles):
    # Build VALUES clause
    values = " ".join('"%s"' % t.replace('"', '\\"') for t in titles)
    query = """
    SELECT ?film ?filmLabel ?actor ?actorLabel WHERE {
      VALUES ?title { %s }
      ?film rdfs:label ?title.
      ?film rdfs:label ?filmLabel.
      FILTER(LANG(?filmLabel) = "en")
      ?film wdt:P31/wdt:P279* wd:Q11424.
      ?film wdt:P161 ?actor.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % values
    params = urllib.parse.urlencode({"query": query, "format": "json"})
    url = SPARQL + "?" + params
    req = urllib.request.Request(url, headers={
        "User-Agent": "ReelChainPrototype/0.1 (educational demo)",
        "Accept": "application/sparql-results+json"
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_from_sparql(data):
    films = {}
    actors = {}
    for row in data["results"]["bindings"]:
        fl = row["filmLabel"]["value"]
        al = row["actorLabel"]["value"]
        films.setdefault(fl, [])
        if al not in films[fl]:
            films[fl].append(al)
        actors.setdefault(al, [])
        if fl not in actors[al]:
            actors[al].append(fl)
    return films, actors


# ---- Embedded fallback (verified, real cast for a core set) ----
FALLBACK_FILMS = {
    "The Godfather": ["Marlon Brando", "Al Pacino", "James Caan", "Robert Duvall", "John Cazale", "Diane Keaton"],
    "Heat": ["Al Pacino", "Robert De Niro", "Val Kilmer", "Jon Voight", "Tom Sizemore"],
    "Jackie Brown": ["Pam Grier", "Samuel L. Jackson", "Robert De Niro", "Bridget Fonda", "Michael Keaton", "Chris Tucker"],
    "Pulp Fiction": ["John Travolta", "Samuel L. Jackson", "Uma Thurman", "Bruce Willis", "Tim Roth", "Harvey Keitel"],
    "Reservoir Dogs": ["Harvey Keitel", "Tim Roth", "Michael Madsen", "Chris Penn", "Steve Buscemi", "Lawrence Tierney"],
    "Kill Bill: Vol. 1": ["Uma Thurman", "Lucy Liu", "David Carradine", "Daryl Hannah", "Vivica A. Fox"],
    "Kill Bill: Vol. 2": ["Uma Thurman", "David Carradine", "Michael Madsen", "Daryl Hannah", "Samuel L. Jackson"],
    "Inglourious Basterds": ["Brad Pitt", "Diane Kruger", "Christoph Waltz", "Eli Roth", "Michael Fassbender"],
    "Django Unchained": ["Jamie Foxx", "Christoph Waltz", "Leonardo DiCaprio", "Samuel L. Jackson", "Kerry Washington"],
    "Once Upon a Time in Hollywood": ["Leonardo DiCaprio", "Brad Pitt", "Margot Robbie", "Al Pacino", "Damian Lewis", "Emile Hirsch", "Margaret Qualley", "Tim Roth", "Kurt Russell"],
    "GoodFellas": ["Robert De Niro", "Ray Liotta", "Joe Pesci", "Lorraine Bracco", "Paul Sorvino"],
    "Casino": ["Robert De Niro", "Sharon Stone", "Joe Pesci", "James Woods"],
    "The Departed": ["Leonardo DiCaprio", "Matt Damon", "Jack Nicholson", "Mark Wahlberg", "Martin Sheen", "Alec Baldwin"],
    "The Wolf of Wall Street": ["Leonardo DiCaprio", "Jonah Hill", "Margot Robbie", "Matthew McConaughey", "Kyle Chandler"],
    "Taxi Driver": ["Robert De Niro", "Jodie Foster", "Cybill Shepherd", "Harvey Keitel"],
    "Raging Bull": ["Robert De Niro", "Cathy Moriarty", "Joe Pesci"],
    "The Avengers": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson", "Mark Ruffalo", "Chris Hemsworth", "Jeremy Renner", "Samuel L. Jackson"],
    "Avengers: Endgame": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson", "Mark Ruffalo", "Chris Hemsworth", "Jeremy Renner", "Samuel L. Jackson", "Brie Larson", "Paul Rudd"],
    "Iron Man": ["Robert Downey Jr.", "Gwyneth Paltrow", "Terrence Howard", "Jeff Bridges", "Samuel L. Jackson"],
    "Black Panther": ["Chadwick Boseman", "Michael B. Jordan", "Lupita Nyong'o", "Letitia Wright", "Martin Freeman", "Andy Serkis"],
    "Captain America: The First Avenger": ["Chris Evans", "Hayley Atwell", "Sebastian Stan", "Hugo Weaving", "Samuel L. Jackson"],
    "Thor": ["Chris Hemsworth", "Natalie Portman", "Tom Hiddleston", "Anthony Hopkins", "Stellan Skarsgard"],
    "Guardians of the Galaxy": ["Chris Pratt", "Zoe Saldana", "Dave Bautista", "Bradley Cooper", "Vin Diesel", "Karen Gillan"],
    "Star Wars": ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Peter Cushing", "Alec Guinness"],
    "The Empire Strikes Back": ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Billy Dee Williams"],
    "Return of the Jedi": ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Billy Dee Williams", "Ian McDiarmid"],
    "The Force Awakens": ["Harrison Ford", "Mark Hamill", "Carrie Fisher", "Daisy Ridley", "John Boyega", "Adam Driver"],
    "The Dark Knight": ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine", "Gary Oldman", "Morgan Freeman"],
    "The Dark Knight Rises": ["Christian Bale", "Tom Hardy", "Anne Hathaway", "Michael Caine", "Gary Oldman", "Morgan Freeman"],
    "Batman Begins": ["Christian Bale", "Michael Caine", "Liam Neeson", "Katie Holmes", "Gary Oldman", "Morgan Freeman"],
    "Inception": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page", "Tom Hardy", "Ken Watanabe", "Cillian Murphy", "Michael Caine"],
    "Interstellar": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain", "Michael Caine", "Matt Damon"],
    "Fight Club": ["Brad Pitt", "Edward Norton", "Helena Bonham Carter", "Meat Loaf"],
    "Se7en": ["Brad Pitt", "Morgan Freeman", "Kevin Spacey", "Gwyneth Paltrow"],
    "The Social Network": ["Jesse Eisenberg", "Andrew Garfield", "Justin Timberlake", "Armie Hammer"],
    "Ocean's Eleven": ["George Clooney", "Brad Pitt", "Matt Damon", "Julia Roberts", "Andy Garcia", "Casey Affleck", "Don Cheadle"],
    "Ocean's Twelve": ["George Clooney", "Brad Pitt", "Matt Damon", "Julia Roberts", "Catherine Zeta-Jones", "Andy Garcia"],
    "Ocean's Thirteen": ["George Clooney", "Brad Pitt", "Matt Damon", "Al Pacino", "Andy Garcia", "Don Cheadle", "Elliott Gould"],
    "Forrest Gump": ["Tom Hanks", "Robin Wright", "Gary Sinise", "Sally Field"],
    "Saving Private Ryan": ["Tom Hanks", "Matt Damon", "Tom Sizemore", "Edward Burns", "Barry Pepper"],
    "Catch Me If You Can": ["Leonardo DiCaprio", "Tom Hanks", "Christopher Walken", "Amy Adams"],
    "Toy Story": ["Tom Hanks", "Tim Allen", "Don Rickles", "Jim Varney"],
    "Toy Story 3": ["Tom Hanks", "Tim Allen", "Michael Keaton", "Ned Beatty"],
    "Up": ["Ed Asner", "Christopher Plummer", "Jordan Nagai"],
    "Knives Out": ["Daniel Craig", "Chris Evans", "Ana de Armas", "Jamie Lee Curtis", "Michael Shannon", "Christopher Plummer"],
    "Glass Onion": ["Daniel Craig", "Edward Norton", "Janelle Monae", "Kathryn Hahn", "Dave Bautista", "Kate Hudson"],
    "Skyfall": ["Daniel Craig", "Javier Bardem", "Naomie Harris", "Ralph Fiennes", "Judi Dench"],
    "Casino Royale": ["Daniel Craig", "Eva Green", "Mads Mikkelsen", "Judi Dench"],
    "Mad Max: Fury Road": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult", "Hugh Keays-Byrne"],
    "The Matrix": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss", "Hugo Weaving", "Joe Pantoliano"],
    "John Wick": ["Keanu Reeves", "Michael Nyqvist", "Alfie Allen", "Willem Dafoe", "Ian McShane"],
    "The Shawshank Redemption": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
    "The Green Mile": ["Tom Hanks", "Michael Clarke Duncan", "David Morse", "Bonnie Hunt", "James Cromwell"],
    "The Fugitive": ["Harrison Ford", "Tommy Lee Jones", "Sela Ward", "Julianne Moore"],
    "A Few Good Men": ["Tom Cruise", "Jack Nicholson", "Demi Moore", "Kevin Bacon", "Kiefer Sutherland"],
    "The Silence of the Lambs": ["Jodie Foster", "Anthony Hopkins", "Scott Glenn", "Ted Levine"],
    "The Usual Suspects": ["Kevin Spacey", "Gabriel Byrne", "Benicio del Toro", "Stephen Baldwin", "Chazz Palminteri"],
    "Titanic": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane", "Kathy Bates"],
    "Avatar": ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver", "Stephen Lang"],
    "Aliens": ["Sigourney Weaver", "Michael Biehn", "Carrie Henn", "Lance Henriksen"],
    "Terminator 2: Judgment Day": ["Arnold Schwarzenegger", "Linda Hamilton", "Edward Furlong", "Robert Patrick"],
    "The Terminator": ["Arnold Schwarzenegger", "Linda Hamilton", "Michael Biehn", "Paul Winfield"],
    "Tropic Thunder": ["Ben Stiller", "Robert Downey Jr.", "Jack Black", "Tom Cruise", "Matthew McConaughey"],
    "The Hangover": ["Bradley Cooper", "Ed Helms", "Zach Galifianakis", "Justin Bartha"],
    "Silver Linings Playbook": ["Bradley Cooper", "Jennifer Lawrence", "Robert De Niro", "Jacki Weaver", "Chris Tucker"],
    "American Hustle": ["Christian Bale", "Amy Adams", "Bradley Cooper", "Jennifer Lawrence", "Jeremy Renner", "Robert De Niro"],
    "No Country for Old Men": ["Tommy Lee Jones", "Javier Bardem", "Josh Brolin", "Woody Harrelson"],
    "Fargo": ["Frances McDormand", "William H. Macy", "Steve Buscemi", "Peter Stormare"],
    "The Big Lebowski": ["Jeff Bridges", "John Goodman", "Steve Buscemi", "Julianne Moore", "Sam Elliott"],
    "True Grit": ["Jeff Bridges", "Hailee Steinfeld", "Matt Damon", "Josh Brolin"],
    "There Will Be Blood": ["Daniel Day-Lewis", "Paul Dano", "Kevin J. O'Connor", "Ciarán Hinds"],
    "Boogie Nights": ["Mark Wahlberg", "Julianne Moore", "Burt Reynolds", "John C. Reilly", "Heather Graham", "Don Cheadle"],
    "Magnolia": ["Tom Cruise", "Jason Robards", "Julianne Moore", "Philip Seymour Hoffman", "John C. Reilly"],
    "Snatch": ["Jason Statham", "Brad Pitt", "Benicio del Toro", "Vinnie Jones", "Alan Ford"],
    "Lock, Stock and Two Smoking Barrels": ["Jason Statham", "Nick Moran", "Jason Flemyng", "Dexter Fletcher", "Vinnie Jones"],
    "Sherlock Holmes": ["Robert Downey Jr.", "Jude Law", "Rachel McAdams", "Mark Strong"],
    "The Hobbit: An Unexpected Journey": ["Ian McKellen", "Martin Freeman", "Richard Armitage", "Andy Serkis"],
    "The Lord of the Rings: The Fellowship of the Ring": ["Elijah Wood", "Ian McKellen", "Viggo Mortensen", "Sean Astin", "Orlando Bloom", "Cate Blanchett", "Andy Serkis"],
    "The Lord of the Rings: The Return of the King": ["Elijah Wood", "Ian McKellen", "Viggo Mortensen", "Sean Astin", "Orlando Bloom", "Cate Blanchett", "Andy Serkis"],
    "Jurassic Park": ["Sam Neill", "Laura Dern", "Jeff Goldblum", "Richard Attenborough"],
    "Jurassic World": ["Chris Pratt", "Bryce Dallas Howard", "Vincent D'Onofrio", "BD Wong"],
    "Indiana Jones and the Raiders of the Lost Ark": ["Harrison Ford", "Karen Allen", "Paul Freeman", "John Rhys-Davies"],
    "E.T. the Extra-Terrestrial": ["Henry Thomas", "Drew Barrymore", "Dee Wallace", "Peter Coyote"],
    "Jaws": ["Roy Scheider", "Robert Shaw", "Richard Dreyfuss", "Lorraine Gary"],
    "Lincoln": ["Daniel Day-Lewis", "Sally Field", "David Strathairn", "Tommy Lee Jones"],
    "Bridge of Spies": ["Tom Hanks", "Mark Rylance", "Amy Ryan", "Alan Alda"],
    "The Truman Show": ["Jim Carrey", "Ed Harris", "Laura Linney", "Noah Emmerich"],
    "Eternal Sunshine of the Spotless Mind": ["Jim Carrey", "Kate Winslet", "Kirsten Dunst", "Mark Ruffalo"],
    "Step Brothers": ["Will Ferrell", "John C. Reilly", "Richard Jenkins", "Mary Steenburgen"],
    "Anchorman: The Legend of Ron Burgundy": ["Will Ferrell", "Christina Applegate", "Paul Rudd", "Steve Carell", "David Koechner"],
    "Talladega Nights: The Ballad of Ricky Bobby": ["Will Ferrell", "John C. Reilly", "Sacha Baron Cohen", "Gary Cole"],
    "Dodgeball: A True Underdog Story": ["Vince Vaughn", "Ben Stiller", "Christine Taylor", "Rip Torn"],
    "Due Date": ["Robert Downey Jr.", "Zach Galifianakis", "Michelle Monaghan", "Juliette Lewis"],
    "American Sniper": ["Bradley Cooper", "Sienna Miller", "Kyle Gallner", "Luke Grimes"],
    "Sully": ["Tom Hanks", "Aaron Eckhart", "Laura Linney", "Mike O'Malley"],
    "No Time to Die": ["Daniel Craig", "Ana de Armas", "Rami Malek", "Léa Seydoux", "Ralph Fiennes"],
    "Spectre": ["Daniel Craig", "Christoph Waltz", "Léa Seydoux", "Ralph Fiennes", "Monica Bellucci"],
    "Rogue One": ["Felicity Jones", "Diego Luna", "Ben Mendelsohn", "Forest Whitaker", "Mads Mikkelsen"],
    "The Last Jedi": ["Mark Hamill", "Carrie Fisher", "Daisy Ridley", "John Boyega", "Adam Driver", "Oscar Isaac"],
    "The Matrix Reloaded": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss", "Hugo Weaving", "Jada Pinkett Smith"],
    "John Wick: Chapter 2": ["Keanu Reeves", "Riccardo Scamarcio", "Ian McShane", "Laurence Fishburne", "Common"],
    "L.A. Confidential": ["Kevin Spacey", "Russell Crowe", "Guy Pearce", "Kim Basinger", "James Cromwell"],
    "The Rock": ["Sean Connery", "Nicolas Cage", "Ed Harris", "John Spencer"],
    "Con Air": ["Nicolas Cage", "John Cusack", "John Malkovich", "Steve Buscemi"],
    "Misery": ["James Caan", "Kathy Bates", "Richard Farnsworth", "Frances Sternhagen"],
    "Stand by Me": ["Wil Wheaton", "River Phoenix", "Corey Feldman", "Jerry O'Connell", "Kiefer Sutherland"],
    "True Romance": ["Christian Slater", "Patricia Arquette", "Dennis Hopper", "Val Kilmer", "Samuel L. Jackson", "Brad Pitt", "Christopher Walken"],
    "Natural Born Killers": ["Woody Harrelson", "Juliette Lewis", "Robert Downey Jr.", "Tom Sizemore", "Tommy Lee Jones"],
    "Cape Fear": ["Robert De Niro", "Nick Nolte", "Jessica Lange", "Joe Pesci"],
    "Mean Streets": ["Robert De Niro", "Harvey Keitel", "David Proval", "Amy Robinson"],
    "Hugo": ["Ben Kingsley", "Sacha Baron Cohen", "Asa Butterfield", "Chloe Grace Moretz"],
    "Shutter Island": ["Leonardo DiCaprio", "Mark Ruffalo", "Ben Kingsley", "Michelle Williams", "Max von Sydow"],
    "The Terminal": ["Tom Hanks", "Catherine Zeta-Jones", "Stanley Tucci", "Chi McBride"],
    "Cast Away": ["Tom Hanks", "Helen Hunt", "Nick Searcy", "Chris Noth"],
    "WALL-E": ["Ben Burtt", "Elissa Knight", "Jeff Garlin", "Fred Willard"],
    "Finding Nemo": ["Albert Brooks", "Ellen DeGeneres", "Alexander Gould", "Willem Dafoe"],
    "The Big Short": ["Christian Bale", "Steve Carell", "Ryan Gosling", "Brad Pitt", "Hamish Linklater"],
    "Gone Girl": ["Ben Affleck", "Rosamund Pike", "Neil Patrick Harris", "Tyler Perry"],
    "American Hustle": ["Christian Bale", "Amy Adams", "Bradley Cooper", "Jennifer Lawrence", "Jeremy Renner", "Robert De Niro"],
}

# Build fallback actor index
def build_fallback():
    films = {k: list(v) for k, v in FALLBACK_FILMS.items()}
    actors = {}
    for f, cast in films.items():
        for a in cast:
            actors.setdefault(a, [])
            if f not in actors[a]:
                actors[a].append(f)
    return films, actors


def main():
    films, actors = None, None
    try:
        print("Querying Wikidata SPARQL for film cast...", file=sys.stderr)
        data = run_query(sorted(set(FILM_TITLES)))
        films, actors = build_from_sparql(data)
        # Merge fallback for any film the query missed (more coverage = more solvable puzzles)
        fb_f, fb_a = build_fallback()
        for f, cast in fb_f.items():
            if f not in films:
                films[f] = cast
            else:
                for a in cast:
                    if a not in films[f]:
                        films[f].append(a)
        for a, fl in fb_a.items():
            for f in fl:
                actors.setdefault(a, [])
                if f not in actors[a]:
                    actors[a].append(f)
        print("Wikidata query OK. Films: %d, Actors: %d" % (len(films), len(actors)), file=sys.stderr)
    except Exception as e:
        print("Wikidata fetch failed (%s); using embedded curated dataset." % e, file=sys.stderr)
        films, actors = build_fallback()
        print("Fallback dataset. Films: %d, Actors: %d" % (len(films), len(actors)), file=sys.stderr)

    out = {"films": films, "actors": actors}
    with open("data.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("Wrote data.json", file=sys.stderr)


if __name__ == "__main__":
    main()
