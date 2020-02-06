import time

import requests
import pandas as pd


def main():
    """
    Grabs all the character data from the most recent encounter, for the defined encounter_id, and parses ot the gear
    worn by each player during that encounter.

    In warcraftlogs api, the encounter_id will be the same for a boss no matter what lockout it was logged (think of
    it as a boss id). It will remain the same from week to week.

    Character names are defined in the `character_names` file with one character name per line
    :return:
    """
    sep = "; "  # How each item will be seperated on the line. Default is `;` to make it easier to have google sheets split into columns.
    encounter_id = 669  # The id of the encounter to parse gear from. 669 is Sulfuron
    pause_time_in_seconds = 5  # Wait time between calls. Part of the api throttling.
    server_name = "Kurinnaxx"
    server_region = "US"

    f = open("character_names", "r")
    character_names = f.readlines()
    for character_name in character_names:
        # Get character data and parse it into a dataframe
        character_name = character_name.strip()
        character_data = get_character_data_for_encounter(
            character_name, server_name, server_region, encounter_id
        )
        df = pd.DataFrame.from_dict(character_data)

        # Get the index of the row with the latest/largest timestamp
        latest_timestamp_row_index = df["startTime"].idxmax()

        # Dataframe of the gear from that row
        gear_data_frame = pd.DataFrame(df.iloc[latest_timestamp_row_index].gear)

        # Initialize the gear list with the character_name so it appears first in the row
        gear_list = [character_name]
        gear_list.extend(gear_data_frame["name"].tolist())
        print(*gear_list, sep=sep)
        time.sleep(pause_time_in_seconds)


def get_character_data_for_encounter(
    character_name: str, server_name: str, server_region: str, encounter_id: int
):
    """
    Retrieves the character data for the given character_name and given encounter_id
    :param character_name:
    :param server_name:
    :param server_region:
    :param encounter_id:
    :return:
    """
    response = requests.get(
        f"""https://classic.warcraftlogs.com:443/v1/parses/character/{character_name}/{server_name}/{server_region}?encounter={encounter_id}&api_key=3e2ec7e0216381cafd02364b41d6c32b"""
    )
    return response.json()


if __name__ == "__main__":
    main()
