---
name: claude-animation
description: Make a short hand-painted cartoon starring Clawd (the Claude mascot) or any character you design, written in p5.js and p5.brush and rendered locally to MP4. Brush strokes, boiling ink lines, flat 2D, no text. Use when the user asks for a Clawd animation, a hand-painted or watercolour cartoon, a character animation, a little animated story or music video with a mascot, or mentions Claude Animation Base.
---

# Claude Animation

A starter kit for hand-painted character animation: Clawd with 31 emotions, five drawn key views, hats, emotes and dances, plus a painting engine, a shot timeline with brush-wipe transitions and a headless renderer that makes contact sheets, frame strips, crops and the final MP4.

`KIT` below means the `kit/` folder next to this file (this skill's base directory + `/kit`).

## Set up the project

1. Pick a short project name (lowercase, hyphens) and copy the kit into the folder the user is working in: `cp -R "<KIT>" "<name>"`. Work only in that copy; never edit the kit itself.
2. In the project folder run `npm install` (p5, p5.brush, puppeteer-core). It needs Node.js, Google Chrome or Chromium, and ffmpeg. If one is missing, tell the user in your first message instead of installing system software yourself.
3. Read `ANIMATION_GUIDE.md` in the project **in full** before drawing anything, and look at `docs/emotions.jpg` and `docs/views.jpg`. The guide holds the rules (handmade, alive, one piece, no text, timing for the viewer), the workflow (storyboard first, build shot by shot, check contact sheets) and the full API.

## Make the video

Follow the guide. In short:

- Write the storyboard before code, and show it to the user when they asked for input.
- Put the film in `src/scenes/` (one file per scene, each added as a `<script>` in `studio.html`) and set length and tempo in `src/config.js`. `src/scenes/demo.js` is a worked example.
- Check your own work with the renderer, from the project folder:

  ```bash
  node render.mjs --sheet=0.5,1,1.5,2 --out=out/check/a.jpg     # contact sheet of chosen times
  node render.mjs --strip=2.0:2.5 --out=out/check/strip.jpg     # every frame in a stretch
  node render.mjs --clip --out=out/video.mp4                    # final MP4
  ```

  Open each check image and fix what you see before moving on.

## Machines without a GPU

p5.brush watercolour fills are slow without a GPU (seconds per frame). On Linux add `--soft-gl` when there is no GPU at all, or `--gpu-angle=gl-egl` (or `vulkan`) on a headless NVIDIA node; `node gpu_probe.mjs <chrome path>` shows which renderer each flag set gets. On integrated graphics, consider replacing the watercolour fills with something cheaper. If Chrome is not in a standard place, pass `--chrome=<path>` or set `CHROME_PATH`.

## Deliver

`out/video.mp4` in the project folder. Tell the user where it is and that `studio.html` (opened in Chrome) scrubs through the film.

Source: [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase), MIT (see `LICENSE`).
