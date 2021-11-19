# -*- coding: utf-8 -*-
import openpyxl
import os
import pandas as pd

def check_cell(cell):
    """
    Функция для проверки значения ячейки, поскольку некоторые уникумы ставят в ячейки ЛОЖЬ и простой тернарный оператор некорректно считает
    :param cell: Значение проверяемой ячейки
    :return: 0 если в ячейке пусто или стоит ЛОЖЬ, 1 если в ячейке что то есть. число если в ячейке находится число
    """
    if cell is None:
        return 0
    elif type(cell) is int:
        return cell
    elif type(cell) is float:
        return int(cell)
    elif type(cell) is bool:
        if cell is True:
            return 1
        else:
            return 0

    elif  cell.lower() == 'ЛОЖЬ' or 'нет' in cell.lower():
        return 0
    else:
        return 1


# Создаем словарь, где ключом будет название вопроса, а значение в зависимости от вопроса будет либо словарь, либо просто число

d = {'Наличие  мероприятий, направленных на профессиональное самоопределение и профориентацию обучающихся по программам СПО и студентов вузов':0,
     'Системная и массовая поддержка обучающихся по программам СПО и студентов вузов в проектировании индивидуальной профессиональной траектории ':0,
     'Наличие  формата «сквозного» учебно-профессионального портфолио обучающихся по программам СПО и студентов вузов, пополняемого и используемого на всех этапах профессионального самоопределения':0,
     'Наличие в организациях СПО и вузах  курса «Введение в специальность» для обучающихся по программам СПО и студентов вузов на первом году обучения':0,
     'Количество и доля организации СПО и вузов , имеющих в своей образовательной программе курс «Введение в специальность» для обучающихся по программам СПО и студентов вузов на первом году обучения(два показателя) (ПОДТВЕРДИТЬ НАЛИЧИЕ)':
         {'Количество (шт.)':0,'Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ':0},

     'Наличие в организациях СПО и вузах  специальных программ адаптации студентов-первокурсников':0,

     'Количество и доля организации СПО и вузов , имеющих специальные программы адаптации студентов-первокурсников(два показателя)  (ПОДТВЕРДИТЬ НАЛИЧИЕ)':
         {'Количество (шт.)':0,'Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ':0},

     'Наличие  конкурсов профессионального мастерства для обучающихся по программам СПО и студентов вузов':0,

     'Организация знакомства обучающихся по программам СПО и студентов вузов с корпоративной культурой льных предприятий-партнеров':0,

     'Введение элементов корпоративной культуры льных предприятий-партнеров в учебную среду организации СПО и вузов ':0,

     'Обеспечение возможностей для оплачиваемой профессиональной деятельности обучающихся по программам СПО и студентов вузов':0,

     'Организация обучения на рабочем месте в сопровождении наставника для обучающихся по программам СПО и студентов вузов':0,

    'Помощь в трудоустройстве обучающихся по программам СПО и студентов вузов ':0,

    'Количество соглашений между организациями СПО и вузами , включающих в качестве целевого направления взаимодействия работу по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов':0,

    'Количество и доля организации СПО и вузов , имеющих договоры с предприятиями / социальными партнерами, включающие в качестве целевого направления взаимодействия работу по направлению профессионального самоопределения и профориентации школьников (ПОДТВЕРДИТЬ НАЛИЧИЕ)(два показателя)':
         {'Количество (шт.)':0,'Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ':0},

    'Количество и доля некоммерческих организации, участвующих в реализации деятельности по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(два показателя) (ПОДТВЕРДИТЬ УЧАСТИЕ)':
         {'Количество (шт.)':0,'Общее число некоммерческих организации ) НЕ ЗАПОЛНЯТЬ':0},

    'Количество и доля мероприятий по направлению профессионального самоопределения и профориентации для обучающихся по программам СПО и студентов вузов, предполагающих непосредственное участие представителей работодателей(два показателя) (ПОДТВЕРДИТЬ НАЛИЧИЕ)':
         {'Количество (шт.)':0,'Общее число мероприятий по направлению профессионального самоопределения и профориентации для представителей возрастной категории) НЕ ЗАПОЛНЯТЬ':0},

    'Наличие реализуемых  программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов':0,

    'Количество и динамика реализуемых  программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(два показателя)':
         {'Количество (шт.)':0,'Динамика по отношению к предыдущему уч. году(+ / -)':0},

    'Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)':
         {'Кружки и студии технического творчества':0,'Кружки и студии художественного творчества':0,'Система индивидуальных/групповых консультаций':0,'Встречи с профессионалами':0,'Проектная деятельность':0,'Просмотр и обсуждение документальных и художественных фильмов':0,'Чтение и обсуждение книг о представителях выбранной профессии':0,'Работа с электронными образовательными ресурсами':0,'Экскурсии на предприятия':0,'Стажировки на предприятиях':0,'Другое: …':''},

    'Методика организации программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)':
         {'Модули по профессиональному самоопределению и профориентации, интегрированные в образовательную программу':0,'Элективные курсы':0,'Программы дополнительного образования':0,'Внеурочная деятельность':0,'Другое: …':''},

    'Количество и доля педагогических и руководящих работников организации СПО и вузов , занимающихся проведением работы по направлению сопровождения профессионального самоопределения и профориентации школьников(два показателя)':
         {'Количество (чел.)':0,'Общее число педагогических и руководящих работников организации СПО и вузов )':0},

    'Количество и доля педагогических и руководящих работников организации СПО и вузов , прошедших повышение квалификации по направлению сопровождения профессионального самоопределения и профориентации школьников(два показателя)':
         {'Количество (чел.)':0,'Общее число педагогических и руководящих работников организации СПО и вузов )':0},

    'Количество и доля педагогических и руководящих работников организации СПО и вузов , прошедших повышение квалификации по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов, относящихся к категории инвалидов, детей-инвалидов и лиц с ОВЗ(два показателя)':
         {'Количество (чел.)':0,'Общее число педагогических и руководящих работников организации СПО и вузов )':0},

    'Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)':
         {'Сотрудники организации СПО и вузов ':{
             'Сотрудник центра развития карьеры / содействия трудоустройству в организации СПО':0,'Сотрудник центра развития карьеры / содействия трудоустройству в вузе':0,'Психолог, педагог-психолог':0,'Педагог / мастер производственного обучения':0,'Преподаватель вуза':0,'Педагог дополнительного образования':0,'Педагог-библиотекарь':0,'Медицинский работник':0,'Другое: …':''},
             'Внешние сотрудники':{
                 'Специалист центра занятости населения':0,'Специалист по профориентации, профконсультант':0,'Другое: …':'',
             }},

    33:0,
    'Средний опыт работы педагогических и руководящих работников организации СПО и вузов , занимающихся деятельностью по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов':0,

    34:0,
    'Средний опыт работы специалиста по профессиональному самоопределению и профориентации обучающихся по программам СПО и студентов вузов(при условии наличия отдельной ставки специалиста)':0,

    'Наличие центров по профессиональной ориентации и содействию трудоустройству обучающихся по программам СПО и студентов вузов(два показателя)':
         {'Количество (шт.)':0,'Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ':0},

    'Наличие  базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов':0,

    'Количество базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов ':0,

    'Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)':
         {'Центр опережающей профессиональной подготовки (ЦОПП)':0,'Отраслевые ресурсные центры (ОРЦ)':0,'Специализированные центры компетенций (СЦК)':0,'Межльный центр компетенций (МЦК)':0,'Многофункциональный центр профессиональных компетенций (МЦПК)':0,
          'Центр молодежного инновационного творчества (ЦМИТ)':0,'Институт развития образования (ИРО)':0,'Центры профессиональной ориентации':0,'Центры непрерывного образования':0,'Организации среднего профессионального образования (СПО)':0,'Высшие учебные заведения (вузы)':0,'Научные центры на базе факультетов / кафедр / лабораторий вузов':0,'Центры развития карьеры / содействия трудоустройству при организациях СПО':0,
          'Центры развития карьеры / содействия трудоустройству при вузах':0,'льные профильные классы/группы при образовательных учреждениях':0,'Учебно-тренировочные центры':0,'Единый льный профориентационный Интернет-портал':0,'Детско-юношеский центр':0,'Службы занятости населения':0,'Передвижной центр профориентации':0,'Центры профориентации на базе работодателей':0,'Другое: …':''},





}

