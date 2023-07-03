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
def add(uzer_input: str) -> str:
    text = uzer_input.split()
    if len(text) >= 4:
        rec = Record(Name(text[1].capitalize()), [Phone(text[2])], Birthday(text[3]))
        flag, text1 = adress_book.add_record(rec)
        if flag:
            return f"Контакт {text[1].capitalize()} з номером {[phone.value for phone in rec.phones]} та з Birthday {text[3]} створений" 
    elif len(text) > 2:
        rec = Record(Name(text[1].capitalize()), [Phone(text[2])])
        flag, text1 = adress_book.add_record(rec)
        if flag:
            return f"Контакт {text[1].capitalize()} з номером {[phone.value for phone in rec.phones]} створений" 
    else:
        rec = Record(Name(text[1].capitalize()), Phone())
        flag, text1 = adress_book.add_record(rec)
        if flag:
            return f"Контакт {text[1].capitalize()} без номера телефону створений" 
    
    return text1

# Додавання телефону до контакту
@input_error
def add_phone(uzer_input: str) -> str:
    text = uzer_input.split()
    rec = adress_book[text[2].capitalize()]
    rec.add_phone(Phone(text[3]))
    return f"До контакту {text[2].capitalize()} доданий новий телефон"

# Додає день народження 
@input_error
def add_birthday(uzer_input: str) -> str:
    text = uzer_input.split()
    rec = adress_book[text[2].capitalize()]
    rec.add_to_birthday(Birthday(text[3])) 
    return f"Birthday для {text[2].capitalize()} записаний"

# Заміна телефону A на телефон B 
@input_error
def change_phone(uzer_input: str) -> str:
    text = uzer_input.split()
    rec = adress_book[text[2].capitalize()]
    ret = f"{rec.name.value} : {[phone.value for phone in adress_book[rec.name.value].phones]}\n" + "Змінено на\n"
    rec.edit_phone(Phone(text[3]), Phone(text[4]))
    ret += f"{rec.name.value} : {[phone.value for phone in rec.phones]}"
    return ret

# Зупиняє роботу асистента.
@input_error
def exit_uzer(_):
    global flag_exit
    flag_exit = False
    return "Good bye!"
    
# Ассистент за ім'ям знаходить в контактах номер.
@input_error
def phone(uzer_input: str) -> str:
    text = uzer_input.split()
    rec = adress_book[text[1].capitalize()]
    try:
        return f"Номер телефону {text[1].capitalize()} це : {[phone.value for phone in rec.phones]}"
    except AttributeError:
        return f"До контакту {text[1].capitalize()} ще не додано номер телефону "

# Видаляє мобільний телефон
@input_error
def remove_phones(uzer_input: str) -> str:
    text = uzer_input.split()
    rec = adress_book[text[2].capitalize()]
    rec.remove_phone(Phone(text[3]))
    return f"Номер телефону {text[2].capitalize()} : {text[3]}\nВидалений"

# Показує скільки днів лишилося до дня народження
@input_error
def days_to_birthday(uzer_input: str):
    text = uzer_input.split()
    rec = adress_book[text[1].capitalize()]
    time = rec.days_to_birthday() 
    if len(time) < 10:
        return f"До контакту {text[1].capitalize()} не додано дату birthday"
    else:
        return f"До дня народження {text[1].capitalize()} залишолося {time}"
    
# Повертає сторінки книги контактів з кількістю N контактів на сторінці
@input_error
def show_page(uzer_input:str, count=5) -> None:
    n = 1
    text = uzer_input.split()
    if len(text) > 2:
        count = text[2]
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
@input_error
def helper(_):
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
@input_error
def hello(_):
    return "How can I help you?"

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
    "add" : add, # Додає контакт в книгу контактів +
    "add phone" : add_phone, # Додає номер телефону до контакту *
    "add birthday" : add_birthday, # Додає день народження *
    "birthday" : days_to_birthday, # Показує скільки днів лишилося до дня народження *
    "change phone": change_phone, # Заміна телефону A на телефон B *
    "close exit good bye" : exit_uzer, # Виходить з асистента *
    "hello": hello, # Виводить привітання *
    "help" : helper, # Пояснює команди та надає шаблони *
    "phone" : phone, # Виводить номер телефону за ім'ям *
    "remove phone" : remove_phones, # Видаляє телефон *
    "show page" : show_page # Виводить книгу контактів посторінково *
}

# Знаходить команду.
@input_error    
def handler(uzer_input: str):
    text = uzer_input.lower()
    if text in "close exit good bye":
        return COMMANDS["close exit good bye"]
 
    found_keywords = []
    for keyword in COMMANDS.keys():
        if text.find(keyword) != -1:
            found_keywords.append(keyword)
    comannds = list(filter(lambda x: len(x) == max(len(com) for com in found_keywords), found_keywords))
    return COMMANDS[comannds[0]]

@input_error
def main():
    while flag_exit: 
        uzer_input = input("-->")
        com = handler(uzer_input)
        print(com(uzer_input.lower()))

if __name__ == "__main__":
    main()