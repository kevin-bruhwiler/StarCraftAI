import cybw
import StarCraftAI as SCAI
from time import sleep

client = cybw.BWAPIClient
broodwar = cybw.Broodwar
agent = SCAI.StarCraftAI()


def reconnect():
    while not client.connect():
        sleep(0.5)

print("Connecting...")
reconnect()

while True:
    while not broodwar.isInGame():
        client.update()
        if not client.isConnected():
            print("Reconnecting...")
            reconnect()

    agent.initialize()

    frames = 0

    while broodwar.isInGame():

        frames += 1

        if frames == 5:
            if cybw.Broodwar.isReplay():
                for event in broodwar.getEvents():
                    if event.getType() == cybw.EventType.UnitDestroy:
                        for player_state in agent.replay_game_states:
                            player_state.remove_unit(event.getUnit())
                    elif event.getType() == cybw.EventType.UnitMorph:
                        for player_state in agent.replay_game_states:
                            player_state.update_unit(event.getUnit())
                    elif event.getType() == cybw.EventType.UnitShow:
                        for player_state in agent.replay_game_states:
                            player_state.update_unit(event.getUnit())
                    elif event.getType() == cybw.EventType.UnitHide:
                        pass
            else:
                for event in broodwar.getEvents():
                    if event.getType() == cybw.EventType.UnitDestroy:
                        for player_state in agent.game_state:
                            player_state.remove_unit(event.getUnit())
                    elif event.getType() == cybw.EventType.UnitMorph:
                        for player_state in agent.game_state:
                            player_state.update_unit(event.getUnit())
                    elif event.getType() == cybw.EventType.UnitShow:
                        for player_state in agent.game_state:
                            player_state.update_unit(event.getUnit())
                    elif event.getType() == cybw.EventType.UnitHide:
                        pass

            agent.run()

            frames = 0

        broodwar.drawTextScreen(cybw.Position(300, 0), "FPS: " + str(broodwar.getAverageFPS()))
        client.update()

