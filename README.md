# 🧠 Binary & Files: A Guide for People Who Thought Computers Were Magic

> *Spoiler: they're not. It's just a lot of 1s and 0s having an existential crisis.*

---

## Table of Contents
- [What Even Is Binary](#what-even-is-binary)
- [Image to Binary](#image-to-binary)
- [Binary to Image](#binary-to-image)
- [What Does Each 0 and 1 Actually Mean](#what-does-each-0-and-1-actually-mean)
- [Can You Trick a PNG Into Thinking It's a JPEG](#can-you-trick-a-png-into-thinking-its-a-jpeg)
- [Magic Bytes: The ID Cards of the File World](#magic-bytes-the-id-cards-of-the-file-world)

---

## What Even Is Binary

Congratulations. You've discovered that computers, the devices running your entire civilization, are fundamentally just very fast at asking "is it a 1 or a 0?" over and over again, billions of times per second.

A **bit** is a single `0` or `1`. Eight of them together form a **byte**, which represents a number from `0` to `255`. That's it. That's the whole trick. Everything — your photos, your music, your embarrassing browser history — is just a very long sequence of these.

```
01001000 01100101 01111001  →  "Hey"
```

Yes. "Hey" is just three numbers dressed up in a trench coat.

---

## Image to Binary

Want to see what your selfie looks like to a computer? Here's the code. It will output an incomprehensible wall of 1s and 0s that means absolutely nothing to you but everything to your CPU.

```python
import os

def image_to_binary(image_path):
    if not os.path.exists(image_path):
        print("Error: File not found.")
        return

    with open(image_path, "rb") as img:
        data = img.read()

    print(f"Size: {len(data)} bytes\n")

    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        print(' '.join(format(byte, '08b') for byte in chunk))

path = input("Enter image path: ").strip()
image_to_binary(path)
```

**How it works:**
1. Opens the image in `rb` (read binary) mode — as in, "don't you dare interpret this as text"
2. Reads every byte of the file
3. Converts each byte to its 8-bit binary form with `format(byte, '08b')`
4. Prints 4 bytes per line so your terminal doesn't file a complaint

> ⚠️ A 1MB image = ~8 million digits. Your terminal will not enjoy this. Your computer will not enjoy this. Nobody will enjoy this. You've been warned.

---

## Binary to Image

Okay so you've stared at the void. Now you want the void to stare back as a JPEG. Here's how you reverse the whole thing:

```python
binary_input = input("Enter binary code: ").strip()

bytes_list = binary_input.split()
data = bytes([int(b, 2) for b in bytes_list])

with open("output_image.png", "wb") as img:
    img.write(data)

print("Image saved as output_image.png")
```

**How it works:**
1. Splits the binary string by spaces into 8-bit chunks
2. Converts each chunk back to an integer (`int(b, 2)` — the `2` means base 2, because we're not animals)
3. Packs them into a `bytes` object
4. Writes it to a file in `wb` (write binary) mode, reconstructing the original image

> ⚠️ This only works if you paste the **complete** binary of an image. Pasting half of it will produce a corrupt file, which your image viewer will open as a deeply personal insult.

---

## What Does Each 0 and 1 Actually Mean

Great question. The answer is: *it depends where in the file you are*, which is a very computer science answer.

**A single byte:**
```
01001000  =  72
```

**Where that byte lives determines what it means:**

| Location | What the byte means |
|----------|-------------------|
| Start of file | "I am a PNG" or "I am a JPEG" (file identity crisis) |
| Middle (pixel data) | A color intensity value from 0 (none) to 255 (full) |
| End | Metadata, checksums, or the computer equivalent of a signature |

**For color images, pixels are stored in groups of 3 bytes — RGB:**
```
11111111 00000000 00000000  →  pure red   (255, 0, 0)
00000000 11111111 00000000  →  pure green (0, 255, 0)
00000000 00000000 11111111  →  pure blue  (0, 0, 255)
```

So your entire profile photo is just millions of these triplets, each one telling the screen exactly how much red, green, and blue to shine at your eyeballs. Romantic, isn't it.

---

## Can You Trick a PNG Into Thinking It's a JPEG

No. And yes. But mostly no.

If you change the first few bytes of a PNG to say "I am a JPEG", your image viewer will open it, see that the *rest* of the file is still PNG-encoded garbage, and politely refuse to display anything. Or crash. Probably crash.

**Why?** Because PNG and JPEG aren't just different labels — they're entirely different ways of storing pixel data:

| | PNG | JPEG |
|---|---|---|
| Compression | Lossless (every pixel, exactly) | Lossy (good enough, your eyes won't notice) |
| Pixel storage | Raw filtered bytes | Frequency blocks from a math algorithm |
| Structure | Chunks with CRC checksums | Segments with binary markers |

Changing the header is like putting a "This is a Pizza" sticker on a burger. The sticker lies. The burger knows what it is.

**The ONE exception:** if someone took a JPEG file and just renamed it `.png` without re-encoding it, then yes — fixing the header bytes would actually restore it. Because the underlying data was always JPEG. The file just had an identity crisis.

**The real way to convert formats:**
```python
from PIL import Image
img = Image.open("photo.png")
img.save("photo.jpg")  # full re-encoding, the honest way
```

---

## Magic Bytes: The ID Cards of the File World

Every file format starts with a special sequence of bytes called **Magic Bytes** (yes, that's the real name — computer scientists occasionally have fun). The computer reads these first and goes "ah yes, I know how to handle this."

### The Lineup

**PNG** — `89 50 4E 47 0D 0A 1A 0A`
```
‰PNG....
```
The `89` at the start is a non-ASCII byte specifically chosen to prevent text editors from accidentally opening it. The rest literally spells `PNG`. Subtle it is not.

---

**JPEG** — `FF D8 FF E0`

No ASCII. Purely cryptic binary markers. JPEG doesn't feel the need to introduce itself to you.

---

**MP3** — `49 44 33`
```
ID3
```
Spells `ID3` — the metadata tag format that stores the artist, album, and song title before the actual audio even starts.

---

**MP4** — `00 00 00 18 66 74 79 70`
```
....ftyp
```
The `ftyp` part means "file type box." The bytes before it are the size of that box. Very bureaucratic.

---

**PDF** — `25 50 44 46 2D`
```
%PDF-
```
Literally starts with `%PDF-` every single time, no exceptions. The most honest file format. Points for transparency.

---

**ZIP** — `50 4B 03 04`
```
PK..
```
`PK` stands for **Phil Katz**, the guy who invented ZIP in the 1980s. He put his initials in every ZIP file that has ever existed. Also: `.docx`, `.xlsx`, and `.jar` files are secretly ZIP files with a costume on. They have these same magic bytes.

---

**EXE (Windows executables)** — `4D 5A`
```
MZ
```
Stands for **Mark Zbikowski**, a Microsoft engineer from the early 80s. Every Windows program that has ever run starts with his initials. He is everywhere. He cannot be stopped.

---

### The Full Cheat Sheet

| Format | Magic Bytes (Hex) | What You See |
|--------|------------------|--------------|
| PNG | `89 50 4E 47` | `‰PNG` |
| JPEG | `FF D8 FF` | nothing readable |
| MP3 | `49 44 33` | `ID3` |
| MP4 | `66 74 79 70` | `ftyp` |
| PDF | `25 50 44 46` | `%PDF` |
| ZIP | `50 4B 03 04` | `PK` |
| EXE | `4D 5A` | `MZ` |
| GIF | `47 49 46 38` | `GIF8` |

---

## Final Thoughts

Everything on your computer is binary. Every photo, song, document, and meme is just a very long number that a very fast machine is interpreting according to rules defined by people who, in many cases, put their initials at the start of the file.

The next time your image viewer says "unsupported file format", it read the first 4 bytes, didn't recognize them, and gave up. Which is honestly a relatable reaction.

---

