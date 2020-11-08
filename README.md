# ATAURUS (Attribution of Authorship Russian)

The repository for recognizing the author of russian texts or articles.

## Features extraction

The list of features that will be used in this program: [FEATURES.md](doc/FEATURES.md)

## Quick start

Clone the repository:
```shell script
git clone https://github.com/Lpshkn/Ataurus.git
cd Ataurus
```

At first, you have to create the Docker image:
```shell script
sudo docker build -t ataurus .
```

Depending on the mode of working, you can pass a .csv file into the program using `-f` option
or pass a text using `-i` option:
```shell script
sudo docker run --rm ataurus -i "Решая одну из своих задач, я столкнулся с необходимостью рассылать пользователям данные для аутентификации."
```
```shell script
sudo docker run --rm ataurus -f data/data.csv
```