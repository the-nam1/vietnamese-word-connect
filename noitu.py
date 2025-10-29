import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re

class WordSuggester:
    def __init__(self, words):
        self.words = [w.strip() for w in words if w.strip()]
        self.raw_lower = [w.lower() for w in self.words]

    def _tokens(self, text):
        parts = re.split(r"[\s\-\_\,]+", text)
        return [p for p in parts if p]

    def find_start_end(self, syllable):
        q = syllable.lower().strip()
        starts = []
        ends = []
        for w, raw in zip(self.words, self.raw_lower):
            tokens = self._tokens(raw)
            if tokens:
                if tokens[0] == q:
                    starts.append(w)
                if tokens[-1] == q:
                    ends.append(w)
        starts = sorted(dict.fromkeys(starts))
        ends = sorted(dict.fromkeys(ends))
        return starts, ends

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('tester')
        self.geometry('560x360')
        self._build_ui()
        self.suggester = None

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill='x', padx=8, pady=8)
        tk.Label(top, text='Âm tiết:').pack(side='left')
        self.entry = tk.Entry(top)
        self.entry.pack(side='left', fill='x', expand=True, padx=6)
        btn = tk.Button(top, text='Gợi ý', command=self.on_suggest)
        btn.pack(side='left')
        load = tk.Button(top, text='Tải danh sách', command=self.on_load)
        load.pack(side='left', padx=6)

        cols = ('start', 'end')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('start', text='Bắt đầu bằng')
        self.tree.heading('end', text='Kết thúc bằng')
        self.tree.column('start', width=260, anchor='w')
        self.tree.column('end', width=260, anchor='w')
        self.tree.pack(fill='both', expand=True, padx=8, pady=8)
        self.tree.bind('<Double-1>', self.on_copy)

        footer = tk.Label(self, text='Double-click để sao chép từ đã chọn.')
        footer.pack(side='bottom', fill='x')

    def on_load(self):
        path = filedialog.askopenfilename(title='Chọn file danh sách từ', filetypes=[('Text files','*.txt'),('All','*.*')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                words = [line.rstrip('\n') for line in f if line.strip()]
            if not words:
                messagebox.showwarning('Tập tin trống', 'Tập tin không chứa từ nào.')
                return
            self.suggester = WordSuggester(words)
            messagebox.showinfo('Đã tải', f'Đã tải {len(words)} từ.')
        except Exception as e:
            messagebox.showerror('Lỗi', f'Không thể tải file:\n{e}')

    def on_suggest(self):
        if not self.suggester:
            messagebox.showwarning('Chưa tải danh sách', 'Vui lòng tải danh sách từ trước khi gợi ý.')
            return
        q = self.entry.get().strip()
        if not q:
            messagebox.showwarning('Nhập thiếu', 'Vui lòng nhập âm tiết.')
            return
        starts, ends = self.suggester.find_start_end(q)
        self.tree.delete(*self.tree.get_children())
        maxlen = max(len(starts), len(ends))
        for i in range(maxlen):
            a = starts[i] if i < len(starts) else ''
            b = ends[i] if i < len(ends) else ''
            self.tree.insert('', 'end', values=(a, b))

    def on_copy(self, event=None):
        sel = self.tree.focus()
        if not sel:
            return
        vals = self.tree.item(sel, 'values')
        word = vals[0] or vals[1]
        if not word:
            return
        self.clipboard_clear()
        self.clipboard_append(word)
        messagebox.showinfo('Đã sao chép', f'Đã sao chép: {word}')

if __name__ == '__main__':
    app = App()
    app.mainloop()
