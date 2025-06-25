import full_calendar_component as fcc
from dash import *
import dash
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from datetime import datetime, date, timedelta
import dash_quill
from TimeTable import TimeTable

dash._dash_renderer._set_react_version("18.2.0")

FILENAME = 'TimeTable.db'
TT = TimeTable(FILENAME)

app = Dash(__name__, prevent_initial_callbacks=True)

quill_mods = [
    [{"header": "1"}, {"header": "2"}, {"font": []}],
    [{"size": []}],
    ["bold", "italic", "underline", "strike", "blockquote"],
    [{"list": "ordered"}, {"list": "bullet"}, {"indent": "-1"}, {"indent": "+1"}],
    ["link", "image"],
]

# Get today's date
today = datetime.now()

# Format the date
formatted_date = today.strftime("%Y-%m-%d")

app.layout = html.Div(style={"width": "100%", "align-items": "center"},
    children=[
        dcc.Dropdown(list(TT.teachers.values()), placeholder="Преподаватель", id='teacher-select-dropdown',
                     multi=True),
        dcc.Dropdown(list(TT.classrooms.values()), placeholder="Аудитория", id='classroom-select-dropdown',
                     multi=True),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Button(
                "Показать",
                color="green",
                variant="outline",
                id="filter-button",
            )
            ]),

        # dmc.Space(h=20),




        fcc.FullCalendarComponent(
            id="calendar",  # Unique ID for the component
            initialView="timeGridDay",  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "listWeek,timeGridDay,timeGridWeek,dayGridMonth",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=TT.get_events(),
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
            businessHours= [{'daysOfWeek': [1, 2, 3]}]
        ),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="modal",
                    size="xl",
                    title="Event Details",
                    zIndex=10000,
                    children=[
                        html.Div(id="modal_event_display_context"),
                        dmc.Space(h=20),
                        #кнопка закрытия при просмотре события
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Закрыть",
                                    color="green",
                                    variant="outline",
                                    id="modal-close-button",
                                )
                            ],
                            align="start",
                        ),

                        dmc.Space(h=20),

                        #Кнопка удаления события
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Удалить",
                                    color="red",
                                    variant="outline",
                                    id="delete-event-button",
                                ),
                            ],
                            align="end",
                        ),
                    ],
                )
            ],
        ),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="add_modal",
                    title="Новое событие",
                    size="xl",
                    children=[
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    html.Div(
                                        dmc.DatePickerInput(
                                            id="start_date",
                                            label="Дата начала",
                                            value=str(datetime.now().date()),
                                            styles={"width": "100%"},
                                            disabled=True,
                                            required=True,
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    html.Div(
                                        dmc.TimeInput(
                                            label="Время начала",
                                            withSeconds=False,
                                            value="9:15",
                                            id="start_time",
                                            required=True,
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.Select(
                                            label="Выберете преподавателя",
                                            placeholder="Выберите",
                                            id="teacher_select",
                                            value=list(TT.teachers.values())[0],
                                            data=list(TT.teachers.values()),
                                            style={"width": "100%", "marginBottom": 10},
                                            required=True,
                                        )
                                    ],
                                ),
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.Select(
                                            label="Выберете аудиторию",
                                            placeholder="Выберите",
                                            id="classroom_input",
                                            value=list(map(str, TT.classrooms.values()))[0],
                                            data=list(map(str, TT.classrooms.values())),
                                            style={"width": "100%", "marginBottom": 10},
                                            required=True,
                                        )
                                    ],
                                ),                            ],
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    html.Div(
                                        dmc.DatePickerInput(
                                            id="end_date",
                                            label="Дата конца",
                                            value=datetime.now().date(),
                                            styles={"width": "100%"},
                                            required=True,
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    html.Div(
                                        dmc.TimeInput(
                                            label="Время конца",
                                            withSeconds=False,
                                            value=datetime.now(),
                                            id="end_time",
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),

                            ],
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.Select(
                                            label="Выберете дисциплину",
                                            placeholder="Выберите",
                                            id="event_name_input",
                                            value=list(TT.disciplines.values())[0],
                                            data=list(TT.disciplines.values()),
                                            style={"width": "100%", "marginBottom": 10},
                                            required=True,
                                        ),
                                    ],
                                ),


                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.Select(
                                            label="Выберете цвет события",
                                            placeholder="Фиолетовый",
                                            id="event_color_select",
                                            value="bg-gradient-primary",
                                            data=[
                                                {
                                                    "value": "bg-gradient-primary",
                                                    "label": "Фиолетовый",
                                                },
                                                {
                                                    "value": "bg-gradient-secondary",
                                                    "label": "Серый",
                                                },
                                                {
                                                    "value": "bg-gradient-success",
                                                    "label": "Бирюзовый",
                                                },
                                                {
                                                    "value": "bg-gradient-info",
                                                    "label": "Синий",
                                                },
                                                {
                                                    "value": "bg-gradient-warning",
                                                    "label": "Оранжевый",
                                                },
                                                {
                                                    "value": "bg-gradient-danger",
                                                    "label": "Красный",
                                                },
                                            ],
                                            style={"width": "100%", "marginBottom": 10},
                                            required=True,
                                        )
                                    ],
                                ),

                            ]
                        ),
                        dash_quill.Quill(
                            id="rich_text_input",
                            modules={
                                "toolbar": quill_mods,
                                "clipboard": {
                                    "matchVisual": False,
                                },
                            },
                        ),
                        dmc.Accordion(
                            children=[
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionPanel(
                                            html.Div(
                                                id="rich_text_output",
                                                style={
                                                    "height": "300px",
                                                    "overflowY": "scroll",
                                                },
                                            )
                                        ),
                                    ],
                                    value="raw_html",
                                ),
                            ],
                        ),
                        dmc.Space(h=20),

                        dmc.Group(
                            [
                                # Кнопка сохранить новое событие
                                dmc.Button(
                                    "Сохранить",
                                    id="modal_submit_new_event_button",
                                    color="green",
                                ),
                                # Кнопка закрыть окно нового события
                                dmc.Button(
                                    "Закрыть",
                                    color="red",
                                    variant="outline",
                                    id="modal_close_new_event_button",
                                ),
                            ],
                            align="right",
                        ),

                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("modal", "opened"),
    Output("modal", "title"),
    Output("modal_event_display_context", "children"),
    Input("modal-close-button", "n_clicks"),
    Input("calendar", "clickedEvent"),
    State("modal", "opened"),
)
def open_event_modal(n, clickedEvent, opened):    # Нажатие на событие
    # print("Просмотр события")
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]


    if button_id == "calendar" and clickedEvent is not None:
        event_title = clickedEvent["title"]
        event_context = clickedEvent["extendedProps"]["context"]
        return (
            True,
            event_title,
            html.Div(
                dash_quill.Quill(
                    id="input3",
                    value=f"{event_context}",
                    modules={
                        "toolbar": False,
                        "clipboard": {
                            "matchVisual": False,
                        },
                    },
                ),
                style={"width": "100%", "overflowY": "auto"},
            ),
        )
    elif button_id == "modal-close-button" and n is not None:
        return False, dash.no_update, dash.no_update

    return opened, dash.no_update


