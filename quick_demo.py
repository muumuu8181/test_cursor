#!/usr/bin/env python3
"""
動画冗長部分削除ツール - クイックデモ

このスクリプトは、実際の動画ファイルなしでツールの機能を示します。
"""

import numpy as np
import matplotlib.pyplot as plt
from video_editor import VideoRedundancyRemover


def simulate_audio_analysis():
    """音声分析のシミュレーション"""
    print("🎵 音声分析のシミュレーション")
    print("-" * 30)
    
    # サンプル音声データを生成（実際の音声分析のシミュレーション）
    duration = 60  # 60秒の音声
    sample_rate = 20  # 20Hz（分析用の低いサンプルレート）
    
    # 時間軸を作成
    times = np.linspace(0, duration, duration * sample_rate)
    
    # 音声レベルをシミュレート（dB）
    # 通常の音声レベル（-20dB）と無音区間（-60dB）を混在
    audio_levels = np.random.normal(-25, 5, len(times))
    
    # 無音区間を挿入
    silence_periods = [
        (10, 13),   # 10-13秒: 長い沈黙
        (25, 26),   # 25-26秒: 短い沈黙
        (40, 44),   # 40-44秒: 長い沈黙
        (55, 57),   # 55-57秒: 短い沈黙
    ]
    
    for start, end in silence_periods:
        mask = (times >= start) & (times <= end)
        audio_levels[mask] = np.random.normal(-55, 2, np.sum(mask))
    
    # 動画編集ツールを初期化
    remover = VideoRedundancyRemover(
        silence_threshold=-40,
        min_silence_duration=0.5,
        fade_duration=0.1,
        aggressive_mode=False
    )
    
    # 冗長区間を検出
    redundant_segments = remover.detect_redundant_segments(times, audio_levels)
    
    # 結果を表示
    print(f"📊 分析結果:")
    print(f"   元の動画時間: {duration}秒")
    print(f"   検出された冗長区間: {len(redundant_segments)}個")
    
    total_redundant_time = sum(end - start for start, end in redundant_segments)
    print(f"   削除予定時間: {total_redundant_time:.2f}秒")
    print(f"   予想最終時間: {duration - total_redundant_time:.2f}秒")
    print(f"   短縮率: {(total_redundant_time / duration) * 100:.1f}%")
    
    # 冗長区間の詳細を表示
    print(f"\n📋 検出された冗長区間:")
    for i, (start, end) in enumerate(redundant_segments, 1):
        print(f"   {i}. {start:.1f}秒 - {end:.1f}秒 (時間: {end-start:.1f}秒)")
    
    # グラフを生成
    create_analysis_plot(times, audio_levels, redundant_segments, remover.silence_threshold)
    
    return redundant_segments


