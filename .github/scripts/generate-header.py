#!/usr/bin/env python3
"""
ヘッダー画像生成スクリプト 🐱✨

fal.aiのnano-banana-proを使って画像を生成するニャ！
または、SVG形式でベクター画像を出力できるニャ！

Usage:
    # PNG画像（fal.ai）
    python generate-header.py --tag v1.0.0 --theme feature --output header.png

    # SVG画像（ベクター）
    python generate-header.py --tag v1.0.0 --format svg --output header.svg

    # パターンとカラーマップを指定
    python generate-header.py --tag v1.0.0 --format svg --pattern stripes --colormap ocean
"""

import argparse
import os
import sys
from pathlib import Path


# 猫っぽいメッセージ 🐱
def meow_print(message: str, level: str = "info") -> None:
    """猫っぽいメッセージを表示するニャ"""
    icons = {
        "info": "🐱",
        "success": "😺",
        "error": "😿",
        "warning": "😸",
        "debug": "🙀"
    }
    icon = icons.get(level, "🐱")
    print(f"{icon} {message}")


# テーマ別のプロンプトテンプレート 🎨
PROMPT_TEMPLATES = {
    "feature": """A futuristic, abstract background featuring a stunning gradient from deep blue to vibrant purple, reminiscent of a cosmic nebula. Floating geometric particles and digital data streams weave through the composition, creating a sense of innovation and technological advancement. The colors blend seamlessly, evoking the excitement of new features and capabilities being unleashed. Clean, modern, with soft lighting effects and a subtle glass-like texture overlay.""",

    "bugfix": """A serene, abstract background with a smooth gradient from calming green to refreshing blue, symbolizing stability and resolution. Delicate light particles float upward like fireflies, creating a sense of harmony and balance. Soft, ethereal lighting with a subtle wave pattern suggests gentle improvement and refinement. The composition evokes the feeling of a system restored to perfect health, with clean lines and a peaceful atmosphere.""",

    "major": """A spectacular, vibrant abstract background featuring an explosive gradient from deep purple through hot pink to warm orange, creating a sense of momentous occasion and celebration. Dynamic energy flows through the composition with swirling patterns of light and color, like a cosmic event. Golden sparkles and star-like particles dance across the canvas, suggesting something extraordinary and transformative. The image radiates excitement and importance, with rich, saturated colors that demand attention.""",

    "patch": """A clean, minimalist abstract background with an elegant gradient from silver to light blue, conveying precision and reliability. Fine geometric lines and subtle grid patterns create a sense of order and attention to detail. Soft, professional lighting with a subtle metallic texture suggests quality and refinement. The composition embodies the feeling of careful maintenance and improvement, like a finely tuned instrument being perfected.""",

    "first": """A magical, celebratory abstract background featuring a stunning rainbow gradient that flows across the entire spectrum. Ethereal particles of light shimmer and sparkle throughout, creating an atmosphere of wonder and new beginnings. The colors blend in a dreamy, cosmic swirl, suggesting infinite possibilities and the dawn of something special. Soft, glowing orbs of light float gracefully, like wishes being granted. The image radiates hope, excitement, and the joy of a first release, with a captivating otherworldly beauty."""
}


# アスペクト比の設定 📐
ASPECT_RATIOS = {
    "16:9": {"width": 1920, "height": 1080},
    "4:3": {"width": 1440, "height": 1080},
    "1:1": {"width": 1080, "height": 1080},
    "21:9": {"width": 2560, "height": 1080},
}


# カラーマップ定義 🎨
# SVGグラデーション用の色ペア
COLORMAPS = {
    "cat": {
        "name": "Cat Theme",
        "colors": ["#ff9f43", "#ee5a24", "#feca57"],
        "bg_start": "#1a1a2e",
        "bg_mid": "#2d3436",
        "bg_end": "#1a1a2e",
        "text": ["#74b9ff", "#a29bfe", "#fd79a8"],
        "pattern_color": "#ff9f43"
    },
    "ocean": {
        "name": "Ocean",
        "colors": ["#0077b6", "#00b4d8", "#90e0ef"],
        "bg_start": "#023e8a",
        "bg_mid": "#0077b6",
        "bg_end": "#03045e",
        "text": ["#caf0f8", "#90e0ef", "#ade8f4"],
        "pattern_color": "#00b4d8"
    },
    "sunset": {
        "name": "Sunset",
        "colors": ["#ff6b6b", "#feca57", "#ff9ff3"],
        "bg_start": "#2d3436",
        "bg_mid": "#636e72",
        "bg_end": "#2d3436",
        "text": ["#ffeaa7", "#fdcb6e", "#f8b500"],
        "pattern_color": "#ff6b6b"
    },
    "forest": {
        "name": "Forest",
        "colors": ["#27ae60", "#2ecc71", "#58d68d"],
        "bg_start": "#1e5128",
        "bg_mid": "#194d2c",
        "bg_end": "#0f3d1f",
        "text": ["#a9dfbf", "#7dcea0", "#52be80"],
        "pattern_color": "#27ae60"
    },
    "neon": {
        "name": "Neon",
        "colors": ["#ff00ff", "#00ffff", "#ff00aa"],
        "bg_start": "#0a0a0a",
        "bg_mid": "#1a1a1a",
        "bg_end": "#0a0a0a",
        "text": ["#ff00ff", "#00ffff", "#ff00aa"],
        "pattern_color": "#ff00ff"
    }
}


