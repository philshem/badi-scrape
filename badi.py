import csv
import datetime
import websockets
import json
import asyncio


async def fetch_anzahl_gaeste(uri):

    async with websockets.connect(uri) as websocket:
        # Send a request to fetch all data
        await websocket.send("all")

        # Receive response
        response = await websocket.recv()
        data = json.loads(response)

        # Find the entry for "SSD-4" or similar
        for entry in data:
            if entry.get("uid") == "SSD-4":
                anzahl_gaeste = entry.get("currentfill")
                print(f"Anzahl Gäste: {anzahl_gaeste}")
                return int(anzahl_gaeste)


def main():
    uri = "wss://badi-public.crowdmonitor.ch:9591/api"

    # Get and print the guest count
    guest_count = asyncio.run(fetch_anzahl_gaeste(uri))
    print(uri, guest_count)

    if guest_count is not None and guest_count >= 0:
        # Write to CSV
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data/swimmers.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, uri, guest_count])

        print(f"Data written to CSV: {timestamp}, {uri}, {guest_count}")


if __name__ == "__main__":
    main()
