
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


# PLAYER DATA

@dataclass
class Player:
    """Stores one basketball player's information."""
    name: str
    jersey_number: int
    points: int
    rebounds: int
    assists: int


# WEBSITE DATA

@dataclass
class State:
    """Stores all information for the basketball tracker."""
    players: list[Player] = field(default_factory=list)
    team_name: str = "My Basketball Team"
    games_played: int = 0
    selected_player: str = ""


# HOME PAGE

@route
def index(state: State) -> Page:
    """Displays the basketball tracker homepage."""
    return Page(state, [
        Text("🏀 BASKETBALL TRACKER 🏀"),
        Text("--------------------"),
        Text("Welcome to your basketball dashboard!"),
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


# VIEW PLAYERS

@route
def players(state: State) -> Page:
    """Displays all players on the team."""
    content = [
        Text("TEAM ROSTER"),
        Text("--------------------")
    ]

    if len(state.players) == 0:
        content.append(Text("No players have been added yet."))
    else:
        for player in state.players:
            content.append(Text(
                player.name + " | Jersey #" +
                str(player.jersey_number)
            ))
            content.append(Text(
                "Points: " + str(player.points) +
                " | Rebounds: " + str(player.rebounds) +
                " | Assists: " + str(player.assists)
            ))

    content.append(Button("Home", "/"))

    return Page(state, content)


# ADD PLAYER

@route
def add_player(state: State) -> Page:
    """Allows users to add a new basketball player."""
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
def add_player_submit(state: State, name: str,
                      jersey: str, points: str,
                      rebounds: str, assists: str) -> Page:
    """Adds a new player to the team."""

    if name.strip() == "":
        return Page(state, [
            Text("Please enter a player name."),
            Button("Try Again", add_player)
        ])

    if not jersey.isdigit() or not points.isdigit():
        return Page(state, [
            Text("Jersey number and points must be numbers."),
            Button("Try Again", add_player)
        ])

    if not rebounds.isdigit() or not assists.isdigit():
        return Page(state, [
            Text("Rebounds and assists must be numbers."),
            Button("Try Again", add_player)
        ])

    new_player = Player(
        name,
        int(jersey),
        int(points),
        int(rebounds),
        int(assists)
    )

    state.players.append(new_player)

    return Page(state, [
        Text(name + " was successfully added!"),
        Button("View Players", players),
        Button("Add Another Player", add_player),
        Button("Home", "/")
    ])


# PLAYER STATISTICS

@route
def stats(state: State) -> Page:
    """Allows users to select a player to view their stats."""
    content = [
        Text("PLAYER STATISTICS"),
        Text("--------------------")
    ]

    if len(state.players) == 0:
        content.append(Text("No players available."))
    else:
        content.append(Text("Select a player:"))

        for player in state.players:
            content.append(
                Button(
                    player.name,
                    view_stats,
                    arguments={"name": player.name}
                )
            )

    content.append(Button("Home", "/"))

    return Page(state, content)


@route
def view_stats(state: State, name: str) -> Page:
    """Displays the statistics of a selected player."""
    state.selected_player = name

    for player in state.players:
        if player.name == name:
            return Page(state, [
                Text("STATS FOR " + player.name.upper()),
                Text("--------------------"),
                Text("Jersey Number: " + str(player.jersey_number)),
                Text("Points: " + str(player.points)),
                Text("Rebounds: " + str(player.rebounds)),
                Text("Assists: " + str(player.assists)),
                Button("Back to Players", stats),
                Button("Home", "/")
            ])

    return Page(state, [
        Text("Player not found."),
        Button("Back to Statistics", stats),
        Button("Home", "/")
    ])


# UPDATE PLAYER STATISTICS

@route
def update_player(state: State) -> Page:
    """Allows users to choose a player to update."""
    content = [
        Text("UPDATE PLAYER STATS"),
        Text("--------------------")
    ]

    if len(state.players) == 0:
        content.append(Text("No players available to update."))
    else:
        for player in state.players:
            content.append(
                Button(
                    player.name,
                    update_stats,
                    arguments={"name": player.name}
                )
            )

    content.append(Button("Home", "/"))

    return Page(state, content)


@route
def update_stats(state: State, name: str) -> Page:
    """Allows users to edit a player's statistics."""

    for player in state.players:
        if player.name == name:
            return Page(state, [
                Text("UPDATE STATS FOR " + player.name.upper()),
                Text("--------------------"),
                Text("Enter the player's new statistics:"),

                Text("Points:"),
                TextBox("points", str(player.points)),

                Text("Rebounds:"),
                TextBox("rebounds", str(player.rebounds)),

                Text("Assists:"),
                TextBox("assists", str(player.assists)),

                Button(
                    "Save Statistics",
                    save_stats,
                    arguments={"name": name}
                ),

                Button("Cancel", update_player)
            ])

    return Page(state, [
        Text("Player not found."),
        Button("Home", "/")
    ])


@route
def save_stats(state: State, name: str,
               points: str, rebounds: str,
               assists: str) -> Page:
    """Saves the updated player statistics."""

    if (not points.isdigit()
            or not rebounds.isdigit()
            or not assists.isdigit()):

        return Page(state, [
            Text("Please enter numbers for all statistics."),
            Button(
                "Try Again",
                update_stats,
                arguments={"name": name}
            )
        ])

    for player in state.players:
        if player.name == name:

            player.points = int(points)
            player.rebounds = int(rebounds)
            player.assists = int(assists)

            return Page(state, [
                Text("STATISTICS SUCCESSFULLY UPDATED!"),
                Text("--------------------"),
                Text("Player: " + player.name),
                Text("Points: " + str(player.points)),
                Text("Rebounds: " + str(player.rebounds)),
                Text("Assists: " + str(player.assists)),
                Button("Home", "/"),
                Button("Update Another Player", update_player),
                Button("View Statistics", stats)
            ])

    return Page(state, [
        Text("Player not found."),
        Button("Home", "/")
    ])


# LEADERBOARD

@route
def leaderboard(state: State) -> Page:
    """Displays players ranked by their points."""
    content = [
        Text("TEAM LEADERBOARD"),
        Text("--------------------")
    ]

    if len(state.players) == 0:
        content.append(Text("No players available yet."))
    else:
        ranked_players = sorted(
            state.players,
            key=lambda player: player.points,
            reverse=True
        )

        position = 1

        for player in ranked_players:
            content.append(Text(
                str(position) + ". " + player.name +
                " - " + str(player.points) + " points"
            ))
            position += 1

    content.append(Button("Home", "/"))

    return Page(state, content)


# DELETE PLAYER

@route
def delete_player(state: State) -> Page:
    """Allows users to choose a player to delete."""
    content = [
        Text("DELETE A PLAYER"),
        Text("--------------------")
    ]

    if len(state.players) == 0:
        content.append(Text("There are no players to delete."))
    else:
        for player in state.players:
            content.append(
                Button(
                    player.name,
                    confirm_delete,
                    arguments={"name": player.name}
                )
            )

    content.append(Button("Home", "/"))

    return Page(state, content)


@route
def confirm_delete(state: State, name: str) -> Page:
    """Confirms which player the user wants to delete."""
    state.selected_player = name

    return Page(state, [
        Text("DELETE " + name + "?"),
        Text("Are you sure you want to remove this player?"),
        Button(
            "Yes, Delete Player",
            remove_player,
            arguments={"name": name}
        ),
        Button("Cancel", delete_player),
        Button("Home", "/")
    ])


@route
def remove_player(state: State, name: str) -> Page:
    """Removes a player from the team."""

    for player in state.players:
        if player.name == name:
            state.players.remove(player)
            state.selected_player = ""

            return Page(state, [
                Text(name + " was successfully deleted."),
                Button("View Players", players),
                Button("Home", "/")
            ])

    return Page(state, [
        Text("Player not found."),
        Button("Home", "/")
    ])


# TEAM SETTINGS

@route
def team_settings(state: State) -> Page:
    """Allows users to update team information."""
    return Page(state, [
        Text("TEAM SETTINGS"),
        Text("--------------------"),
        Text("Current Team: " + state.team_name),
        TextBox("team_name", "New Team Name"),
        Button("Save Team Name", save_team_name),
        Text("Games Played: " + str(state.games_played)),
        Button("Record a Game", record_game),
        Button("Home", "/")
    ])


@route
def save_team_name(state: State, team_name: str) -> Page:
    """Changes the basketball team's name."""

    if team_name.strip() == "":
        return Page(state, [
            Text("Please enter a team name."),
            Button("Try Again", team_settings)
        ])

    state.team_name = team_name

    return Page(state, [
        Text("Team name successfully changed!"),
        Text("New Team Name: " + state.team_name),
        Button("Team Settings", team_settings),
        Button("Home", "/")
    ])


@route
def record_game(state: State) -> Page:
    """Increases the number of games played."""
    state.games_played += 1

    return Page(state, [
        Text("Game successfully recorded!"),
        Text("Total Games Played: " + str(state.games_played)),
        Button("Team Settings", team_settings),
        Button("Home", "/")
    ])


# START WEBSITE

start_server(State())

