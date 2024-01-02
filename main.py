class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name):
        self.name = name
        self.contents = []


class FileSystem:
    def __init__(self, total_size=64 * 1024, block_size=512):
        self.total_size = total_size
        self.block_size = block_size
        self.free_space = total_size
        self.root = Directory('root')
        self.current_directory = self.root

    def create_file(self, name, size):
        if size > self.free_space:
            print("Недостаточно свободного места.")
            return

        if any(isinstance(item, File) and item.name == name for item in self.current_directory.contents):
            print(f"Файл с именем {name} уже существует в текущей директории.")
        else:
            file = File(name, size)
            self.current_directory.contents.append(file)
            self.free_space -= size
            print(f"Файл {name} успешно создан в текущей директории.")

    def delete_file(self, name):
        file = next((f for f in self.current_directory.contents if isinstance(f, File) and f.name == name), None)
        if file:
            self.current_directory.contents.remove(file)
            self.free_space += file.size
        else:
            print(f"Файл {name} не найден.")

    def copy_file(self, src_name, dest_name):
        src_file = next((f for f in self.current_directory.contents if isinstance(f, File) and f.name == src_name), None)
        if src_file:
            if src_file.size <= self.free_space:
                dest_file = File(dest_name, src_file.size)
                self.current_directory.contents.append(dest_file)
                self.free_space -= src_file.size
            else:
                print("Недостаточно свободного места для копирования.")
        else:
            print(f"Файл {src_name} не найден.")

    def move_file(self, src_name, directory):
        src_file = next((f for f in self.current_directory.contents if isinstance(f, File) and f.name == src_name), None)

        if src_file:
            dest_file = next((f for f in self.current_directory.contents if isinstance(f, File) and f.name == f"{directory}/{src_name}"), None)
            if dest_file is None:
                src_file.name = f"{directory}/{src_name}"
                print(f"Файл {src_name} успешно перемещен в {directory}.")
            else:
                print(f"Файл с именем {src_name} уже существует в директории - {directory}.")
        else:
            print(f"Файл {src_name} не найден.")

    def rename_file(self, old_name, new_name):
        file = next((f for f in self.current_directory.contents if isinstance(f, File) and f.name == old_name), None)
        if file:
            file.name = new_name
        else:
            print(f"Файл {old_name} не найден.")

    def display_contents(self):
        print("Содержимое текущей директории:")
        for item in self.current_directory.contents:
            if isinstance(item, File):
                print(f"Файл: {item.name}, Размер: {item.size} байт")
            elif isinstance(item, Directory):
                print(f"Директория: {item.name}")


fs = FileSystem()


while True:
    print("\n1. Создать файл")
    print("2. Удалить файл")
    print("3. Копировать файл")
    print("4. Переместить файл")
    print("5. Переименовать файл")
    print("6. Показать содержимое текущей директории")
    print("7. Выйти")

    choice = input("Выберите действие (1-7): ")

    if choice == '1':
        name = input("Введите имя файла: ")
        size = int(input("Введите размер файла (в байтах): "))
        fs.create_file(name, size)
    elif choice == '2':
        name = input("Введите имя файла для удаления: ")
        fs.delete_file(name)
    elif choice == '3':
        src_name = input("Введите имя файла для копирования: ")
        dest_name = input("Введите новое имя файла: ")
        fs.copy_file(src_name, dest_name)
    elif choice == '4':
        src_name = input("Введите имя файла для перемещения: ")
        directory = input("Введите директорию, в которую хотите переместить файл: ")
        fs.move_file(src_name, directory)
    elif choice == '5':
        old_name = input("Введите текущее имя файла: ")
        new_name = input("Введите новое имя файла: ")
        fs.rename_file(old_name, new_name)
    elif choice == '6':
        fs.display_contents()
    elif choice == '7':
        print("Программа завершена.")
        break
    else:
        print("Неверный выбор. Пожалуйста, введите число от 1 до 7.")
