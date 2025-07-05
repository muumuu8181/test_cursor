#!/usr/bin/env python3
"""
Video Redundancy Remover - 冗長な間を削除する動画編集ツール

This tool automatically detects and removes redundant pauses/silent parts 
from videos to create shorter, more concise versions.
"""

import os
import sys
import argparse
import numpy as np
import librosa
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.AudioClip import AudioArrayClip
from scipy.signal import find_peaks
from tqdm import tqdm
import matplotlib.pyplot as plt


class VideoRedundancyRemover:
    """動画の冗長な間を削除するクラス"""
    
    def __init__(self, silence_threshold=-40, min_silence_duration=0.5, 
                 fade_duration=0.1, aggressive_mode=False):
        """
        初期化
        
        Args:
            silence_threshold: 無音判定の閾値（dB）
            min_silence_duration: 削除対象とする最小無音時間（秒）
            fade_duration: フェードイン/アウトの時間（秒）
            aggressive_mode: より積極的な削除を行うかどうか
        """
        self.silence_threshold = silence_threshold
        self.min_silence_duration = min_silence_duration
        self.fade_duration = fade_duration
        self.aggressive_mode = aggressive_mode
        
    def analyze_audio(self, audio_path):
        """音声を分析して無音区間を検出"""
        print("音声を分析中...")
        
        # 音声ファイルを読み込み
        y, sr = librosa.load(audio_path, sr=None)
        
        # RMS（Root Mean Square）を計算してボリュームレベルを取得
        frame_length = int(sr * 0.1)  # 0.1秒のフレーム
        hop_length = int(sr * 0.05)   # 0.05秒のホップ
        
        rms = librosa.feature.rms(y=y, frame_length=frame_length, 
                                 hop_length=hop_length)[0]
        
        # dBに変換
        rms_db = librosa.amplitude_to_db(rms)
        
        # 時間軸を作成
        times = librosa.frames_to_time(np.arange(len(rms_db)), 
                                      sr=sr, hop_length=hop_length)
        
        return times, rms_db, sr
    
    def detect_silence_segments(self, times, rms_db):
        """無音区間を検出"""
        print("無音区間を検出中...")
        
        # 無音判定
        silence_mask = rms_db < self.silence_threshold
        
        # 連続する無音区間をグループ化
        silence_segments = []
        start_time = None
        
        for i, (time, is_silent) in enumerate(zip(times, silence_mask)):
            if is_silent and start_time is None:
                start_time = time
            elif not is_silent and start_time is not None:
                duration = time - start_time
                if duration >= self.min_silence_duration:
                    silence_segments.append((start_time, time))
                start_time = None
        
        # 最後が無音で終わる場合
        if start_time is not None:
            duration = times[-1] - start_time
            if duration >= self.min_silence_duration:
                silence_segments.append((start_time, times[-1]))
        
        return silence_segments
    
    def detect_redundant_segments(self, times, rms_db):
        """冗長な区間（単純な繰り返しや長い沈黙など）を検出"""
        print("冗長な区間を検出中...")
        
        redundant_segments = []
        
        # 基本的な無音区間
        silence_segments = self.detect_silence_segments(times, rms_db)
        redundant_segments.extend(silence_segments)
        
        if self.aggressive_mode:
            # より積極的な検出
            # 非常に低いボリュームの区間も対象とする
            low_volume_threshold = self.silence_threshold + 10
            low_volume_mask = rms_db < low_volume_threshold
            
            # 低音量区間をグループ化
            start_time = None
            for i, (time, is_low_volume) in enumerate(zip(times, low_volume_mask)):
                if is_low_volume and start_time is None:
                    start_time = time
                elif not is_low_volume and start_time is not None:
                    duration = time - start_time
                    if duration >= self.min_silence_duration * 2:  # より長い区間のみ
                        redundant_segments.append((start_time, time))
                    start_time = None
        
        # 重複を削除してソート
        redundant_segments = sorted(list(set(redundant_segments)))
        
        return redundant_segments
    
    def process_video(self, input_path, output_path=None):
        """動画を処理して冗長な部分を削除"""
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_condensed{ext}"
        
        print(f"動画を処理中: {input_path}")
        
        # 動画を読み込み
        video = VideoFileClip(input_path)
        
        # 一時的に音声を抽出
        temp_audio_path = "temp_audio.wav"
        video.audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
        
        try:
            # 音声を分析
            times, rms_db, sr = self.analyze_audio(temp_audio_path)
            
            # 冗長な区間を検出
            redundant_segments = self.detect_redundant_segments(times, rms_db)
            
            print(f"検出された冗長区間: {len(redundant_segments)}個")
            
            # 統計情報を表示
            total_redundant_time = sum(end - start for start, end in redundant_segments)
            print(f"削除予定時間: {total_redundant_time:.2f}秒")
            print(f"元の動画時間: {video.duration:.2f}秒")
            print(f"予想最終時間: {video.duration - total_redundant_time:.2f}秒")
            
            # 保持する区間を計算
            keep_segments = []
            last_end = 0
            
            for start, end in redundant_segments:
                if start > last_end:
                    keep_segments.append((last_end, start))
                last_end = end
            
            # 最後の区間
            if last_end < video.duration:
                keep_segments.append((last_end, video.duration))
            
            # 動画クリップを作成
            video_clips = []
            for start, end in tqdm(keep_segments, desc="動画クリップを作成中"):
                if end - start > 0.1:  # 0.1秒以上の区間のみ
                    clip = video.subclip(start, end)
                    if self.fade_duration > 0:
                        clip = clip.fadeout(self.fade_duration).fadein(self.fade_duration)
                    video_clips.append(clip)
            
            if video_clips:
                # クリップを結合
                print("クリップを結合中...")
                final_video = concatenate_videoclips(video_clips)
                
                # 出力
                print(f"動画を出力中: {output_path}")
                final_video.write_videofile(output_path, codec='libx264', 
                                          audio_codec='aac', verbose=False, logger=None)
                
                print("✅ 処理完了!")
                print(f"出力ファイル: {output_path}")
                print(f"元の時間: {video.duration:.2f}秒")
                print(f"新しい時間: {final_video.duration:.2f}秒")
                print(f"短縮時間: {video.duration - final_video.duration:.2f}秒")
                print(f"短縮率: {((video.duration - final_video.duration) / video.duration) * 100:.1f}%")
                
                # クリーンアップ
                final_video.close()
            else:
                print("❌ 保持する区間が見つかりませんでした。")
                
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            video.close()
    
    def visualize_analysis(self, input_path, output_path="audio_analysis.png"):
        """音声分析結果を可視化"""
        print("音声分析を可視化中...")
        
        # 一時的に音声を抽出
        video = VideoFileClip(input_path)
        temp_audio_path = "temp_audio_viz.wav"
        video.audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
        
        try:
            # 音声を分析
            times, rms_db, sr = self.analyze_audio(temp_audio_path)
            redundant_segments = self.detect_redundant_segments(times, rms_db)
            
            # グラフを作成
            plt.figure(figsize=(15, 6))
            plt.plot(times, rms_db, label='Audio Level (dB)', alpha=0.7)
            plt.axhline(y=self.silence_threshold, color='r', linestyle='--', 
                       label=f'Silence Threshold ({self.silence_threshold}dB)')
            
            # 冗長区間をハイライト
            for start, end in redundant_segments:
                plt.axvspan(start, end, alpha=0.3, color='red', label='Redundant Segments')
            
            plt.xlabel('Time (seconds)')
            plt.ylabel('Audio Level (dB)')
            plt.title('Audio Analysis - Redundant Segments Detection')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"分析結果を保存: {output_path}")
            
        finally:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            video.close()


