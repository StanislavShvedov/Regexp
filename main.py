import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
def clear_FIO(contacts):
    clear_contact_list = []
    count = 0
    for contact in contacts:
        if contact[0] == '' or contact[1] == '' or contact[2] == '':
            fio = ' '.join(contact[0:3]).split()
            if len(fio) == 3:
                contact[0], contact[1], contact[2] = fio[0], fio[1], fio[2]
            elif len(fio) == 2:
                contact[0], contact[1], contact[2] = fio[0], fio[1], None
            elif len(fio) == 2:
                contact[0], contact[1], contact[2] = fio[0], None, None
        clear_contact_list.append(contact)

    return clear_contact_list

clear_contacts = clear_FIO(contacts_list)


def remove_duplication(contacts):
    clear_contacts = clear_FIO(contacts)

    # Словарь для хранения уникальных контактов
    merged_contacts = {}

    for contact in clear_contacts:
        key = (contact[0], contact[1])  # Ключ на основе фамилии и имени

        if key not in merged_contacts:
            merged_contacts[key] = {
                'last_name': contact[0],
                'first_name': contact[1],
                'surname': contact[2],
                'organization': contact[3],
                'position': contact[4],
                'phone': contact[5],
                'email': contact[6]
            }
        else:
            # Объединяем данные
            for i, field in enumerate(['surname', 'organization', 'position', 'phone', 'email']):
                if not merged_contacts[key][field] and contact[i + 2]:  # Индекс смещается на 2
                    merged_contacts[key][field] = contact[i + 2]

    final_contacts = list(merged_contacts.values())
    result = []
    for contact in final_contacts:
        result.append([contact['last_name'], contact['first_name'], contact['surname'], contact['organization'],
                       contact['position'], contact['phone'], contact['email']])

    for contact in result[1:]:
        if 'доб' in contact[5]:
            pattern = r"(\+7|8)?\s\(?(\d+)\)?[\s-](\d+)[\s-](\d+)[\s-](\d+)[\s](\(?[а-я]*\.[\s](\d+)\)?)?"
            pattern_sub = r"+7(\2)\3-\4-\5 доп.\7"
            result_contact = re.sub(pattern, pattern_sub, contact[5])
            contact[5] = result_contact

        elif 'доб' not in contact[5]:
            pattern = r"(\+7|8)?\s?\(?(\d{3})\)?[\s-]?(\d{3})\-?(\d{2})\-?(\d+)"
            pattern_sub = r"+7(\2)\3-\4-\5"
            result_contact = re.sub(pattern, pattern_sub, contact[5])
            contact[5] = result_contact

    return result


result = remove_duplication(clear_contacts)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(result)