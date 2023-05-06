// Преобразовать url изображения в формате `@/` на путь который указан в `ENV_default_host_to_src`

import { TPropertiesMark } from "./interface";

// Если в url нет `@/` то тогда оставить его без изменений
export function ParseUrlSrc(url_src: string) {
    // @ts-ignore
    return url_src.replace("@/", ENV_default_host_to_src);
}

// Скачать статический файл указанному URL
export interface TDownloadStatic {
    text: Promise<string>;
    ok: boolean;
    status: number;
}
export async function DownloadStatic(url_src: string) {
    const response = await fetch(url_src, {
        method: "GET",
    });
    return { text: response.text(), ok: response.ok, status: response.status };
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
    geom_whattodo_det: { [key: number]: string }
): string[] {
    let whattodo: string[] = [];
    if (newValue && newValue["whattodo"]) {
        for (let i of newValue["whattodo"]) {
            whattodo.push(geom_whattodo_det[i]);
        }
    }
    return whattodo;
}
