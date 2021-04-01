# ATAURUS (Attribution of Authorship Russian)

- [RUSSIAN version](README.md#Описание)
- [ENGLISH version](README.md#Description)

## Description

The program for recognizing the author of russian texts or articles.

## Features extraction

The list of features that will be used in this program: [FEATURES.md](doc/FEATURES.md)

## Quick start

Clone the repository:
```shell script
git clone https://github.com/Lpshkn/Ataurus.git ataurus
cd ataurus
```

At first, you have to create the Docker image:
```shell script
sudo docker build -t ataurus .
```

There are 3 main commands for working with the program: `train`, `predict` and `info`:
* `train` - training a model on the input data. While training extracted features from texts serialize to 
`.config` directory. The trained model will be serialized into the same directory (if `-o` option didn't specify).

* `predict` - predicting target classes for the input data. If the input file was processed earlier (and saved in 
`.config` directory), it will be retrieved from the cache.

* `info` - getting information about the model, containing in the `.config` directory.

### Training

```shell script
sudo docker run \
-v <path to a directory>/data:/ataurus/data \
-v <path to a directory>/.config:/ataurus/.config \
ataurus train ./data/train2.csv
```
or
```shell script
sudo docker run \
-v $PWD/data:/ataurus/data \
-v $PWD/.config:/ataurus/.config \
ataurus train ./data/train2.csv
```

### Getting information

```shell script
sudo docker run -v <path to a directory>/.config:/ataurus/.config ataurus info
```
or
```shell script
sudo docker run -v $PWD/.config:/ataurus/.config ataurus info
```

### Predicting

```shell script
sudo docker run \
-v <path to a directory>/data:/ataurus/data \
-v <path to a directory>/.config:/ataurus/.config \
ataurus predict ./data/test2.csv
```
or
```shell script
sudo docker run \
-v $PWD/data:/ataurus/data \
-v $PWD/.config:/ataurus/.config \
ataurus predict ./data/test2.csv
```

## Testing

To run tests:

```shell script
nosetests --with-coverage --cover-package=ataurus
```

___

## Описание

Программа для атрибуции текстов.

## Быстрый старт

Копируем репозиторий:

```shell script
git clone https://github.com/Lpshkn/Ataurus.git ataurus
cd ataurus
```

Запустить pylint можно командой:
```shell script
pylint ataurus
```
Запустить тесты и проверить покрытие тестами командной:
```shell script
nosetests --with-coverage --cover-package=ataurus
```

Сначала необходимо собрать Docker-образ:
```shell script
sudo docker build -t ataurus .
```  

Определены 3 основные команды для работы с программой: `train`, `predict` и `info`:
* `train`  - обучение модели на входных данных. После обучения выделенные из текста признаки кэшируются, а модель
  модель сохраняется для последующего использования с командой `predict` (путь выходной модели можно задать опцией
  `-o`)
 
* `predict` - предсказывает целевые классы для входных данных. Если поданный на вход файл был обработан ранее, то он
  будет получен из кэша. Данную команду следует использовать после обучении модели (команда `train`)  

* `info` - данная команда выдаст информацию о модели (если не указывать опцию `-m`, то будет использоваться название
  по-умолчанию)
  
**Примечание**: далее в приведенных командах будет задействована директория .config, необходимая для сохранения 
обученных моделей и промежуточных данных, позволяющих оптимизировать работу программы. 
 
**Произведем обучение модели**:
```shell script
sudo docker run \
-v <путь к каталогу>/data:/ataurus/data \
-v <путь к каталогу>/.config:/ataurus/.config \
ataurus train ./data/train2.csv
```
или
```shell script
sudo docker run \
-v $PWD/data:/ataurus/data \
-v $PWD/.config:/ataurus/.config \
ataurus train ./data/train2.csv
```

**Получить информацию о модели можно командой**:
```shell script
sudo docker run -v <путь к каталогу>/.config:/ataurus/.config ataurus info
```
или
```shell script
sudo docker run -v $PWD/.config:/ataurus/.config ataurus info
```

**Чтобы сделать предсказание для тестовых данных**:
```shell script
sudo docker run \
-v <путь к каталогу>/data:/ataurus/data \
-v <путь к каталогу>/.config:/ataurus/.config \
ataurus predict ./data/test2.csv
```
или
```shell script
sudo docker run \
-v $PWD/data:/ataurus/data \
-v $PWD/.config:/ataurus/.config \
ataurus predict ./data/test2.csv
```

#### Примечание:  
Проверить кэширование можно, если запустить `train` или `predict` с файлом test2.csv или train2.csv ещё раз: 
выделение признаков из текста не будет производиться заново.

