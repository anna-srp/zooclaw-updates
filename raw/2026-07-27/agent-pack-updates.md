# Agent Pack updates — 2026-07-27

- total_packs: 12
- updated_count: 1


## slide-master (versions=9, is_new=False)

- added: []
- removed: []
- modified: ['./agent-pack.yaml', './scripts/deck_tokens.py']


### slide-master diff (latest -> previous)

```
(node:2906) [UNDICI-EHPA] Warning: EnvHttpProxyAgent is experimental, expect them to change at any time.
(Use `node --trace-warnings ...` to show where the warning was created)
===== [modified] ./agent-pack.yaml =====
3c3
< version: 0.4.1
---
> version: 0.4.2

===== [modified] ./scripts/deck_tokens.py =====
8c8,12
<     load_style(style_id: str, brand: dict | None = None) -> dict
---
>     load_style(
>         style_id: str,
>         brand: dict | None = None,
>         clamp_brand: bool = True,
>     ) -> dict
21a26
> import colorsys
62a68,99
> 
> class BrandContrastError(ValueError):
>     """A brand accent cannot satisfy the W2 palette-safety contract."""
> 
>     def __init__(
>         self,
>         *,
>         role: str,
>         failing_check: str,
>         ratio: float,
>         archetype: str,
>         original_hex: str,
>         clamped_hex: str | None,
>         final_attempted_hex: str | None,
>         hint: str,
>     ) -> None:
>         self.payload = {
>             "role": role,
>             "failing_check": failing_check,
>             "ratio": ratio,
>             "archetype": archetype,
>             "original_hex": original_hex,
>             "clamped_hex": clamped_hex,
>             "final_attempted_hex": final_attempted_hex,
>             "hint": hint,
>         }
>         super().__init__(
>             f"brand color {role!r} {original_hex} cannot satisfy "
>             f"{failing_check!r} for style {archetype!r} "
>             f"(ratio={ratio:.3f}): {hint}"
>         )
> 
446c483,487
< def load_style(style_id: str, brand: dict | None = None) -> dict:
---
> def load_style(
>     style_id: str,
>     brand: dict | None = None,
>     clamp_brand: bool = True,
> ) -> dict:
455c496,499
<     value (Sweep D vocab validation).
---
>     value (Sweep D vocab validation). When ``clamp_brand`` is true, an
>     explicitly provided brand accent is finalized through the W2
>     hue-preserving envelope and contrast guard; explicitly provided
>     ``accent2`` / ``chart_highlight`` values remain raw.
467a512
>         provided_color_roles = set((brand.get("colors") or {}).keys())
468a514,519
>         if clamp_brand and "accent" in provided_color_roles:
>             _finalize_brand_accents(
>                 tokens,
>                 style_id,
>                 provided_color_roles=provided_color_roles,
>             )
661a713,888
> def _hsl_to_hex(h: float, s: float, l: float) -> str:
>     """Re-emit HSL as deterministic lower-case ``#rrggbb``."""
>     r, g, b = colorsys.hls_to_rgb((h % 360.0) / 360.0, l, s)
>     return "#%02x%02x%02x" % (
>         round(r * 255),
>         round(g * 255),
>         round(b * 255),
>     )
> 
> 
> def _hue_sep(h1: float, h2: float) -> float:
>     """Smallest circular hue separation in degrees, in the range 0..180."""
>     delta = abs(h1 - h2) % 360.0
>     return min(delta, 360.0 - delta)
> 
> 
> def _clamp_once(
>     hexval: str,
>     l_lo: float,
>     l_hi: float,
>     s_lo: float,
>     s_hi: float,
> ) -> str:
>     """Clamp HSL lightness/saturation once while preserving hue."""
>     h, s, l = _hsl(hexval)
>     l2 = min(max(l, l_lo), l_hi)
>     s2 = min(max(s, s_lo), s_hi)
>     if l2 == l and s2 == s:
>         return hexval
>     return _hsl_to_hex(h, s2, l2)
> 
> 
> QUANT_EPS = 1.0 / 255.0
> 
> 
> def _clamp_into(
>     hexval: str,
>     l_lo: float,
>     l_hi: float,
>     s_lo: float,
>     s_hi: float,
> ) -> str:
>     """Clamp to a stable, materially envelope-safe 8-bit hex value."""
>     cur = hexval
>     for _ in range(4):
>         nxt = _clamp_once(cur, l_lo, l_hi, s_lo, s_hi)
>         if nxt == cur:
>             break
>         cur = nxt
> 
>     hue = _hsl(cur)[0]
>     for axis, lo, hi, value_index in (
>         ("lightness", l_lo, l_hi, 2),
>         ("saturation", s_lo, s_hi, 1),
>     ):
>         value = _hsl(cur)[value_index]
>         if value < lo - QUANT_EPS:
>             boundary, direction = lo, 1.0
>         elif value > hi + QUANT_EPS:
>             boundary, direction = hi, -1.0
>         else:
>             continue
> 
>         for step in range(1, 4):
>             target = min(
>                 max(boundary + direction * step * QUANT_EPS, lo),
>                 hi,
>             )
>             _, parsed_s, par

```
