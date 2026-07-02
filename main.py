import asyncio
from game import Game
# Trigger rebuild

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())

