from dataclasses import dataclass, field
from drafter import *

set_website_title("Basketball Tracker")
set_site_information(
    author="Justin Serio",
    description="A basketball statistic tracker for teams",
    sources="Conversation with LLM.pdf",
    planning="Copy of CS1 Final Project 1_ Design.pdf",
    links=["https://github.com/jdserio/cisc108-final-demo-"]
)
hide_debug_information()
set_website_framed(False)


@dataclass
class Player:
    """Stores one basketball player's information."""
    name: str
    jersey_number: int
    points: int
    rebounds: int
    assists: int


@dataclass
class State:
    """Stores all information for the basketball tracker."""
    players: list[Player] = field(default_factory=list)
    team_name: str = "My Basketball Team"
    games_played: int = 0
    selected_player: str = ""


@route
def index(state: State) -> Page:
    """Displays the basketball tracker homepage."""
    return Page(state, [
        Text("BASKETBALL TRACKER"),
        Text("--------------------"),
        Text("Welcome to your basketball team dashboard!"),
        Text("Manage players and track their statistics."),
        Text("Team: " + state.team_name),
        Text("Games Played: " + str(state.games_played)),
        Text("Total Players: " + str(len(state.players))),
        Text("--------------------"),
        Text("WHAT WOULD YOU LIKE TO DO?"),
        Button("View Players", players),
        Button("Add Player", add_player),
        Button("Player Statistics", stats),
        Button("Update Statistics", update_player),
        Button("Leaderboard", leaderboard),
        Button("Delete Player", delete_player),
        Button("Team Settings", team_settings)
    ])


@route
def players(state: State) -> Page:
    """Displays all players on the team."""
    content: list = [Text("TEAM ROSTER"), Text("--------------------")]
    if len(state.players) == 0:
        content.append(Text("No players have been added yet."))
    else:
        for player in state.players:
            content.append(Text(
                player.name + " | Jersey #" + str(player.jersey_number)
            ))
            content.append(Text(
                "Points: " + str(player.points) +
                " | Rebounds: " + str(player.rebounds) +
                " | Assists: " + str(player.assists)
            ))
    content.append(Button("Home", "/"))
    return Page(state, content)


@route
def add_player(state: State) -> Page:
    """Displays the form for adding a player."""
    return Page(state, [
        Text("ADD A PLAYER"),
        Text("--------------------"),
        TextBox("name", "Player Name"),
        TextBox("jersey", "Jersey Number"),
        TextBox("points", "Points"),
        TextBox("rebounds", "Rebounds"),
        TextBox("assists", "Assists"),
        Button("Add Player", add_player_submit),
        Button("Home", "/")
    ])


@route
def add_player_submit(state: State, name: str, jersey: str,
                      points: str, rebounds: str,
