// ------------ UrlGet ---------------
// Режим отображения карты, или места
export enum UrlGetParamsTypeView {
    main_map = "mm",
}

// Все возможные GET параметры в URL
export enum UrlGetParams {
    // Широта
    latitude = "x",
    // Долгота
    longitude = "y",
    // Приближение карты
    zoom = "z",
    // Режим отображения
    type_view = "v",
    // Идентификатор `ИмяТочкиРадиусов` из которого будут получены `geomap`
    geomap = "g",
}
// -------------------------------------------------

// ----- geomap ---------------------------------------- //
// Тип для хранения координат
export interface TCoord {
    // широта
    latitude: number;
    // долгота
    longitude: number;
}
// Алиас для ИмяГруппы мест
export type NameGeom = string;

// Тип для списка координат из внешних источников
export interface Tgeom_place_coord_list_item {
    // Уникальный идентификатор места
    id: number;
    // Рейтинг места
    rating: number;
    // Короткое название места. Максимальная длинна 16 символов
    simpl_name: string;
    // Адрес места
    address: string;
    // Названия для фильтрации, отвечающая на вопрос что делать в этом месте
    whattodo: number[];
}
export interface TPropertiesMark extends Tgeom_place_coord_list_item {
    // Названия группы маркеров
    name_marker: string;
    // Координаты места [широта,долгота]
    coord: [number, number];
}
export interface Tgeom_place_coord_list {
    [key: NameGeom]: Tgeom_place_coord_list_item;
}
export interface Tgeom_place_style {
    [key: NameGeom]: {
        name_marker: string;
        img_url: string;
        img_size: [number, number];
    };
}
export interface Tgeom_place_coord {
    [key: NameGeom]: Tgeom_place_coord_list;
}
export interface Tgeomap {
    // projection: string;
    geom_place_style: Tgeom_place_style;
    // geom_whattodo_det: { [key: string | number]: string };
    geom_place_coord: Tgeom_place_coord;
}
// ------------------------------------------------- //

// ----- meta_geomap ---------------------------------------- //

export interface Tmeta_geomapJson_names_radius {
    // По этому имени пользователи будут фильтровать "Имена точек радиуса".
    hum: string;
    // Путь к статическому файлу, который хранить в себе информацию обо всех местах в этом радиусе.
    name_path: string;
    // ID БД шарда, где храниться группа
    shard: number;
}


export interface Tmeta_geomapJson_Item {
    // names_radius: {
    //     [key: number]: Tmeta_geomapJson_names_radius;
    // };
    id: number,
    self_url: string,
    name: string,
    arial_in_map: number,
    // arial_in_map_obj: {
    //     "id": 1,
    //     "self_url": "http://localhost:8181/api/v1/arial_in_map/1/",
    //     "name": "Санкт-Петербург - радиус 200км от дворцовой площади"
    // },
    shard: number
}
export interface Tmeta_geomapJson {
    // names_radius: {
    //     [key: number]: Tmeta_geomapJson_names_radius;
    // };
    // TODO: Учесть пагинацию !
    results: Tmeta_geomapJson_Item[];
}


// ------------------------------------------------- //

// ------------ public_place_details -----------

// День.Месяц.Год Час:Минуты
export type DateTime = string;
// Час:Минуты
export type Time = string;
// Когда это место возможно посетить
export enum EWhenPossibleVisit {
    StaticWorkSchedule = "Постоянный график работы",
    OneTimeTemporaryEvent = "Одноразовое временно событие",
    PeriodicPlace = "Переодическое место",
}
// Средняя людность:
export enum EAveragePopulation {
    UncomfortableFrequentCrowding = "Дискомфортная частая людность",
    UncomfortableFrequentCrowdingExceptWeekends = "Дискомфортная людность по выходным и праздникам, но в рабочие дни комфортная",
    ComfortableCrowd = "Комфортная людность",
    Privacy = "Уединение",
    Loneliness = "Одиночество",
}
// День недели
export enum Eweekday {
    Monday = "понедельник",
    Tuesday = "вторник",
    Wednesday = "среда",
    Thursday = "четверг",
    Friday = "пятница",
    Saturday = "суббота",
    Sunday = "воскресенье",
}
// Валюта
export enum EAverageCostVisit {
    RUB = "руб",
    USD = "доллар",
    EUR = "евро",
    CNY = "юань",
}

export interface TInternetСontacts {
    phones?: string[];
    website?: string;
    tg?: string;
    vk?: string;
    any_social?: string[];
    yandex_map?: string;
    any_link?: string[];
}

export interface Tpublic_place_details extends TPropertiesMark {
    // Когда это место возможно посетить
    WhenPossibleVisit: {
        type: EWhenPossibleVisit;
        data: {
            // Дни недели в которые это место работает.
            // Если в какой-то день недели это место не работает, то это день не нужно указывать
            // Если у этого места нет графика работы, то не нужно указывать ключ "weekday"
            weekday?: {
                [key in Eweekday]: {
                    start: Time;
                    end: Time;
                };
            };
            // Начала периода: День.Месяц.Год Час:Минуты
            start_period?: DateTime;
            // Конец периода: День.Месяц.Год Час:Минуты
            end_period?: DateTime;
            // Дата(ы) начала события.
            dates?: DateTime[];
        };
    };
    // Средняя стоимость посещения.
    AverageCostVisit: {
        currency: EAverageCostVisit;
        value: number;
    };
    // Средняя людность:
    AveragePopulation: EAveragePopulation;
    // Это место в интернете
    InternetСontacts: TInternetСontacts;
    // У скольких пользователей, это место добавлено в избранные.
    FavoritesCountMore: number;
}

// ------------
