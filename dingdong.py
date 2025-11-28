import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from pynput import keyboard
import threading
import winsound
from pathlib import Path

# 데이터 파일 경로 (사용자 문서 폴더에 저장)
import os
from pathlib import Path

# 사용자 문서 폴더에 저장
USER_DOCS = str(Path.home() / "Documents")
DATA_FILE = os.path.join(USER_DOCS, "tracking_data.json")

class TrackingApp:
    def __init__(self):
        self.data = self.load_data()
        self.input_window = None
        self.main_window = None
        self.creating_input_window = False
        self.creating_main_window = False
        
    def load_data(self):
        """저장된 데이터 불러오기"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """데이터 저장하기"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"저장 오류: {e}")
    
    def show_input_window(self):
        """입력 창 표시"""
        # 이미 창이 있거나 생성 중이면 무시
        if self.creating_input_window:
            return
        
        if self.input_window and self.input_window.winfo_exists():
            self.input_window.lift()
            self.input_window.focus_force()
            return
        
        self.creating_input_window = True
        
        self.input_window = tk.Toplevel()
        self.input_window.title("메모 입력")
        self.input_window.geometry("400x150")
        self.input_window.configure(bg='white')
        
        # 항상 위에 표시
        self.input_window.attributes('-topmost', True)
        
        # 텍스트 입력 영역
        text_frame = tk.Frame(self.input_window, bg='white')
        text_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.text_input = tk.Text(text_frame, font=('맑은 고딕', 11), wrap='word')
        self.text_input.pack(fill='both', expand=True)
        
        # 한글 입력 모드로 설정
        try:
            import win32api
            import win32con
            # 한글 IME 활성화 (0x0412 = 한국어)
            self.input_window.after(100, lambda: self.text_input.focus_force())
        except:
            pass
        
        self.text_input.focus()
        
        # 안내 문구
        info_label = tk.Label(self.input_window, text="1+Enter: 생각 | 2+Enter: 할일 | 3+Enter: 상태", 
                            bg='white', fg='gray', font=('맑은 고딕', 9))
        info_label.pack(pady=5)
        
        # 키 바인딩
        self.input_window.bind('<Key>', self.on_key_press)
        self.input_window.bind('<Escape>', lambda e: self.on_input_window_close())
        
        # 창이 닫힐 때 플래그 해제
        self.input_window.protocol("WM_DELETE_WINDOW", self.on_input_window_close)
        
        self.creating_input_window = False
    
    def on_input_window_close(self):
        """입력창 닫기"""
        if self.input_window:
            self.input_window.destroy()
            self.input_window = None
        
    def on_key_press(self, event):
        """키 입력 처리"""
        # Enter 키가 눌렸을 때만 처리
        if event.keysym != 'Return':
            return
            
        content = self.text_input.get('1.0', 'end-1c').strip()
        
        # 마지막 문자 확인
        if content and len(content) > 0:
            last_char = content[-1]
            
            category_map = {
                '1': '생각',
                '2': '할일',
                '3': '상태'
            }
            
            if last_char in category_map:
                # 마지막 숫자 제거
                content = content[:-1].strip()
                category = category_map[last_char]
                
                if content:  # 내용이 있을 때만 저장
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    entry = {
                        'timestamp': timestamp,
                        'category': category,
                        'content': content
                    }
                    
                    self.data.append(entry)
                    self.save_data()
                    
                    # 소리 재생
                    winsound.Beep(1000, 200)
                    
                    # 메인 창이 열려있으면 새로고침
                    if self.main_window and self.main_window.winfo_exists():
                        self.refresh_main_window()
                
                # 내용 있든 없든 창은 닫기
                if self.input_window:
                    self.input_window.destroy()
                    self.input_window = None
                
                # 기본 Enter 동작 막기
                return 'break'
    
    def show_main_window(self):
        """메인 조회 창 표시"""
        # 이미 창이 있거나 생성 중이면 무시
        if self.creating_main_window:
            return
        
        if self.main_window and self.main_window.winfo_exists():
            self.main_window.deiconify()  # 숨겨진 창 다시 보이기
            self.main_window.lift()
            self.main_window.focus_force()
            return
        
        self.creating_main_window = True
        
        self.main_window = tk.Toplevel()  # Tk() 대신 Toplevel() 사용
        self.main_window.title("상태 트래킹")
        self.main_window.geometry("800x600")
        
        # 창 닫기 이벤트 처리 (완전 종료 안 함)
        self.main_window.protocol("WM_DELETE_WINDOW", self.hide_main_window)
        
        # 필터 영역
        filter_frame = tk.Frame(self.main_window)
        filter_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(filter_frame, text="날짜:").pack(side='left', padx=5)
        self.date_var = tk.StringVar(value="오늘")
        date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, 
                                  values=["오늘", "어제", "최근 7일", "전체"], width=10)
        date_combo.pack(side='left', padx=5)
        
        tk.Label(filter_frame, text="분류:").pack(side='left', padx=5)
        self.category_var = tk.StringVar(value="전체")
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                      values=["전체", "생각", "할일", "상태"], width=10)
        category_combo.pack(side='left', padx=5)
        
        tk.Button(filter_frame, text="조회", command=self.refresh_main_window).pack(side='left', padx=5)
        tk.Button(filter_frame, text="TXT 추출", command=self.export_to_txt).pack(side='left', padx=5)
        tk.Button(filter_frame, text="데이터 리셋", command=self.reset_data).pack(side='left', padx=5)
        tk.Button(filter_frame, text="입력창 열기 (Ctrl+Space)", 
                 command=self.show_input_window).pack(side='left', padx=5)
        tk.Button(filter_frame, text="종료", command=self.quit_program, 
                 bg='#ffcccc').pack(side='left', padx=5)
        
        # 안내 문구
        info_frame = tk.Frame(self.main_window)
        info_frame.pack(pady=5)
        tk.Label(info_frame, text="단축키: Ctrl+Space (입력창) | Ctrl+Shift+Space (조회창)", 
                fg='gray', font=('맑은 고딕', 9)).pack()
        
        # 목록 영역
        list_frame = tk.Frame(self.main_window)
        list_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # 스크롤바
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                  font=('맑은 고딕', 10))
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        self.refresh_main_window()
        
        self.creating_main_window = False
    
    def hide_main_window(self):
        """메인 창 숨기기 (종료 안 함)"""
        if self.main_window:
            self.main_window.withdraw()
    
    def refresh_main_window(self):
        """메인 창 새로고침"""
        self.listbox.delete(0, tk.END)
        
        # 필터링
        filtered_data = self.filter_data()
        
        if not filtered_data:
            self.listbox.insert(tk.END, "기록이 없습니다.")
            return
        
        for entry in reversed(filtered_data):  # 최신순
            display_text = f"[{entry['timestamp']}] [{entry['category']}] {entry['content']}"
            self.listbox.insert(tk.END, display_text)
    
    def filter_data(self):
        """데이터 필터링"""
        filtered = self.data[:]
        
        # 날짜 필터
        date_filter = self.date_var.get()
        today = datetime.now().date()
        
        if date_filter == "오늘":
            filtered = [e for e in filtered 
                       if datetime.strptime(e['timestamp'], "%Y-%m-%d %H:%M:%S").date() == today]
        elif date_filter == "어제":
            from datetime import timedelta
            yesterday = today - timedelta(days=1)
            filtered = [e for e in filtered 
                       if datetime.strptime(e['timestamp'], "%Y-%m-%d %H:%M:%S").date() == yesterday]
        elif date_filter == "최근 7일":
            from datetime import timedelta
            week_ago = today - timedelta(days=7)
            filtered = [e for e in filtered 
                       if datetime.strptime(e['timestamp'], "%Y-%m-%d %H:%M:%S").date() >= week_ago]
        
        # 분류 필터
        category_filter = self.category_var.get()
        if category_filter != "전체":
            filtered = [e for e in filtered if e['category'] == category_filter]
        
        return filtered
    
    def export_to_txt(self):
        """현재 필터링된 데이터를 TXT로 추출"""
        filtered_data = self.filter_data()
        
        if not filtered_data:
            messagebox.showinfo("알림", "추출할 데이터가 없습니다.")
            return
        
        # 파일명 생성
        date_filter = self.date_var.get()
        category_filter = self.category_var.get()
        filename = f"트래킹_{date_filter}_{category_filter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # 저장 위치 선택
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=filename,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"=== 상태 트래킹 기록 ===\n")
                f.write(f"추출 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"필터: {date_filter} / {category_filter}\n")
                f.write(f"총 {len(filtered_data)}개 항목\n")
                f.write("="*50 + "\n\n")
                
                for entry in reversed(filtered_data):
                    f.write(f"[{entry['timestamp']}] [{entry['category']}]\n")
                    f.write(f"{entry['content']}\n\n")
            
            messagebox.showinfo("완료", f"파일이 저장되었습니다:\n{filepath}")
    
    def reset_data(self):
        """데이터 리셋"""
        result = messagebox.askyesno(
            "데이터 리셋", 
            "정말로 모든 데이터를 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다."
        )
        
        if result:
            self.data = []
            self.save_data()
            self.refresh_main_window()
            messagebox.showinfo("완료", "모든 데이터가 삭제되었습니다.")
    
    def quit_program(self):
        """프로그램 완전 종료"""
        result = messagebox.askyesno(
            "프로그램 종료",
            "프로그램을 완전히 종료하시겠습니까?\n(백그라운드 실행도 중단됩니다)"
        )
        
        if result:
            import sys
            sys.exit(0)

def on_activate_input():
    """입력창 단축키 활성화"""
    app.show_input_window()

def on_activate_main():
    """메인창 단축키 활성화"""
    app.show_main_window()

def start_hotkey_listener():
    """전역 단축키 리스너 시작"""
    with keyboard.GlobalHotKeys({
        '<ctrl>+<space>': on_activate_input,
        '<ctrl>+<shift>+<space>': on_activate_main
    }) as h:
        h.join()

if __name__ == "__main__":
    app = TrackingApp()
    
    # 단축키 리스너를 별도 스레드에서 실행
    hotkey_thread = threading.Thread(target=start_hotkey_listener, daemon=True)
    hotkey_thread.start()
    
    # 백그라운드 실행 (메인 창 자동으로 안 열림)
    # Shift+Space로 언제든 열 수 있음
    root = tk.Tk()
    root.withdraw()  # 숨기기
    root.mainloop()
