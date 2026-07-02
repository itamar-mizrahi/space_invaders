import asyncio
import sys

print("Hello from main.py before Game import!")

try:
    from game import Game
    print("Successfully imported Game!")
except Exception as e:
    print(f"Error importing Game: {e}")

async def main():
    print("Inside async def main()!")
    try:
        game = Game()
        print("Game initialized!")
        await game.run()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    print("Starting asyncio.run(main())")
    asyncio.run(main())
