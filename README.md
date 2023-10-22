\## Запуск проекта \### Предварительные требования

Убедитесь, что у вас установлены следующие компоненты:

\- Docker (https://www.docker.com/) 

\- Docker Compose (https://docs.docker.com/compose/)

\### Шаги для запуска

1\. Клонируйте репозиторий на свой локальный компьютер:

git clone https://github.com/YauheniApanas/testBitwise.git

2\. Перейдите в директорию проекта:

cd ваш_репозиторий

3\. Создайте файл \`.env\` в корневой директории проекта и добавьте
следующие переменные среды:

DB=your_database_name 
USER=your_username 
PASSWORD=your_password

4\. Запустите контейнеры Docker с помощью Docker Compose:

docker-compose up

5\. После успешного запуска, Flask-приложение будет доступно по
адресу \`http://localhost:5000\`.

Для тестирования запросов к API можно использовать Insomnia(https://insomnia.rest) или Postman(https://www.postman.com/).

Пример POST запроса к API: http://0.0.0.0:5000/api/questions с параметрами JSON формата {
	"questions_num": 1
}
