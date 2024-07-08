# **Задание 3.** Напишите приложение, которое работает с заметками
# Приложение должно создавать, читать, редактировать и удалять заметки.
# Для этого создайте функции для каждой операции с
# заметками и основную функцию, которая управляет работой приложения.

# +
# Задание 4. Добавьте вывод всех заметок пользователя

import os
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_note(note_text, note_name):
    """получает название и текст заметки, а затем создает текстовый файл с этим названием и текстом"""
    if not note_text.strip():
        logger.error("Текст заметки не может быть пустым.")
        return
    with open(f"{note_name}.txt", "w", encoding="utf-8") as file:
        file.write(note_text)
    logger.info(f"Заметка {note_name} успешно создана.")


def create_note():
    """запрашивает у пользователя название и текст заметки, а затем вызывает функцию build_note(note_text, note_name)"""
    note_name = input("Введите название заметки для создания: ").strip()
    if not note_name:
        logger.error("Название заметки не может быть пустым")
        return
    note_text = input("Введите текст заметки: ")
    build_note(note_text, note_name)


def read_note():
    """запрашивает у пользователя название заметки. Если файл с таким названием существует, функция считывает содержимое
    файла и выводит его на экран. Если файла не существует, функция выводит сообщение, что заметка не найдена.
    Для проверки наличия файла используйте функцию os.path.isfile из модуля os.
    Не забудьте импортировать этот модуль."""
    note_name = input("Введите название заметки: ")
    if os.path.isfile(note_name + ".txt"):
        with open(f"{note_name}.txt", "r", encoding="utf-8") as file:
            print(file.read())
        return note_name
    else:
        logger.error(f"Заметка {note_name} не найдена.")
        return ''


def edit_note():
    """запрашивает у пользователя название заметки. Если файл с введенным именем существует, функция считывает и выводит
     содержимое файла, запрашивает у пользователя новый текст заметки и обновляет содержимое файла. Если файла не
      существует, она выводит сообщение, что заметка не найдена."""
    note_name = read_note()
    if note_name != '':
        note_text = input("Введите новый текст заметки: ")
        with open(f"{note_name}.txt", "w", encoding="utf-8") as file:
            file.write(note_text)
        logger.info(f"Заметка {note_name} обновлена.")


def delete_note():
    """запрашивает у пользователя название заметки. Если файл с введенным именем существует, функция удаляет файл.
    Для удаления используйте функцию os.remove из модуля os. Если файла не существует, она выводит сообщение,
    что заметка не найдена."""
    note_name = input("Введите название заметки для удаления: ")
    if os.path.isfile(note_name + '.txt'):
        os.remove(note_name + '.txt')
        logger.info(f"Заметка {note_name} удалена.")
    else:
        logger.error("Заметка не найдена.")


def display_notes():
    """выводит все заметки пользователя"""
    # формирование списка файлов с замктками
    notes = [note for note in os.listdir() if note.endswith(".txt")]
    # создание словаря с именем файла и длинной заметки
    dic_notes = {}
    for i in notes:
        with open(i, "r", encoding="utf-8") as file:
            dic_notes[i] = len(file.read())

    # сортировка заметок по уменьшению длинны
    sorted_notes = sorted(dic_notes.items(), key=lambda item: item[1], reverse=True)
    # вывод заметок в порядке уменьшения длинны
    for i in sorted_notes:
        with open(i[0], "r", encoding="utf-8") as file:
            print(f'Заметка "{i[0]}".')
            print(file.read(), '\n')


def display_sorted_notes():
    """выводит все заметки пользователя в порядке уменьшения длинны"""
    # формирование списка файлов с замктками
    notes = [note for note in os.listdir() if note.endswith(".txt")]
    # создание словаря с именем файла и длинной заметки
    dic_notes = {}
    for i in notes:
        with open(i, "r", encoding="utf-8") as file:
            dic_notes[i] = len(file.read())
    # сортировка заметок по уменьшению длинны
    sorted_notes = sorted(dic_notes.items(), key=lambda item: item[1], reverse=True)
    # вывод заметок в порядке уменьшения длинны
    for i in sorted_notes:
        with open(i[0], "r", encoding="utf-8") as file:
            print(f'Заметка "{i[0]}".')
            print(file.read(), '\n')


def main():
    """содержит основной цикл программы. Функция отображает меню с вариантами действий с заметками, которые пользователь
     может выбрать. Затем функция выполняет действие, которое выбрал пользователь."""

    while True:
        # запрашиваем дейстие с заметкой у пользователя
        sel = input("Что вы хотите сделать с заметкой?\n"
                    "Создать       - 1\n"
                    "Читать        - 2\n"
                    "Редактировать - 3\n"
                    "Удалить       - 4\n"
                    "Вывести все заметки в порядке уменьшения длинны - 5\n"
                    ":> ")
        # выполнение действий с заметками
        if sel == "1":
            create_note()
        elif sel == "2":
            read_note()
        elif sel == "3":
            edit_note()
        elif sel == "4":
            delete_note()
        elif sel == "5":
            display_sorted_notes()
        else:
            logger.info('Не верно введен вариант действия с заметклй.')

        # выход из программы
        time.sleep(0.1)
        if input('Продолжить работу с заметками (y/n)?\n:> ').lower() == 'n':
            break


if __name__ == "__main__":
    main()

