# SqliteBOT

This bot interacts with the Sqlite3 library.
I have moved the buttons and the token to a separate file config.py (they say it's more correct or even better to keep tokens and stuff in config,
and keep a separate file under the buttons, but I thought it made no sense for such a small bot to bother so much).
In the future I plan to refine the bot: 
1. I have already made an additional admin rights check field. 
Now I want to add a full-fledged admin panel. 
2.Add more tables and establish dependencies between them.

#SETUP
So to install this bot on your computer, you will need to copy my repository to your PC. 
To do this, you can use the gh repo clone Vasiliii/SqliteBOT command if you have github installed. 
Well, or you can copy my code from files to your project (if you are so desperate).

Next , you will have to install the library to work with telegramAPI . 
In this bot, I used the pyTelegramBotAPI library.
To install it, you just need to write in the command line (opens with the win+R keys and the cmd command) enter the pip install pyTelegramBotAPI command. 
After installing the library, you will need to insert your API token into the TOKEN variable in the file config.py .

After all the above manipulations, you just have to run main.py file and go to your bot

Этот бот взаимодействует с библиотекой Sqlite3.
Я вынес кнопки и токен в отдельный файл config.py (говорят так правильнее или даже лучше в config  держать токены и прочее,
а под кнопки держать отдельный файл, но я посчитал что для такого маленького бота нет смысла так заморачиваться).
В будущем я планирую доработать бота: 
1. Я уже сделал дополнительное поле проверки прав администратора. 
Теперь хочу  добавить полноценную админ панель. 
2.Добавить ещё  таблиц и установить между ними зависимости.

#УСТАНОВКА
Итак для установки этого бота к себе на компьютер вам потребуется скопировать мой репозиторий себе на  ПК. 
Для этого вы можете воспользоваться командой gh repo clone Vasiliii/SqliteBOT если у вас установлен github. 
Ну или вы можете копировать мой код из файлов себе в проект (если вы уж настолько отчаянный).

Далее вам придется установить библиотеку для работы с telegramAPI . 
В данном  боте я использовал библиотеку pyTelegramBotAPI.
Для ее установки вам всего лишь надо написать в командной строке(открывается клавишами win+R и командой cmd) ввести команду pip install pyTelegramBotAPI. 
После установки библиотеки вам потребуется вставить свой API token в переменную   TOKEN в файле config.py.

После всех вышеописанных манипуляций вам остается только запустить main.py файл и перейти к вашему боту 
