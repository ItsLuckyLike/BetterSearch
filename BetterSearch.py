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

version = "1.1.0"

import os
import json
import platform
import subprocess
import threading
import ctypes
from ctypes import wintypes
import re
import time
import hashlib
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# -- Colour Palette -------------------------------------------------------------
BG = "#101010"   # main background
BG_PANEL = "#202020"   # label-frame panels
BG_INPUT = "#000000"   # entry / combo fields
FG = "#cddad3"
FG_DIM = "#acbacc"
GREEN = "#3fb950"
BORDER = "#303830"
SEL_BG = "#0B244A"
FILE_COPIED= "#86aedb"
FILE_RENAMED = "#ded4af"
FILE_DELETED = "#e6b0b0"
FILE_MOVED = "#707880"
FILE_RENAMED_STALE = "#707880"
# TAG_ODD = "#080808"
# TAG_EVEN = "#181818"

# -- Colour Palette (Light) ---------------------------------------------------
BG_L = "#f0f0f0"
BG_PANEL_L = "#e0e0e0"
BG_INPUT_L = "#ffffff"
FG_L = "#2a302b"
FG_DIM_L = "#57606a"
GREEN_L = "#1c883a"
BORDER_L = "#d0d7de"
SEL_BG_L = "#0B244A"
FILE_COPIED_L = "#1e55a2"
FILE_RENAMED_L = "#826401"
FILE_DELETED_L = "#92161e"
FILE_MOVED_L = "#57606a"
FILE_RENAMED_STALE_L = "#57606a"

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

def send_to_trash(paths):
    sys_name = platform.system()
    if sys_name == "Windows":
        p_from = "\x00".join(str(Path(p).resolve()) for p in paths) + "\x00\x00"
        
        class SHFILEOPSTRUCTW(ctypes.Structure):
            _fields_ = [
                ("hwnd", wintypes.HWND),
                ("wFunc", wintypes.UINT),
                ("pFrom", ctypes.c_wchar_p),
                ("pTo", ctypes.c_wchar_p),
                ("fFlags", ctypes.c_ushort),
                ("fAnyOperationsAborted", wintypes.BOOL),
                ("hNameMappings", wintypes.LPVOID),
                ("lpszProgressTitle", ctypes.c_wchar_p),
            ]
        
        struct = SHFILEOPSTRUCTW()
        struct.hwnd = 0
        struct.wFunc = 3  # FO_DELETE
        struct.pFrom = p_from
        struct.pTo = None
        struct.fFlags = 0x0040 | 0x0010  # FOF_ALLOWUNDO | FOF_NOCONFIRMATION
        struct.fAnyOperationsAborted = False
        struct.hNameMappings = None
        struct.lpszProgressTitle = None
        
        res = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(struct))
        return res == 0 and not struct.fAnyOperationsAborted
    elif sys_name == "Darwin":
        success = True
        for p in paths:
            abs_p = str(Path(p).resolve())
            cmd = ["osascript", "-e", f'tell application "Finder" to delete POSIX file "{abs_p}"']
            res = subprocess.run(cmd, capture_output=True)
            if res.returncode != 0:
                success = False
        return success
    return False

def apply_dark_theme(root):
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=BG, foreground=FG, font=("Consolas", 9), bordercolor=BORDER, darkcolor=BG, lightcolor=BG)
    s.configure("TFrame", background=BG)
    s.configure("TLabelframe", background=BG_PANEL, foreground=GREEN, bordercolor=BORDER, relief="groove")
    s.configure("TLabelframe.Label", background=BG, foreground=GREEN, font=("Consolas", 9, "bold"))
    s.configure("TLabel", background=BG, foreground=FG)
    s.configure("Panel.TLabel", background=BG_PANEL, foreground=FG_DIM) 
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
    s.map("Treeview", background=[("selected", SEL_BG)])
    root.configure(background=BG)

def apply_light_theme(root):
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=BG_L, foreground=FG_L, font=("Consolas", 9), bordercolor=BORDER_L, darkcolor=BG_L, lightcolor=BG_L)
    s.configure("TFrame", background=BG_L)
    s.configure("TLabelframe", background=BG_PANEL_L, foreground=GREEN_L, bordercolor=BORDER_L, relief="groove")
    s.configure("TLabelframe.Label", background=BG_L, foreground=GREEN_L, font=("Consolas", 9, "bold"))
    s.configure("TLabel", background=BG_L, foreground=FG_L)
    s.configure("Panel.TLabel", background=BG_PANEL_L, foreground=FG_DIM_L) 
    s.configure("TEntry", fieldbackground=BG_INPUT_L, foreground=FG_L, insertcolor=GREEN_L, bordercolor=BORDER_L, selectbackground=SEL_BG_L)
    s.configure("TCombobox", fieldbackground=BG_INPUT_L, foreground=FG_L, selectbackground=SEL_BG_L, bordercolor=BORDER_L, arrowcolor=GREEN_L)
    s.map("TCombobox", fieldbackground=[("readonly", BG_INPUT_L)], foreground=[("readonly", FG_L)], selectbackground=[("readonly", SEL_BG_L)])
    s.configure("TCheckbutton", background=BG_PANEL_L, foreground=FG_L)
    s.map("TCheckbutton", background=[("active", BG_PANEL_L)], foreground=[("active", GREEN_L)])
    s.configure("TButton", background=BG_INPUT_L, foreground=GREEN_L, bordercolor=BORDER_L, padding=5)
    s.map("TButton", background=[("active", "#eaeef2"), ("disabled", BG_L)], foreground=[("disabled", FG_DIM_L)])
    s.configure("TScrollbar", background=BG_PANEL_L, troughcolor=BG_INPUT_L, bordercolor=BORDER_L, arrowcolor=FG_DIM_L)
    s.configure("TSeparator", background=BORDER_L)
    s.configure("TProgressbar", background=GREEN_L, troughcolor=BG_INPUT_L, bordercolor=BORDER_L)
    s.configure("Treeview", background=BG_INPUT_L, foreground=FG_L, fieldbackground=BG_INPUT_L, bordercolor=BORDER_L, rowheight=20, font=("Consolas", 9))
    s.configure("Treeview.Heading", background=BG_PANEL_L, foreground=GREEN_L, font=("Consolas", 9, "bold"), relief="flat")
    s.map("Treeview", background=[("selected", SEL_BG_L)])
    root.configure(background=BG_L)

