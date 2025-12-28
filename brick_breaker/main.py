from game import Game


def main():
    print("Starting Brick Breaker Game...")
    print("Defender of the Crystal Kingdom")
    print("=" * 50)
    print("Controls:")
    print("- Move paddle: Mouse or LEFT/RIGHT arrow keys")
    print("- Launch ball: SPACEBAR")
    print("- Pause: P key")
    print("- Menu: ESC key")
    print("=" * 50)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()