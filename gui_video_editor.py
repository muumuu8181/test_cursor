#!/usr/bin/env python3
"""
GUI Video Redundancy Remover - 動画冗長部分削除ツール（GUI版）

シンプルなGUIを使用して動画の冗長な間を削除する
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
from video_editor import VideoRedundancyRemover


class VideoEditorGUI:
    """動画編集ツールのGUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("動画冗長部分削除ツール")
        self.root.geometry("600x500")
        
        # 変数
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.threshold = tk.DoubleVar(value=-40.0)
        self.min_duration = tk.DoubleVar(value=0.5)
        self.fade_duration = tk.DoubleVar(value=0.1)
        self.aggressive_mode = tk.BooleanVar(value=False)
        self.visualize = tk.BooleanVar(value=False)
        
        self.create_widgets()
        
    def create_widgets(self):
        """ウィジェットを作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 入力ファイル選択
        ttk.Label(main_frame, text="入力動画ファイル:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="選択", command=self.select_input_file).grid(row=0, column=2, padx=5)
        
        # 出力ファイル選択
        ttk.Label(main_frame, text="出力動画ファイル:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="選択", command=self.select_output_file).grid(row=1, column=2, padx=5)
        
        # 設定フレーム
        settings_frame = ttk.LabelFrame(main_frame, text="設定", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        
        # 無音判定閾値
        ttk.Label(settings_frame, text="無音判定閾値 (dB):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Scale(settings_frame, from_=-60, to=-20, variable=self.threshold, 
                 orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, padx=5)
        ttk.Label(settings_frame, textvariable=self.threshold).grid(row=0, column=2, padx=5)
        
        # 最小無音時間
        ttk.Label(settings_frame, text="最小無音時間 (秒):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Scale(settings_frame, from_=0.1, to=2.0, variable=self.min_duration, 
                 orient=tk.HORIZONTAL, length=200).grid(row=1, column=1, padx=5)
        ttk.Label(settings_frame, textvariable=self.min_duration).grid(row=1, column=2, padx=5)
        
        # フェード時間
        ttk.Label(settings_frame, text="フェード時間 (秒):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Scale(settings_frame, from_=0.0, to=1.0, variable=self.fade_duration, 
                 orient=tk.HORIZONTAL, length=200).grid(row=2, column=1, padx=5)
        ttk.Label(settings_frame, textvariable=self.fade_duration).grid(row=2, column=2, padx=5)
        
        # オプション
        options_frame = ttk.LabelFrame(main_frame, text="オプション", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        ttk.Checkbutton(options_frame, text="積極的モード", 
                       variable=self.aggressive_mode).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="分析結果を可視化", 
                       variable=self.visualize).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # 実行ボタン
        ttk.Button(main_frame, text="動画を処理", command=self.process_video,
                  style="Accent.TButton").grid(row=4, column=0, columnspan=3, pady=20)
        
        # プログレスバー
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky="ew", pady=5)
        
        # ログ表示
        log_frame = ttk.LabelFrame(main_frame, text="ログ", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # グリッドの重みを設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def select_input_file(self):
        """入力ファイルを選択"""
        filename = filedialog.askopenfilename(
            title="動画ファイルを選択",
            filetypes=[
                ("動画ファイル", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
                ("すべてのファイル", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            # 出力ファイル名を自動生成
            if not self.output_file.get():
                name, ext = os.path.splitext(filename)
                self.output_file.set(f"{name}_condensed{ext}")
    
    def select_output_file(self):
        """出力ファイルを選択"""
        filename = filedialog.asksaveasfilename(
            title="出力ファイルを選択",
            defaultextension=".mp4",
            filetypes=[
                ("MP4ファイル", "*.mp4"),
                ("動画ファイル", "*.avi *.mov *.mkv *.wmv *.flv"),
                ("すべてのファイル", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
    
    def log(self, message):
        """ログメッセージを表示"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def process_video(self):
        """動画を処理"""
        if not self.input_file.get():
            messagebox.showerror("エラー", "入力ファイルを選択してください")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("エラー", "入力ファイルが見つかりません")
            return
        
                # 処理を別スレッドで実行
        threading.Thread(target=self._process_video_thread, daemon=True).start()
    
    def _process_video_thread(self):
        """動画処理のスレッド"""
        try:
            # プログレスバーを開始
            self.progress.start()
            
            # ログをクリア
            self.log_text.delete(1.0, tk.END)
            
            self.log("処理を開始しています...")
            
            # 動画編集ツールを初期化
            remover = VideoRedundancyRemover(
                silence_threshold=int(self.threshold.get()),
                min_silence_duration=self.min_duration.get(),
                fade_duration=self.fade_duration.get(),
                aggressive_mode=self.aggressive_mode.get()
            )
            
            # 可視化が要求された場合
            if self.visualize.get():
                self.log("分析結果を可視化中...")
                remover.visualize_analysis(self.input_file.get())
            
            # 動画を処理
            self.log("動画処理を開始...")
            remover.process_video(self.input_file.get(), self.output_file.get())
            
            self.log("✅ 処理が完了しました!")
            messagebox.showinfo("完了", "動画の処理が完了しました！")
            
        except Exception as e:
            self.log(f"❌ エラーが発生しました: {str(e)}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました:\n{str(e)}")
        
        finally:
            # プログレスバーを停止
            self.progress.stop()


def main():
    """メイン関数"""
    root = tk.Tk()
    app = VideoEditorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()