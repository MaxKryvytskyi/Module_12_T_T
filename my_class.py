import re
from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value=None):
        self.__value = None
        self.value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value:str):
        if value: self.__value = value
    
    def __str__(self):
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
    
    # def __eq__(self, other:object) -> bool:
    #     return self.value == other.value


class Name(Field):
    pass
    

class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str) -> None:
        if value:
            correct_phone = ""
            for i in value: 
                if i in "+0123456789": correct_phone += i

            if len(correct_phone) == 13: self.__value = correct_phone # "+380123456789"
            elif len(correct_phone) == 12: self.__value = "+" + correct_phone # "380123456789"
            elif len(correct_phone) == 10: self.__value = "+38" + correct_phone # "0123456789"
            elif len(correct_phone) == 9: self.__value = "+380" + correct_phone # "123456789"
            else: raise IncorrectPhoneeFormat


class Birthday(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value:str) -> None:
        today = datetime.now()
        birthday = datetime.strptime(value, r'%d-%m-%Y')
    
        if type(today) == type(birthday): self.__value = birthday 
        else: raise IncorrectDateFormat
    

class Record:
    def __init__(self, name:Name, phone: Phone=None, birthday: Birthday=None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        if birthday: self.add_to_birthday(birthday)
        if phone: self.phones.append(phone)

    # Додає номер 
    def add_phone(self, phones:Phone) -> str:
        if len(self.phones) < 9:
            if phones not in self.phones:
                self.phones.append(phones)
                return f"Phone {phones} add to contact {self.name}"
            return f"The contact {self.name} already has the phone {phones}"
        else: 
            return f"The limit of phones is 9"
        
    # Видаляє номер 
    def remove_phone(self, phones:Phone) -> None:
        if len(self.phones) == 0:
            return "This contact has no phone numbers saved"
        for n in self.phones:
            if n.value == phones.value: 
                self.phones.remove(n)
                return phones

    # Заміна номера А на номер Б
    def change_phone(self, old_phone:Phone, new_phone:Phone) -> str:
        for phones in self.phones:
            if str(old_phone) == str(phones):
                self.remove_phone(old_phone)
                self.add_phone(new_phone)
                return f"Phone {old_phone} change to {new_phone} for {self.name} contact "
        return f"Phone {old_phone} for contact {self.name} doesn`t exist"
        
    # Відмаловує телефони певного контакту 
    def phone_print(self, name: Name, phones: Phone) -> str:
        result = ""
        
        dict_phone = {"Phone 1" : "", "Phone 2" : "", "Phone 3" : "", 
                      "Phone 4" : "", "Phone 5" : "", "Phone 6" : "", 
                      "Phone 7" : "", "Phone 8" : "", "Phone 9" : ""}

        for n, v in enumerate(phones):
            dict_phone[f"Phone {n+1}"] = v

        result += " {:^90}".format(" "*31 + "_"*30 + " "*29) + "\n"
        result += "{:<31}|{:^30}|{:>30}".format("", f"{name} Phones","") + "\n"
        result += " {:<90}".format(" "*30 + "|" + "_"*30 + "|" + " "*29) + "\n"

        if len(phones) > 0:
            result += " {:^91}".format("_"*91) + "\n"
            result += "|{:^30}|{:^30}|{:^29}|".format("Phone 1", f"Phone 2","Phone 3") + "\n"
            result += "|{:^30}|{:^30}|{:^29}|".format(str(dict_phone["Phone 1"]), str(dict_phone["Phone 2"]), str(dict_phone["Phone 3"])) + "\n"
            result += "|{:<30}|{:^30}|{:>28}|".format("_"*30, "_"*30, "_"*29) + "\n"

        if len(phones) > 3:
            result += " {:^91}".format("_"*91) + "\n"
            result += "|{:^30}|{:^30}|{:^29}|".format("Phone 4", f"Phone 5", "Phone 6") + "\n"
            result += "|{:^30}|{:^30}|{:^29}|".format(str(dict_phone["Phone 4"]), str(dict_phone["Phone 5"]), str(dict_phone["Phone 6"])) + "\n"
            result += "|{:<30}|{:^30}|{:>28}|".format("_"*30, "_"*30, "_"*29) + "\n"

        if len(phones) > 6:
            result += " {:^91}".format("_"*91) + "\n"
            result += "|{:^30}|{:^30}|{:^29}|".format("Phone 7", f"Phone 8","Phone 9") + "\n"
            result += "|{:^30}|{:^30}|{:^29}|".format(str(dict_phone["Phone 7"]), str(dict_phone["Phone 8"]), str(dict_phone["Phone 9"])) + "\n"
            result += "|{:<30}|{:^30}|{:>28}|".format("_"*30, "_"*30, "_"*29) + "\n"

        if len(phones) != 0: return f"{result}"
        else: return f"No phone number added to {name} contact yet "


    # Додає birthday
    def add_to_birthday(self, birthday:Birthday) -> None:
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

    def __str__(self):
        return "{}{}{}".format(self.name, " " + ", ".join([str(p) for p in self.phones]) if self.phones else "", 
                               " " + f"{self.birthday.value.strftime('%d-%m-%Y') if self.birthday else ''}")


class IncorrectDateFormat(Exception):
    pass


class IncorrectPhoneeFormat(Exception):
    pass


class AddtextsBook(UserDict):
    # Додає в словник экземпляр классу Record
    def add_record(self, record: Record) -> str:
        if record.name.value not in self.keys():
            self.data[record.name.value] = record
            t = str(record) + " "
            return f"{t}add successful"
        else:
            return f"Contact with name {record.name} already exist. Try add phone command for add extra phone."

    # Ітерується за книгою контактів
    def iterator(self, num:int) -> str:
        result = self.create_page(num)
        if result == None: return "No saved contacts"
        for _, value in result.items():
            yield value

    # Розбиває книгу контактів посторінково 
    def create_page(self, num:int) -> dict|None:

        if len(self.data) == 0: return None
        result_list = {}
        count = 1
        page = 1

        new_list1 = []
        for i in self.data.values():
            value_birthday = "No birthday date"
            name_value = f"{i.name.value} "
            phone_value = f" {[el.value for el in i.phones]}"
            birthday_value = f"{i.birthday.value.strftime('%d-%m-%Y') if i.birthday else value_birthday}"
            
            new_list = [name_value, phone_value, birthday_value]
            new_list1.append(new_list)
            if count == int(num):
                result_list[page] = self.create_print_page(page, new_list1, True)
                new_list1.clear()
                page += 1
                count = 0
            count += 1

        result_list[page] = self.create_print_page(page, new_list1, True)

        return result_list

    # Записує книгу контактів посторінково для виводу в консоль 
    def create_print_page(self, page:int, contacts:list, flag:bool) -> str:
        result = ""
        n = 12
        pattern = r"[\[\'\'\"\"\]]"  # видаляємо зайве
        if page > 9: n = 11
        elif page > 99: n = 10
        if contacts:
            if flag:
                x = "Page" 
                result += " {:^90}".format(" "*31 + "_"*30 + " "*29) + "\n"
                result += " {:^92}".format("|" + " "*n +f"{x} {page}" + " "*12 + "|") + "\n"
                result += " {:<90}".format(" "*30 + "|" + "_"*30 + "|" + " "*29) + "\n"
            else:
                x = "Coincidence"
                result += " {:^90}".format(" "*31 + "_"*30 + " "*29) + "\n"
                result += " {:^92}".format("|" + " "*(n-4) +f"{page} {x}" + " "*9 + "|") + "\n"
                result += " {:<90}".format(" "*30 + "|" + "_"*30 + "|" + " "*29) + "\n"


            for i in range(0, len(contacts)):
                name_value, phone_value, birthday_value = contacts[i]
                p = str(phone_value).split(",")
                count = 1 

                if len(p) > 1:
                    for iii in p:
                        new_i = re.sub(pattern, "", iii)
                        if count == 1 and i == 0:
                            result += " {:^90}".format("_"*92) + "\n"
                            result += "| {:<29}| {:<29}| {:<29}|".format(f"Name : {name_value}", f"Phone {count} :{new_i}", f"Birthday {birthday_value}") + "\n"
                        else:
                            result += "| {:<29}| {:<29}| {:<29}|".format("", f"Phone {count} :{new_i}", "") + "\n"
                        count += 1
                
                else:
                    new_i = re.sub(pattern, "", phone_value)
                    if i == 0: result += " {:^90}".format("_"*92) + "\n"
                    else: result += "{:^90}".format("|" + "_"*30 +"|"+ "_"*30 +"|"+ "_"*30 +"|") + "\n"
                    result += "| {:<29}| {:<29}| {:<29}|".format(f"Name : {name_value}", f"Phone {count} :{new_i}", f"Birthday {birthday_value}") + "\n"
            
            result += "{:^90}".format("|" + "_"*30 +"|"+ "_"*30 +"|"+ "_"*30 +"|") + "\n"
            return result
        return None

    # Виконує пошук в кнізі контактів за ключовим значенням
    def search_contacts(self, name:list) -> str:
        dict_contacts = {}
        text = f"Nothing found"
        if name:
            num = 0
            for i in name:
                birthday = self.data[i].birthday.value.strftime('%d-%m-%Y') if self.data[i].birthday else "No birthday date"
                dict_contacts[num] = [str(self.data[i].name), f" {self.data[i].phones}", birthday]
                num += 1
            text = self.create_print_page(len(dict_contacts), dict_contacts, False)
        
        return text