def create_analysis_plot(times, audio_levels, redundant_segments, threshold):
    """分析結果のプロットを作成"""
    print(f"\n📈 分析結果を可視化中...")
    
    plt.figure(figsize=(15, 6))
    
    # 音声レベルをプロット
    plt.plot(times, audio_levels, label='音声レベル (dB)', alpha=0.7, color='blue')
    
    # 無音判定閾値をプロット
    plt.axhline(y=threshold, color='red', linestyle='--', 
                label=f'無音判定閾値 ({threshold}dB)')
    
    # 冗長区間をハイライト
    for i, (start, end) in enumerate(redundant_segments):
        if i == 0:
            plt.axvspan(start, end, alpha=0.3, color='red', label='削除対象区間')
        else:
            plt.axvspan(start, end, alpha=0.3, color='red')
    
    plt.xlabel('時間 (秒)')
    plt.ylabel('音声レベル (dB)')
    plt.title('音声分析結果 - 冗長区間検出デモ')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 画像を保存
    plt.savefig('demo_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✅ 分析結果を保存: demo_analysis.png")
    
    # 画像を表示（環境によっては表示されない場合があります）
    try:
        plt.show()
    except:
        print("   （グラフの表示がサポートされていません）")
    
    plt.close()


def demonstrate_different_settings():
    """異なる設定での結果を比較"""
    print(f"\n⚙️  異なる設定での結果比較")
    print("-" * 40)
    
    # サンプル音声データ
    duration = 30
    sample_rate = 20
    times = np.linspace(0, duration, duration * sample_rate)
    
    # 音声レベルを生成
    audio_levels = np.random.normal(-25, 5, len(times))
    
    # 無音区間を挿入
    silence_periods = [(5, 8), (15, 16), (22, 25)]
    for start, end in silence_periods:
        mask = (times >= start) & (times <= end)
        audio_levels[mask] = np.random.normal(-55, 2, np.sum(mask))
    
    # 異なる設定を試す
    settings = [
        {
            "name": "保守的設定",
            "silence_threshold": -35,
            "min_silence_duration": 1.0,
            "aggressive_mode": False
        },
        {
            "name": "標準設定",
            "silence_threshold": -40,
            "min_silence_duration": 0.5,
            "aggressive_mode": False
        },
        {
            "name": "積極的設定",
            "silence_threshold": -45,
            "min_silence_duration": 0.3,
            "aggressive_mode": True
        }
    ]
    
    for setting in settings:
        print(f"\n📋 {setting['name']}:")
        print(f"   無音判定閾値: {setting['silence_threshold']}dB")
        print(f"   最小無音時間: {setting['min_silence_duration']}秒")
        print(f"   積極的モード: {'ON' if setting['aggressive_mode'] else 'OFF'}")
        
        # ツールを初期化
        remover = VideoRedundancyRemover(
            silence_threshold=setting['silence_threshold'],
            min_silence_duration=setting['min_silence_duration'],
            fade_duration=0.1,
            aggressive_mode=setting['aggressive_mode']
        )
        
        # 冗長区間を検出
        redundant_segments = remover.detect_redundant_segments(times, audio_levels)
        
        # 結果を表示
        total_redundant_time = sum(end - start for start, end in redundant_segments)
        print(f"   検出区間数: {len(redundant_segments)}個")
        print(f"   削除時間: {total_redundant_time:.2f}秒")
        print(f"   短縮率: {(total_redundant_time / duration) * 100:.1f}%")


def show_performance_info():
    """パフォーマンス情報を表示"""
    print(f"\n⚡ パフォーマンス情報")
    print("-" * 25)
    
    video_lengths = [
        (5, "5分"),
        (10, "10分"),
        (30, "30分"),
        (60, "1時間"),
        (120, "2時間")
    ]
    
    print("📊 予想処理時間:")
    for minutes, label in video_lengths:
        # 概算処理時間（実際の処理時間は環境によって異なります）
        estimated_time = minutes * 0.3  # 元の動画の約30%の時間
        print(f"   {label}の動画: 約{estimated_time:.1f}分")
    
    print(f"\n💾 予想メモリ使用量:")
    for minutes, label in video_lengths:
        # 概算メモリ使用量
        estimated_memory = minutes * 8  # 1分あたり約8MB
        print(f"   {label}の動画: 約{estimated_memory}MB")


def main():
    """メイン関数"""
    print("🎬 動画冗長部分削除ツール - クイックデモ")
    print("=" * 50)
    
    # 各種デモを実行
    simulate_audio_analysis()
    demonstrate_different_settings()
    show_performance_info()
    
    print("\n" + "=" * 50)
    print("🎯 次のステップ:")
    print("1. 実際の動画ファイルで試してみる:")
    print("   python video_editor.py your_video.mp4")
    print("2. GUI版を使用してみる:")
    print("   python gui_video_editor.py")
    print("3. 複数ファイルを一括処理してみる:")
    print("   python batch_process.py *.mp4 -o output")


if __name__ == "__main__":
    main()