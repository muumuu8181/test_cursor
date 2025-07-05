#!/usr/bin/env python3
"""
Batch Video Processing - 複数動画の一括処理

複数の動画ファイルを一度に処理して冗長な部分を削除する
"""

import os
import sys
import argparse
import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from video_editor import VideoRedundancyRemover


def process_single_video(video_path, output_dir, settings):
    """単一の動画を処理"""
    try:
        print(f"処理中: {video_path}")
        
        # 出力パスを生成
        video_name = Path(video_path).stem
        video_ext = Path(video_path).suffix
        output_path = os.path.join(output_dir, f"{video_name}_condensed{video_ext}")
        
        # 動画編集ツールを初期化
        remover = VideoRedundancyRemover(
            silence_threshold=settings['threshold'],
            min_silence_duration=settings['min_duration'],
            fade_duration=settings['fade_duration'],
            aggressive_mode=settings['aggressive']
        )
        
        # 動画を処理
        remover.process_video(video_path, output_path)
        
        return {'success': True, 'input': video_path, 'output': output_path}
        
    except Exception as e:
        return {'success': False, 'input': video_path, 'error': str(e)}


def batch_process_videos(input_patterns, output_dir, settings, max_workers=2):
    """複数の動画を一括処理"""
    # 入力ファイルリストを作成
    video_files = []
    for pattern in input_patterns:
        if os.path.isfile(pattern):
            video_files.append(pattern)
        else:
            # グロブパターンとして処理
            video_files.extend(glob.glob(pattern))
    
    if not video_files:
        print("❌ 処理対象のファイルが見つかりません")
        return
    
    # 重複を削除
    video_files = list(set(video_files))
    
    print(f"処理対象: {len(video_files)}個のファイル")
    for video_file in video_files:
        print(f"  - {video_file}")
    
    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 結果記録用
    results = []
    
    # 並列処理で動画を処理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # タスクを投入
        futures = [
            executor.submit(process_single_video, video_file, output_dir, settings)
            for video_file in video_files
        ]
        
        # 結果を収集
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['success']:
                print(f"✅ 完了: {result['input']} -> {result['output']}")
            else:
                print(f"❌ エラー: {result['input']} - {result['error']}")
    
    # 結果を集計
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\n=== 処理結果 ===")
    print(f"成功: {successful}個")
    print(f"失敗: {failed}個")
    print(f"合計: {len(results)}個")
    
    # 失敗したファイルの詳細を表示
    if failed > 0:
        print("\n=== 失敗したファイル ===")
        for result in results:
            if not result['success']:
                print(f"  - {result['input']}: {result['error']}")


def main():
    parser = argparse.ArgumentParser(description='複数動画の一括処理ツール')
    parser.add_argument('inputs', nargs='+', help='入力動画ファイル（複数可、グロブパターン対応）')
    parser.add_argument('-o', '--output-dir', default='output', 
                       help='出力ディレクトリ、デフォルト: output')
    parser.add_argument('-t', '--threshold', type=float, default=-40,
                       help='無音判定の閾値（dB）、デフォルト: -40')
    parser.add_argument('-d', '--duration', type=float, default=0.5,
                       help='削除対象とする最小無音時間（秒）、デフォルト: 0.5')
    parser.add_argument('-f', '--fade', type=float, default=0.1,
                       help='フェードイン/アウトの時間（秒）、デフォルト: 0.1')
    parser.add_argument('-a', '--aggressive', action='store_true',
                       help='より積極的な削除を行う')
    parser.add_argument('-w', '--workers', type=int, default=2,
                       help='並列処理の数、デフォルト: 2')
    
    args = parser.parse_args()
    
    # 設定
    settings = {
        'threshold': args.threshold,
        'min_duration': args.duration,
        'fade_duration': args.fade,
        'aggressive': args.aggressive
    }
    
    # 一括処理を実行
    batch_process_videos(args.inputs, args.output_dir, settings, args.workers)


if __name__ == "__main__":
    main()