import cybw
import StarCraftAI as scai
import AutoObserver
from time import sleep

client = cybw.BWAPIClient
broodwar = cybw.Broodwar
agent = scai.StarCraftAI()
observer = AutoObserver.AutoObserver()


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
        observer.observe()
        frames += 1

        if frames == 5:
            agent.run()
            frames = 0

        broodwar.drawTextScreen(cybw.Position(300, 0), "FPS: " + str(broodwar.getAverageFPS()))
        client.update()

