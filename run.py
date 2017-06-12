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

    if broodwar.isReplay():
        broodwar << "The following players are in this replay:\n"
        players = broodwar.getPlayers()

    else:
        agent.run()

        broodwar.drawTextScreen(cybw.Position(300, 0), "FPS: " + str(broodwar.getAverageFPS()))
        client.update()
