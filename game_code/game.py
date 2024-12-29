"""
Этот модуль содержит класс TravelGame, который управляет логикой и интерфейсом игры "Путешественник".

Класс TravelGame отвечает за:
- Инициализацию игры и ее элементов интерфейса.
- Отображение различных локаций с описаниями, изображениями и аудио.
- Обработку действий игрока, таких как взятие предметов и переход к следующим локациям.
- Отображение вводных окон и сообщений об ошибках.

Использует библиотеки Tkinter для создания графического интерфейса и Pygame для воспроизведения музыки.
"""

import tkinter as tk
from tkinter import messagebox #для отображения сообщений пользователю
from PIL import Image, ImageTk #для работы с изображениями
import pygame  #для воспроизведения музыки
from exceptions import InvalidImagePathError, InvalidAudioPathError  # исключения
import os


class TravelGame:
    """Класс для управления игрой Путешественник."""
    def __init__(self, root):
        """Инициализация игры."""
        self.take_button = None
        self.next_button = None
        self.description_label = None
        self.title_label = None
        self.image_id = None
        self.photo = None
        self.canvas = None
        self.root = root
        self.root.title("Путешественник")
        #инициализация Pygame Mixer
        pygame.mixer.init()

        self.current_location = 0
        self.item_window_open = False  #флаг для отслеживания состояния окна предмета
        self.intro_window = None  #инициализируем ссылку на вступительное окно

        #локации
        self.locations = [
            {
                "name": "Розовая долина",
                "description": "Это красивое место с розовыми цветами и великолепными пейзажами.",
                "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/_.jpeg",
                "audio": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/audios/e4c1fdca51422a9.mp3",  # Путь к аудиофайлу
                "item": {
                    "name": "Цветочек",
                    "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/_ (1).jpeg",
                }
            },
            {
                "name": "Синее озеро",
                "description": "Чистое синее озеро, которое отражает небеса.",
                "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/Голубое озеро_ Кавказские горы.jpeg",
                "audio": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/audios/7b4b160fc601b02.mp3",  # Путь к аудиофайлу
                "item": {
                    "name": "Лягушка",
                    "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/ЛЯГУШКА.jpeg",
                }
            },
            {
                "name": "Зачарованная пещера",
                "description": "Пещера, полная волшебства. Здесь можно услышать эхо древних заклинаний.",
                "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/The Crystal Caverns.jpeg",
                "audio": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/audios/16c1e01f002d91a.mp3",  # Путь к аудиофайлу
                "item": {
                    "name": "Кристалл мудрости",
                    "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/Chrome Diopside Phone Wallpaper.jpeg",
                }
            },
            {
                "name": "Лес Сказок",
                "description": "В этом лесу деревья шепчут древние сказания, а цветы светятся в темноте.",
                "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/Арт аниме светящийся лес.jpeg",
                "audio": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/audios/bd6704ab7470ce8.mp3",  # Путь к аудиофайлу
                "item": {
                    "name": "Сказочный гриб",
                    "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/_ (3).jpeg",
                }
            },
            {
                "name": "Звездная поляна",
                "description": "Поляна, где звезды падают на землю, образуя волшебные узоры.",
                "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/_ (2).jpeg",
                "audio": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/audios/Night-Interior-of-Minas-Gerais-Brazil.mp3",  # Путь к аудиофайлу
                "item": {
                    "name": "Звездочка",
                    "image": "/Users/dara/PycharmProjects/ПРОЕКТ ОП 2/images/Jupiter and Saturn Will Form a Rare “Double Planet” in the Sky Before Christmas.jpeg",
                }
            }
        ]

        self.show_intro()  # показываем вступительное окно

    def show_intro(self):
        """Метод для отображения вступительного окна."""
        self.intro_window = tk.Toplevel(self.root)
        self.intro_window.title("Добро пожаловать в Путешественник!")

        intro_text = 'Добро пожаловать в игру "Путешественник"!\n\n' \
                     "В этой игре вы будете исследовать различные волшебные локации,\n" \
                     "собирать уникальные предметы и наслаждаться красивыми пейзажами.\n\n" \
                     'Нажмите "Начать", чтобы отправиться в путешествие!'

        intro_label = tk.Label(self.intro_window, text=intro_text, font=("Comic Sans MS", 14),
                               wraplength=400)  # создаем метку с текстом вступления и заданным шрифтом
        intro_label.pack(pady=20)  # размещаем метку в окне с отступом по вертикали

        start_button = tk.Button(self.intro_window, text="Начать",  # создаем кнопку с текстом "Начать"
                                 command=self.start_game, bg="lightgreen",
                                 # указываем функцию, вызываемую при нажатии, и цвет фона
                                 font=("Comic Sans MS", 16))  # задаем шрифт для кнопки
        start_button.pack(pady=10)  # размещаем кнопку в окне с отступом по вертикали

        #центрируем окно
        self.intro_window.update_idletasks()  #обновляем размеры окна
        window_width = self.intro_window.winfo_width()
        window_height = self.intro_window.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (window_height // 2)
        self.intro_window.geometry(
            f"{window_width}x{window_height}+{x}+{y}")  #размер и расположение окна

    def start_game(self):
        """Метод для запуска основной игры."""
        self.intro_window.destroy()  # закрываем вступительное окно
        self.intro_window = None  # обнуляем ссылку на вступительное окно

        #основное окно
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.photo = None
        self.image_id = None

        self.title_label = tk.Label(self.root, font=("Arial", 24))
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')  # заголовок по центру сверху

        self.description_label = tk.Label(self.root, font=("Arial", 14), wraplength=400)
        self.description_label.place(relx=0.5, rely=0.1, anchor='center')  # описание по центру ниже заголовка

        self.take_button = tk.Button(self.root, text="Взять предмет", command=self.take_item, bg="pink",
                                     font=("Arial", 16), width=15)
        self.take_button.place(relx=0.5, rely=0.85, anchor='center')  # кнопка "Взять предмет"

        self.next_button = tk.Button(self.root, text="Далее", command=self.next_location, bg="lightblue",
                                     font=("Arial", 16), width=15)
        self.next_button.place(relx=0.5, rely=0.9, anchor='center')  # кнопка "Далее"

        self.update_location()

    @staticmethod
    def validate_image_path(path):
        """Проверка корректности пути к изображению."""
        if not isinstance(path, str) or not path.endswith(('.jpeg', '.jpg', '.png')):
            raise InvalidImagePathError(f"Некорректный путь к изображению: {path}")

    def validate_audio_path(path):
        """Проверка корректности пути к аудиофайлу."""
        valid_extensions = ('.mp3', '.wav', '.ogg')  # Добавьте другие расширения при необходимости

        # Проверка на корректный путь и существование файла
        if not isinstance(path, str) or not path.lower().endswith(valid_extensions) or not os.path.isfile(path):
            raise InvalidAudioPathError(f"Некорректный путь к аудиофайлу: {path}")

    def update_location(self):
        """Обновление информации о текущей локации."""
        location = self.locations[self.current_location]
        self.title_label.config(text=location["name"])
        self.description_label.config(text=location["description"])

        try:
            self.validate_image_path(location["image"])  #путь к изображению
            img = Image.open(location["image"])
            img_width, img_height = img.size

            #размер изображения
            img = img.resize((int(img_width), int(img_height)), Image.LANCZOS)

            self.photo = ImageTk.PhotoImage(img)

            #удаляем предыдущее изображение, если есть
            if self.image_id is not None:
                self.canvas.delete(self.image_id)

            # отображаем изображение
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # размер окна
            window_height = img_height + 150  # +150 пикселей для текста и кнопок
            window_width = img_width
            self.root.geometry(f"{window_width}x{window_height}")  # Устанавливаем размеры окна

            # центрируем окно
            x = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
            y = (self.root.winfo_screenheight() // 2) - (window_height // 2)
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

            self.root.update_idletasks()  # обновляем размер окна

            #музыка
            pygame.mixer.music.load(location["audio"])  #аудиофайл
            pygame.mixer.music.play(-1)  # воспроизводим музыку в цикле
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            messagebox.showerror("Ошибка", str(e))

    def take_item(self):
        """Обработчик для взятия предмета."""
        if self.item_window_open:  # проверяем, открыто ли окно
            return  # если открыто, выходим из метода

        self.item_window_open = True  # устанавливаем флаг, что окно открыто

        location = self.locations[self.current_location]
        item = location["item"]

        # создаем новое окно для показа предмета
        item_window = tk.Toplevel(self.root)
        item_window.title("Вы взяли предмет")

        item_label = tk.Label(item_window, text=f"Вы взяли {item['name']}!", font=("Arial", 16))
        item_label.pack()

        try:
            item_img = Image.open(item["image"])
            item_img = item_img.resize((200, 200), Image.LANCZOS)  #изменяем размер изображения предмета
            item_photo = ImageTk.PhotoImage(item_img)

            item_image_label = tk.Label(item_window, image=item_photo)
            item_image_label.image = item_photo  #сохраняем ссылку на изображение
            item_image_label.pack()
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Изображение предмета не найдено.")

        close_button = tk.Button(item_window, text="Закрыть", command=lambda: [item_window.destroy(), self.reset_item_window()])
        close_button.pack()

        # центрируем окно
        item_window.update_idletasks()  # обновляем размеры окна
        window_width = item_window.winfo_width()
        window_height = item_window.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (window_height // 2)
        item_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # устанавливаем размеры и расположение окна

    def reset_item_window(self):
        """Сбрасываем флаг, когда окно закрыто."""
        self.item_window_open = False

    def next_location(self):
        """Переход к следующей локации."""
        self.current_location += 1
        if self.current_location >= len(self.locations):
            messagebox.showinfo("Конец игры", "Вы посетили все места!")
            self
            self.root.quit()  # закрываем приложение
            return

        # останавливаем музыку, перед переходом к следующей локации
        pygame.mixer.music.stop()
        self.update_location()  # обновляем информацию о новой локации

