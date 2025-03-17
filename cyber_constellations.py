import cv2
import numpy as np
import random
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, colorchooser
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os

class CyberConstellationsApp:
    def __init__(self, root):
        # Инициализация основного окна приложения
        self.root = root
        self.root.title("Cyber Constellations Generator")
        self.root.configure(bg='#2b2b2b')  # Установка тёмного фона окна
        self.root.geometry("1200x800")     # Установка размера окна
        
        # Установка начального языка интерфейса (русский)
        self.language = "ru"
        
        # Словарь с текстами интерфейса на русском и английском
        self.texts = {
            "ru": {
                "title": "Генератор Киберсозвездий",
                "load_image": "Загрузить изображение",
                "load_font": "Загрузить шрифт",
                "color_settings": "Настройка цветов",
                "line_color": "Выбрать цвет линий",
                "box_color": "Выбрать цвет боксов",
                "text_color": "Выбрать цвет текста",
                "box_count": "Количество боксов:",
                "canvas_width": "Ширина канваса:",  # Текст для ширины канваса
                "canvas_height": "Высота канваса:",  # Текст для высоты канваса
                "gen_mode": "Режим генерации:",
                "overlay": "Простое наложение",
                "constellation": "Только созвездия",
                "scaling": "Масштабирование",
                "box_size": "Размер боксов:",
                "line_thickness": "Толщина линий:",
                "text_size": "Размер текста:",
                "contrast": "Контрастность",
                "line_contrast": "Контраст линий:",
                "box_contrast": "Контраст боксов:",
                "text_contrast": "Контраст текста:",
                "thickness": "Жирность",
                "box_thickness": "Жирность боксов:",
                "text_thickness": "Жирность текста:",
                "generate": "Генерировать созвездия",
                "save": "Сохранить результат",
                "font": "Шрифт:",
                "error": "Ошибка",
                "load_error": "Не удалось загрузить изображение: {}",
                "font_error": "Не удалось загрузить шрифт: {}",
                "no_image": "Сначала загрузите изображение",
                "gen_error": "Ошибка при генерации созвездий: {}",
                "save_warning": "Нет изображения для сохранения",
                "save_error": "Ошибка при сохранении: {}",
                "save_success": "Изображение сохранено"
            },
            "en": {
                "title": "Cyber Constellations Generator",
                "load_image": "Load Image",
                "load_font": "Load Font",
                "color_settings": "Color Settings",
                "line_color": "Choose Line Color",
                "box_color": "Choose Box Color",
                "text_color": "Choose Text Color",
                "box_count": "Number of Boxes:",
                "canvas_width": "Canvas Width:",  # Текст для ширины канваса
                "canvas_height": "Canvas Height:",  # Текст для высоты канваса
                "gen_mode": "Generation Mode:",
                "overlay": "Simple Overlay",
                "constellation": "Constellations Only",
                "scaling": "Scaling",
                "box_size": "Box Size:",
                "line_thickness": "Line Thickness:",
                "text_size": "Text Size:",
                "contrast": "Contrast",
                "line_contrast": "Line Contrast:",
                "box_contrast": "Box Contrast:",
                "text_contrast": "Text Contrast:",
                "thickness": "Thickness",
                "box_thickness": "Box Thickness:",
                "text_thickness": "Text Thickness:",
                "generate": "Generate Constellations",
                "save": "Save Result",
                "font": "Font:",
                "error": "Error",
                "load_error": "Failed to load image: {}",
                "font_error": "Failed to load font: {}",
                "no_image": "Load an image first",
                "gen_error": "Error generating constellations: {}",
                "save_warning": "No image to save",
                "save_error": "Error saving image: {}",
                "save_success": "Image saved"
            }
        }
        
        # Словарь встроенных шрифтов OpenCV для текста созвездий
        self.fonts = {
            "Simplex": cv2.FONT_HERSHEY_SIMPLEX,
            "Plain": cv2.FONT_HERSHEY_PLAIN,
            "Duplex": cv2.FONT_HERSHEY_DUPLEX,
            "Complex": cv2.FONT_HERSHEY_COMPLEX,
            "Triplex": cv2.FONT_HERSHEY_TRIPLEX,
            "Complex Small": cv2.FONT_HERSHEY_COMPLEX_SMALL,
            "Script Simplex": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            "Script Complex": cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        }
        self.selected_font = "Simplex"  # Начальный выбор шрифта
        self.custom_font = None         # Переменная для хранения пользовательского шрифта
        
        # Создание главного контейнера для размещения элементов интерфейса
        main_container = tk.Frame(self.root, bg='#2b2b2b')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Создание прокручиваемой панели управления слева
        self.control_canvas = tk.Canvas(main_container, bg='#2b2b2b', width=250, highlightthickness=0)
        self.control_scrollbar = tk.Scrollbar(main_container, orient="vertical", command=self.control_canvas.yview)
        self.control_frame = tk.Frame(self.control_canvas, bg='#2b2b2b')
        
        self.control_canvas.configure(yscrollcommand=self.control_scrollbar.set)
        self.control_canvas.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.control_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.control_canvas.create_window((0, 0), window=self.control_frame, anchor="nw")
        
        # Создание области для отображения изображения справа
        self.image_frame = tk.Frame(main_container, bg='#1e1e1e')
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.image_frame, bg='#1e1e1e')
        self.scrollbar_y = tk.Scrollbar(self.image_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.image_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(self.canvas, bg='#1e1e1e')
        self.canvas.create_window((0, 0), window=self.image_label, anchor="nw")
        
        # Переменные для хранения исходного и обработанного изображений
        self.original_image = None
        self.processed_image = None
        
        # Начальные цвета для линий, боксов и текста
        self.line_color = '#000000'  # Черный для линий
        self.box_color = '#00FF00'   # Зелёный для боксов
        self.text_color = '#000000'  # Черный для текста
        
        # Создание виджетов интерфейса и настройка событий прокрутки
        self.create_widgets()
        self.update_language()
        self.control_canvas.bind("<Configure>", self.on_control_frame_configure)
        self.control_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.control_canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.control_canvas.bind("<Button-5>", self.on_mouse_wheel)
        self.bind_scroll_to_widgets(self.control_frame)

    # Эта функция обновляет область прокрутки панели управления при изменении её размера
    def on_control_frame_configure(self, event):
        self.control_canvas.configure(scrollregion=self.control_canvas.bbox("all"))

    # Эта функция обрабатывает прокрутку колёсиком мыши в панели управления
    def on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.control_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.control_canvas.yview_scroll(1, "units")
        return "break"

    # Эта функция привязывает прокрутку колёсиком ко всем виджетам в панели управления
    def bind_scroll_to_widgets(self, widget):
        widget.bind("<MouseWheel>", self.on_mouse_wheel)
        widget.bind("<Button-4>", self.on_mouse_wheel)
        widget.bind("<Button-5>", self.on_mouse_wheel)
        for child in widget.winfo_children():
            self.bind_scroll_to_widgets(child)

    # Эта функция создаёт все виджеты интерфейса в заданном порядке
    def create_widgets(self):
        # 1. Режим генерации
        self.gen_mode_label = tk.Label(self.control_frame, bg='#2b2b2b', fg='white')
        self.gen_mode_label.pack(pady=5)
        self.generation_mode = tk.StringVar(value="simple_overlay")
        self.overlay_radio = tk.Radiobutton(self.control_frame, variable=self.generation_mode, value="simple_overlay", bg='#2b2b2b', fg='white', selectcolor='#404040')
        self.overlay_radio.pack()
        self.constellation_radio = tk.Radiobutton(self.control_frame, variable=self.generation_mode, value="constellation", bg='#2b2b2b', fg='white', selectcolor='#404040')
        self.constellation_radio.pack()

        # 2. Генерировать созвездия
        self.generate_button = tk.Button(self.control_frame, command=self.generate_constellations, bg='#404040', fg='white', padx=10, pady=5)
        self.generate_button.pack(pady=5, fill=tk.X)
        
        # 3. Сохранить результат
        self.save_button = tk.Button(self.control_frame, command=self.save_result, bg='#404040', fg='white', padx=10, pady=5)
        self.save_button.pack(pady=5, fill=tk.X)
        
        # 4. Загрузить изображение
        self.load_button = tk.Button(self.control_frame, command=self.load_image, bg='#404040', fg='white', padx=10, pady=5)
        self.load_button.pack(pady=5, fill=tk.X)
        
        # 5. Загрузить шрифт
        self.load_font_button = tk.Button(self.control_frame, command=self.load_font, bg='#404040', fg='white', padx=10, pady=5)
        self.load_font_button.pack(pady=5, fill=tk.X)
        
        # 6. Поменять шрифт (выбор шрифта из выпадающего списка)
        self.font_frame = tk.LabelFrame(self.control_frame, bg='#2b2b2b', fg='white')
        self.font_frame.pack(fill=tk.X, padx=5, pady=5)
        self.font_label = tk.Label(self.font_frame, bg='#2b2b2b', fg='white')
        self.font_label.pack(pady=2)
        self.font_var = tk.StringVar(value="Simplex")
        self.font_menu = ttk.Combobox(self.font_frame, textvariable=self.font_var, values=list(self.fonts.keys()), state="readonly")
        self.font_menu.pack(fill=tk.X, pady=2)
        self.font_menu.bind("<<ComboboxSelected>>", self.update_font)
        
        # 7. Поменять язык интерфейса
        self.lang_button = tk.Button(self.control_frame, text="EN/RU", command=self.toggle_language, bg='#404040', fg='white', padx=10, pady=5)
        self.lang_button.pack(pady=5, fill=tk.X)
        
        # 8. Настройка цветов
        self.color_frame = tk.LabelFrame(self.control_frame, bg='#2b2b2b', fg='white')
        self.color_frame.pack(fill=tk.X, padx=5, pady=5)
        self.line_color_btn = tk.Button(self.color_frame, command=lambda: self.choose_color('line'), bg='#404040', fg='white')
        self.line_color_btn.pack(fill=tk.X, pady=2)
        self.box_color_btn = tk.Button(self.color_frame, command=lambda: self.choose_color('box'), bg='#404040', fg='white')
        self.box_color_btn.pack(fill=tk.X, pady=2)
        self.text_color_btn = tk.Button(self.color_frame, command=lambda: self.choose_color('text'), bg='#404040', fg='white')
        self.text_color_btn.pack(fill=tk.X, pady=2)
        
        # 9. Количество боксов
        self.box_count_label = tk.Label(self.control_frame, bg='#2b2b2b', fg='white')
        self.box_count_label.pack(pady=5)
        self.box_count = tk.Scale(self.control_frame, from_=5, to=100, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.box_count.pack(fill=tk.X, pady=5)
        
        # Слайдеры и текстовые поля для изменения размера канваса при генерации без изображения
        self.canvas_width_label = tk.Label(self.control_frame, bg='#2b2b2b', fg='white')
        self.canvas_width_label.pack(pady=5)
        self.canvas_width = tk.Scale(self.control_frame, from_=200, to=2000, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.canvas_width.set(800)  # Значение по умолчанию для ширины
        self.canvas_width.pack(fill=tk.X, pady=5)
        self.canvas_width_entry = tk.Entry(self.control_frame, bg='#404040', fg='white', insertbackground='white')
        self.canvas_width_entry.insert(0, "800")  # Начальное значение в текстовом поле
        self.canvas_width_entry.pack(pady=2)
        self.canvas_width_entry.bind("<Return>", lambda event: self.update_canvas_width_from_entry())
        
        self.canvas_height_label = tk.Label(self.control_frame, bg='#2b2b2b', fg='white')
        self.canvas_height_label.pack(pady=5)
        self.canvas_height = tk.Scale(self.control_frame, from_=200, to=2000, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.canvas_height.set(600)  # Значение по умолчанию для высоты
        self.canvas_height.pack(fill=tk.X, pady=5)
        self.canvas_height_entry = tk.Entry(self.control_frame, bg='#404040', fg='white', insertbackground='white')
        self.canvas_height_entry.insert(0, "600")  # Начальное значение в текстовом поле
        self.canvas_height_entry.pack(pady=2)
        self.canvas_height_entry.bind("<Return>", lambda event: self.update_canvas_height_from_entry())
        
        # 10. Масштабирование
        self.scale_frame = tk.LabelFrame(self.control_frame, bg='#2b2b2b', fg='white')
        self.scale_frame.pack(fill=tk.X, padx=5, pady=5)
        self.box_size_label = tk.Label(self.scale_frame, bg='#2b2b2b', fg='white')
        self.box_size_label.pack(pady=2)
        self.box_scale = tk.Scale(self.scale_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.box_scale.set(1.0)
        self.box_scale.pack(fill=tk.X, pady=2)
        
        self.line_thickness_label = tk.Label(self.scale_frame, bg='#2b2b2b', fg='white')
        self.line_thickness_label.pack(pady=2)
        self.line_thickness = tk.Scale(self.scale_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.line_thickness.set(2)
        self.line_thickness.pack(fill=tk.X, pady=2)
        
        self.text_size_label = tk.Label(self.scale_frame, bg='#2b2b2b', fg='white')
        self.text_size_label.pack(pady=2)
        self.text_scale = tk.Scale(self.scale_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.text_scale.set(1.0)
        self.text_scale.pack(fill=tk.X, pady=2)
        
        # 11. Контрастность
        self.contrast_frame = tk.LabelFrame(self.control_frame, bg='#2b2b2b', fg='white')
        self.contrast_frame.pack(fill=tk.X, padx=5, pady=5)
        self.line_contrast_label = tk.Label(self.contrast_frame, bg='#2b2b2b', fg='white')
        self.line_contrast_label.pack(pady=2)
        self.line_contrast = tk.Scale(self.contrast_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.line_contrast.set(1.0)
        self.line_contrast.pack(fill=tk.X, pady=2)
        
        self.box_contrast_label = tk.Label(self.contrast_frame, bg='#2b2b2b', fg='white')
        self.box_contrast_label.pack(pady=2)
        self.box_contrast = tk.Scale(self.contrast_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.box_contrast.set(1.0)
        self.box_contrast.pack(fill=tk.X, pady=2)
        
        self.text_contrast_label = tk.Label(self.contrast_frame, bg='#2b2b2b', fg='white')
        self.text_contrast_label.pack(pady=2)
        self.text_contrast = tk.Scale(self.contrast_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.text_contrast.set(1.0)
        self.text_contrast.pack(fill=tk.X, pady=2)
        
        # 12. Жирность
        self.thickness_frame = tk.LabelFrame(self.control_frame, bg='#2b2b2b', fg='white')
        self.thickness_frame.pack(fill=tk.X, padx=5, pady=5)
        self.box_thickness_label = tk.Label(self.thickness_frame, bg='#2b2b2b', fg='white')
        self.box_thickness_label.pack(pady=2)
        self.box_thickness = tk.Scale(self.thickness_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.box_thickness.set(2)
        self.box_thickness.pack(fill=tk.X, pady=2)
        
        self.text_thickness_label = tk.Label(self.thickness_frame, bg='#2b2b2b', fg='white')
        self.text_thickness_label.pack(pady=2)
        self.text_thickness = tk.Scale(self.thickness_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg='#404040', fg='white')
        self.text_thickness.set(2)
        self.text_thickness.pack(fill=tk.X, pady=2)

    # Эта функция обновляет ширину канваса из текстового поля
    def update_canvas_width_from_entry(self):
        try:
            value = int(self.canvas_width_entry.get())
            if 200 <= value <= 2000:
                self.canvas_width.set(value)
            else:
                messagebox.showerror(self.texts[self.language]["error"], "Ширина канваса должна быть от 200 до 2000")
        except ValueError:
            messagebox.showerror(self.texts[self.language]["error"], "Введите корректное число для ширины")

    # Эта функция обновляет высоту канваса из текстового поля
    def update_canvas_height_from_entry(self):
        try:
            value = int(self.canvas_height_entry.get())
            if 200 <= value <= 2000:
                self.canvas_height.set(value)
            else:
                messagebox.showerror(self.texts[self.language]["error"], "Высота канваса должна быть от 200 до 2000")
        except ValueError:
            messagebox.showerror(self.texts[self.language]["error"], "Введите корректное число для высоты")

    # Эта функция переключает язык интерфейса между русским и английским
    def toggle_language(self):
        self.language = "en" if self.language == "ru" else "ru"
        self.update_language()

    # Эта функция обновляет текст всех виджетов в зависимости от выбранного языка
    def update_language(self):
        t = self.texts[self.language]
        self.root.title(t["title"])
        self.load_button.config(text=t["load_image"])
        self.load_font_button.config(text=t["load_font"])
        self.generate_button.config(text=t["generate"])
        self.save_button.config(text=t["save"])
        self.lang_button.config(text="EN/RU")
        self.color_frame.config(text=t["color_settings"])
        self.line_color_btn.config(text=t["line_color"])
        self.box_color_btn.config(text=t["box_color"])
        self.text_color_btn.config(text=t["text_color"])
        self.box_count_label.config(text=t["box_count"])
        self.canvas_width_label.config(text=t["canvas_width"])  # Обновление текста для ширины канваса
        self.canvas_height_label.config(text=t["canvas_height"])  # Обновление текста для высоты канваса
        self.gen_mode_label.config(text=t["gen_mode"])
        self.overlay_radio.config(text=t["overlay"])
        self.constellation_radio.config(text=t["constellation"])
        self.scale_frame.config(text=t["scaling"])
        self.box_size_label.config(text=t["box_size"])
        self.line_thickness_label.config(text=t["line_thickness"])
        self.text_size_label.config(text=t["text_size"])
        self.contrast_frame.config(text=t["contrast"])
        self.line_contrast_label.config(text=t["line_contrast"])
        self.box_contrast_label.config(text=t["box_contrast"])
        self.text_contrast_label.config(text=t["text_contrast"])
        self.thickness_frame.config(text=t["thickness"])
        self.box_thickness_label.config(text=t["box_thickness"])
        self.text_thickness_label.config(text=t["text_thickness"])
        self.font_frame.config(text=t["font"])
        self.font_label.config(text=t["font"])

    # Эта функция обновляет выбранный шрифт из выпадающего списка
    def update_font(self, event=None):
        self.selected_font = self.font_var.get()
        self.custom_font = None  # Сбрасывает пользовательский шрифт при выборе встроенного

    # Эта функция позволяет загрузить пользовательский шрифт из файла (.ttf или .otf)
    def load_font(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf *.otf"), ("All files", "*.*")])
            if not file_path:
                return
            self.custom_font = ImageFont.truetype(file_path, size=20)
            self.selected_font = None
            self.font_var.set(os.path.basename(file_path))
        except Exception as e:
            messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["font_error"].format(str(e)))

    # Эта функция открывает диалог выбора цвета для линий, боксов или текста
    def choose_color(self, color_type):
        color = colorchooser.askcolor(title=f"Choose color for {color_type}")[1]
        if color:
            if color_type == 'line':
                self.line_color = color
            elif color_type == 'box':
                self.box_color = color
            elif color_type == 'text':
                self.text_color = color

    # Эта функция преобразует цвет из HEX-формата в RGB для OpenCV
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Эта функция загружает изображение из файла и отображает его
    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")])
            if not file_path:
                return
            pil_image = Image.open(file_path)
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')  # Конвертация RGBA в RGB
            img_array = np.array(pil_image)
            if img_array is None or img_array.size == 0:
                raise ValueError("Failed to convert image to array")
            self.original_image = img_array
            self.display_image(self.original_image)
        except Exception as e:
            messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["load_error"].format(str(e)))

    # Эта функция отображает изображение в правой части интерфейса с поддержкой масштабирования
    def display_image(self, image):
        if image is None or image.size == 0:
            return
        try:
            pil_image = Image.fromarray(image)
            max_size = (1000, 800)
            pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)  # Уменьшение изображения до заданного размера
            photo = ImageTk.PhotoImage(pil_image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.canvas.configure(scrollregion=(0, 0, pil_image.width, pil_image.height))
        except Exception as e:
            messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["load_error"].format(str(e)))

    # Эта функция запускает процесс генерации созвездий на изображении или пустом фоне с заданным размером канваса
    def generate_constellations(self):
        if self.generation_mode.get() == "constellation":
            # Использование значений слайдеров (или текстовых полей) для ширины и высоты в режиме "Только созвездия"
            width = self.canvas_width.get()
            height = self.canvas_height.get()
            self.original_image = None
        else:
            if self.original_image is None:
                messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["no_image"])
                return
            height, width = self.original_image.shape[:2]  # Размер загруженного изображения
        try:
            result = self.create_constellation(width, height)
            self.processed_image = result
            self.display_image(result)
        except Exception as e:
            messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["gen_error"].format(str(e)))

    # Эта функция создаёт созвездия: линии, боксы и текст на изображении или пустом канвасе
    def create_constellation(self, width, height):
        if self.generation_mode.get() == "simple_overlay" and self.original_image is not None:
            result = np.copy(self.original_image)  # Копия загруженного изображения для наложения
        else:
            result = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)  # Белый фон для режима "Только созвездия" с заданным размером

        points = []
        num_points = self.box_count.get()  # Количество точек (боксов) из слайдера
        for _ in range(num_points):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            points.append((x, y))

        # Рисование линий между точками
        for i in range(len(points)-1):
            cv2.line(result, points[i], points[i+1], self.hex_to_rgb(self.line_color), self.line_thickness.get())

        # Рисование боксов вокруг точек
        box_size = int(min(width, height) // 50 * self.box_scale.get())
        for x, y in points:
            cv2.rectangle(result, (x - box_size, y - box_size), (x + box_size, y + box_size), 
                         self.hex_to_rgb(self.box_color), self.box_thickness.get())

        # Добавление текста над боксами
        font_size = self.text_scale.get() * (min(width, height) / 1000)
        if self.custom_font:
            pil_image = Image.fromarray(result)
            draw = ImageDraw.Draw(pil_image)
            for x, y in points:
                text = random.choice(["BDSM_brain", "chemical=anthropoids", "tragedy-ROM", "retro-ADAM", "vital=plug-in", 
    "ultra=machinary", "violence_zone", "techno-junkies", "hyperlinks", "virus_accelerates",
    "respiration-byte", "flesh-modules", "acid_screams", "hydromania", "murder-protocol",
    "cold-blooded_disease", "artificial_sun", "chromosomal_aberration", "soul/gram",
    "terror_fear=cells", "drug_embryo", "digital=vamped", "cadaver_feti=PLAY", "acidHUMANIX",
    "data=mutant", "FUCKNAM_gene=TV", "dogs_systems", "hallucination_molecule",
    "chloroform_larvas", "clone-dive", "internal_organ_medium", "spiral_mechanism",
    "chemical_tragedy-ROM", "parasite_guy", "hyperreal_existence-code", "BDSM_state_script",
    "boy_roid_nature", "LEVEL_0", "DNA=channels", "insanity_medium", "genomics_screen-saver",
    "cadaver_feti=mode", "surrender_gimmick", "cruel=emulators", "human_body_pill",
    "cyber_quality", "murderous_intention", "density_0", "skizophysical_escape",
    "eyeball_device", "reptilian_form", "HYPE_acid_PLAY", "suicide_space", "tragedy-ROM",
    "techno-junkies'_trash", "softwarable_BDSM", "SAVE_icon", "terror_fear=cells",
    "modem=heart", "acid_existence-code", "cadaver_mechanism", "script_monitor_screen",
    "murder-browser", "non-resettable_murder-browser", "technocrisis", "cadaver_feti_existence-code",
    "BDSM_planet", "nightmare_abolition_circuit", "desire-protocol", "murder_region",
    "HDD_murder_region", "surrender-site", "brain_universe", "acid_murder_nature",
    "spherical_condition_script", "chemical=anthropoid_acid", "state=monitor_screens",
    "internal_organ_consciousness", "genomics_cyber_crime", "FUCKNAM=vaio-code",
    "hybrid_modem=heart", "hydromaniac_existence-code", "3D_HYPE_thread",
    "internal_organ_medium", "murder_protocol", "cadaver_mechanism", "retro-ADAM_genome",
    "crime_space", "cyber_quality_system", "HYPE_vaio-code", "BDSM_screen-saver",
    "neuromatic_cadaver", "acidHUMANIX_circuit", "sensor_techno-junkies", "nightmare_continent",
    "reptilian_script", "acidHUMANIX_vaio-code", "chromosomal_screams", "hunting_grotesque",
    "eyeball_hypervirus", "mutation_organism", "gene_TV", "chromosome_parasite",
    "synthetic_prosthetic", "erased_mindware", "hacked_bioform", "Umwelt", "Qualia", "Autopoiesis", "Cybernetica", "Sententia", "Noogenesis", "Technognosis", "Mindware", "Epiphenom", 
    "Neurotica", "Cognitron", "Perceptum", "Sentinum", "Exogramma", "Machinatio", "Neuralis", "Cogitex", "Somatium", "Eidolon", 
    "Substratum", "Syntellect", "Intellectum", "Mentifex", "Neurograph", "Cyberium", "Virtuosis", "Exocortex", "Cogitatus", 
    "Techneidos", "Memetica", "Psybernetica", "Infomorph", "Neomem", "Cyborgium", "Datagnosis", "Mindflux", "Biognosis", 
    "Pansentia", "Neurophage", "Cogitron", "Automnemon", "Machinamentum", "Logisoma", "Autognosis", "Sensomorph", "Noologica", 
    "Noosphericum", "Psybertrix", "Technosoma", "Cyberdaemon", "Synthosentia", "Noomorph", "Neurontis", "Sapientum", "Mentem", 
    "Cogitanda", "Perceptica", "Infocortex", "Machinorum", "Eidomatrix", "Datacogito", "Cyberethos", "Sentiograph", "Cyberlogos", 
    "Neomnesia", "Exocognit", "Egoformat", "Neurothesis", "Cogitoform", "Psyberia", "Technoesis", "Cyberphren", "Omnicortex", 
    "Logisentis", "Somniphorm", "Memetron", "Neurofactum", "Autognitio", "Hypermentis", "Cogitaris", "Nooformat", "Informatum", 
    "Neurolexis", "Sentiomech", "Cybermorph", "Intellecta", "Omnipsyche", "Neuralum", "Neomind", "Cogitrix", "PerceptumX", 
    "Psyberstate", "Cyberflux", "Infomatrix", "Dataphren", "Cybernoia", "Nootronic", "Neurosentia", "Exosentis", "Synthognos", 
    "Cyberion", "Nooframe"])
                text_color_rgb = self.hex_to_rgb(self.text_color)
                font = self.custom_font.font_variant(size=int(font_size * 20))
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_w = text_bbox[2] - text_bbox[0]
                text_h = text_bbox[3] - text_bbox[1]
                text_pos = (x - text_w // 2, y - box_size - text_h - 10)
                draw.text(text_pos, text, fill=text_color_rgb, font=font)
            result = np.array(pil_image)
        else:
            for x, y in points:
                text = random.choice(["BDSM_brain", "chemical=anthropoids", "tragedy-ROM", "retro-ADAM", "vital=plug-in", 
    "ultra=machinary", "violence_zone", "techno-junkies", "hyperlinks", "virus_accelerates",
    "respiration-byte", "flesh-modules", "acid_screams", "hydromania", "murder-protocol",
    "cold-blooded_disease", "artificial_sun", "chromosomal_aberration", "soul/gram",
    "terror_fear=cells", "drug_embryo", "digital=vamped", "cadaver_feti=PLAY", "acidHUMANIX",
    "data=mutant", "FUCKNAM_gene=TV", "dogs_systems", "hallucination_molecule",
    "chloroform_larvas", "clone-dive", "internal_organ_medium", "spiral_mechanism",
    "chemical_tragedy-ROM", "parasite_guy", "hyperreal_existence-code", "BDSM_state_script",
    "boy_roid_nature", "LEVEL_0", "DNA=channels", "insanity_medium", "genomics_screen-saver",
    "cadaver_feti=mode", "surrender_gimmick", "cruel=emulators", "human_body_pill",
    "cyber_quality", "murderous_intention", "density_0", "skizophysical_escape",
    "eyeball_device", "reptilian_form", "HYPE_acid_PLAY", "suicide_space", "tragedy-ROM",
    "techno-junkies'_trash", "softwarable_BDSM", "SAVE_icon", "terror_fear=cells",
    "modem=heart", "acid_existence-code", "cadaver_mechanism", "script_monitor_screen",
    "murder-browser", "non-resettable_murder-browser", "technocrisis", "cadaver_feti_existence-code",
    "BDSM_planet", "nightmare_abolition_circuit", "desire-protocol", "murder_region",
    "HDD_murder_region", "surrender-site", "brain_universe", "acid_murder_nature",
    "spherical_condition_script", "chemical=anthropoid_acid", "state=monitor_screens",
    "internal_organ_consciousness", "genomics_cyber_crime", "FUCKNAM=vaio-code",
    "hybrid_modem=heart", "hydromaniac_existence-code", "3D_HYPE_thread",
    "internal_organ_medium", "murder_protocol", "cadaver_mechanism", "retro-ADAM_genome",
    "crime_space", "cyber_quality_system", "HYPE_vaio-code", "BDSM_screen-saver",
    "neuromatic_cadaver", "acidHUMANIX_circuit", "sensor_techno-junkies", "nightmare_continent",
    "reptilian_script", "acidHUMANIX_vaio-code", "chromosomal_screams", "hunting_grotesque",
    "eyeball_hypervirus", "mutation_organism", "gene_TV", "chromosome_parasite",
    "synthetic_prosthetic", "erased_mindware", "hacked_bioform", "Umwelt", "Qualia", "Autopoiesis", "Cybernetica", "Sententia", "Noogenesis", "Technognosis", "Mindware", "Epiphenom", 
    "Neurotica", "Cognitron", "Perceptum", "Sentinum", "Exogramma", "Machinatio", "Neuralis", "Cogitex", "Somatium", "Eidolon", 
    "Substratum", "Syntellect", "Intellectum", "Mentifex", "Neurograph", "Cyberium", "Virtuosis", "Exocortex", "Cogitatus", 
    "Techneidos", "Memetica", "Psybernetica", "Infomorph", "Neomem", "Cyborgium", "Datagnosis", "Mindflux", "Biognosis", 
    "Pansentia", "Neurophage", "Cogitron", "Automnemon", "Machinamentum", "Logisoma", "Autognosis", "Sensomorph", "Noologica", 
    "Noosphericum", "Psybertrix", "Technosoma", "Cyberdaemon", "Synthosentia", "Noomorph", "Neurontis", "Sapientum", "Mentem", 
    "Cogitanda", "Perceptica", "Infocortex", "Machinorum", "Eidomatrix", "Datacogito", "Cyberethos", "Sentiograph", "Cyberlogos", 
    "Neomnesia", "Exocognit", "Egoformat", "Neurothesis", "Cogitoform", "Psyberia", "Technoesis", "Cyberphren", "Omnicortex", 
    "Logisentis", "Somniphorm", "Memetron", "Neurofactum", "Autognitio", "Hypermentis", "Cogitaris", "Nooformat", "Informatum", 
    "Neurolexis", "Sentiomech", "Cybermorph", "Intellecta", "Omnipsyche", "Neuralum", "Neomind", "Cogitrix", "PerceptumX", 
    "Psyberstate", "Cyberflux", "Infomatrix", "Dataphren", "Cybernoia", "Nootronic", "Neurosentia", "Exosentis", "Synthognos", 
    "Cyberion", "Nooframe"])
                (text_w, text_h), _ = cv2.getTextSize(text, self.fonts[self.selected_font], font_size, self.text_thickness.get())
                text_pos = (x - text_w // 2, y - box_size - 10)
                cv2.putText(result, text, text_pos, self.fonts[self.selected_font], 
                           font_size, self.hex_to_rgb(self.text_color), self.text_thickness.get())

        return result

    # Эта функция сохраняет обработанное изображение в файл
    def save_result(self):
        if self.processed_image is None:
            messagebox.showwarning(self.texts[self.language]["error"], self.texts[self.language]["save_warning"])
            return
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if not file_path:  # Проверка на пустой путь
                return  # Если пользователь отменил выбор, просто выходим
            result_bgr = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR)  # Конвертация RGB в BGR для OpenCV
            success = cv2.imwrite(file_path, result_bgr)  # Сохраняем и проверяем результат
            if success:
                messagebox.showinfo(self.texts[self.language]["save_success"], self.texts[self.language]["save_success"])
            else:
                raise Exception("Не удалось записать файл (возможно, проблема с путем или правами доступа)")
        except Exception as e:
            messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["save_error"].format(str(e)))

# Запуск приложения   
if __name__ == "__main__":
    root = tk.Tk()
    app = CyberConstellationsApp(root)
    root.mainloop()