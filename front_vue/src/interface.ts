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
    // Идентификатор канала
    channel = "c",
    // Идентификатор выбранного места(маркера)
    mark = 'm'
}
// -------------------------------------------------

// ----- geomap ---------------------------------------- //
export interface TCoord {
    // широта
    latitude: number;
    // долгота
    longitude: number;
}

export interface TTypePlaceObj {
    // Уникальный идентификатор типа
    id: number;
    self_url: string;
    // Имя типа
    name: string;
    // Путь к иконке маркера
    img_url: string;
    // Широта фота в 0.3
    img_size_w: number;
    // Высота фота в 0.3
    img_size_h: number;
}

export interface TWhatTodoObj {
    // Чем можно заняться в этом места
    id: number;
    self_url: string;
    todo: string;
}

export interface TArialObj {
    // Уникальный идентификатор ареала
    id: number;
    self_url: string;
    name: string;
}

export interface TChannelGeomapObj {
    // Уникальный идентификатор канала
    id: number;
    self_url: string;
    name: string;
    arial_in_map: number;
    arial_in_map_obj: TArialObj;
    shard: number;
}

export interface TGeomap {
    // Уникальный идентификатор места
    id: string;
    self_url: string;
    // Координаты места Широта
    cord_x: string;
    // Координаты места Долгота
    cord_y: string;
    // Короткое название места. Максимальная длинна 16 символов
    simpl_name: string;
    // Рейтинг места
    rating: number;
    // Адрес места
    address: string;
    // Id канала к которому принадлежит место
    channel_geomap: number;
    channel_geomap_obj: TChannelGeomapObj;
    // Чем можно заняться в этом месте
    what_todo: number[];
    what_todo_obj: TWhatTodoObj[];
    // Тип места
    type_place: number;
    type_place_obj: TTypePlaceObj;
}
export interface TPropertiesMark extends TGeomap { };
export interface Tchannel_geomapJson { }

// export interface TPropertiesMark extends TGeomap {
//     // Названия группы маркеров
//     name_marker: string;
//     // Координаты места [широта,долгота]
//     coord: [number, number];
// }
// export interface Tgeom_place_coord_list {
//     [key: NameGeom]: Tgeom_place_coord_list_item;
// }

// export interface Tgeom_place_coord {
//     [key: NameGeom]: Tgeom_place_coord_list;
// }

// ------------------------------------------------- //

// ----- channel_geomap ---------------------------------------- //

// export interface Tchannel_geomapJson_names_radius {
//     // По этому имени пользователи будут фильтровать "Имена точек радиуса".
//     hum: string;
//     // Путь к статическому файлу, который хранить в себе информацию обо всех местах в этом радиусе.
//     name_path: string;
//     // ID БД шарда, где храниться группа
//     shard: number;
// }



// export interface Tchannel_geomapJson {
//     // names_radius: {
//     //     [key: number]: Tchannel_geomapJson_names_radius;
//     // };
//     results: TChannelGeomap[];
// }


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
