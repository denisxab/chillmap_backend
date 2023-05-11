# pages

-   MapApp.vue = Главная страница с картой

# components

-   MapContainer.vue = Карта
-   OverBox.vue = Окно поверх краты
    -   ExtraFeaturesWindow.vue = Список дополнительных возможностей работы с картой
        -   AddPlace.vue = Создание нового места
-   FacileFromMarker.vue = Поверхностная информация о выбранном месте
    -   ParamsList.vue = Используется как список чем можно заняться в этом месте
-   DetailFromPlace.vue = Детальная информация о выбранном месте
    -   ParamsList.vue = Используется как список чем можно заняться в этом месте

# TS

-   helper.ts = Вспомогательные пере используемые функции
-   interface.ts = Хранилище интерфейсов
-   router.ts = Настройка роутинга SPA приложения