# パターン定義 🐾
# SVG pattern要素の定義
PATTERNS = {
    "paws": {
        "name": "Paw Prints",
        "pattern": '''<pattern id="pattern" width="60" height="60" patternUnits="userSpaceOnUse">
      <g opacity="0.08">
        <circle cx="20" cy="20" r="6" fill="{pattern_color}"/>
        <circle cx="35" cy="15" r="3" fill="{pattern_color}"/>
        <circle cx="45" cy="20" r="3" fill="{pattern_color}"/>
        <circle cx="50" cy="28" r="3" fill="{pattern_color}"/>
        <circle cx="30" cy="28" r="3" fill="{pattern_color}"/>
      </g>
    </pattern>'''
    },
    "stripes": {
        "name": "Stripes",
        "pattern": '''<pattern id="pattern" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <g opacity="0.05">
        <rect x="0" y="0" width="20" height="40" fill="{pattern_color}"/>
      </g>
    </pattern>'''
    },
    "dots": {
        "name": "Dots",
        "pattern": '''<pattern id="pattern" width="30" height="30" patternUnits="userSpaceOnUse">
      <g opacity="0.1">
        <circle cx="15" cy="15" r="4" fill="{pattern_color}"/>
      </g>
    </pattern>'''
    },
    "geometric": {
        "name": "Geometric",
        "pattern": '''<pattern id="pattern" width="50" height="50" patternUnits="userSpaceOnUse">
      <g opacity="0.06">
        <polygon points="25,0 50,25 25,50 0,25" fill="{pattern_color}"/>
      </g>
    </pattern>'''
    },
    "waves": {
        "name": "Waves",
        "pattern": '''<pattern id="pattern" width="100" height="30" patternUnits="userSpaceOnUse">
      <g opacity="0.08">
        <path d="M0,15 Q25,5 50,15 T100,15" fill="none" stroke="{pattern_color}" stroke-width="2"/>
        <path d="M0,25 Q25,15 50,25 T100,25" fill="none" stroke="{pattern_color}" stroke-width="1.5"/>
      </g>
    </pattern>'''
    }
}


def get_fal_key() -> str:
    """FAL_KEY環境変数からAPIキーを取得するニャ"""
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        meow_print("FAL_KEY環境変数が設定されていないニャ... 💦", "error")
        meow_print("export FAL_KEY='your-api-key' って設定してね！", "info")
        sys.exit(1)
    return api_key


def detect_theme_from_tag(tag: str) -> str:
    """タグからテーマを自動検出するニャ"""
    tag_lower = tag.lower()

    # メジャーリリース (v2.0.0, v3.0.0 など)
    if "v0." in tag or tag.count(".") == 2 and tag.split(".")[1] == "0":
        if "v0.1.0" in tag or "v1.0.0" in tag:
            return "first"
        return "major"

    # マイナーリリース (v1.1.0, v1.2.0 など)
    if tag.count(".") == 2 and tag.split(".")[2] == "0":
        return "feature"

    # パッチリリース (v1.1.1, v1.1.2 など)
    if tag.count(".") == 2:
        return "patch"

    # デフォルトはfeature
    return "feature"


def build_prompt(tag: str, theme: str) -> str:
    """プロンプトを構築するニャ"""
    base_prompt = PROMPT_TEMPLATES.get(theme, PROMPT_TEMPLATES["feature"])

    # タグ情報を追加
    prompt = f"""{base_prompt}

In the center, subtly incorporate version text "{tag}" in a modern, minimalist style. The text should be elegant and not overpower the abstract beauty of the background. Use a clean, contemporary font with a subtle glow effect that complements the color scheme."""

    return prompt