@app.callback(
    Output("calendar", "events", allow_duplicate=True),
    Input('delete-event-button', 'n_clicks'),
    State("calendar", "clickedEvent")
)
# Удаление события
def delete_event(n, clickedEvent):
    id = clickedEvent['extendedProps']['class_id']
    TT.delete_event(id)

    return TT.get_events()




@app.callback(
    Output("add_modal", "opened"),
    Output("start_date", "value"),
    Output("end_date", "value"),
    Output("start_time", "value"),
    Output("end_time", "value"),
    Input("calendar", "dateClicked"),
    Input("modal_close_new_event_button", "n_clicks"),
    State("add_modal", "opened"),
)
def open_add_modal(dateClicked, close_clicks, opened):   #окно создания нового события
    # print("Создание нового события")

    ctx = callback_context


    # if not ctx.triggered:
    #     raise PreventUpdate
    # else:
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "calendar" and dateClicked is not None:
        try:
            start_time = datetime.fromisoformat(dateClicked).time()
            start_date_obj = datetime.fromisoformat(dateClicked)
            start_date = start_date_obj.strftime("%Y-%m-%d")
            end_date = start_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            start_time = datetime.now().time()
            start_date_obj = datetime.fromisoformat(dateClicked)
            start_date = start_date_obj.strftime("%Y-%m-%d")
            end_date = start_date_obj.strftime("%Y-%m-%d")
        end_time = datetime.combine(date.today(), start_time) + timedelta(hours=1)
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M")
        end_time_str = end_time.strftime("%Y-%m-%d %H:%M")
        return True, start_date, end_date, start_time_str, end_time_str

    elif button_id == "modal_close_new_event_button" and close_clicks is not None:
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    return opened, dash.no_update, dash.no_update, dash.no_update, dash.no_update


