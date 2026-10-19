import re
from dataclasses import dataclass


@dataclass
class Matrix:
    ai: list[re.Pattern]
    risk: list[re.Pattern]

    @classmethod
    def from_config(cls, cfg: dict) -> "Matrix":
        def comp(terms):
            return [re.compile(rf"(?<!\w){t}(?!\w)", re.I) if re.search(r"[\\\[\]]", t)
                    else re.compile(rf"(?<!\w){re.escape(t)}(?!\w)", re.I) for t in terms]
        return cls(comp(cfg["ai_tooling"]), comp(cfg["risk"]))

    def score(self, title: str, summary: str) -> tuple[int, str, bool]:
        """Return (score, matched terms, relevant). Relevant = at least one AI term AND one risk term."""
        total, matched = 0, []
        hit_ai = hit_risk = False
        for group, flag in ((self.ai, "ai"), (self.risk, "risk")):
            for rx in group:
                in_title = len(rx.findall(title or ""))
                in_body = len(rx.findall(summary or ""))
                if in_title or in_body:
                    total += 3 * min(in_title, 2) + min(in_body, 3)
                    matched.append(rx.pattern.replace(r"(?<!\w)", "").replace(r"(?!\w)", "").replace("\\", ""))
                    if flag == "ai":
                        hit_ai = True
                    else:
                        hit_risk = True
        return total, ", ".join(matched), hit_ai and hit_risk