def generate_image(prompt: str, output_path: str, aspect_ratio: str, api_key: str) -> bool:
    """fal.aiで画像を生成するニャ"""
    try:
        import fal_client
    except ImportError:
        meow_print("fal-clientがインストールされていないニャ... 💦", "error")
        meow_print("pip install fal-client でインストールしてね！", "info")
        return False

    meow_print("fal.aiに接続中... 🚀", "info")

    # アスペクト比からサイズを取得
    size = ASPECT_RATIOS.get(aspect_ratio, ASPECT_RATIOS["16:9"])
    width = size["width"]
    height = size["height"]

    meow_print(f"画像サイズ: {width}x{height} ({aspect_ratio})", "info")
    meow_print("nano-banana-proで生成中... 🎨", "info")

    # 環境変数にFAL_KEYを設定
    os.environ["FAL_KEY"] = api_key

    try:
        # fal.aiのAPIを呼び出し
        result = fal_client.subscribe(
            "fal-ai/nano-banana-pro",
            arguments={
                "prompt": prompt,
                "num_images": 1,
                "aspect_ratio": aspect_ratio,
                "output_format": "png",
                "resolution": "2K",
                "safety_tolerance": "4"
            },
            with_logs=True
        )

        # 結果から画像を取得
        if isinstance(result, dict) and result.get("images"):
            image_url = result["images"][0]["url"]
        elif hasattr(result, 'get'):
            images = result.get('images', [])
            if images and len(images) > 0:
                image_url = images[0].get('url') if isinstance(images[0], dict) else images[0]
            else:
                image_url = None
        else:
            image_url = getattr(result, 'image_url', None)

        if not image_url:
            meow_print("画像URLが取得できなかったニャ... 💦", "error")
            meow_print(f"結果: {result}", "debug")
            return False

        meow_print(f"画像をダウンロード中... 📥", "info")

        # 画像をダウンロード
        import urllib.request
        urllib.request.urlretrieve(image_url, output_path)

        meow_print(f"画像を保存したニャ！: {output_path} 😺", "success")
        return True

    except Exception as e:
        meow_print(f"画像生成でエラーが発生したニャ... 😿", "error")
        meow_print(f"エラー詳細: {str(e)}", "error")
        return False


