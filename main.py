import gi
gi.require_version('Gtk', '3.0') # noqa
gi.require_version('GLib', '2.0') # noqa
gi.require_version('AppIndicator3', '0.1') # noqa
import psutil
import signal
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator


class SystemUsage:
    """Class to encapsulate system usage monitoring logic."""
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent()

    @staticmethod
    def get_ram_usage():
        return psutil.virtual_memory().percent


class SystemTrayApp:
    """Class to create and manage the system tray application."""
    def __init__(self):
        self.ram_label = None
        self.cpu_label = None
        self.indicator = appindicator.Indicator.new(
            "customtray", "indicator-messages", appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        self.setup_menu()

    def setup_menu(self):
        self.cpu_label = Gtk.MenuItem(label=f"CPU: Initializing...")
        self.ram_label = Gtk.MenuItem(label=f"RAM: Initializing...")
        self.menu.append(self.cpu_label)
        self.menu.append(self.ram_label)

        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self.quit)
        self.menu.append(item_quit)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def update_usage(self):
        cpu_usage = SystemUsage.get_cpu_usage()
        ram_usage = SystemUsage.get_ram_usage()
        self.cpu_label.set_label(f"CPU: {cpu_usage}%")
        self.ram_label.set_label(f"RAM: {ram_usage}%")
        self.indicator.set_label(f"CPU: {cpu_usage}% RAM: {ram_usage}%", "")
        return True

    def quit(self, *args):
        Gtk.main_quit()

    def run(self):
        GLib.timeout_add_seconds(1, self.update_usage)
        Gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = SystemTrayApp()
    app.run()