@app.callback(
    Output("calendar", "events"),
    Output("add_modal", "opened", allow_duplicate=True),
    Output("event_name_input", "value"),
    Output("event_color_select", "value"),
    Output("rich_text_input", "value"),
    Input("modal_submit_new_event_button", "n_clicks"),
    State("start_date", "value"),
    State("start_time", "value"),
    State('teacher_select', 'value'),
    State('classroom_input', 'value'),
    State("end_date", "value"),
    State("end_time", "value"),
    State("event_name_input", "value"),
    State("event_color_select", "value"),
    State("rich_text_output", "children"),
    State("calendar", "events"),
    State('teacher-select-dropdown', 'value'),
    State('classroom-select-dropdown', 'value')
)

# Сохранения нового события
def add_new_event(
    n,
    start_date,
    start_time,
    teacher,
    classroom,
    end_date,
    end_time,
    event_name,
    event_color,
    event_context,
    current_events,
    teacher_select,
    classroom_select
):
    # print("Сохранения нового события")
    # if n is None:
    #     raise PreventUpdate
    start_time_obj = datetime.strptime(start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
    end_time_obj = datetime.strptime(end_date + ' ' + end_time, "%Y-%m-%d %H:%M")

    start_time_str = start_time_obj.strftime("%H:%M:%S")
    end_time_str = end_time_obj.strftime("%H:%M:%S")

    start_date = f"{start_date}T{start_time_str}"
    end_date = f"{end_date}T{end_time_str}"

    new_event = {
        'allDay': False,
        "title": event_name,
        "start": start_date,
        "end": end_date,
        "classNames": event_color,
        "extendedProps": {'context': event_context},
        'classroom': classroom,
        'teacher': teacher
    }
    TT.add_event(new_event)
    if not teacher_select and not classroom_select:
        return TT.get_events(), False, "", "bg-gradient-primary", ""
    elif not teacher_select:
        return [event for event in TT.get_events() if event['classroom'] in classroom_select], False, "", "bg-gradient-primary", ""
    elif not classroom_select:
        return [event for event in TT.get_events() if event['teacher'] in teacher_select], False, "", "bg-gradient-primary", ""
    else:
        return [event for event in TT.get_events() if event['teacher'] in teacher_select and event['classroom'] in classroom_select], False, "", "bg-gradient-primary", ""

@app.callback(
    Output("calendar", "events", allow_duplicate=True),
    Input('filter-button', 'n_clicks'),
    State('teacher-select-dropdown', 'value'),
    State('classroom-select-dropdown', 'value')
)
def teacher_classroom_filter(n, teacher, classroom):
    if not teacher and not classroom:
        return TT.get_events()
    elif not teacher:
        return [event for event in TT.get_events() if event['classroom'] in classroom]
    elif not classroom:
        return [event for event in TT.get_events() if event['teacher'] in teacher]
    else:
        return [event for event in TT.get_events() if event['teacher'] in teacher and event['classroom'] in classroom]



@app.callback(
    Output("rich_text_output", "children"),
    [Input("rich_text_input", "value")],
    [State("rich_text_input", "charCount")],
)
def display_output(value, charCount):
    return value


if __name__ == "__main__":
    app.run(debug=True, port=8056)
