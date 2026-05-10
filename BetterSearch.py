"""
MIT License

Copyright (c) 2026 ItsLuckyLike

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
import platform
import subprocess
import threading
import ctypes
import re
import time
import hashlib
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# -- Colour Palette -------------------------------------------------------------
BG = "#101010"   # main background
BG_PANEL = "#202020"   # label-frame panels
BG_INPUT = "#000000"   # entry / combo fields
FG = "#c9d1d9"
FG_DIM = "#acbacc"
GREEN = "#3fb950"
GREEN_HI = "#56d364"
BORDER = "#303830"
SEL_BG = "#1f6feb"
# TAG_ODD = "#080808"
# TAG_EVEN = "#181818"

SETTINGS_FILE = re.sub(".py", ".settings.json", str(os.path.realpath(__file__)))

ICON_B64 = "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"

def fmt_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def fmt_date(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def get_ctime(st):
    return getattr(st, "st_birthtime", st.st_ctime)


def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def apply_dark_theme(root):
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=BG, foreground=FG, font=("Consolas", 9), bordercolor=BORDER, darkcolor=BG, lightcolor=BG)
    s.configure("TFrame", background=BG)
    s.configure("TLabelframe", background=BG_PANEL, foreground=GREEN, bordercolor=BORDER, relief="groove")
    s.configure("TLabelframe.Label", background=BG, foreground=GREEN, font=("Consolas", 9, "bold"))
    s.configure("TLabel", background=BG, foreground=FG)
    s.configure("TEntry", fieldbackground=BG_INPUT, foreground=FG, insertcolor=GREEN, bordercolor=BORDER, selectbackground=SEL_BG)
    s.configure("TCombobox", fieldbackground=BG_INPUT, foreground=FG, selectbackground=SEL_BG, bordercolor=BORDER, arrowcolor=GREEN)
    s.map("TCombobox", fieldbackground=[("readonly", BG_INPUT)], foreground=[("readonly", FG)], selectbackground=[("readonly", SEL_BG)])
    s.configure("TCheckbutton", background=BG_PANEL, foreground=FG)
    s.map("TCheckbutton", background=[("active", BG_PANEL)], foreground=[("active", GREEN)])
    s.configure("TButton", background=BG_INPUT, foreground=GREEN, bordercolor=BORDER, padding=5)
    s.map("TButton", background=[("active", "#141414"), ("disabled", BG)], foreground=[("disabled", FG_DIM)])
    s.configure("TScrollbar", background=BG_PANEL, troughcolor=BG_INPUT, bordercolor=BORDER, arrowcolor=FG_DIM)
    s.configure("TSeparator", background=BORDER)
    s.configure("TProgressbar", background=GREEN, troughcolor=BG_INPUT, bordercolor=BORDER)
    s.configure("Treeview", background=BG_INPUT, foreground=FG, fieldbackground=BG_INPUT, bordercolor=BORDER, rowheight=20, font=("Consolas", 9))
    s.configure("Treeview.Heading", background=BG_PANEL, foreground=GREEN, font=("Consolas", 9, "bold"), relief="flat")
    s.map("Treeview", background=[("selected", SEL_BG)], foreground=[("selected", FG)])
    root.configure(background=BG)


class BetterSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("BetterSearch")
        self.root.geometry("1600x860")
        self.target_folder = ""
        self.is_searching = False
        self.stop_requested = False
        self.files_processed = 0
        apply_dark_theme(root)
        self.build_ui()
        self.load_settings()
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    # --------------- UI BUILD ---------------------------------------------------
    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=4)
        self.root.rowconfigure(0, weight=1)

        # -- LEFT PANEL ----------------------------------------------------------
        left_frame = ttk.LabelFrame(self.root, text="Source", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.license = ttk.Label(left_frame, text="Copyright (c) 2026 ItsLuckyLike", wraplength=150, foreground=FG_DIM, background=BG_PANEL)
        self.license.pack(side="bottom", fill=tk.X, pady=5)

        ttk.Button(left_frame, text="Browse Folder", command=self.select_folder).pack(fill=tk.X)
        self.lbl_folder = ttk.Label(left_frame, text="No folder selected", wraplength=150, foreground=FG_DIM, background=BG_PANEL)
        self.lbl_folder.pack(fill=tk.X, pady=10)
        ttk.Separator(left_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="Export Results", command=self.export_results).pack(fill=tk.X, pady=2)

        # -- MIDDLE PANEL (scrollable canvas) ------------------------------------
        mid_canvas = tk.Canvas(self.root, highlightthickness=0, background=BG, width=280)
        mid_scroll = ttk.Scrollbar(self.root, orient="vertical", command=mid_canvas.yview)
        scroll_frame = ttk.Frame(mid_canvas)
        scroll_frame.bind("<Configure>", lambda e: mid_canvas.configure(scrollregion=mid_canvas.bbox("all")))
        mid_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        mid_canvas.configure(yscrollcommand=mid_scroll.set)
        mid_canvas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        mid_scroll.grid(row=0, column=1, sticky="nse")
        mid_canvas.bind_all("<MouseWheel>", lambda e: mid_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # -- Basic Filters ------------------------------------------------------
        core_grp = ttk.LabelFrame(scroll_frame, text="Basic Filters", padding=10)
        core_grp.pack(fill=tk.X, padx=5, pady=5)

        self.add_label(core_grp, "Search For:")
        self.cb_file_type = self.add_combo(core_grp, ["File", "Folder", "Both"], "File")

        self.add_label(core_grp, "Name Pattern:")
        self.ent_name = self.add_entry(core_grp, "*")
        self.var_name_regex = tk.BooleanVar(value=False)
        ttk.Checkbutton(core_grp, text="Disable regex", variable=self.var_name_regex).pack(anchor="w", pady=(0, 5))

        self.add_label(core_grp, "Exclude Names (semicolon separated):")
        self.ent_exclude = self.add_entry(core_grp, ".*")

        self.add_label(core_grp, "Extensions  (.py;.txt = include  -.exe = exclude):")
        self.ent_ext = self.add_entry(core_grp, "")

        ttk.Separator(core_grp, orient="horizontal").pack(fill=tk.X, pady=5)
        self.add_label(core_grp, "File Content Filter:")
        self.cb_cont_mode = self.add_combo(
            core_grp, ["Disabled", "Contains", "Does Not Contain", "Matches Regex"], "Disabled")
        self.ent_cont_text = self.add_entry(core_grp, "")

        # -- File Attributes ----------------------------------------------------
        meta_grp = ttk.LabelFrame(scroll_frame, text="File Attributes", padding=10)
        meta_grp.pack(fill=tk.X, padx=5, pady=5)

        self.add_label(meta_grp, "Min Size (kB):")
        self.ent_min_size = self.add_entry(meta_grp, "0")
        self.add_label(meta_grp, "Max Size (kB, 0 = disabled):")
        self.ent_max_size = self.add_entry(meta_grp, "0")
        self.add_label(meta_grp, "Modified within last # days (0 = disabled):")
        self.ent_days = self.add_entry(meta_grp, "0")
        self.add_label(meta_grp, "Created* within last # days (0 = disabled):")
        self.ent_cdays = self.add_entry(meta_grp, "0")
        ttk.Label(meta_grp, text="* Linux: metadata-change time, not birth time.", foreground=FG_DIM, font=("Consolas", 8), background=BG_PANEL).pack(anchor="w", pady=(0, 2))

        # -- Search Settings ----------------------------------------------------
        srch_grp = ttk.LabelFrame(scroll_frame, text="Search Settings", padding=10)
        srch_grp.pack(fill=tk.X, padx=5, pady=5)

        self.add_label(srch_grp, "Max Depth (0 = unlimited):")
        self.ent_depth = self.add_entry(srch_grp, "0")

        # -- Sibling Constraints ------------------------------------------------
        fell_grp = ttk.LabelFrame(scroll_frame, text="Sibling Constraints", padding=10)
        fell_grp.pack(fill=tk.X, padx=5, pady=5)

        self.cb_fell_type = self.add_combo(
            fell_grp, ["Disabled", "Has Sibling File", "Has Sibling Folder", "No Sibling File", "No Sibling Folder"], "Disabled")
        self.add_label(fell_grp, "Sibling Name Pattern:")
        self.ent_fell_name = self.add_entry(fell_grp, "*")
        self.add_label(fell_grp, "Sibling Content Filter:")
        self.cb_fell_cont_mode = self.add_combo(
            fell_grp, ["Disabled", "Contains", "Does Not Contain", "Matches Regex"], "Disabled")
        self.ent_fell_cont_text = self.add_entry(fell_grp, "")

        # -- Search Controls ----------------------------------------------------
        btn_container = ttk.Frame(scroll_frame)
        btn_container.pack(fill=tk.X, pady=10, padx=5)
        btn_container.columnconfigure(0, weight=70)
        btn_container.columnconfigure(1, weight=30)

        self.btn_search = ttk.Button(btn_container, text="▶  Start Search", command=self.start_search_thread)
        self.btn_search.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        self.btn_dupes = ttk.Button(btn_container, text="⊕  Dupes", command=self.start_dupe_thread)
        self.btn_dupes.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        self.progress = ttk.Progressbar(scroll_frame, orient="horizontal", mode="indeterminate")
        self.progress.pack(fill=tk.X, padx=5, pady=(5, 2))
        self.lbl_counter = ttk.Label(scroll_frame, text=f"Found: 0  /  Scanned: 0", foreground=GREEN, background=BG)
        self.lbl_counter.pack()

        # -- RIGHT PANEL --------------------------------------------------------
        right_frame = ttk.LabelFrame(self.root, text="Results", padding=5)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        cols = ("size", "created", "modified")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="tree headings", selectmode="browse")
        self.tree.heading("#0", text="Path", anchor="w")
        self.tree.heading("size", text="Size", anchor="e")
        self.tree.heading("created", text="Created*", anchor="w")
        self.tree.heading("modified", text="Modified", anchor="w")
        self.tree.column("#0", width=420, stretch=True)
        self.tree.column("size", width=75, stretch=False, anchor="e")
        self.tree.column("created", width=130, stretch=False)
        self.tree.column("modified", width=130, stretch=False)

        # self.tree.tag_configure("dup_odd", background=TAG_ODD)
        # self.tree.tag_configure("dup_even", background=TAG_EVEN)
        self.tree.tag_configure("group", foreground=GREEN, font=("Consolas", 9, "bold"))

        vsb = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(right_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<Double-1>", lambda e: self.open_selected())

        self.ctx_menu = tk.Menu(self.root, tearoff=0, bg=BG_INPUT, fg=FG, activebackground=SEL_BG, activeforeground=FG, font=("Consolas", 9))
        self.ctx_menu.add_command(label="Open Location", command=self.open_selected)
        self.ctx_menu.add_command(label="Copy Full Path", command=self.copy_path)
        self.ctx_menu.add_command(label="Copy Filename", command=self.copy_filename)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.txt_log = tk.Text(right_frame, height=3, state=tk.DISABLED, background=BG_INPUT, foreground=FG_DIM, insertbackground=GREEN, font=("Consolas", 8), borderwidth=0)
        self.txt_log.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    # -- UI Helpers --------------------------------------------------------------
    def add_label(self, parent, text):
        ttk.Label(parent, text=text, foreground=FG_DIM, background=BG_PANEL).pack(anchor="w")

    def add_entry(self, parent, default):
        e = ttk.Entry(parent)
        e.insert(0, default)
        e.pack(fill=tk.X, pady=(0, 5))
        return e

    def add_combo(self, parent, vals, default):
        c = ttk.Combobox(parent, values=vals, state="readonly")
        c.set(default)
        c.pack(fill=tk.X, pady=(0, 5))
        return c

    def log(self, msg):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, f"> {msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    # -- Folder ------------------------------------------------------------------
    def select_folder(self):
        f = filedialog.askdirectory()
        if f:
            self.target_folder = f
            self.lbl_folder.config(text=f, foreground=GREEN)

    # -- Result Interaction ------------------------------------------------------
    def _focused_path(self):
        sel = self.tree.focus()
        if not sel:
            return None
        if self.tree.get_children(sel) and not self.tree.parent(sel):
            return None  # group header node
        text = self.tree.item(sel, "text")
        return Path(text) if text else None

    def open_selected(self):
        path = self._focused_path()
        if not path:
            return
        d = path.parent if path.is_file() else path
        if platform.system() == "Windows":
            os.startfile(d)
        else:
            subprocess.Popen(["xdg-open" if platform.system() == "Linux" else "open", str(d)])

    def copy_path(self):
        p = self._focused_path()
        if p:
            self.root.clipboard_clear()
            self.root.clipboard_append(str(p))

    def copy_filename(self):
        p = self._focused_path()
        if p:
            self.root.clipboard_clear()
            self.root.clipboard_append(p.name)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.focus(item)
            self.tree.selection_set(item)
            self.ctx_menu.post(event.x_root, event.y_root)

    # -- Export ------------------------------------------------------------------
    def export_results(self):
        if not self.tree.get_children():
            return messagebox.showinfo("Export", "No results to export.")
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text File", "*.txt"), ("CSV", "*.csv")])
        if not save_path:
            return
        with open(save_path, "w", encoding="utf-8") as f:
            for item in self.tree.get_children():
                children = self.tree.get_children(item)
                if children:
                    f.write(f"\n{self.tree.item(item, 'text')}\n")
                    for child in children:
                        vals = "\t".join(self.tree.item(child, "values"))
                        f.write(f"  {self.tree.item(child, 'text')}\t{vals}\n")
                else:
                    vals = "\t".join(self.tree.item(item, "values"))
                    f.write(f"{self.tree.item(item, 'text')}\t{vals}\n")
        self.log(f"Exported → {Path(save_path).name}")

    # -- Persistent Settings -----------------------------------------------------
    def _set_entry(self, widget, val):
        widget.delete(0, tk.END)
        widget.insert(0, val)

    def save_settings(self):
        settings = {
            "target_folder": self.target_folder,
            "file_type": self.cb_file_type.get(),
            "name_pattern": self.ent_name.get(),
            "use_regex": self.var_name_regex.get(),
            "exclude": self.ent_exclude.get(),
            "ext_filter": self.ent_ext.get(),
            "cont_mode": self.cb_cont_mode.get(),
            "cont_text": self.ent_cont_text.get(),
            "min_size": self.ent_min_size.get(),
            "max_size": self.ent_max_size.get(),
            "days_mod": self.ent_days.get(),
            "days_crt": self.ent_cdays.get(),
            "max_depth": self.ent_depth.get(),
            "fell_type": self.cb_fell_type.get(),
            "fell_name": self.ent_fell_name.get(),
            "fell_cont_mode": self.cb_fell_cont_mode.get(),
            "fell_cont_text": self.ent_fell_cont_text.get(),
            }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
        except Exception:
            pass

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                s = json.load(f)
        except Exception:
            return
        if s.get("target_folder"):
            self.target_folder = s["target_folder"]
            self.lbl_folder.config(text=self.target_folder, foreground=GREEN)
        self.cb_file_type.set(s.get("file_type", "File"))
        self._set_entry(self.ent_name, s.get("name_pattern", "*"))
        self.var_name_regex.set(s.get("use_regex", False))
        self._set_entry(self.ent_exclude, s.get("exclude", ".*"))
        self._set_entry(self.ent_ext, s.get("ext_filter", ""))
        self.cb_cont_mode.set(s.get("cont_mode", "Disabled"))
        self._set_entry(self.ent_cont_text, s.get("cont_text", ""))
        self._set_entry(self.ent_min_size, s.get("min_size", "0"))
        self._set_entry(self.ent_max_size, s.get("max_size", "0"))
        self._set_entry(self.ent_days, s.get("days_mod", "0"))
        self._set_entry(self.ent_cdays, s.get("days_crt", "0"))
        self._set_entry(self.ent_depth, s.get("max_depth", "0"))
        self.cb_fell_type.set(s.get("fell_type", "Disabled"))
        self._set_entry(self.ent_fell_name, s.get("fell_name", "*"))
        self.cb_fell_cont_mode.set(s.get("fell_cont_mode", "Disabled"))
        self._set_entry(self.ent_fell_cont_text, s.get("fell_cont_text", ""))

    def on_close(self):
        self.save_settings()
        self.root.destroy()

    # -- Thread Lifecycle --------------------------------------------------------
    def request_stop(self):
        if self.is_searching:
            self.stop_requested = True
            self.log("Stopping...")
            self.btn_search.config(state=tk.DISABLED)
            self.btn_dupes.config(state=tk.DISABLED)

    def _start_thread(self, target):
        if not self.target_folder:
            return messagebox.showwarning("!", "Select a folder first.")
        self.is_searching = True
        self.stop_requested = False
        # Both buttons transform into stop buttons
        self.btn_search.config(text="■  Stop", command=self.request_stop)
        self.btn_dupes.config(text="■  Stop", command=self.request_stop)
        self.tree.delete(*self.tree.get_children())
        self.files_processed = 0
        self.progress.start(1)
        threading.Thread(target=target, daemon=True).start()

    def _end_thread(self):
        self.progress.stop()
        self.btn_search.config(text="▶  Start Search", command=self.start_search_thread, state=tk.NORMAL)
        self.btn_dupes.config(text="⊕  Dupes", command=self.start_dupe_thread, state=tk.NORMAL)
        self.is_searching = False
        self.stop_requested = False

    # -- Search ------------------------------------------------------------------
    def start_search_thread(self):
        self._start_thread(self.run_search)

    def _parse_ext_filter(self):
        """Return (include_set, exclude_set) from the extension field.
        Entries starting with '-' go into exclude; all others into include.
        """
        raw = [x.strip().lower() for x in self.ent_ext.get().split(";") if x.strip()]
        include = {e for e in raw if not e.startswith("-")}
        exclude = {e.lstrip("-") for e in raw if e.startswith("-")}
        return include, exclude

    def run_search(self):
        try:
            root_path = Path(self.target_folder)
            found_count = 0
            results_buffer = []
            # Pre-read all filter params (avoid per-iter tkinter calls)
            t_pref = self.cb_file_type.get()
            name_pattern = self.ent_name.get()
            use_regex = self.var_name_regex.get()  # True → re.search, False → glob
            exclude_list = [x.strip() for x in self.ent_exclude.get().split(";") if x.strip()]
            ext_inc, ext_exc = self._parse_ext_filter()
            min_sz = float(self.ent_min_size.get() or 0) * 1024
            max_sz = float(self.ent_max_size.get() or 0) * 1024
            days_mod = float(self.ent_days.get() or 0) * 86400
            days_crt = float(self.ent_cdays.get() or 0) * 86400
            max_depth = int(self.ent_depth.get() or 0)
            root_depth = str(root_path).count(os.sep)  # used for fast depth check
            now = time.time()
            c_mode = self.cb_cont_mode.get()
            c_text = self.ent_cont_text.get()
            f_mode = self.cb_fell_type.get()
            fc_mode = self.cb_fell_cont_mode.get()
            fell_name = self.ent_fell_name.get()
            fc_text = self.ent_fell_cont_text.get()

            self.log("Searching...")

            for item in root_path.rglob("*"):
                if self.stop_requested:
                    self.log("Search aborted.")
                    break

                # Depth — fast string-count, no Path object creation
                if max_depth > 0:
                    if str(item).count(os.sep) - root_depth > max_depth:
                        continue

                self.files_processed += 1
                if self.files_processed % 250 == 0:
                    self.lbl_counter.config(text=f"Found: {found_count}  /  Scanned: {self.files_processed}")

                # 1. Type
                is_file = item.is_file()
                is_dir = not is_file
                if t_pref == "File" and is_dir: continue
                if t_pref == "Folder" and is_file: continue

                # 2. Name pattern
                if use_regex:
                    try:
                        if not re.search(name_pattern, item.name): continue
                    except: continue
                else:
                    if not item.match(name_pattern): continue

                # 3. Exclusions
                if any(ex in item.name for ex in exclude_list): continue

                # 4. Extension filter (include/exclude)
                if is_file:
                    suf = item.suffix.lower()
                    if ext_inc and suf not in ext_inc: continue
                    if ext_exc and suf in ext_exc: continue

                # 5. Size / date
                size_str = ctime_str = mtime_str = ""
                if is_file:
                    try:
                        st = item.stat()
                        if min_sz   > 0 and st.st_size < min_sz: continue
                        if max_sz   > 0 and st.st_size > max_sz: continue
                        if days_mod > 0 and (now - st.st_mtime) > days_mod: continue
                        if days_crt > 0 and (now - get_ctime(st)) > days_crt: continue
                        size_str = fmt_size(st.st_size)
                        ctime_str = fmt_date(get_ctime(st))
                        mtime_str = fmt_date(st.st_mtime)
                    except: continue

                # 6. Content check
                if c_mode != "Disabled" and is_file:
                    try:
                        with open(item, "r", encoding="utf-8", errors="ignore") as fh:
                            body = fh.read()
                            if c_mode == "Contains" and c_text not in body: continue
                            if c_mode == "Does Not Contain" and c_text in body: continue
                            if c_mode == "Matches Regex" and not re.search(c_text, body): continue
                    except:
                        self.log(f"Skipped (read error): {item.name}")
                        continue

                # 7. Sibling check
                if f_mode != "Disabled" or fc_mode != "Disabled":
                    siblings = list(item.parent.glob(fell_name))
                    has_file_list = [s for s in siblings if s.is_file() and s != item]
                    has_dir_list = [s for s in siblings if s.is_dir() and s != item]

                    if f_mode == "Has Sibling File" and not has_file_list: continue
                    if f_mode == "Has Sibling Folder" and not has_dir_list: continue
                    if f_mode == "No Sibling File" and has_file_list: continue
                    if f_mode == "No Sibling Folder" and has_dir_list: continue

                    if fc_mode != "Disabled":
                        match_found = False
                        for s_file in has_file_list:
                            try:
                                with open(s_file, "r", encoding="utf-8", errors="ignore") as fh:
                                    s_body = fh.read()
                                    if fc_mode == "Contains" and fc_text in s_body: match_found = True
                                    elif fc_mode == "Does Not Contain" and fc_text not in s_body: match_found = True
                                    elif fc_mode == "Matches Regex" and re.search(fc_text, s_body): match_found = True
                                    if match_found: break
                            except: continue
                        if not match_found: continue

                # ✓ All filters passed
                found_count += 1
                results_buffer.append((str(item), size_str, ctime_str, mtime_str))

            self.log(f"Loading {found_count} matches.")
            self.lbl_counter.config(text=f"Loading {found_count} matches.")
            for row in results_buffer:
                self.tree.insert("", tk.END, text=row[0], values=row[1:])
            results_buffer.clear()
            self.log(f"Done. {found_count} matches  /  {self.files_processed} scanned.")
            self.lbl_counter.config(text=f"Found: {found_count}  /  Scanned: {self.files_processed}")

        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self._end_thread()

    # -- Find Duplicates ---------------------------------------------------------
    def start_dupe_thread(self):
        self._start_thread(self.run_find_dupes)

    def run_find_dupes(self):
        try:
            root_path = Path(self.target_folder)

            # Stage 1: group by size — no hashing yet
            self.log("Grouping by size...")
            size_map = {}
            for item in root_path.rglob("*"):
                if self.stop_requested: break
                if not item.is_file(): continue
                self.files_processed += 1
                if self.files_processed % 250 == 0:
                    self.lbl_counter.config(text=f"Scanned: {self.files_processed}")
                try:
                    size_map.setdefault(item.stat().st_size, []).append(item)
                except: continue

            if self.stop_requested:
                self.log("Aborted.")
                return

            # Stage 2: MD5-hash only size-collision candidates
            candidates = [f for files in size_map.values() if len(files) > 1 for f in files]
            self.log(f"Hashing {len(candidates)} candidates...")
            hash_map = {}
            for i, item in enumerate(candidates):
                if self.stop_requested: break
                try:
                    h = file_hash(item)
                    hash_map.setdefault(h, []).append(item)
                except: continue
                if i % 50 == 0:
                    self.lbl_counter.config(text=f"Hashed: {i} / {len(candidates)}")

            dupes = {h: files for h, files in hash_map.items() if len(files) > 1}

            if not dupes:
                self.log("No duplicates found.")
                return

            redundant = sum(len(v) - 1 for v in dupes.values())
            self.log(f"Found {len(dupes)} duplicate groups  ({redundant} redundant files).")
            self.lbl_counter.config(text=f"Duplicate groups: {len(dupes)}")

            for i, (_, files) in enumerate(sorted(dupes.items())):
                if self.stop_requested:
                    self.log("Aborted.")
                    return
                
                try:
                    sz_str = fmt_size(files[0].stat().st_size)
                except:
                    sz_str = "?"
                group_node = self.tree.insert(
                    "", tk.END, text=f"Group {i + 1}  ·  {len(files)} files  ·  {sz_str} each", tags=("group",), open=False)
                for f in files:
                    try:
                        st = f.stat()
                        size_str = fmt_size(st.st_size)
                        ctime_str = fmt_date(get_ctime(st))
                        mtime_str = fmt_date(st.st_mtime)
                    except:
                        size_str = ctime_str = mtime_str = ""
                    self.tree.insert(group_node, tk.END, text=str(f), values=(size_str, ctime_str, mtime_str))

            # self.tree.tag_configure("dup_odd", background=TAG_ODD)
            # self.tree.tag_configure("dup_even", background=TAG_EVEN)
        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self._end_thread()


if __name__ == "__main__":
    root = tk.Tk()
    icon = tk.PhotoImage(data=ICON_B64)
    root.iconphoto(True, icon)
    app = BetterSearch(root)
    root.mainloop()