def generate_svg(
    tag: str,
    output_path: str,
    pattern: str = "paws",
    colormap: str = "cat",
    width: int = 1200,
    height: int = 315
) -> bool:
    """SVGヘッダー画像を生成するニャ 🐱

    Args:
        tag: バージョンタグ (例: v1.0.0)
        output_path: 出力ファイルパス
        pattern: パターン名 (paws, stripes, dots, geometric, waves)
        colormap: カラーマップ名 (cat, ocean, sunset, forest, neon)
        width: 画像幅
        height: 画像高さ
    """
    # カラーマップを取得
    colors = COLORMAPS.get(colormap, COLORMAPS["cat"])
    pattern_def = PATTERNS.get(pattern, PATTERNS["paws"])

    # パターンの色を置換
    pattern_svg = pattern_def["pattern"].format(pattern_color=colors["pattern_color"])

    # テキストグラデーションの色
    text_colors = colors["text"]
    text_gradient_stops = "\n".join([
        f'      <stop offset="{i*50}%" style="stop-color:{color}">\n'
        f'        <animate attributeName="stop-color" values="{color};{text_colors[(i+1)%3]};{color}" dur="4s" repeatCount="indefinite"/>\n'
        f'      </stop>'
        for i, color in enumerate(text_colors)
    ])

    # メイングラデーションの色
    main_colors = colors["colors"]
    main_gradient_stops = "\n".join([
        f'      <stop offset="{i*50}%" style="stop-color:{color}">\n'
        f'        <animate attributeName="stop-color" values="{color};{main_colors[(i+1)%3]};{color}" dur="3s" repeatCount="indefinite"/>\n'
        f'      </stop>'
        for i, color in enumerate(main_colors)
    ])

    # SVGテンプレート
    svg_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Gradient Background - {colormap.capitalize()} Colors -->
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors["bg_start"]}">
        <animate attributeName="stop-color" values="{colors["bg_start"]};{colors["bg_mid"]};{colors["bg_start"]}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" style="stop-color:{colors["bg_mid"]}">
        <animate attributeName="stop-color" values="{colors["bg_mid"]};{colors["bg_end"]};{colors["bg_mid"]}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" style="stop-color:{colors["bg_end"]}">
        <animate attributeName="stop-color" values="{colors["bg_end"]};{colors["bg_mid"]};{colors["bg_end"]}" dur="8s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Main Gradient -->
    <linearGradient id="main-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
{main_gradient_stops}
    </linearGradient>

    <!-- Text Gradient -->
    <linearGradient id="text-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
{text_gradient_stops}
    </linearGradient>

    <!-- Glow Effect -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="coloredBlur">
        <animate attributeName="stdDeviation" values="4;6;4" dur="2s" repeatCount="indefinite"/>
      </feGaussianBlur>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Pattern: {pattern_def["name"]} -->
{pattern_svg}
  </defs>

  <style>
    @keyframes float {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-8px); }}
    }}
    @keyframes shimmer {{
      0% {{ opacity: 0.3; }}
      50% {{ opacity: 0.8; }}
      100% {{ opacity: 0.3; }}
    }}
    @keyframes slideIn {{
      from {{ opacity: 0; transform: translateX(-20px); }}
      to {{ opacity: 1; transform: translateX(0); }}
    }}
    .main-text {{ animation: float 3s ease-in-out infinite; }}
    .badge {{ animation: slideIn 0.5s ease-out; }}
    .sparkle {{ animation: shimmer 2s ease-in-out infinite; }}
  </style>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bg-gradient)"/>
  <rect width="{width}" height="{height}" fill="url(#pattern)"/>

  <!-- Decorative Circles -->
  <circle cx="80" cy="{height//2}" r="70" fill="none" stroke="{colors["pattern_color"]}" stroke-width="2" opacity="0.1">
    <animate attributeName="r" values="70;75;70" dur="4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{width-80}" cy="{height//2}" r="90" fill="none" stroke="{colors["text"][0]}" stroke-width="2" opacity="0.1">
    <animate attributeName="r" values="90;95;90" dur="5s" repeatCount="indefinite"/>
  </circle>

  <!-- Version Badge -->
  <g class="badge">
    <rect x="{width//2 - 120}" y="40" width="240" height="45" rx="22.5" fill="url(#main-gradient)" opacity="0.4"/>
    <text x="{width//2}" y="70" text-anchor="middle" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="20" font-weight="600" fill="#fff" letter-spacing="2">{tag.upper()}</text>
  </g>

  <!-- Main Text -->
  <text x="{width//2}" y="{height//2 + 30}" text-anchor="middle" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="48" font-weight="900" fill="url(#text-gradient)" filter="url(#glow)" letter-spacing="3" class="main-text">RELEASE {tag.lstrip('v')}</text>

  <!-- Sparkles -->
  <g class="sparkle">
    <polygon points="{width*0.25},{height*0.25} {width*0.25+5},{height*0.25+10} {width*0.25+15},{height*0.25+10} {width*0.25+7},{height*0.25+17} {width*0.25+10},{height*0.25+27} {width*0.25},{height*0.25+20} {width*0.25-10},{height*0.25+27} {width*0.25-7},{height*0.25+17} {width*0.25-15},{height*0.25+10} {width*0.25-5},{height*0.25+10}" fill="{colors["colors"][1]}"/>
  </g>
  <g class="sparkle" style="animation-delay: 0.7s">
    <polygon points="{width*0.75},{height*0.75} {width*0.75+3},{height*0.75+7} {width*0.75+10},{height*0.75+7} {width*0.75+4},{height*0.75+12} {width*0.75+6},{height*0.75+19} {width*0.75},{height*0.75+14} {width*0.75-6},{height*0.75+19} {width*0.75-4},{height*0.75+12} {width*0.75-10},{height*0.75+7} {width*0.75-3},{height*0.75+7}" fill="{colors["text"][1]}"/>
  </g>
  <g class="sparkle" style="animation-delay: 1.4s">
    <polygon points="{width*0.2},{height*0.8} {width*0.2+3},{height*0.8+7} {width*0.2+10},{height*0.8+7} {width*0.2+4},{height*0.8+12} {width*0.2+6},{height*0.8+19} {width*0.2},{height*0.8+14} {width*0.2-6},{height*0.8+19} {width*0.2-4},{height*0.8+12} {width*0.2-10},{height*0.8+7} {width*0.2-3},{height*0.8+7}" fill="{colors["text"][2]}"/>
  </g>

  <!-- Corner Decorations -->
  <g opacity="0.2" fill="{colors["pattern_color"]}">
    <circle cx="20" cy="{height-20}" r="4"/>
    <circle cx="{width-20}" cy="20" r="4"/>
    <circle cx="{width-20}" cy="{height-20}" r="4"/>
  </g>