class BetterSearch:
    def __init__(self, root):
        self.root = root
        self.root.title(f"BetterSearch v{version}")
        self.root.geometry("1200x645")
        self.target_folder = ""
        self.is_searching = False
        self.stop_requested = False
        self.files_processed = 0
        self.current_theme = "dark"
        
        # Track completed operations for Undo
        self.transaction_ledger = []
        
        # Interactive thread resolution
        self.resolve_event = threading.Event()
        self.resolve_choice = None
        
        self.build_ui()
        self.load_settings()
        self.update_tree_tags()
        if self.current_theme == "dark":
            apply_dark_theme(root)
        else:
            apply_light_theme(root)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    # --------------- UI BUILD ---------------------------------------------------
    def build_ui(self):
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # -- LEFT PANEL ----------------------------------------------------------
        self.left_frame = ttk.LabelFrame(self.main_pane, text="Source", padding=10)
        self.main_pane.add(self.left_frame, weight=0)
        
        ttk.Button(self.left_frame, text="Browse Folder", command=self.select_folder).pack(fill=tk.X)
        self.lbl_folder = ttk.Label(self.left_frame, text="No folder selected", wraplength=150, style="Panel.TLabel", foreground="#ff0000")
        self.lbl_folder.pack(fill=tk.X, pady=10)
        
        ttk.Separator(self.left_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        
        self.btn_undo = ttk.Button(self.left_frame, text="⟲ Undo Last Action", state=tk.DISABLED, command=self.undo_last_action)
        self.btn_undo.pack(fill=tk.X, pady=(2, 2))
        
        ttk.Button(self.left_frame, text="Export Results", command=self.export_results).pack(fill=tk.X, pady=2)
        
        # Theme & License stacking correctly at the bottom 
        self.license = ttk.Label(self.left_frame, text="Copyright (c) 2026 ItsLuckyLike", wraplength=150, style="Panel.TLabel")
        self.license.pack(side="bottom", fill=tk.X, pady=5)
        
        self.btn_theme = ttk.Button(self.left_frame, text="🌓 Toggle Theme", command=self.toggle_theme)
        self.btn_theme.pack(side="bottom", fill=tk.X, pady=(5, 2))

        # -- MIDDLE PANEL --------------------------------------------------------
        self.mid_container = ttk.Frame(self.main_pane)
        self.main_pane.add(self.mid_container, weight=0)

        # Bottom section of middle pane (Search Controls always visible)
        self.search_ctrl_frame = ttk.Frame(self.mid_container, padding=5)
        self.search_ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X)

        btn_container = ttk.Frame(self.search_ctrl_frame)
        btn_container.pack(fill=tk.X, pady=5)
        btn_container.columnconfigure(0, weight=70)
        btn_container.columnconfigure(1, weight=30)
        self.btn_search = ttk.Button(btn_container, text="▶  Start Search", command=self.start_search_thread)
        self.btn_search.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        self.btn_dupes = ttk.Button(btn_container, text="⊕  Dupes", command=self.start_dupe_thread)
        self.btn_dupes.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        self.progress = ttk.Progressbar(self.search_ctrl_frame, orient="horizontal", mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(5, 2))
        self.lbl_counter = ttk.Label(self.search_ctrl_frame, text=f"Found: 0  /  Scanned: 0", foreground=GREEN)
        self.lbl_counter.pack()

        # Top section of middle pane (Scrollable Canvas for Parameters)
        self.mid_canvas = tk.Canvas(self.mid_container, highlightthickness=0, background=BG, width=320)
        mid_scroll = ttk.Scrollbar(self.mid_container, orient="vertical", command=self.mid_canvas.yview)
        
        self.mid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mid_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scroll_frame = ttk.Frame(self.mid_canvas)
        self.scroll_frame.bind("<Configure>", lambda e: self.mid_canvas.configure(scrollregion=self.mid_canvas.bbox("all")))
        self.mid_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.mid_canvas.configure(yscrollcommand=mid_scroll.set)
        self.mid_canvas.bind_all("<MouseWheel>", lambda e: self.mid_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # -- Basic Filters ------------------------------------------------------
        core_grp = ttk.LabelFrame(self.scroll_frame, text="Basic Filters", padding=10)
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
        self.cb_cont_mode = self.add_combo(core_grp, ["Disabled", "Contains", "Does Not Contain", "Matches Regex"], "Disabled")
        self.ent_cont_text = self.add_entry(core_grp, "")

        # -- File Attributes ----------------------------------------------------
        meta_grp = ttk.LabelFrame(self.scroll_frame, text="File Attributes", padding=10)
        meta_grp.pack(fill=tk.X, padx=5, pady=5)
        self.add_label(meta_grp, "Min Size (kB):")
        self.ent_min_size = self.add_entry(meta_grp, "0")
        self.add_label(meta_grp, "Max Size (kB, 0 = disabled):")
        self.ent_max_size = self.add_entry(meta_grp, "0")
        self.add_label(meta_grp, "Modified within last # days (0 = disabled):")
        self.ent_days = self.add_entry(meta_grp, "0")
        self.add_label(meta_grp, "Created* within last # days (0 = disabled):")
        self.ent_cdays = self.add_entry(meta_grp, "0")
        ttk.Label(meta_grp, text="* Linux: metadata-change time, not birth time.", style="Panel.TLabel", font=("Consolas", 8)).pack(anchor="w", pady=(0, 2))

        # -- Search Settings ----------------------------------------------------
        srch_grp = ttk.LabelFrame(self.scroll_frame, text="Search Settings", padding=10)
        srch_grp.pack(fill=tk.X, padx=5, pady=5)
        self.add_label(srch_grp, "Max Depth (0 = unlimited):")
        self.ent_depth = self.add_entry(srch_grp, "0")

        # -- Sibling Constraints ------------------------------------------------
        fell_grp = ttk.LabelFrame(self.scroll_frame, text="Sibling Constraints", padding=10)
        fell_grp.pack(fill=tk.X, padx=5, pady=5)
        self.cb_fell_type = self.add_combo(fell_grp, ["Disabled", "Has Sibling File", "Has Sibling Folder", "No Sibling File", "No Sibling Folder"], "Disabled")
        self.add_label(fell_grp, "Sibling Name Pattern:")
        self.ent_fell_name = self.add_entry(fell_grp, "*")
        self.add_label(fell_grp, "Sibling Content Filter:")
        self.cb_fell_cont_mode = self.add_combo(fell_grp, ["Disabled", "Contains", "Does Not Contain", "Matches Regex"], "Disabled")
        self.ent_fell_cont_text = self.add_entry(fell_grp, "")

        # -- RIGHT PANEL --------------------------------------------------------
        right_frame = ttk.LabelFrame(self.main_pane, text="Results", padding=5)
        self.main_pane.add(right_frame, weight=1)
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        cols = ("size", "created", "modified")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="Path", anchor="w")
        self.tree.heading("size", text="Size", anchor="e")
        self.tree.heading("created", text="Created*", anchor="w")
        self.tree.heading("modified", text="Modified", anchor="w")
        self.tree.column("#0", width=420, stretch=True)
        self.tree.column("size", width=75, stretch=False, anchor="e")
        self.tree.column("created", width=130, stretch=False)
        self.tree.column("modified", width=130, stretch=False)

        self.tree.tag_configure("group", foreground=GREEN, font=("Consolas", 9, "bold"))
        self.tree.tag_configure("copied")
        self.tree.tag_configure("renamed")
        self.tree.tag_configure("deleted")
        self.tree.tag_configure("moved")
        self.tree.tag_configure("renamed_stale")

        vsb = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(right_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Keybind for Select All
        self.tree.bind("<Control-a>", self.select_all)
        self.tree.bind("<Double-1>", lambda e: self.open_selected())

        self.ctx_menu = tk.Menu(self.root, tearoff=0, bg=BG_INPUT, fg=FG, activebackground=SEL_BG, activeforeground=FG, font=("Consolas", 9))
        self.ctx_menu.add_command(label="Open Location", command=self.open_location_selected)
        self.ctx_menu.add_command(label="Copy Full Path", command=self.copy_path)
        self.ctx_menu.add_command(label="Copy Filename", command=self.copy_filename)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label="Copy To...", command=lambda: self.show_transfer_dialog("copy"))
        self.ctx_menu.add_command(label="Move To...", command=lambda: self.show_transfer_dialog("move"))
        self.ctx_menu.add_command(label="Rename", command=self.rename_selected)
        self.ctx_menu.add_command(label="Delete", command=self.delete_selected)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label="Select All", command=self.select_all)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.txt_log = tk.Text(right_frame, height=6, state=tk.DISABLED, background=BG_INPUT, foreground=FG_DIM, insertbackground=GREEN, font=("Consolas", 8), borderwidth=0)
        self.txt_log.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    # -- UI Helpers --------------------------------------------------------------
    def add_label(self, parent, text):
        ttk.Label(parent, text=text, style="Panel.TLabel").pack(anchor="w")

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
        def _append():
            self.txt_log.config(state=tk.NORMAL)
            self.txt_log.insert(tk.END, f"> {msg}\n")
            self.txt_log.see(tk.END)
            self.txt_log.config(state=tk.DISABLED)
        self.root.after(0, _append)
    
    def update_tree_tags(self): # Determine the colors based on the current theme
        if self.current_theme == "dark":
            colors = {
                "copied": FILE_COPIED,
                "renamed": FILE_RENAMED,
                "deleted": FILE_DELETED,
                "moved": FILE_MOVED,
                "renamed_stale": FILE_RENAMED_STALE
            }
        else:
            colors = {
                "copied": FILE_COPIED_L,
                "renamed": FILE_RENAMED_L,
                "deleted": FILE_DELETED_L,
                "moved": FILE_MOVED_L,
                "renamed_stale": FILE_RENAMED_STALE_L
            }
        
        for tag, color in colors.items():
            self.tree.tag_configure(tag, foreground=color)
    
    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            apply_light_theme(self.root)
            self.update_tree_tags()
        else:
            self.current_theme = "dark"
            apply_dark_theme(self.root)
            self.update_tree_tags()

    # -- Folder ------------------------------------------------------------------
    def select_folder(self):
        f = filedialog.askdirectory()
        if f:
            self.target_folder = f
            self.lbl_folder.config(text=f, foreground=GREEN if self.current_theme == "dark" else "#1a7f37")

    # -- Result Interaction ------------------------------------------------------
    def select_all(self, event=None):
        items = []
        def _get_items(node):
            for child in self.tree.get_children(node):
                items.append(child)
                _get_items(child)
        _get_items("")
        if items:
            self.tree.selection_set(items)
        return "break"

    def _focused_path(self):
        sel = self.tree.focus()
        if not sel:
            return None
        if self.tree.get_children(sel) and not self.tree.parent(sel):
            return None
        text = self.tree.item(sel, "text")
        return Path(text) if text else None

    def _selected_paths(self):
        items = self.tree.selection()
        paths = []
        for item in items:
            if self.tree.get_children(item) and not self.tree.parent(item):
                continue
            text = self.tree.item(item, "text")
            if text:
                paths.append((item, Path(text)))
        return paths

    def open_location_selected(self):
        path = self._focused_path()
        if not path: return
        d = path.parent if path.is_file() else path
        if platform.system() == "Windows": os.startfile(d)
        else: subprocess.Popen(["xdg-open" if platform.system() == "Linux" else "open", str(d)])

    def open_selected(self):
        path = self._focused_path()
        if not path:
            return

        try:
            if platform.system() == "Windows":
                os.startfile(path)
            else:
                subprocess.Popen([
                    "xdg-open" if platform.system() == "Linux" else "open",
                    str(path)
                ])
        except Exception as e:
            self.log(f"Open failed: {e}")
    
    def copy_path(self):
        p = self._focused_path()
        if p:
            self.root.clipboard_append(str(p))

    def copy_filename(self):
        p = self._focused_path()
        if p:
            self.root.clipboard_append(p.name)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            current_selection = self.tree.selection()
            if item not in current_selection:
                self.tree.focus(item)
                self.tree.selection_set(item)
            self.ctx_menu.post(event.x_root, event.y_root)

    # -- Interactive Error Resolution ---------------------------------------------
    def ask_error_resolution(self, error_msg, filepath):
        self.resolve_choice = None
        self.resolve_event.clear()
        
        def _show_dialog():
            top = tk.Toplevel(self.root)
            top.title("BetterSearch - Operation Halted")
            top.geometry("450x180")
            top.resizable(False, False)
            top.transient(self.root)
            top.grab_set()
            
            top.configure(background=BG if self.current_theme == "dark" else BG_L)
            
            ttk.Label(top, text="Error Encountered", font=("Consolas", 10, "bold")).pack(pady=(15,5), padx=20, anchor="w")
            ttk.Label(top, text=f"File: {filepath}", style="Panel.TLabel").pack(padx=20, anchor="w")
            ttk.Label(top, text=f"Reason: {error_msg}", foreground="#ff6b6b" if self.current_theme == "dark" else "#cf222e").pack(padx=20, pady=(0,10), anchor="w")
            
            btn_frame = ttk.Frame(top)
            btn_frame.pack(side="bottom", fill=tk.X, pady=15, padx=20)
            
            def _choose(choice):
                self.resolve_choice = choice
                top.destroy()
                self.resolve_event.set()
                
            ttk.Button(btn_frame, text="Abort All", command=lambda: _choose("abort")).pack(side="right", padx=2)
            ttk.Button(btn_frame, text="Skip File", command=lambda: _choose("skip")).pack(side="right", padx=2)
            ttk.Button(btn_frame, text="Retry", command=lambda: _choose("retry")).pack(side="right", padx=2)
            
            top.protocol("WM_DELETE_WINDOW", lambda: _choose("abort"))
            
        self.root.after(0, _show_dialog)
        self.resolve_event.wait()
        return self.resolve_choice

    # -- Operations & Undo Ledger ------------------------------------------------
    def push_to_ledger(self, op_type, changes):
        """Logs changes for Undo functionality."""
        if changes:
            self.transaction_ledger.append({"op": op_type, "changes": changes})
            self.log(f"Transaction logged: {len(changes)} item(s). Ready for Undo.")
            self.root.after(0, lambda: self.btn_undo.config(state=tk.NORMAL, text=f"⟲ Undo {op_type.capitalize()}"))

    def undo_last_action(self):
        if not self.transaction_ledger:
            messagebox.showinfo("Undo", "No operations left to undo.")
            return
            
        last_txn = self.transaction_ledger.pop()
        op = last_txn["op"]
        changes = last_txn["changes"]
        
        self.log(f"Reversing operation: {op} on {len(changes)} items...")
        
        def _run_undo():
            success_count = 0
            for item in changes:
                src = item["src"]
                dst = item["dst"]
                try:
                    if op == "copy":
                        if dst.exists():
                            if dst.is_file(): dst.unlink()
                            else: shutil.rmtree(dst)
                            success_count += 1
                    elif op in ("move", "rename"):
                        if dst.exists():
                            dst.rename(src)
                            success_count += 1
                except Exception as e:
                    self.log(f"Failed to reverse {dst.name}: {e}")
                    
            self.log(f"Undo complete. Reverted {success_count}/{len(changes)}.")
            
            def _update_button():
                if self.transaction_ledger:
                    next_op = self.transaction_ledger[-1]["op"]
                    self.btn_undo.config(state=tk.NORMAL, text=f"⟲ Undo {next_op.capitalize()}")
                else:
                    self.btn_undo.config(state=tk.DISABLED, text="⟲ Undo Last Action")
                    
            self.root.after(0, _update_button)
        
        threading.Thread(target=_run_undo, daemon=True).start()

    def show_transfer_dialog(self, op_type):
        selected = self._selected_paths()
        if not selected: return
        
        top = tk.Toplevel(self.root)
        top.title(f"BetterSearch - Transfer Options ({op_type.capitalize()})")
        top.geometry("550x320")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()
        
        top.configure(background=BG if self.current_theme == "dark" else BG_L)
        
        ttk.Label(top, text="Transfer Options", font=("Consolas", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15,5))
        
        # Target Path Selection
        ttk.Label(top, text="Target:").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        ent_target = ttk.Entry(top, width=45)
        ent_target.grid(row=1, column=1, sticky="w", pady=5)
        
        def _browse_target():
            d = filedialog.askdirectory(title="Select Destination Directory")
            if d:
                ent_target.delete(0, tk.END)
                ent_target.insert(0, d)
                
        ttk.Button(top, text="Browse", command=_browse_target).grid(row=1, column=2, padx=5)
        
        # Options
        var_verify = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Verify process integrity after transfer (File Size Validation)", variable=var_verify).grid(row=2, column=0, columnspan=3, sticky="w", padx=15, pady=2)
        
        var_md5 = tk.BooleanVar(value=False)
        ttk.Checkbutton(top, text="Strict MD5 Hash Validation (Slower)", variable=var_md5).grid(row=3, column=0, columnspan=3, sticky="w", padx=15, pady=2)
        
        ttk.Label(top, text="Collision Handling:").grid(row=4, column=0, sticky="w", padx=15, pady=5)
        var_collision = tk.StringVar(value="auto")
        
        radio_frame = ttk.Frame(top)
        radio_frame.grid(row=5, column=0, columnspan=3, sticky="w", padx=25)
        ttk.Radiobutton(radio_frame, text="Auto-rename (e.g., file (1).txt)", value="auto", variable=var_collision).pack(anchor="w")
        ttk.Radiobutton(radio_frame, text="Skip if name matches", value="skip", variable=var_collision).pack(anchor="w")
        ttk.Radiobutton(radio_frame, text="Overwrite existing files", value="overwrite", variable=var_collision).pack(anchor="w")
        
        def _proceed():
            target_dir = ent_target.get()
            if not target_dir or not Path(target_dir).is_dir():
                messagebox.showerror("Error", "Please select a valid destination directory.")
                return
            top.destroy()
            threading.Thread(target=self._run_transfer_operation, args=(selected, Path(target_dir), op_type, var_collision.get(), var_verify.get(), var_md5.get()), daemon=True).start()

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=6, column=0, columnspan=3, sticky="e", padx=15, pady=15)
        ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Proceed", command=_proceed).pack(side="right", padx=5)

    def _get_available_name(self, target):
        idx = 1
        new_target = target
        while new_target.exists():
            new_target = target.with_name(f"{target.stem} ({idx}){target.suffix}")
            idx += 1
        return new_target

    def _run_transfer_operation(self, selected, dest_dir, op_type, collision_mode, verify_integrity, verify_md5):
        self.root.after(0, lambda: self.progress.configure(mode="determinate", maximum=100))
        self.root.after(0, lambda: self.progress.set(0))
        
        total = len(selected)
        self.log(f"Starting {op_type} operation for {total} item(s) to {dest_dir}...")
        
        transfer_results = []
        any_failed = False
        aborted = False
        ledger_entries = []
        
        for i, (item_id, src) in enumerate(selected):
            if aborted: break
            
            if not src.exists():
                self.log(f"Source vanished: {src}")
                any_failed = True
                continue
                
            target = dest_dir / src.name
            
            if target.exists():
                if collision_mode == "skip":
                    self.log(f"Skipped (collision): {target.name}")
                    continue
                elif collision_mode == "overwrite":
                    try:
                        if target.is_file(): target.unlink()
                        else: shutil.rmtree(target)
                    except Exception as e:
                        self.log(f"Overwrite clear failed: {e}")
                        any_failed = True
                        continue
                elif collision_mode == "auto":
                    target = self._get_available_name(target)
            
            success = False
            while not success and not aborted:
                try:
                    if src.is_file(): shutil.copy2(src, target)
                    elif src.is_dir(): shutil.copytree(src, target, dirs_exist_ok=True)
                    success = True
                    self.root.after(0, lambda idx=item_id: self.tree.item(idx, tags=("copied",)))
                    
                    if verify_integrity and success:
                        if not target.exists() or (src.is_file() and target.stat().st_size != src.stat().st_size):
                            raise Exception("Integrity check failed: Size mismatch or missing target.")
                    if verify_md5 and success and src.is_file():
                        if file_hash(src) != file_hash(target):
                            raise Exception("MD5 Hash validation failed.")
                            
                except Exception as e:
                    choice = self.ask_error_resolution(str(e), src.name)
                    if choice == "retry": continue
                    elif choice == "skip": break
                    elif choice == "abort":
                        aborted = True
                        break
                        
            if success:
                ledger_entries.append({"src": src, "dst": target})
                transfer_results.append((item_id, src, target, True))

                if op_type == "copy":
                    self.root.after(
                        0,
                        lambda idx=item_id: self.tree.item(idx, tags=("copied",))
                    )
            else:
                any_failed = True
                
            val = int(((i + 1) / total) * 50 if op_type == "move" else ((i + 1) / total) * 100)
            self.root.after(0, lambda v=val: self.progress.set(v))
            
        if op_type == "move" and not aborted:
            if any_failed:
                self.log("Move operation aborted source-deletion Phase 2 because validation checks failed.")
            else:
                self.log("Verification checks passed completely. Starting Phase 2: Source removal...")
                for i, (item_id, src, target, success) in enumerate(transfer_results):
                    try:
                        if src.is_file():
                            src.unlink()
                        elif src.is_dir():
                            shutil.rmtree(src)

                        self.root.after(
                            0,
                            lambda idx=item_id, tgt=str(target):
                                self.tree.item(idx, text=tgt, tags=("moved",))
                        )
                    except Exception as e:
                        self.log(f"Failed to clear source element {src.name}: {e}")
                    val = 50 + int(((i + 1) / total) * 50)
                    self.root.after(0, lambda v=val: self.progress.set(v))
        
        self.push_to_ledger(op_type, ledger_entries)
        
        succeeded_count = len(ledger_entries)
        self.log(f"Operation complete. Succeeded: {succeeded_count}/{total}.")
        self.root.after(0, lambda: self.progress.configure(mode="indeterminate"))
        self.root.after(0, lambda: self._prompt_update_parameters(dest_dir))

    def _prompt_update_parameters(self, new_dir):
        top = tk.Toplevel(self.root)
        top.title("BetterSearch - Update Search Target")
        top.geometry("450x180")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()
        
        top.configure(background=BG if self.current_theme == "dark" else BG_L)
        
        ttk.Label(top, text="Transfer Complete", font=("Consolas", 10, "bold")).pack(pady=(15,5), padx=20, anchor="w")
        ttk.Label(top, text=f"Would you like to change the search target to the destination directory?\n\n{new_dir}", style="Panel.TLabel", wraplength=400).pack(padx=20, anchor="w")
        
        def _set_dir():
            self.target_folder = str(new_dir)
            self.lbl_folder.config(text=self.target_folder, foreground=GREEN if self.current_theme == "dark" else "#1a7f37")
            self.save_settings()
            self.log(f"Source parameter updated to: {new_dir}")
            top.destroy()
            
        def _set_and_search():
            _set_dir()
            self.start_search_thread()

        btn_frame = ttk.Frame(top)
        btn_frame.pack(side="bottom", fill=tk.X, pady=15, padx=20)
        ttk.Button(btn_frame, text="No", command=top.destroy).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Yes & Start Search", command=_set_and_search).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Yes", command=_set_dir).pack(side="right", padx=5)

    def delete_selected(self):
        selected = self._selected_paths()
        if not selected: return
            
        top = tk.Toplevel(self.root)
        top.title("BetterSearch - Confirm Deletion")
        top.geometry("500x220")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()
        
        top.configure(background=BG if self.current_theme == "dark" else BG_L)
        
        ttk.Label(top, text="Are you sure you want to delete the selected item(s)?", font=("Consolas", 10, "bold")).pack(pady=(15,5), padx=20, anchor="w")
        ttk.Label(top, text=f"This action will affect {len(selected)} file(s).", style="Panel.TLabel").pack(padx=20, anchor="w")
        
        var_trash = tk.BooleanVar(value=True)
        chk_trash = ttk.Checkbutton(top, text="Move to Recycle Bin/Trash (Windows/macOS only)", variable=var_trash)
        chk_trash.pack(pady=(15,5), padx=20, anchor="w")
        
        if platform.system() not in ("Windows", "Darwin"):
            var_trash.set(value=False)
            chk_trash.config(state=tk.DISABLED)
            ttk.Label(top, text="* Native system trash features unavailable on standard Linux.", font=("Consolas", 8), foreground="#ff4444").pack(padx=20, anchor="w")
            
        btn_frame = ttk.Frame(top)
        btn_frame.pack(side="bottom", fill=tk.X, pady=15, padx=20)
        
        def on_confirm():
            v_trash = var_trash.get()
            top.destroy()
            threading.Thread(target=self._run_delete_operation, args=(selected, v_trash), daemon=True).start()
            
        ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Delete", command=on_confirm).pack(side="right", padx=5)

    def _run_delete_operation(self, selected, use_trash):
        self.root.after(0, lambda: self.progress.configure(mode="determinate", maximum=100))
        self.root.after(0, lambda: self.progress.set(0))
        
        total = len(selected)
        deleted_count = 0
        self.log(f"Starting cleanup sequence targeting {total} elements...")
        
        if use_trash and platform.system() in ("Windows", "Darwin"):
            paths_to_trash = [p for _, p in selected]
            try:
                if send_to_trash(paths_to_trash):
                    for item_id, _ in selected:
                        self.root.after(0, lambda idx=item_id: self.tree.item(idx, tags=("deleted",)))
                    deleted_count = total
                    self.log(f"Successfully processed items into the system trash framework.")
                else:
                    self.log("Unified bulk system trash request rejected. Attempting step-by-step...")
                    for i, (item_id, p) in enumerate(selected):
                        if send_to_trash([p]):
                            self.root.after(0, lambda idx=item_id: self.tree.item(idx, tags=("deleted",)))
                            deleted_count += 1
                        else: self.log(f"Failed handling: {p.name}")
                        val = int(((i + 1) / total) * 100)
                        self.root.after(0, lambda v=val: self.progress.set(v))
            except Exception as e:
                self.log(f"Trash ecosystem operation crash failure details: {e}")
        else:
            for i, (item_id, p) in enumerate(selected):
                try:
                    if p.is_file(): p.unlink()
                    elif p.is_dir(): shutil.rmtree(p)
                    self.root.after(0, lambda idx=item_id: self.tree.item(idx, tags=("deleted",)))
                    deleted_count += 1
                except Exception as e:
                    self.log(f"Permanent system removal block on {p.name}: {e}")
                val = int(((i + 1) / total) * 100)
                self.root.after(0, lambda v=val: self.progress.set(v))
                
        self.log(f"Cleanup run finalized. Cleared records: {deleted_count}/{total}.")
        self.root.after(0, lambda: self.progress.configure(mode="indeterminate"))

    def rename_selected(self):
        selected = self._selected_paths()
        if not selected: return
            
        top = tk.Toplevel(self.root)
        top.title("BetterSearch - Rename files")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()
        
        top.configure(background=BG if self.current_theme == "dark" else BG_L)
        
        is_single = len(selected) == 1
        
        if is_single:
            top.geometry("450x120")
            ttk.Label(top, text="New Filename:", font=("Consolas", 10, "bold")).pack(padx=15, pady=(15, 5), anchor="w")
            ent_single = ttk.Entry(top)
            ent_single.insert(0, selected[0][1].name)
            ent_single.pack(fill=tk.X, padx=15, pady=2)
            
            def _run_single():
                new_name = ent_single.get()
                top.destroy()
                threading.Thread(target=self._run_rename_single, args=(selected[0], new_name), daemon=True).start()
                
            btn_frame = ttk.Frame(top)
            btn_frame.pack(side="bottom", fill=tk.X, pady=10, padx=15)
            ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side="right", padx=5)
            ttk.Button(btn_frame, text="Rename", command=_run_single).pack(side="right", padx=5)
        else:
            top.geometry("550x350")
            
            # Find & Replace Section
            grp_fr = ttk.LabelFrame(top, text="Find & Replace", padding=10)
            grp_fr.pack(fill=tk.X, padx=15, pady=10)
            
            ttk.Label(grp_fr, text="Find Pattern:").grid(row=0, column=0, sticky="w", pady=2)
            ent_find = ttk.Entry(grp_fr, width=25)
            ent_find.grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(grp_fr, text="Replace:").grid(row=1, column=0, sticky="w", pady=2)
            ent_replace = ttk.Entry(grp_fr, width=25)
            ent_replace.grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(grp_fr, text="* Leave Replace empty to delete matches.", style="Panel.TLabel", font=("Consolas", 8)).grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
            
            # Index Manipulation Section
            grp_idx = ttk.LabelFrame(top, text="Index Manipulation", padding=10)
            grp_idx.pack(fill=tk.X, padx=15, pady=5)
            
            ttk.Label(grp_idx, text="Insert text:").grid(row=0, column=0, sticky="w")
            ent_ins_txt = ttk.Entry(grp_idx, width=15)
            ent_ins_txt.grid(row=0, column=1, padx=5)
            ttk.Label(grp_idx, text="at index:").grid(row=0, column=2)
            ent_ins_idx = ttk.Entry(grp_idx, width=5)
            ent_ins_idx.grid(row=0, column=3, padx=5)
            
            ttk.Label(grp_idx, text="Remove:").grid(row=1, column=0, sticky="w", pady=5)
            ent_rem_cnt = ttk.Entry(grp_idx, width=5)
            ent_rem_cnt.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(grp_idx, text="chars at index:").grid(row=1, column=2)
            ent_rem_idx = ttk.Entry(grp_idx, width=5)
            ent_rem_idx.grid(row=1, column=3, padx=5)
            
            def _run_batch():
                config = {
                    "find": ent_find.get(),
                    "replace": ent_replace.get(),
                    "ins_txt": ent_ins_txt.get(),
                    "ins_idx": int(ent_ins_idx.get()) if ent_ins_idx.get().isdigit() else None,
                    "rem_cnt": int(ent_rem_cnt.get()) if ent_rem_cnt.get().isdigit() else None,
                    "rem_idx": int(ent_rem_idx.get()) if ent_rem_idx.get().isdigit() else None
                }
                top.destroy()
                threading.Thread(target=self._run_rename_batch, args=(selected, config), daemon=True).start()
                
            btn_frame = ttk.Frame(top)
            btn_frame.pack(side="bottom", fill=tk.X, pady=10, padx=15)
            ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side="right", padx=5)
            ttk.Button(btn_frame, text="Apply Matrix", command=_run_batch).pack(side="right", padx=5)

    def _run_rename_single(self, selection, new_name):
        item_id, src = selection
        if not src.exists(): return
        
        target = src.parent / new_name
        try:
            src.rename(target)
            self.root.after(
                0,
                lambda: self.tree.item(item_id, text=str(target), tags=("renamed",))
            )
            self.push_to_ledger("rename", [{"src": src, "dst": target}])
            self.log(f"Renamed 1 item successfully.")
        except Exception as e:
            self.log(f"Rename failed: {e}")

    def _run_rename_batch(self, selected, config):
        self.root.after(0, lambda: self.progress.configure(mode="determinate", maximum=100))
        self.root.after(0, lambda: self.progress.set(0))
        
        total = len(selected)
        renamed_count = 0
        ledger_entries = []
        
        find_p = config["find"]
        rep_p = config["replace"]
        
        for i, (item_id, src) in enumerate(selected):
            if not src.exists(): continue
                
            old_name = src.name
            new_name = old_name
            
            # Find and Replace (supports standard string replacement/removal)
            if find_p:
                new_name = new_name.replace(find_p, rep_p)
                
            # Index Removal
            if config["rem_cnt"] is not None and config["rem_idx"] is not None:
                idx = config["rem_idx"]
                cnt = config["rem_cnt"]
                new_name = new_name[:idx] + new_name[idx + cnt:]
                
            # Index Insertion
            if config["ins_txt"] and config["ins_idx"] is not None:
                idx = config["ins_idx"]
                new_name = new_name[:idx] + config["ins_txt"] + new_name[idx:]
                
            if new_name == old_name: continue
            new_path = src.parent / new_name
            
            try:
                src.rename(new_path)
                ledger_entries.append({"src": src, "dst": new_path})
                renamed_count += 1
                self.root.after(
                    0,
                    lambda idx=item_id, np=str(new_path):
                        self.tree.item(idx, text=np, tags=("renamed",))
                )
            except Exception as e:
                self.log(f"Failed to rename {old_name}: {e}")
                
            val = int(((i + 1) / total) * 100)
            self.root.after(0, lambda v=val: self.progress.set(v))
            
        self.push_to_ledger("rename", ledger_entries)
        self.log(f"Mutation run ended. Transformed: {renamed_count}/{total} entities.")
        self.root.after(0, lambda: self.progress.configure(mode="indeterminate"))

    # -- Export ------------------------------------------------------------------
    def export_results(self):
        if not self.tree.get_children():
            return messagebox.showinfo("Export", "No results to export.")
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt"), ("CSV", "*.csv")])
        if not save_path: return
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
            "theme": self.current_theme
            }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
        except Exception: pass

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                s = json.load(f)
        except Exception: return
        self.current_theme = s.get("theme", "dark")
        if s.get("target_folder"):
            self.target_folder = s["target_folder"]
            self.lbl_folder.config(text=self.target_folder, foreground=GREEN if self.current_theme == "dark" else "#1a7f37")
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
        self.btn_search.config(text="■  Stop", command=self.request_stop)
        self.btn_dupes.config(text="■  Stop", command=self.request_stop)
        self.tree.delete(*self.tree.get_children())
        self.files_processed = 0
        self.progress.configure(mode="indeterminate")
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
        raw = [x.strip().lower() for x in self.ent_ext.get().split(";") if x.strip()]
        include = {e for e in raw if not e.startswith("-")}
        exclude = {e.lstrip("-") for e in raw if e.startswith("-")}
        return include, exclude

    def run_search(self):
        try:
            root_path = Path(self.target_folder)
            found_count = 0
            results_buffer = []
            t_pref = self.cb_file_type.get()
            name_pattern = self.ent_name.get()
            use_regex = self.var_name_regex.get()
            exclude_list = [x.strip() for x in self.ent_exclude.get().split(";") if x.strip()]
            ext_inc, ext_exc = self._parse_ext_filter()
            min_sz = float(self.ent_min_size.get() or 0) * 1024
            max_sz = float(self.ent_max_size.get() or 0) * 1024
            days_mod = float(self.ent_days.get() or 0) * 86400
            days_crt = float(self.ent_cdays.get() or 0) * 86400
            max_depth = int(self.ent_depth.get() or 0)
            root_depth = str(root_path).count(os.sep)
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

                if max_depth > 0:
                    if str(item).count(os.sep) - root_depth > max_depth: continue

                self.files_processed += 1
                if self.files_processed % 250 == 0:
                    self.root.after(0, lambda c=found_count, p=self.files_processed: self.lbl_counter.config(text=f"Found: {c}  /  Scanned: {p}"))

                is_file = item.is_file()
                is_dir = not is_file
                if t_pref == "File" and is_dir: continue
                if t_pref == "Folder" and is_file: continue

                if use_regex:
                    try:
                        if not re.search(name_pattern, item.name): continue
                    except: continue
                else:
                    if not item.match(name_pattern): continue

                if any(ex in item.name for ex in exclude_list): continue
                if is_file:
                    suf = item.suffix.lower()
                    if ext_inc and suf not in ext_inc: continue
                    if ext_exc and suf in ext_exc: continue

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

                found_count += 1
                results_buffer.append((str(item), size_str, ctime_str, mtime_str))

            def _finalize(b_res, f_cnt, f_proc):
                self.log(f"Loading {f_cnt} matches.")
                for row in b_res:
                    self.tree.insert("", tk.END, text=row[0], values=row[1:])
                self.log(f"Done. {f_cnt} matches  /  {f_proc} scanned.")
                self.lbl_counter.config(text=f"Found: {f_cnt}  /  Scanned: {f_proc}")
                
            self.root.after(0, _finalize, list(results_buffer), found_count, self.files_processed)

        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.root.after(0, self._end_thread)

    # -- Find Duplicates ---------------------------------------------------------
    def start_dupe_thread(self):
        self._start_thread(self.run_find_dupes)

    def run_find_dupes(self):
        try:
            root_path = Path(self.target_folder)
            self.log("Grouping by size...")
            size_map = {}
            for item in root_path.rglob("*"):
                if self.stop_requested: break
                if not item.is_file(): continue
                self.files_processed += 1
                if self.files_processed % 250 == 0:
                    self.root.after(0, lambda p=self.files_processed: self.lbl_counter.config(text=f"Scanned: {p}"))
                try: size_map.setdefault(item.stat().st_size, []).append(item)
                except: continue

            if self.stop_requested:
                self.log("Aborted.")
                return

            candidates = [f for files in size_map.values() if len(files) > 1 for f in files]
            self.log(f"Hashing {len(candidates)} candidates...")
            hash_map = {}
            for i, item in enumerate(candidates):
                if self.stop_requested: break
                try: hash_map.setdefault(file_hash(item), []).append(item)
                except: continue
                if i % 50 == 0:
                    self.root.after(0, lambda c=i, t=len(candidates): self.lbl_counter.config(text=f"Hashed: {c} / {t}"))

            dupes = {h: files for h, files in hash_map.items() if len(files) > 1}

            if not dupes:
                self.log("No duplicates found.")
                return

            redundant = sum(len(v) - 1 for v in dupes.values())
            self.log(f"Found {len(dupes)} duplicate groups  ({redundant} redundant files).")
            self.root.after(0, lambda d=len(dupes): self.lbl_counter.config(text=f"Duplicate groups: {d}"))

            def _insert_dupes(d_dict):
                for i, (_, files) in enumerate(sorted(d_dict.items())):
                    try: sz_str = fmt_size(files[0].stat().st_size)
                    except: sz_str = "?"
                    group_node = self.tree.insert("", tk.END, text=f"Group {i + 1}  ·  {len(files)} files  ·  {sz_str} each", tags=("group",), open=False)
                    for f in files:
                        try:
                            st = f.stat()
                            size_str = fmt_size(st.st_size)
                            ctime_str = fmt_date(get_ctime(st))
                            mtime_str = fmt_date(st.st_mtime)
                        except: size_str = ctime_str = mtime_str = ""
                        self.tree.insert(group_node, tk.END, text=str(f), values=(size_str, ctime_str, mtime_str))

            if not self.stop_requested:
                self.root.after(0, _insert_dupes, dupes)

        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.root.after(0, self._end_thread)


if __name__ == "__main__":
    root = tk.Tk()
    icon = tk.PhotoImage(data=ICON_B64)
    root.iconphoto(True, icon)
    app = BetterSearch(root)
    root.mainloop()
