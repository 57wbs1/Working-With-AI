# Working With AI

An eleven-lesson self-paced course on using AI tools properly, built for 57 CSC Syn 1.

**Live:** https://57wbs1.github.io/Working-With-AI/

**Unclassified.** Personal account, personal time, no official material.

## Structure

- `index.html` — landing page: what the course is, the eleven lessons, $50 PayNow, access-code entry
- `course.html` — the course itself, one lesson per page
- `assets/video/` — nine clips (Higgsfield / Google Veo 3.1 Lite)
- `assets/img/` — poster frames and the PayNow QR

## Running locally

Videos need a server (relative paths won't load from `file://`):

```bash
python3 -m http.server 8793
```

## Presenting

- **Notes** button, or press `N` — reveals the "SAY THIS" speaking notes. Turn them off before sharing.
- **Light** button — light theme for phones in daylight.
- `←` `→` move between lessons, `C` opens contents, `Esc` closes overlays.
- Each lesson has its own accent colour, so the dots and contents list show progress at a glance.
- Progress and theme persist per browser.

## Structure

Three days, 28 sections: 12 lessons, 15 labs, a troubleshooting playbook and a capstone.
Roughly 20 hours, ending with a deployed URL.

| Day | Covers | Labs |
|---|---|---|
| 1 — Foundations | Agentic AI, the toolkit, costs | Delegate don't instruct · Choose your stack · Sanitisation drill |
| 2 — Working | Skills, MCP, research, decks, files | Build a skill · Connectors · First agentic task · Citation audit · Research end-to-end · Your format · Point it at a folder |
| 3 — Building | Failure modes, vibe coding | Circling drill · Spec · Build v1 · Break and harden · Ship it · **Capstone** |

Every lesson carries a four-question MCQ (40 total, options shuffled, skippable).
Every lab carries a persistent checklist (112 checks) feeding a per-day progress bar.
Ticks and quiz scores save to the browser only — nothing is transmitted.

## Access gate — read this

The gate is **honour-system only, not security.** This is a static site in a public repo, so:

- Anyone can open `course.html` directly if they clear or never set the flag — the check is client-side.
- The whole course is readable in this repo without paying.
- Access codes are stored as SHA-256 hashes, which stops casual source-reading but not anyone determined.

If the paywall needs to actually hold, the repo has to go private and the site needs a host with real
server-side auth. As it stands it will stop casual forwarding and nothing more.

Codes live as hashes in `index.html`. To change them, hash `wwai:<code>` with SHA-256 and replace them.

## PayNow QR

`assets/img/paynow-50.png` encodes an EMVCo/SGQR payload: SGD 50.00 to +6591817066, reference `AIBRIEF`,
fixed amount. The CRC is self-checked at build time.

**Test it with a real scan before sharing.** The payload is constructed to spec and the checksum
validates, but it has not been put through an actual bank app.

To regenerate, see `scripts/paynow.py`.

## Maintenance

Everything factual is stamped **7 Oct 2026** and dates fast:

- Prices moved four times in the quarter before this was written.
- Video links were verified via the YouTube oEmbed API.
- The Perplexity student discount was confirmed against Perplexity's own help centre.
- Model tiers in Lesson 10 will age fastest of all.

Re-check Lessons 04 and 10 before presenting this more than a few weeks out.