</svg>'''

    # 出力ディレクトリの作成
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # SVGファイルを書き込み
    output_file.write_text(svg_template, encoding='utf-8')

    meow_print(f"SVGを保存したニャ！: {output_path} 😺", "success")
    meow_print(f"  パターン: {pattern_def['name']}", "info")
    meow_print(f"  カラーマップ: {colors['name']}", "info")

    return True


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースするニャ"""
    parser = argparse.ArgumentParser(
        description="ヘッダー画像生成スクリプト 🐱✨",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # PNG画像（fal.ai）
  python generate-header.py --tag v1.0.0 --theme feature --output header.png

  # SVG画像（ベクター）
  python generate-header.py --tag v1.0.0 --format svg --output header.svg

  # パターンとカラーマップを指定
  python generate-header.py --tag v1.0.0 --format svg --pattern stripes --colormap ocean

Patterns:
  paws      - 肉球模様（猫っぽい）
  stripes   - 縞模様
  dots      - ドット
  geometric - 幾何学模様
  waves     - 波模様

Colormaps:
  cat    - 猫テーマ（オレンジ×ピンク）
  ocean  - 海（青×水色）
  sunset - 夕日（オレンジ×紫）
  forest - 森（緑×茶色）
  neon   - ネオン（ピンク×シアン）
        """
    )

    parser.add_argument(
        "--tag",
        type=str,
        default="v1.0.0",
        help="リリースタグ (例: v1.0.0, v2.1.3)"
    )

    parser.add_argument(
        "--theme",
        type=str,
        choices=["feature", "bugfix", "major", "patch", "first", "auto"],
        default="auto",
        help="テーマ (autoでタグから自動検出、PNGのみ有効)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="header.png",
        help="出力ファイルパス"
    )

    parser.add_argument(
        "--aspect-ratio",
        type=str,
        choices=["16:9", "4:3", "1:1", "21:9"],
        default="16:9",
        help="アスペクト比（PNGのみ有効）"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["png", "svg"],
        default="png",
        help="出力フォーマット（png: fal.ai、svg: ベクター）"
    )

    parser.add_argument(
        "--pattern",
        type=str,
        choices=["paws", "stripes", "dots", "geometric", "waves"],
        default="paws",
        help="パターン（SVGのみ有効）"
    )

    parser.add_argument(
        "--colormap",
        type=str,
        choices=["cat", "ocean", "sunset", "forest", "neon"],
        default="cat",
        help="カラーマップ（SVGのみ有効）"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=1200,
        help="画像幅（SVGのみ有効）"
    )

    parser.add_argument(
        "--height",
        type=int,
        default=315,
        help="画像高さ（SVGのみ有効）"
    )

    return parser.parse_args()


def main() -> int:
    """メイン関数ニャ"""
    meow_print("ヘッダー画像生成スクリプトを起動するニャ！ 🐱✨", "info")

    args = parse_args()

    if args.format == "svg":
        # SVGモード
        meow_print("SVGモードで生成するニャ！ 🎨", "info")

        # 出力ファイルの拡張子をチェック
        output_path = args.output
        if not output_path.endswith('.svg'):
            output_path = str(Path(output_path).with_suffix('.svg'))

        success = generate_svg(
            tag=args.tag,
            output_path=output_path,
            pattern=args.pattern,
            colormap=args.colormap,
            width=args.width,
            height=args.height
        )
    else:
        # PNGモード（fal.ai）
        # テーマの決定
        theme = args.theme
        if theme == "auto":
            theme = detect_theme_from_tag(args.tag)
            meow_print(f"タグ '{args.tag}' からテーマ '{theme}' を検出したニャ！ 😺", "info")

        # プロンプトの構築
        meow_print(f"プロンプトを構築中... (テーマ: {theme}) 🎨", "info")
        prompt = build_prompt(args.tag, theme)

        # 出力ディレクトリの作成
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 画像の生成
        api_key = get_fal_key()
        success = generate_image(
            prompt=str(prompt),
            output_path=str(output_path),
            aspect_ratio=args.aspect_ratio,
            api_key=api_key
        )

    if success:
        meow_print("ヘッダー画像の生成が完了したニャ！ 🎉😺", "success")
        return 0
    else:
        meow_print("ヘッダー画像の生成に失敗したニャ... 😿", "error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
