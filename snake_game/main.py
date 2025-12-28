from game import Game


def main():
    print("Starting Emerald Serpent Game...")
    print("The Mystical Garden Quest")
    print("=" * 50)
    print("Controls:")
    print("- Movement: Arrow Keys or WASD")
    print("- Pause: P key")
    print("- Menu: ESC key")
    print("=" * 50)
    print("Objective:")
    print("- Eat food to grow")
    print("- Reach target length to complete levels")
    print("- Avoid walls, obstacles, and yourself")
    print("=" * 50)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()