import { TPropertiesMark } from "./interface";

// Если в URL нет `@/`, то оставляет его без изменений
export function ParseUrlSrc(url_src: string) {
    // @ts-ignore
    return url_src.replace("@/", ENV_default_host_to_src);
}

// Если в URL нет `@/`, то оставляет его без изменений
export function ParseUrlBackend(url_src: string) {
    // @ts-ignore
    return url_src.replace("@/", ENV_default_host_to_backend);
}

// Интерфейс для данных, полученных из URL
export interface TFromUrl {
    data: any;
    ok: boolean;
    status: number;
}

// Загрузка данных по указанному URL методом GET
export async function DownloadFromUrl(url_src: string): Promise<TFromUrl> {
    const response = await fetch(url_src, {
        method: "GET",
    });
    return { data: await response.json(), ok: response.ok, status: response.status };
}

// Отправка данных методом POST в формате JSON на указанный URL
export async function PostJsonFromUrl(url_src: string, data: any): Promise<TFromUrl> {
    const response: Response = await fetch(url_src, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json"
        }
    });
    return { data: await response.text(), ok: response.ok, status: response.status };
}

// Копирование объекта
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

// Конвертирование id в понятные имена для whattodo
export function whattodoIdFromName(newValue: TPropertiesMark): string[] {
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
        return response.data.display_name;
    } else {
        console.error(`Ошибка при получении адреса по координатам: ${lat} ${lon}`);
    }
}
