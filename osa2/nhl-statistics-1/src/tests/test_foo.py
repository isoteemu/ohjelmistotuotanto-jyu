from statistics_service import StatisticsService
from player import Player

from unittest.mock import patch, mock_open
from player_reader import PlayerReader


def test_player_initialization():
    player = Player("John Doe", "Team A", 10, 5)
    assert player.name == "John Doe"
    assert player.team == "Team A"
    assert player.goals == 10
    assert player.assists == 5

def test_player_points():
    player = Player("John Doe", "Team A", 10, 5)
    assert player.points == 15

def test_player_str():
    player = Player("John Doe", "Team A", 10, 5)
    assert str(player) == "John Doe Team A 10 + 5 = 15"



@patch('player_reader.request.urlopen')
def test_get_players(mock_urlopen):
    mock_data = b"John Doe;Team A;Position;10;5\nJane Smith;Team B;Position;8;7\n"
    mock_urlopen.return_value = mock_open(read_data=mock_data).return_value

    reader = PlayerReader("http://example.com/players.txt")
    players = reader.get_players()

    assert len(players) == 2

    assert players[0].name == "John Doe"
    assert players[0].team == "Team A"
    assert players[0].goals == 10
    assert players[0].assists == 5

    assert players[1].name == "Jane Smith"
    assert players[1].team == "Team B"
    assert players[1].goals == 8
    assert players[1].assists == 7


@patch('player_reader.request.urlopen')
def test_statistics_service_initialization(mock_urlopen):
    mock_data = b"John Doe;Team A;Position;10;5\nJane Smith;Team B;Position;8;7\n"
    mock_urlopen.return_value = mock_open(read_data=mock_data).return_value

    reader = PlayerReader("http://example.com/players.txt")
    service = StatisticsService(reader)

    assert len(service._players) == 2


@patch('player_reader.request.urlopen')
def test_search_player(mock_urlopen):
    mock_data = b"John Doe;Team A;Position;10;5\nJane Smith;Team B;Position;8;7\n"
    mock_urlopen.return_value = mock_open(read_data=mock_data).return_value

    reader = PlayerReader("http://example.com/players.txt")
    service = StatisticsService(reader)

    player = service.search("John Doe")
    assert player is not None
    assert player.name == "John Doe"

    player = service.search("Nonexistent Player")
    assert player is None

@patch('player_reader.request.urlopen')
def test_team(mock_urlopen):
    mock_data = b"John Doe;Team A;Position;10;5\nJane Smith;Team B;Position;8;7\n"
    mock_urlopen.return_value = mock_open(read_data=mock_data).return_value

    reader = PlayerReader("http://example.com/players.txt")
    service = StatisticsService(reader)

    team_a_players = service.team("Team A")
    assert len(team_a_players) == 1
    assert team_a_players[0].name == "John Doe"

    team_b_players = service.team("Team B")
    assert len(team_b_players) == 1
    assert team_b_players[0].name == "Jane Smith"

    team_c_players = service.team("Team C")
    assert len(team_c_players) == 0

@patch('player_reader.request.urlopen')
def test_top_players(mock_urlopen):
    mock_data = b"John Doe;Team A;Position;10;5\nJane Smith;Team B;Position;8;7\n"
    mock_urlopen.return_value = mock_open(read_data=mock_data).return_value

    reader = PlayerReader("http://example.com/players.txt")
    service = StatisticsService(reader)

    top_players = service.top(1)
    assert len(top_players) == 2
    assert top_players[0].name == "John Doe"
    assert top_players[1].name == "Jane Smith"
