from my_class import AddtextsBook, Record, Name, Phone, Birthday, IncorrectDateFormat, IncorrectPhoneeFormat


adress_book = AddtextsBook()
flag_exit = True

# Обробка помилок.
def input_error(func):
    def inner(*argsi,**kwargs): 
        try:
            return func(*argsi,**kwargs)
        except TypeError:
            return f"Wrong command"
        except IndexError:
            return f"Enter name and phone separated by a space!"
        except ValueError:
            return f"Incorrect data"
        except KeyError:
            return f"Enter another name."
        except AttributeError:
            return f"Enter command."
        except IncorrectDateFormat:
            return f"Incorrect date format"
        except IncorrectPhoneeFormat:
            return f"Incorrect phone format"
    return inner

# Асистент додає ім'я та номер телефону якщо є до книги контактів.
@input_error
def add(*args: str) -> str:
    name = Name(args[0].capitalize())
    phone = Phone(args[1]) if len(args) >= 2 else None
    birthday = Birthday(args[2]) if len(args) >= 3 else None
    rec = Record(name, phone, birthday)
    return adress_book.add_record(rec)

# Додавання телефону до контакту
@input_error
def add_phone(*args: str) -> str:
    rec = adress_book[args[0].capitalize()]
    return rec.add_phone(Phone(args[1]))

# Додає день народження 
@input_error
def add_birthday(*args: str) -> str:
    rec = adress_book[args[0].capitalize()]
    rec.add_to_birthday(Birthday(args[1])) 
    return f"Date of birth {args[0].capitalize()}, recorded"

# Заміна телефону A на телефон B 
@input_error
def change_phone(*args: str) -> str:
    rec = adress_book.get(args[0].capitalize())
    if rec:
        return rec.change_phone(Phone(args[1]), Phone(args[2]))
    return f"Contact wit name {args[0].capitalize()} doesn`t exist."

# Ассистент за ім'ям знаходить в контактах номер.
@input_error
def phone(*args: str) -> str:
    rec = adress_book[args[0].capitalize()]
    try:
        return f"Phone number {args[0].capitalize()} : {[phone.value for phone in rec.phones]}"
    except AttributeError:
        return f"No phone number added to {args[0].capitalize()} contact yet "

# Видаляє мобільний телефон
@input_error
def remove_phones(*args: str) -> str:
    rec = adress_book[args[0].capitalize()]
    rec.remove_phone(Phone(args[1]))
    return f"Phone number {args[0].capitalize()} : {args[1]}\nDeleted"

# Показує скільки днів лишилося до дня народження
@input_error
def days_to_birthday(*args: str):
    rec = adress_book[args[0].capitalize()]
    time = rec.days_to_birthday() 
    if not time:
        return f"Contact {args[0].capitalize()} has no stored date of birth"
    else:
        return f"To the bottom of the birth of {args[0].capitalize()} remained {time}"
    
# Повертає сторінки книги контактів з кількістю N контактів на сторінці
@input_error
def show_page(*args:str, count=5) -> None:
    n = 1
    if len(args) >= 1:
        count = args[0]
    c = adress_book.iterator(count)
    for _ in range(1000):
        try:
            text = next(c)
        except StopIteration:
            if n > 1 :
                return f"No more pages"
            else:
                return f"No saved contacts"
        stop = input(f"Page : {n}")
        if stop.lower() == "stop":
            return ""
        print(text)
        n += 1

# Пояснює команди та надає шаблони
def helper(*_):
    output = ""
    count = 0

    for k, v in COMMANDS_LIST.items():
        if count == 0:
            output += "{:^90}\n".format(" " + "_"*90 + " ")
        else:
            output += "{:^90}\n".format("|" + "_"*90 + "|")
        output += "|{:^90}|\n".format(f" COMMANDS - {k}")
        output += "{:^90}\n".format("|" + "_"*90 + "|")
        output += "|{:^90}|\n".format(v[0])
        output += "|{:^90}|\n".format(v[1])
        output += "{:^90}\n".format("|" + "_"*90 + "|")
        count += 1
    return output

# Асистент вітається у відповідь.
def hello(*_):
    return "How can I help you?"

# Зупиняє роботу асистента.
def exit_uzer(*_):
    global flag_exit
    flag_exit = False
    return "Good bye!"
    

# Список команд Help
COMMANDS_LIST = {
    "add" : ["Команда яка додає в книгу контактів:", "Команда(add) Ім'я(...) Телефон(...) День Народження(...)"], 
    "add phone" : ["Команда яка додає номер телефону до існуючого списку контактів:", "Команда(add phone) Ім'я(...) Телефон(...)"], 
    "add birthday" : ["Команда яка додає дату дня народження до існуючого списку контактів:", "Команда(add birthday) Ім'я(...) День Народження(...)"],
    "birthday" : ["Команда яка показує скільки залишилося до дня народження існуючого списку контактів:", "Команда(birthday) Ім'я(...)"], 
    "change phone": ["Команда яка замінює в книзі контактів неактуальний телефон:", "Команда(change phone) Ім'я(...) Неактуальний Телефон(...) Актуальний Телефон(...)"], 
    "close, exit, good bye" : ["Команди які закінчують роботу асистента", "Команда(close або exit вбо good bye)"],
    "hello": ["Команда привітання", "Команда(hello)"],
    "help" : ["Команда з прикладами команд", "Команда(help)"], 
    "phone" : ["Команда яка з книги контактів виводить номер телефону", "Команда(phone) Ім'я(...)"], 
    "remove phone" : ["Команда яка з книги контактів видаляє номер телефону", "Команда(remove phone) Ім'я(...) Телефон(...)"],
    "show page" : ["Команда яка виводить книгу контактів посторінково", "Команда(show page) Контактів на сторінці(...)"]
}

# Список команд.
COMMANDS = {
    add : ("add", ), # Додає контакт в книгу контактів *
    add_phone : ("add phone", ), # Додає номер телефону до контакту *
    add_birthday : ("add birthday", ), # Додає день народження *
    days_to_birthday : ("birthday", ), # Показує скільки днів лишилося до дня народження *
    change_phone: ("change phone", ), # Заміна телефону A на телефон B *
    exit_uzer : ("close", "exit", "good bye"), # Виходить з асистента *
    hello : ("hello", ), # Виводить привітання *
    helper : ("help", ), # Пояснює команди та надає шаблони *
    phone : ("phone", ), # Виводить номер телефону за ім'ям *
    remove_phones : ("remove phone", ), # Видаляє телефон *
    show_page : ("show page", ) # Виводить книгу контактів посторінково *
}

# Знаходить команду.
@input_error    
def handler(uzer_input: str):
    found_keywords = []
    for _, args_com in COMMANDS.items():
        for a_com in args_com:
            if uzer_input.lower().startswith(a_com):
                found_keywords.append(a_com)
    comannds = list(filter(lambda x: len(x) == max(len(com) for com in found_keywords), found_keywords))
    
    for command, kwds in COMMANDS.items():
        for kwd in kwds:
            if comannds[0].startswith(kwd) and len(comannds[0]) == len(kwd):
                return command, uzer_input[len(kwd):].strip().split()
    raise TypeError()


@input_error
def main():
    while flag_exit: 
        uzer_input = input("-->")
        com, data = handler(uzer_input)
        print(com, data)
        print(com(*data))

if __name__ == "__main__":
    main()