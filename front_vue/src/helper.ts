// Преобразовать url изображения в формате `@/` на путь который указан в `ENV_default_host_to_src`

import { TPropertiesMark } from "./interface";

// Если в url нет `@/` то тогда оставить его без изменений
export function ParseUrlSrc(url_src: string) {
    // @ts-ignore
    return url_src.replace("@/", ENV_default_host_to_src);
}

// Если в url нет `@/` то тогда оставить его без изменений
export function ParseUrlBackend(url_src: string) {
    // @ts-ignore
    return url_src.replace("@/", ENV_default_host_to_backend);
}

// Скачать статический файл указанному URL
export interface TDownloadFromUrl {
    data: object;
    ok: boolean;
    status: number;
}
export async function DownloadFromUrl(url_src: string) {
    const response = await fetch(url_src, {
        method: "GET",
    });
    return { data: await response.json(), ok: response.ok, status: response.status };
}

// Копировать объект
export function clone(value) {
    if (Array.isArray(value)) {
        return value.map(clone);
    } else if (value && typeof value === "object") {
        const res = {};
        for (const key in value) {
            res[key] = clone(value[key]);
        }
        return res;
    } else {
        return value;
    }
}
// Конвертировать id в понятные имена для whattodo
export function whattodoIdFromName(
    newValue: TPropertiesMark,
): string[] {
    let whattodo: string[] = [];
    newValue.what_todo_obj.forEach(element => {
        whattodo.push(element.todo)
    });
    return whattodo;
}


// Функция для получения адреса по координатам
export async function getAddress(lat: string, lon: string): Promise<string> {
    const response = await DownloadFromUrl(
        `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`
    );
    if (response.ok) {
        return response.data.display_name
    }
    else {
        console.error(`Ошибка при получении адреса по координатам: ${lat} ${lon}`);
    }
}