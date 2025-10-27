import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)


    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField(label="Marca", width=200)
    input_modello = ft.TextField(label="Modello", width=200)
    input_anno = ft.TextField(label="Anno", width=200)

    textOut = ft.TextField(width=100, text_size=24,
                           disabled=True, border_color="green",
                           text_align=ft.TextAlign.CENTER)

    textOut.value = 0

    def handlerMinus(e):
        currentVal = int(textOut.value)
        if (currentVal > 0):
            currentVal = currentVal - 1
            textOut.value = str(currentVal)
            textOut.update()

    def handlerPlus(e):
        currentVal = int(textOut.value)
        currentVal = currentVal + 1
        textOut.value = str(currentVal)
        textOut.update()

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_ROUNDED,
                             icon_size=24, icon_color="green",
                             on_click=handlerMinus)
    btnPlus = ft.IconButton(icon=ft.Icons.ADD_CIRCLE_ROUNDED,
                            icon_size=24, icon_color="green",
                            on_click=handlerPlus)

    button_posti = ft.Row([ft.Text("Posti:"),btnMinus, textOut, btnPlus],
                 alignment=ft.MainAxisAlignment.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def aggiungi_automobile(e):
        marca = input_marca.value
        modello = input_modello.value
        anno_str = input_anno.value
        posti_str = textOut.value

        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno_str, posti_str)

            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""
            textOut.value = ""

            aggiorna_lista_auto()

            page.update()
        except Exception as ex:
            alert.show_alert(f"Errore durante l'aggiunta: {ex}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    btn_aggiungi_auto = ft.ElevatedButton("Conferma", on_click=aggiungi_automobile)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi Nuova Automobile", size=20),
        ft.Row([input_marca,input_modello,input_anno,button_posti]),
        btn_aggiungi_auto,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
