import cybw
import StarCraftAI as SCAI
from time import sleep

client = cybw.BWAPIClient
Broodwar = cybw.Broodwar

def reconnect():
    while not client.connect():
        sleep(0.5)

print("Connecting...")
reconnect()
while True:
    print("waiting to enter match")
    while not Broodwar.isInGame():
        client.update()
        if not client.isConnected():
            print("Reconnecting...")
            reconnect()

    # need newline to flush buffer
    Broodwar << "The map is " << Broodwar.mapName() << ", a " \
        << len(Broodwar.getStartLocations()) << "player map" << "\n"

    # Enable some cheat flags
    Broodwar.enableFlag(cybw.Flag.UserInput)

    show_bullets = False
    show_visibility_data = False

    if Broodwar.isReplay():
        Broodwar << "The following players are in this replay:\n"
        players = Broodwar.getPlayers()

    else:
        SCAI.run()

        Broodwar.drawTextScreen(cybw.Position(300, 0), "FPS: " + str(Broodwar.getAverageFPS()))
        client.update()
