import gi
import pytz
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TimeZoneWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Available Time Zones")
        self.set_border_width(10)
        self.set_default_size(300, 400)

        # Vertical box to hold widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Entry for filtering
        self.filter_entry = Gtk.Entry()
        self.filter_entry.set_placeholder_text("Type to filter time zones")
        vbox.pack_start(self.filter_entry, False, False, 0)

        # Create a TreeStore with one string column to store time zone data
        self.store = Gtk.ListStore(str)
        for tz in sorted(pytz.all_timezones):
            self.store.append([tz])

        # TreeModelFilter for filtering the TreeStore
        self.filter = self.store.filter_new()
        self.filter.set_visible_func(self.timezone_filter_func)

        # TreeView setup
        self.treeview = Gtk.TreeView(model=self.filter)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Time Zone", renderer, text=0)
        self.treeview.append_column(column)
        vbox.pack_start(self.treeview, True, True, 0)

        # Connect the entry signal
        self.filter_entry.connect("changed", self.on_filter_entry_changed)

        # Show all widgets
        self.show_all()

    def timezone_filter_func(self, model, iter, data):
        """Filter function that determines if the row should be shown."""
        if self.filter_entry.get_text() == '':
            return True
        else:
            return self.filter_entry.get_text().lower() in model[iter][0].lower()

    def on_filter_entry_changed(self, entry):
        """Called whenever the filter entry text is changed."""
        self.filter.refilter()

def main():
    win = TimeZoneWindow()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()
