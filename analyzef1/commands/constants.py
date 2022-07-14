YEAR = [2018, 2019, 2020, 2021, 2022]
LOCATION = ['Sakhir', 'Jeddah', 'Melbourne', 'Imola', 'Miami', 'Barcelona', 'Monaco', 'Baku', 'Montréal', 'Silverstone', 'Spielberg', 'Le Castellet', 'Budapest', 'Spa-Francorchamps', 'Zandvoort', 'Monza', 'Marina Bay', 'Suzuka', 'Austin', 'Mexico City', 'São Paulo', 'Yas Island']
SESSION = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SQ', 'R']

CHOOSE_SESSION = ['Year', 'Location', 'Session']


UINAVBAR = ['Upcoming Events', 'Leaderboard', 'Previous Events']

DRIVER_TEAM_MAPPING = {
    # only necessary when loading live timing data that does not include
    # the driver and team listing and no data is available on ergast yet
    '23': {'Abbreviation': 'ALB', 'FirstName': 'Alexander',
           'LastName': 'Albon', 'TeamName': 'Williams'},
    '14': {'Abbreviation': 'ALO', 'FirstName': 'Fernando',
           'LastName': 'Alonso', 'TeamName': 'Alpine F1 Team'},
    '77': {'Abbreviation': 'BOT', 'FirstName': 'Valtteri',
           'LastName': 'Bottas', 'TeamName': 'Alfa Romeo'},
    '10': {'Abbreviation': 'GAS', 'FirstName': 'Pierre',
           'LastName': 'Gasly', 'TeamName': 'AlphaTauri'},
    '44': {'Abbreviation': 'HAM', 'FirstName': 'Lewis',
           'LastName': 'Hamilton', 'TeamName': 'Mercedes'},
    '27': {'Abbreviation': 'HUL', 'FirstName': 'Hülkenberg',
           'LastName': 'Vettel', 'TeamName': 'Aston Martin'},
    '6': {'Abbreviation': 'LAT', 'FirstName': 'Nicholas',
          'LastName': 'Latifi', 'TeamName': 'Williams'},
    '16': {'Abbreviation': 'LEC', 'FirstName': 'Charles',
           'LastName': 'Leclerc', 'TeamName': 'Ferrari'},
    '20': {'Abbreviation': 'MAG', 'FirstName': 'Kevin',
           'LastName': 'Magnussen', 'TeamName': 'Haas F1 Team'},
    '4': {'Abbreviation': 'NOR', 'FirstName': 'Lando',
          'LastName': 'Norris', 'TeamName': 'McLaren'},
    '31': {'Abbreviation': 'OCO', 'FirstName': 'Esteban',
           'LastName': 'Ocon', 'TeamName': 'Alpine F1 Team'},
    '11': {'Abbreviation': 'PER', 'FirstName': 'Sergio',
           'LastName': 'Pérez', 'TeamName': 'Red Bull'},
    '3': {'Abbreviation': 'RIC', 'FirstName': 'Daniel',
          'LastName': 'Ricciardo', 'TeamName': 'McLaren'},
    '63': {'Abbreviation': 'RUS', 'FirstName': 'George',
           'LastName': 'Russell', 'TeamName': 'Mercedes'},
    '55': {'Abbreviation': 'SAI', 'FirstName': 'Carlos',
           'LastName': 'Sainz', 'TeamName': 'Ferrari'},
    '47': {'Abbreviation': 'MSC', 'FirstName': 'Mick',
           'LastName': 'Schumacher', 'TeamName': 'Haas F1 Team'},
    '18': {'Abbreviation': 'STR', 'FirstName': 'Lance',
           'LastName': 'Stroll', 'TeamName': 'Aston Martin'},
    '22': {'Abbreviation': 'TSU', 'FirstName': 'Yuki',
           'LastName': 'Tsunoda', 'TeamName': 'AlphaTauri'},
    '1': {'Abbreviation': 'VER', 'FirstName': 'Max',
          'LastName': 'Verstappen', 'TeamName': 'Red Bull'},
    '5': {'Abbreviation': 'VET', 'FirstName': 'Sebastian',
          'LastName': 'Vettel', 'TeamName': 'Aston Martin'},
    '24': {'Abbreviation': 'ZHO', 'FirstName': 'Guanyu',
           'LastName': 'Zhou', 'TeamName': 'Alfa Romeo'}
}