# Путь к файлам
path = 'data/'
count = 1
# Итерируемся по всем файлам внутри папки указанной в переменной path
for file in os.listdir(path):
    # Загружаем файл эксель
    print(file)
    wb = openpyxl.load_workbook(f'{path}{file}')
    # Получаем активный лист
    sheet = wb.active

    # Вопросы идут по порядку анкеты

    #8
    d['Наличие  мероприятий, направленных на профессиональное самоопределение и профориентацию обучающихся по программам СПО и студентов вузов'] += check_cell(sheet['G8'].value)

    #9
    d['Системная и массовая поддержка обучающихся по программам СПО и студентов вузов в проектировании индивидуальной профессиональной траектории '] += check_cell(sheet['G10'].value)

    #10
    d['Наличие  формата «сквозного» учебно-профессионального портфолио обучающихся по программам СПО и студентов вузов, пополняемого и используемого на всех этапах профессионального самоопределения'] += check_cell(sheet['G12'].value)

    #11
    d['Наличие в организациях СПО и вузах  курса «Введение в специальность» для обучающихся по программам СПО и студентов вузов на первом году обучения'] += check_cell(sheet['G14'].value)

    #12
    d['Количество и доля организации СПО и вузов , имеющих в своей образовательной программе курс «Введение в специальность» для обучающихся по программам СПО и студентов вузов на первом году обучения(два показателя) (ПОДТВЕРДИТЬ НАЛИЧИЕ)']['Количество (шт.)']+= check_cell(sheet['G16'].value)
    d['Количество и доля организации СПО и вузов , имеющих в своей образовательной программе курс «Введение в специальность» для обучающихся по программам СПО и студентов вузов на первом году обучения(два показателя) (ПОДТВЕРДИТЬ НАЛИЧИЕ)']['Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ']+= check_cell(sheet['G17'].value)

    #13
    d['Наличие в организациях СПО и вузах  специальных программ адаптации студентов-первокурсников'] += check_cell(sheet['G19'].value)

    #14
    d['Количество и доля организации СПО и вузов , имеющих специальные программы адаптации студентов-первокурсников(два показателя)  (ПОДТВЕРДИТЬ НАЛИЧИЕ)']['Количество (шт.)']+= check_cell(sheet['G21'].value)
    d['Количество и доля организации СПО и вузов , имеющих специальные программы адаптации студентов-первокурсников(два показателя)  (ПОДТВЕРДИТЬ НАЛИЧИЕ)']['Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ']+= check_cell(sheet['G22'].value)

    #15
    d['Наличие  конкурсов профессионального мастерства для обучающихся по программам СПО и студентов вузов'] += check_cell(sheet['G24'].value)

    #16
    d['Организация знакомства обучающихся по программам СПО и студентов вузов с корпоративной культурой льных предприятий-партнеров'] += check_cell(sheet['G26'].value)

    #17
    d['Введение элементов корпоративной культуры льных предприятий-партнеров в учебную среду организации СПО и вузов '] += check_cell(sheet['G28'].value)

    #18
    d['Обеспечение возможностей для оплачиваемой профессиональной деятельности обучающихся по программам СПО и студентов вузов'] += check_cell(sheet['G30'].value)

    #19
    d['Организация обучения на рабочем месте в сопровождении наставника для обучающихся по программам СПО и студентов вузов'] += check_cell(sheet['G32'].value)

    #20
    d['Помощь в трудоустройстве обучающихся по программам СПО и студентов вузов '] += check_cell(sheet['G34'].value)

    #21
    d['Количество соглашений между организациями СПО и вузами , включающих в качестве целевого направления взаимодействия работу по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов'] += check_cell(sheet['G36'].value)

    #22
    d['Количество и доля организации СПО и вузов , имеющих договоры с предприятиями / социальными партнерами, включающие в качестве целевого направления взаимодействия работу по направлению профессионального самоопределения и профориентации школьников (ПОДТВЕРДИТЬ НАЛИЧИЕ)(два показателя)']['Количество (шт.)'] += check_cell(sheet['G38'].value)
    d['Количество и доля организации СПО и вузов , имеющих договоры с предприятиями / социальными партнерами, включающие в качестве целевого направления взаимодействия работу по направлению профессионального самоопределения и профориентации школьников (ПОДТВЕРДИТЬ НАЛИЧИЕ)(два показателя)']['Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ'] += check_cell(sheet['G39'].value)

    #23
    d['Количество и доля некоммерческих организации, участвующих в реализации деятельности по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(два показателя) (ПОДТВЕРДИТЬ УЧАСТИЕ)']['Количество (шт.)'] += check_cell(sheet['G41'].value)
    d['Количество и доля некоммерческих организации, участвующих в реализации деятельности по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(два показателя) (ПОДТВЕРДИТЬ УЧАСТИЕ)']['Общее число некоммерческих организации ) НЕ ЗАПОЛНЯТЬ'] += check_cell(sheet['G42'].value)

    #24
    d['Количество и доля мероприятий по направлению профессионального самоопределения и профориентации для обучающихся по программам СПО и студентов вузов, предполагающих непосредственное участие представителей работодателей(два показателя) (ПОДТВЕРДИТЬ НАЛИЧИЕ)']['Количество (шт.)'] += check_cell(sheet['G44'].value)
    d['Количество и доля мероприятий по направлению профессионального самоопределения и профориентации для обучающихся по программам СПО и студентов вузов, предполагающих непосредственное участие представителей работодателей(два показателя) (ПОДТВЕРДИТЬ НАЛИЧИЕ)']['Общее число мероприятий по направлению профессионального самоопределения и профориентации для представителей возрастной категории) НЕ ЗАПОЛНЯТЬ'] += check_cell(sheet['G45'].value)

    #25
    d['Наличие реализуемых  программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов'] += check_cell(sheet['G48'].value)

    #26
    d['Количество и динамика реализуемых  программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(два показателя)']['Количество (шт.)'] += check_cell(sheet['G50'].value)
    d['Количество и динамика реализуемых  программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(два показателя)']['Динамика по отношению к предыдущему уч. году(+ / -)'] += check_cell(sheet['G51'].value)

    #27
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Кружки и студии технического творчества'] += check_cell(sheet['G53'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Кружки и студии художественного творчества'] += check_cell(sheet['G54'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Система индивидуальных/групповых консультаций'] += check_cell(sheet['G55'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Встречи с профессионалами'] += check_cell(sheet['G56'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Проектная деятельность'] += check_cell(sheet['G57'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Просмотр и обсуждение документальных и художественных фильмов'] += check_cell(sheet['G58'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Чтение и обсуждение книг о представителях выбранной профессии'] += check_cell(sheet['G59'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Работа с электронными образовательными ресурсами'] += check_cell(sheet['G60'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Экскурсии на предприятия'] += check_cell(sheet['G61'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Стажировки на предприятиях'] += check_cell(sheet['G62'].value)
    d['Форматы программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Другое: …'] += f'{sheet["G63"].value};'

    #28
    d['Методика организации программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Модули по профессиональному самоопределению и профориентации, интегрированные в образовательную программу'] += check_cell(sheet['G65'].value)
    d['Методика организации программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Элективные курсы'] += check_cell(sheet['G66'].value)
    d['Методика организации программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Программы дополнительного образования'] += check_cell(sheet['G67'].value)
    d['Методика организации программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Внеурочная деятельность'] += check_cell(sheet['G68'].value)
    d['Методика организации программ и/или проектов по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Другое: …'] += f'{sheet["G69"].value};'

    #29
    d['Количество и доля педагогических и руководящих работников организации СПО и вузов , занимающихся проведением работы по направлению сопровождения профессионального самоопределения и профориентации школьников(два показателя)']['Количество (чел.)'] += check_cell(sheet['G71'].value)
    d['Количество и доля педагогических и руководящих работников организации СПО и вузов , занимающихся проведением работы по направлению сопровождения профессионального самоопределения и профориентации школьников(два показателя)']['Общее число педагогических и руководящих работников организации СПО и вузов )'] += check_cell(sheet['G72'].value)

    #30
    d['Количество и доля педагогических и руководящих работников организации СПО и вузов , прошедших повышение квалификации по направлению сопровождения профессионального самоопределения и профориентации школьников(два показателя)']['Количество (чел.)'] += check_cell(sheet['G74'].value)
    d['Количество и доля педагогических и руководящих работников организации СПО и вузов , прошедших повышение квалификации по направлению сопровождения профессионального самоопределения и профориентации школьников(два показателя)']['Общее число педагогических и руководящих работников организации СПО и вузов )'] += check_cell(sheet['G75'].value)

    #31
    d['Количество и доля педагогических и руководящих работников организации СПО и вузов , прошедших повышение квалификации по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов, относящихся к категории инвалидов, детей-инвалидов и лиц с ОВЗ(два показателя)']['Количество (чел.)'] += check_cell(sheet['G77'].value)
    d['Количество и доля педагогических и руководящих работников организации СПО и вузов , прошедших повышение квалификации по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов, относящихся к категории инвалидов, детей-инвалидов и лиц с ОВЗ(два показателя)']['Общее число педагогических и руководящих работников организации СПО и вузов )'] += check_cell(sheet['G78'].value)

    #32
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Сотрудник центра развития карьеры / содействия трудоустройству в организации СПО'] += check_cell(sheet['G80'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Сотрудник центра развития карьеры / содействия трудоустройству в вузе'] += check_cell(sheet['G81'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Психолог, педагог-психолог'] += check_cell(sheet['G82'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Педагог / мастер производственного обучения'] += check_cell(sheet['G83'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Преподаватель вуза'] += check_cell(sheet['G84'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Педагог дополнительного образования'] += check_cell(sheet['G85'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Педагог-библиотекарь'] += check_cell(sheet['G86'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Медицинский работник'] += check_cell(sheet['G87'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Сотрудники организации СПО и вузов ']['Другое: …'] +=f'{sheet["G88"].value};'

    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Внешние сотрудники']['Специалист центра занятости населения'] += check_cell(sheet['G89'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Внешние сотрудники']['Специалист по профориентации, профконсультант'] += check_cell(sheet['G90'].value)
    d['Должности педагогических и руководящих работников организации СПО и вузов , занимающихся работой по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Внешние сотрудники']['Другое: …'] +=f'{sheet["G91"].value};'

    #33
    d[33]+= check_cell(sheet['G93'].value)
    d['Средний опыт работы педагогических и руководящих работников организации СПО и вузов , занимающихся деятельностью по направлению сопровождения профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов'] = d[33] / count

    #34
    d[34] += check_cell(sheet['G95'].value)
    d['Средний опыт работы специалиста по профессиональному самоопределению и профориентации обучающихся по программам СПО и студентов вузов(при условии наличия отдельной ставки специалиста)'] = d[34] / count

    #35
    d['Наличие центров по профессиональной ориентации и содействию трудоустройству обучающихся по программам СПО и студентов вузов(два показателя)']['Количество (шт.)'] += check_cell(sheet['G97'].value)
    d['Наличие центров по профессиональной ориентации и содействию трудоустройству обучающихся по программам СПО и студентов вузов(два показателя)']['Общее число организации СПО и вузов ) НЕ ЗАПОЛНЯТЬ'] += check_cell(sheet['G98'].value)

    #36
    d['Наличие  базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов']+= check_cell(sheet['G100'].value)

    #37
    d['Количество базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов ']+= check_cell(sheet['G102'].value)

    #38
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центр опережающей профессиональной подготовки (ЦОПП)'] += check_cell(sheet['G104'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Отраслевые ресурсные центры (ОРЦ)'] += check_cell(sheet['G105'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Специализированные центры компетенций (СЦК)'] += check_cell(sheet['G106'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Межльный центр компетенций (МЦК)'] += check_cell(sheet['G107'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Многофункциональный центр профессиональных компетенций (МЦПК)'] += check_cell(sheet['G108'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центр молодежного инновационного творчества (ЦМИТ)'] += check_cell(sheet['G109'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Институт развития образования (ИРО)'] += check_cell(sheet['G110'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центры профессиональной ориентации'] += check_cell(sheet['G111'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центры непрерывного образования'] += check_cell(sheet['G112'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Организации среднего профессионального образования (СПО)'] += check_cell(sheet['G113'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Высшие учебные заведения (вузы)'] += check_cell(sheet['G114'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Научные центры на базе факультетов / кафедр / лабораторий вузов'] += check_cell(sheet['G115'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центры развития карьеры / содействия трудоустройству при организациях СПО'] += check_cell(sheet['G116'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центры развития карьеры / содействия трудоустройству при вузах'] += check_cell(sheet['G117'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['льные профильные классы/группы при образовательных учреждениях'] += check_cell(sheet['G118'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Учебно-тренировочные центры'] += check_cell(sheet['G119'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Единый льный профориентационный Интернет-портал'] += check_cell(sheet['G120'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Детско-юношеский центр'] += check_cell(sheet['G121'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Службы занятости населения'] += check_cell(sheet['G122'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Передвижной центр профориентации'] += check_cell(sheet['G123'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Центры профориентации на базе работодателей'] += check_cell(sheet['G124'].value)
    d['Формат базовых площадок для организации работы по направлению профессионального самоопределения и профориентации обучающихся по программам СПО и студентов вузов(возможен выбор нескольких вариантов ответа)']['Другое: …'] +=f'{sheet["G125"].value};'






    count += 1




























print(d)