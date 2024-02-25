import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('AppIndicator3', '0.1')
import psutil
import signal
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator


def update_usage(indicator, cpu_label, ram_label):
    ram_label.set_label(f"RAM: {psutil.virtual_memory().percent}%")
    cpu_percent = psutil.cpu_percent()
    cpu_label.set_label(f"CPU: {cpu_percent}%")
    indicator.set_label(f"CPU: {cpu_percent}% RAM: {psutil.virtual_memory().percent}%", "")
    return True


def quit_app(*args):
    Gtk.main_quit()

def main():
    indicator = appindicator.Indicator.new(
        "customtray",
        "indicator-messages",
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()

    item_quit = Gtk.MenuItem(label="Quit")
    item_quit.connect("activate", quit_app)
    menu.append(item_quit)

    cpu_label = Gtk.MenuItem(label=f"CPU: {psutil.cpu_percent()}%")
    ram_label = Gtk.MenuItem(label=f"RAM: {psutil.virtual_memory().percent}%")
    menu.append(cpu_label)
    menu.append(ram_label)

    menu.show_all()
    indicator.set_menu(menu)

    GLib.timeout_add_seconds(1, update_usage, indicator, cpu_label, ram_label)

    Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()


