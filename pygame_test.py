import pygame


def run():
    pygame.init()
    pygame.display.set_mode((180, 120))

    running = True

    while running:
        for event in pygame.event.get():
            print event
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()


if __name__ == '__main__':
    run()
