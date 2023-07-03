import re
from collections import UserDict
from datetime import datetime


class AddtextsBook(UserDict):
    
    def add_record(self, record):
        if record.name.value not in self.keys():
            self.data[record.name.value] = record
            return (True, " ")
        else:
            return (False, "Name already exist. Try add phone command for add extra phone.")
    
    def iterator(self, num:int) -> str:
        result = self.create_page(num)
        if result == None:
            return "No saved contacts"
        for _, value in result.items():
            yield value

    def create_page(self, num:int) -> dict|None:

        if len(self.data) == 0:
            return None
        result_list = {}
        count = 1
        page = 1

        new_list1 = []
        for i in self.data.values():
            value_birthday = "No birthday date"
            name_value = f"Name : {i.name.value} "
            phone_value = f" {[el.value for el in i.phones]}"
            birthday_value = f"Birthday {i.birthday.value if i.birthday else value_birthday}"
            
            new_list = [name_value, phone_value, birthday_value]
            new_list1.append(new_list)
            count += 1
            if count == int(num):
                result_list[page] = self.create_print_page(page, new_list1)
                new_list1.clear()
                page += 1
                count = 0

        result_list[page] = self.create_print_page(page, new_list1)

        return result_list

    def create_print_page(self, page:int, contacts:list) -> str:
        result = ""
        n = 12

        pattern = r"[\[\'\'\"\"\]]"  # видаляємо зайве
        if page > 9:
            n = 11

        elif page > 99:
            n = 10

        result += " {:^90}".format(" "*31 + "_"*30 + " "*29) + "\n"
        result += " {:^92}".format("|" + " "*n +f"Page {page}" + " "*12 + "|") + "\n"
        result += " {:<90}".format(" "*30 + "|" + "_"*30 + "|" + " "*29) + "\n"

        for i in range(0, len(contacts)):
            name_value, phone_value, birthday_value = contacts[i]
            p = phone_value.split(",")
            count = 1 

            if len(p) > 1:
                for iii in p:
                    new_i = re.sub(pattern, "", iii)
                    if count == 1 and i == 0:
                        result += " {:^90}".format("_"*92) + "\n"
                        result += "| {:<29}| {:<29}| {:<29}|".format(name_value, f"Phone {count} :{new_i}", birthday_value) + "\n"
                    else:
                        result += "| {:<29}| {:<29}| {:<29}|".format("", f"Phone {count} :{new_i}", "") + "\n"
                    count += 1
            
            else:
                new_i = re.sub(pattern, "", phone_value)
                if i == 0:
                    result += " {:^90}".format("_"*92) + "\n"
                else:
                    result += "{:^90}".format("|" + "_"*30 +"|"+ "_"*30 +"|"+ "_"*30 +"|") + "\n"
                result += "| {:<29}| {:<29}| {:<29}|".format(name_value, f"Phone {count} :{new_i}", birthday_value) + "\n"
        
        result += "{:^90}".format("|" + "_"*30 +"|"+ "_"*30 +"|"+ "_"*30 +"|") + "\n"
        return result


class Field:

    def __init__(self, value=None):
        self.__value = None
        self.value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value:
            self.__value = value
    
    def __repr__(self) -> str:
        return f"{self.__value}"


class Name(Field):
    pass
    

class Phone(Field):

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value:
            correct_phone = ""
            for i in value: 
                if i in "+0123456789":
                    correct_phone += i
            if len(correct_phone) == 13:    
                self.__value = correct_phone # "+380123456789"
            elif len(correct_phone) == 12: 
                self.__value = "+" + correct_phone # "380123456789"
            elif len(correct_phone) == 10: 
                self.__value = "+38" + correct_phone # "0123456789"
            elif len(correct_phone) == 9:
                self.__value = "+380" + correct_phone # "123456789"
            else:
                raise IncorrectPhoneeFormat
        else:
            self.__value = "No Phone"
            

class Birthday(Field):

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        today = datetime.now()
        birthday = datetime.strptime(value, r'%Y-%m-%d')
    
        if type(today) == type(birthday):
            self.__value = birthday 
        else:
            raise IncorrectDateFormat
    

class Record:

    def __init__(self, name: str, phones=None, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if birthday:
            self.add_to_birthday(birthday)
        if type(phones) == list:
            self.phones.extend(phones)
        else:
            self.phones.append(phones)

    # Додає номер 
    def add_phone(self, phones: Phone) -> None:
        print(phones.value)
        if phones.value not in [phones.value for phones in self.phones]:
            if "No Phone" in [phones.value for phones in self.phones]:
                self.phones[0] = phones
            else:
                self.phones.append(phones)
        else:
            return f"This phone already added."

    # Видаляє номер 
    def remove_phone(self, phones: Phone) -> None:
        for n in self.phones:
            if n.value == phones.value:
                self.phones.remove(n)

    # Заміна номера А на номер Б
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        if old_phone.value == new_phone.value or new_phone.value in [phone.value for phone in self.phones]:
            return f"This phone alredy exist!"
        elif old_phone.value not in [phone.value for phone in self.phones]:
            return f"This phone not found!"
        else:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
            return f"Phone changed."

    # Додає birthday
    def add_to_birthday(self, birthday: Birthday) -> None:
        self.birthday = birthday

    # Виводить залишок до дня народження певної людини 
    def days_to_birthday(self) -> str|None:
        try:
            date_birthday = self.birthday.value
        except AttributeError:
            return None
        current_datetime = datetime.now()
        new_date = date_birthday.replace(year=current_datetime.year)
        days_birthday = new_date - current_datetime

        hours = int(days_birthday.seconds // 3600)
        minutes = int((days_birthday.seconds % 3600) // 60)
        seconds = int(days_birthday.seconds % 60)

        if days_birthday.days >= 0:
            return f"{days_birthday.days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        
        else:
            date = date_birthday.replace(year=current_datetime.year+1)
            days_birthday = date - current_datetime
            return f"{days_birthday.days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


class IncorrectDateFormat(Exception):
    pass


class IncorrectPhoneeFormat(Exception):
    pass