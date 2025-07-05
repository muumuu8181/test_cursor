#!/usr/bin/env python3
"""
動画冗長部分削除ツール - 使用例

このファイルは、VideoRedundancyRemoverクラスの基本的な使用方法を示します。
"""

import os
from video_editor import VideoRedundancyRemover


def basic_usage_example():
    """基本的な使用例"""
    print("=== 基本的な使用例 ===")
    
    # 動画ファイルのパス（実際のファイルパスに変更してください）
    input_video = "sample_video.mp4"
    output_video = "sample_video_condensed.mp4"
    
    # ファイルが存在するかチェック
    if not os.path.exists(input_video):
        print(f"⚠️  サンプル動画ファイルが見つかりません: {input_video}")
        print("   実際の動画ファイルパスに変更してください。")
        return
    
    # 動画編集ツールを初期化
    remover = VideoRedundancyRemover(
        silence_threshold=-40,      # 無音判定閾値（dB）
        min_silence_duration=0.5,   # 最小無音時間（秒）
        fade_duration=0.1,          # フェード時間（秒）
        aggressive_mode=False       # 通常モード
    )
    
    # 動画を処理
    remover.process_video(input_video, output_video)
    
    print(f"✅ 処理完了: {output_video}")


def advanced_usage_example():
    """高度な使用例"""
    print("\n=== 高度な使用例 ===")
    
    input_video = "lecture_video.mp4"
    output_video = "lecture_video_condensed.mp4"
    
    if not os.path.exists(input_video):
        print(f"⚠️  サンプル動画ファイルが見つかりません: {input_video}")
        print("   実際の動画ファイルパスに変更してください。")
        return
    
    # より積極的な設定
    remover = VideoRedundancyRemover(
        silence_threshold=-35,      # より厳しい無音判定
        min_silence_duration=0.8,   # より長い無音のみ削除
        fade_duration=0.2,          # より長いフェード
        aggressive_mode=True        # 積極的モード
    )
    
    # 分析結果を可視化
    print("音声分析を実行中...")
    remover.visualize_analysis(input_video, "lecture_analysis.png")
    
    # 動画を処理
    print("動画を処理中...")
    remover.process_video(input_video, output_video)
    
    print(f"✅ 処理完了: {output_video}")
    print(f"📊 分析結果: lecture_analysis.png")


def batch_processing_example():
    """複数ファイルの処理例"""
    print("\n=== 複数ファイルの処理例 ===")
    
    # 処理するファイルのリスト
    video_files = [
        "video1.mp4",
        "video2.mp4",
        "video3.mp4"
    ]
    
    # 存在するファイルをフィルタリング
    existing_files = [f for f in video_files if os.path.exists(f)]
    
    if not existing_files:
        print("⚠️  処理可能な動画ファイルが見つかりません。")
        print("   video_files リストを実際のファイルパスに変更してください。")
        return
    
    # 設定
    remover = VideoRedundancyRemover(
        silence_threshold=-40,
        min_silence_duration=0.5,
        fade_duration=0.1,
        aggressive_mode=False
    )
    
    # 各ファイルを処理
    for input_file in existing_files:
        try:
            # 出力ファイル名を生成
            name, ext = os.path.splitext(input_file)
            output_file = f"{name}_condensed{ext}"
            
            print(f"処理中: {input_file} -> {output_file}")
            remover.process_video(input_file, output_file)
            print(f"✅ 完了: {output_file}")
            
        except Exception as e:
            print(f"❌ エラー: {input_file} - {str(e)}")


def custom_settings_example():
    """カスタム設定例"""
    print("\n=== カスタム設定例 ===")
    
    # 異なる用途に応じた設定例
    settings_presets = {
        "講義動画": {
            "silence_threshold": -35,
            "min_silence_duration": 1.0,
            "fade_duration": 0.1,
            "aggressive_mode": True,
            "description": "講義の長い沈黙を削除"
        },
        "会議録画": {
            "silence_threshold": -45,
            "min_silence_duration": 0.3,
            "fade_duration": 0.2,
            "aggressive_mode": False,
            "description": "会議の短い沈黙も削除、自然なトランジション"
        },
        "ポッドキャスト": {
            "silence_threshold": -50,
            "min_silence_duration": 0.2,
            "fade_duration": 0.05,
            "aggressive_mode": True,
            "description": "音声コンテンツの微細な沈黙も削除"
        }
    }
    
    # 設定を表示
    for preset_name, settings in settings_presets.items():
        print(f"\n📋 {preset_name}用設定:")
        print(f"   説明: {settings['description']}")
        print(f"   無音判定閾値: {settings['silence_threshold']}dB")
        print(f"   最小無音時間: {settings['min_silence_duration']}秒")
        print(f"   フェード時間: {settings['fade_duration']}秒")
        print(f"   積極的モード: {'ON' if settings['aggressive_mode'] else 'OFF'}")
        
        # 実際に処理する場合のコード例
        print(f"   使用例:")
        print(f"   remover = VideoRedundancyRemover(")
        print(f"       silence_threshold={settings['silence_threshold']},")
        print(f"       min_silence_duration={settings['min_silence_duration']},")
        print(f"       fade_duration={settings['fade_duration']},")
        print(f"       aggressive_mode={settings['aggressive_mode']}")
        print(f"   )")


def main():
    """メイン関数"""
    print("🎬 動画冗長部分削除ツール - 使用例")
    print("=" * 50)
    
    # 各種使用例を実行
    basic_usage_example()
    advanced_usage_example()
    batch_processing_example()
    custom_settings_example()
    
    print("\n" + "=" * 50)
    print("📝 メモ:")
    print("• 実際に処理を行うには、動画ファイルパスを変更してください")
    print("• 設定値は動画の種類に応じて調整してください")
    print("• 大きなファイルの処理には時間がかかる場合があります")


if __name__ == "__main__":
    main()