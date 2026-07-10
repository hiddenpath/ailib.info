#!/usr/bin/env python3
"""Add ja/es support to EcosystemOverview.astro via L(en, zh, ja, es) helper."""

from __future__ import annotations

import re
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "components" / "diagrams" / "EcosystemOverview.astro"

# English -> (ja, es). zh already in file.
JA_ES = {
    "AI-Lib Ecosystem Architecture": ("AI-Lib エコシステムアーキテクチャ", "Arquitectura del ecosistema AI-Lib"),
    "APPLICATION": ("アプリケーション", "APLICACIÓN"),
    "RUNTIME": ("ランタイム", "RUNTIME"),
    "PROTOCOL": ("プロトコル", "PROTOCOLO"),
    "Web Apps / API Services": ("Web アプリ / API サービス", "Apps web / servicios API"),
    "Your application code": ("あなたのアプリケーションコード", "Tu código de aplicación"),
    "AI Agents": ("AI エージェント", "Agentes de IA"),
    "Multi-turn / Tool Calling": ("マルチターン / ツール呼び出し", "Multi-turno / tool calling"),
    "CLI Tools": ("CLI ツール", "Herramientas CLI"),
    "Batch / Data Pipelines": ("バッチ / データパイプライン", "Lotes / pipelines de datos"),
    "Testing & Dev": ("テストと開発", "Pruebas y desarrollo"),
    "Mock Services": ("モックサービス", "Servicios mock"),
    "Load Manifests": ("マニフェスト読み込み", "Cargar manifiestos"),
    "Core Specification": ("コア仕様", "Especificación central"),
    "37 Provider Manifests": ("37 プロバイダーマニフェスト", "37 manifiestos de proveedores"),
    "Model Registry": ("モデルレジストリ", "Registro de modelos"),
    "Mock Server": ("モックサーバー", "Servidor mock"),
    "Local Testing": ("ローカルテスト", "Pruebas locales"),
    "Record/Replay": ("レコード / リプレイ", "Grabar/reproducir"),
    "Snapshot Tests": ("スナップショットテスト", "Pruebas snapshot"),
    "Protocol Compliance Check": ("プロトコル準拠チェック", "Comprobación de cumplimiento"),
    "Dev Testing · CI/CD · No real API needed": (
        "開発テスト · CI/CD · 実 API 不要",
        "Pruebas · CI/CD · sin API real",
    ),
    "mock": ("mock", "mock"),
}

# Multi-line / special zh variants that appear in file
SPECIAL = [
    (
        r"isZh\s*\?\s*'模型实例与能力声明'\s*:\s*'Model instances & capability declarations'",
        "L('Model instances & capability declarations', '模型实例与能力声明', 'モデルインスタンスと能力宣言', 'Instancias de modelo y declaraciones de capacidad')",
    ),
]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    text = text.replace(
        "const isZh = locale === 'zh' || locale === 'zh-cn';",
        """const L = (en: string, zh: string, ja: string, es: string) => {
  if (locale === 'zh' || locale === 'zh-cn') return zh;
  if (locale === 'ja') return ja;
  if (locale === 'es') return es;
  return en;
};""",
    )

    for pattern, repl in SPECIAL:
        text = re.sub(pattern, repl, text)

    def repl_ternary(m: re.Match[str]) -> str:
        zh = m.group(1)
        en = m.group(2)
        ja, es = JA_ES.get(en, (en, en))
        # escape for JS single-quoted strings
        def q(s: str) -> str:
            return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"

        return f"L({q(en)}, {q(zh)}, {q(ja)}, {q(es)})"

    text = re.sub(
        r"isZh\s*\?\s*'([^']*)'\s*:\s*'([^']*)'",
        repl_ternary,
        text,
    )
    # Also handle template with isZh ? `...` : `...` if any
    text = re.sub(
        r"isZh\s*\?\s*`([^`]*)`\s*:\s*`([^`]*)`",
        lambda m: repl_ternary(type("M", (), {"group": lambda i: m.group(i)})()),  # type: ignore
        text,
    )

    PATH.write_text(text, encoding="utf-8", newline="\n")
    remaining = len(re.findall(r"\bisZh\b", text))
    print(f"remaining isZh: {remaining}")
    print("done")


if __name__ == "__main__":
    main()
