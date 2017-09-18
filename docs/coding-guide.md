# Требования к python-коду

1. Все файлы должны начинаться с указания кодировки: `# -*- coding: utf-8 -*-`
1. Python-код должен проходить валидацию с помощью `flake8`:
    * Установить flake8 командой `pip install flake8`
    * Код валидируется командой `flake8 --max-line-length=120 <path>`, где path - папка с python-кодом
1. Python-методы должны иметь docstring в Google-формате ([link](https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments))

# Требования к robot-файлам

1. Если автотесту необходимо подождать какого-то события, это делается с использованием keyword `Wait Until Keyword Succeeds`.
1. Соответствие принципу 1 автотест = 1 файл
1. Соответствие принципу 1 шаг тест-кейса = 1 keyword, расписанный под тест-кейсом. В итоге, тест-кейс состоит из перечисления keywords, расположенных под ним. Пример: [link](../test/JIRA-WF-1/Create_Task_Issue.robot)
1. Все вызовы keyword должны иметь префикс (название библиотеки или имя файла с ресурсами): `API.Create Project`, `DB.Get Project`, `Resource.XXX`
1. Keywords должны быть Camel Case (т.е. `API.Create Project`, а не `API.create project` или `API.Create_project`)
1. Между параметрами 4 пробела
1. Ссылка на кейс в TestRail
1. Наличие тега testrailid

В качестве примера можно ознакомиться с тестом `test/JIRA-WF-1/Create_Task_Issue.robot`

# Дополнительные требования

* При заведении констант, необходимо отдавать предпочтение числовым константам, а не строковым. Например, для типа issue 'Task' лучше хранить ID типа сущности (10002), чем его name ('Task').