from graphics.menu import Menu
import asyncio


def main():
    print("Hello Chess!")

    menu = Menu()
    asyncio.run(menu.menu_screen())

    print('done')
