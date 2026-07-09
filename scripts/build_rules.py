from __future__ import annotations

from pathlib import Path


REPO = "https://github.com/DDcat2025/adobe-shadowrocket-rules"


def read_entries(path: Path) -> list[tuple[str, str]]:
    entries: set[tuple[str, str]] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" in line:
            kind, value = line.split(":", 1)
            kind = kind.strip().lower()
            value = value.strip().lower()
        else:
            kind = "suffix"
            value = line.lower()
        if kind not in {"suffix", "full", "keyword"}:
            raise ValueError(f"Unsupported entry type: {kind}")
        entries.add((kind, value))
    return sorted(entries, key=lambda item: (item[0], item[1]))


def domain_rule(entry: tuple[str, str]) -> str:
    kind, value = entry
    if kind == "full":
        return f"DOMAIN,{value}"
    if kind == "keyword":
        return f"DOMAIN-KEYWORD,{value}"
    return f"DOMAIN-SUFFIX,{value}"


def write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def header(name: str, total: int) -> list[str]:
    return [
        f"# NAME: {name}",
        "# AUTHOR: DDcat2025",
        f"# REPO: {REPO}",
        "# SOURCE: Adobe official network endpoint docs, Adobe Captivate endpoint docs, blackmatrix7 Adobe rule reference",
        f"# TOTAL: {total}",
    ]


def build(
    name: str,
    entries: list[tuple[str, str]],
    shadow_dir: str,
    mihomo_dir: str,
) -> list[str]:
    rules = [domain_rule(entry) for entry in entries]
    lines = header(name, len(rules)) + rules
    write(Path(f"rule/Shadowrocket/{shadow_dir}/{name}.list"), lines)
    write(
        Path(f"rule/Mihomo/{mihomo_dir}/{name}.yaml"),
        header(name, len(rules)) + ["payload:"] + [f"  - {rule}" for rule in rules],
    )
    return rules


def main() -> None:
    adobe_ai = read_entries(Path("data/adobe-ai-domains.txt"))
    behance = read_entries(Path("data/behance-domains.txt"))

    adobe_ai_rules = build("AdobeAI", adobe_ai, "AdobeAI", "AdobeAI")
    behance_rules = build("Behance", behance, "Behance", "Behance")

    merged = sorted(set(adobe_ai_rules + behance_rules))
    write(
        Path("rule/Shadowrocket/AdobeProxy/AdobeProxy.list"),
        header("AdobeProxy", len(merged)) + merged,
    )
    write(
        Path("rule/Mihomo/AdobeProxy/AdobeProxy.yaml"),
        header("AdobeProxy", len(merged)) + ["payload:"] + [f"  - {rule}" for rule in merged],
    )


if __name__ == "__main__":
    main()