def main():
    parser = argparse.ArgumentParser(description='動画の冗長な間を削除するツール')
    parser.add_argument('input', help='入力動画ファイル')
    parser.add_argument('-o', '--output', help='出力動画ファイル')
    parser.add_argument('-t', '--threshold', type=float, default=-40,
                       help='無音判定の閾値（dB）、デフォルト: -40')
    parser.add_argument('-d', '--duration', type=float, default=0.5,
                       help='削除対象とする最小無音時間（秒）、デフォルト: 0.5')
    parser.add_argument('-f', '--fade', type=float, default=0.1,
                       help='フェードイン/アウトの時間（秒）、デフォルト: 0.1')
    parser.add_argument('-a', '--aggressive', action='store_true',
                       help='より積極的な削除を行う')
    parser.add_argument('-v', '--visualize', action='store_true',
                       help='音声分析結果を可視化する')
    
    args = parser.parse_args()
    
    # 入力ファイルの存在確認
    if not os.path.exists(args.input):
        print(f"❌ エラー: 入力ファイルが見つかりません: {args.input}")
        sys.exit(1)
    
    # 動画編集ツールを初期化
    remover = VideoRedundancyRemover(
        silence_threshold=args.threshold,
        min_silence_duration=args.duration,
        fade_duration=args.fade,
        aggressive_mode=args.aggressive
    )
    
    # 可視化が要求された場合
    if args.visualize:
        remover.visualize_analysis(args.input)
    
    # 動画を処理
    remover.process_video(args.input, args.output)


if __name__ == "__main__":
    main()