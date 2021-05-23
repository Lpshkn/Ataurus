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

Программа для атрибуции русских текстов. Для качественной атрибуции, желательно, чтобы на каждого автора приходилось
60-80 статей.

Программа имеет 2 режима работы: `train` и `predict`
```shell
ataurus {train, predict}
```
* `train` - режим обучения модели на входных данных. На вход подаются полный путь, куда будет сериализована обученная 
  модель (аргумент `output`) и входные данные (аргумент `input`) в следующих возможных форматах:
    * connection string - строка подключения к кластеру ElasticSearch (формат `hostname:port/name_index`). При этом 
       документы в индексе **ДОЛЖНЫ** содержать поля `author_nickname` для имени автора и `text` 
      для самого текста;
    * .csv файл, **ОБЯЗАТЕЛЬНО** содержащий столбцы `author` для указания автора и `text` для текстов;
    * сериализованный с помощью `Joblib` `DataFrame` объект. Этот файл содержит DataFrame объект, который хранит в себе
      уже выделенные на этапе обучения (режим `train`) признаки (с помощью опции `-f`).
    ```shell
    ataurus train [-f FEATURES] input output
    ``` 
    После обучения выделенные из текста признаки могут быть сериализованы опцией `-f` с указанием полного пути и 
    имени файла, а модель по окончанию работы сохранится для последующего использования режимом `predict`.  
  
    Сериализация признаков позволяет значительно сократить время на обработку текстов и выделения признаков. Это 
    позволяет подогнать модель машинного обучения под конкретные данные.
  
  
* `predict` - режим составления прогнозов для входных данных. Данный режим следует использовать после обучения 
  модели (режим `train`). На вход подаются полный путь, где расположена сериализованная ранее модель (аргумент `model`),
  а также входные данные в точно таком же формате, как и в режиме `train`. Опция `-f` выполняет ту же работу, что и в 
  режиме `train`.
  
  ```shell
  ataurus predict [-f FEATURES] input model
  ```
  
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


**Примечание 1**: далее в приведенных командах будет задействована директория `result`, необходимая для сохранения 
обученных моделей и сериализованных признаков.
 
**Примечание 2**: если вы будете использовать connection string к ElasticSearch, необходимо будет указать в команде 
`docker run` опцию `--network=host`. Это позволит подключиться к серверу, запущенному на вашем хосте по адресу 
`localhost` (если ничего не изменялось).

**Произведем обучение модели**:
* с помощью connection string
  ```shell script
  docker run --network=host \
  -v $PWD/result:/ataurus/result \
  ataurus:1.0.0 train <hostname>:<port>/<index_name> /ataurus/result/model/<model_name> \
  -f /ataurus/result/features/<features_name>
  ```
  К примеру:
  ```shell
  docker run --network=host \
  -v $PWD/result:/ataurus/result \
  ataurus:1.0.0 train localhost:9200/5ath_18_22 /ataurus/result/model/model_5ath \
  -f /ataurus/result/features/5ath_18_22
  ```
  Здесь для обучения используются данные, полученные из индекса `5ath_18_22` ElasticSearch (содержащий тексты 5 авторов, 
  у которых от 18 до 22 текстов). Обработанные тексты сохраняются с помощью опции `-f` с именем `5ath_18_22`.
  

* с помощью .csv файла
  ```shell
  docker run \
  -v $PWD/result:/ataurus/result \
  -v <path_to_data>:/ataurus/data \
  ataurus:1.0.0 train /ataurus/data/<name_.csv_file> /ataurus/result/model/<model_name> \
  -f /ataurus/result/features/<features_name>
  ```
  К примеру:
  ```shell
  docker run \
  -v $PWD/result:/ataurus/result \
  -v $PWD/data:/ataurus/data \
  ataurus:1.0.0 train /ataurus/data/train1.csv /ataurus/result/model/model_csv \
  -f /ataurus/result/features/train1
  ```
  
* с помощью DataFrame объекта:
  ```shell
  docker run \
  -v $PWD/result:/ataurus/result \
  ataurus:1.0.0 train /ataurus/result/features/5ath_18_22 /ataurus/result/model/model_5ath
  ```
  Здесь обучение происходит на уже выделенных ранее признаках и сериализованных в файл `5ath_18_22`.

**Произведем предсказание авторов**

Поскольку режим `predict` по синтаксису не отличается практически от режима `train`, то приведем пример только для 
.csv файла `test1.csv`. При этом, будем использовать обученную модель `model_csv`.
```shell
docker run \
-v $PWD/result:/ataurus/result \
-v $PWD/data:/ataurus/data \
ataurus:1.0.0 predict /ataurus/data/test1.csv /ataurus/result/model/model_csv
```
