# vietnamese-word-connect
A Python file that suggests words for the Vietnamese Word Connect game.

## Requirements
- Python 3.7+
- tkinter (usually comes included in standard Python installs)

## Usage
Run the script:
```
python noitu.py
```
Steps in the app:
- Click "Tải danh sách" and open your .txt word list.
- Type the syllable into "Âm tiết" (must include correct diacritics).
- Click "Gợi ý".
- The table will show matches in two columns: "Bắt đầu bằng" and "Kết thúc bằng".
- Double-click a cell (row) to copy that word to clipboard.

## Word list format
- Regular text, encoded in UTF-8. 
- Each line has a word or a phrase. 
- Some lines might have multi-word phrases (like 'nắm quyền', "nắm đằng chuôi", ....). 
- Words are separated by spaces, hyphens, underscores, and commas.

### The included word list is designed for 2-syllable Vietnamese Word Connect, compiled by the-nam1 (author). You can freely add more words to the list as needed.
