#!/usr/bin/env python3.4
__author__ = 'rafal'

from gi.repository import Gtk
from gui.about_dialog import AboutDialog
from gui.settings_dialog import SettingsDialog
from gui.window_controller import WindowController


class ProgramView:

    def __init__(self):
        self.glade_file = "gui/main_window.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")

        # Główne widgety okna
        self.statusbar = self.builder.get_object("statusbar")
        self.context_id = self.statusbar.get_context_id("status")
        self.main_image = self.builder.get_object("main_image")
        self.toolbar = self.builder.get_object("toolbar")

        # Elementy menu
        self.open_file_button = self.builder.get_object("open_file_button")
        self.open_camera_button = self.builder.get_object("open_camera_button")
        self.open_database_button = self.builder.get_object("open_database_button")
        self.run_alg_toggle_button = self.builder.get_object("run_alg")
        self.play_toggle_button = self.builder.get_object("play")
        self.pause_toggle_button = self.builder.get_object("pause")
        self.stop_button = self.builder.get_object("stop")
        self.record_toggle_button = self.builder.get_object("record")

        # Elementy potomne
        self.about_dialog = AboutDialog()
        self.settings_dialog = SettingsDialog()
        self.file_chooser_dialog = None


        # Konfiguracja widoczności elementów
        self.main_image.show()
        self.write_on_statusbar("Witaj podróżniku!")
        self.window.show()

        # Obiekt łączący algorytm z oknem
        self.controller = WindowController(self)


    def write_on_statusbar(self, text):
        self.statusbar.push(self.context_id, text)

    def enable_buttons(self):
        self.play_toggle_button.set_active(False)
        self.pause_toggle_button.set_active(True)
        self.play_toggle_button.set_sensitive(True)
        self.pause_toggle_button.set_sensitive(True)
        self.stop_button.set_sensitive(True)
        self.record_toggle_button.set_sensitive(True)
        self.run_alg_toggle_button.set_sensitive(True)
        self.open_file_button.set_sensitive(False)

    def disable_buttons(self):
        self.play_toggle_button.set_sensitive(False)
        self.pause_toggle_button.set_sensitive(False)
        self.stop_button.set_sensitive(False)
        self.record_toggle_button.set_sensitive(False)
        self.run_alg_toggle_button.set_sensitive(False)
        self.open_file_button.set_sensitive(True)

    def on_open_file_button_clicked(self, object, data=None):
        self.__create_file_chooser_dialog()
        response = self.file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            path = self.file_chooser_dialog.get_filename()
            self.controller.set_new_file(path)
            self.write_on_statusbar("Wybrano nowy plik " + path)
            self.enable_buttons()
            # self.main_image.clear()
        self.file_chooser_dialog.destroy()
        self.file_chooser_dialog = None

    def on_open_camera_button_clicked(self, object, data=None):
        # TODO
        self.write_on_statusbar("Wybierz kamerę")

    def on_open_database_clicked(self, object, data=None):
        #TODO
        self.write_on_statusbar("Wybierz bazę danych z samochodami")

    def on_play_toggled(self, object, data=None):
        is_pressed = self.play_toggle_button.get_active()
        self.pause_toggle_button.set_active(not is_pressed)
        if is_pressed:
            self.write_on_statusbar("Odtwarzanie")
            self.controller.play_file()

    def on_pause_toggled(self, object, data=None):
        is_pressed = self.pause_toggle_button.get_active()
        self.play_toggle_button.set_active(not is_pressed)
        if is_pressed:
            self.write_on_statusbar("Pauza")
        self.controller.pause_playing()

    def on_record_toggled(self, object, data=None):
        is_pressed = self.record_toggle_button.get_active()
        self.write_on_statusbar("Nagrywaj albo nie nagrywaj")

    def on_stop_clicked(self, object, data=None):
        self.pause_toggle_button.set_active(True)
        self.play_toggle_button.set_active(False)
        self.disable_buttons()
        self.controller.stop()
        self.main_image.clear()
        self.write_on_statusbar("Stop")

    def on_run_alg_toggled(self, object, data=None):
        self.write_on_statusbar("Uruchom algorytm albo nie uruchom")

    def on_about_button_clicked(self, object, data=None):
        self.write_on_statusbar("O programie")
        self.about_dialog.show()

    def on_documentation_button_clicked(self, object, data=None):
        self.write_on_statusbar("Dokumentacja")

    def on_settings_button_clicked(self, object, data=None):
        self.statusbar.push(self.context_id, "Ustawienia")
        self.settings_dialog.show()

    def on_exit_button_clicked(self, object, data=None):
        self.controller.exit()
        Gtk.main_quit()

    def on_main_window_destroy(self, object, data=None):
        self.controller.exit()
        Gtk.main_quit()

    def __create_file_chooser_dialog(self):
        if self.file_chooser_dialog is None:
            self.file_chooser_dialog = Gtk.FileChooserDialog("Open...", None, Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

if __name__ == "__main__":
    window = ProgramView()
    Gtk.main()



