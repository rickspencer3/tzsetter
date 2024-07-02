import gi
import pytz
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import time
import subprocess



class TimeZoneWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Available Time Zones")

        self.current_timezone = get_current_timezone()
        self._set_window_dimensions()
        self._add_main_window_view()
        self._add_current_timezone_info()
        self._add_filter_ui()
        self._set_up_liststore()
        self._add_treeview_scroller()
        self._set_up_treeview()
        self.show_all()

    def _set_up_treeview(self):
        self.treeview = Gtk.TreeView(model=self.filter)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Time Zone", renderer, text=0)
        self.treeview.append_column(column)
        

        column.set_cell_data_func(renderer, self.highlight_func)
        self.filter_entry.connect("changed", self.on_filter_entry_changed)
        self.scrolled_window.add(self.treeview)

    def _add_treeview_scroller(self):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True) 

        self.vbox.pack_start(self.scrolled_window, True, True, 0)

    def _set_up_liststore(self):
        self.store = Gtk.ListStore(str)
        for tz in sorted(pytz.all_timezones):
            self.store.append([tz])

        self.filter = self.store.filter_new()
        self.filter.set_visible_func(self.timezone_filter_func)

    def _add_filter_ui(self):
        self.filter_entry = Gtk.Entry()
        self.filter_entry.set_placeholder_text("Type to filter time zones")
        self.vbox.pack_start(self.filter_entry, False, False, 0)

    def _add_current_timezone_info(self):
        tz_label = Gtk.Label(label="Current:")

        current_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        current_box.pack_start(tz_label, True, True, 0)

        self._set_current_timezone_label()
        current_box.pack_end(self.tz_text, True, True, 0)

        self.vbox.add(current_box)
        return current_box

    def _set_current_timezone_label(self):
        self.tz_text = Gtk.Label(label=self.current_timezone)

    def _add_main_window_view(self):
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)
        return self.vbox

    def _set_window_dimensions(self):
        self.set_border_width(10)
        self.set_default_size(600, 400)


    def timezone_filter_func(self, model, iter, data):
        """Filter function that determines if the row should be shown."""
        if self.filter_entry.get_text() == '':
            return True
        else:
            return self.filter_entry.get_text().lower() in model[iter][0].lower()

    def on_filter_entry_changed(self, entry):
        """Called whenever the filter entry text is changed."""
        self.filter.refilter()

    def highlight_func(self, column, cell, model, iter, data):
        # Apply highlight to the row that matches the current timezone
        if model[iter][0] == self.current_timezone:
            cell.set_property('background', 'lightblue')
            cell.set_property('foreground', 'black')
        else:
            cell.set_property('background', 'white')
            cell.set_property('foreground', 'black')


def get_current_timezone():
    try:
        # Run the 'timedatectl' command and capture the output
        result = subprocess.run(['timedatectl'], stdout=subprocess.PIPE)

        # Decode the output from bytes to string and split into lines
        output = result.stdout.decode('utf-8').split('\n')

        # Loop through each line to find the time zone
        for line in output:
            if "Time zone" in line:
                # Extract the time zone part after the colon
                timezone = line.split(':')[1].strip()
                return timezone.split(' ')[0]  # Return just the time zone identifier
    except Exception as e:
        print("Failed to get timezone:", e)
        return None


def main():
    win = TimeZoneWindow()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()
