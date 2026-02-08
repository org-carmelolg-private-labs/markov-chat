# Text Corpus Sources

This directory contains text files used as the corpus for the Markov chain text generator.

## Current Text Files

### English Texts

1. **aitw.txt** - Alice's Adventures in Wonderland
   - Author: Lewis Carroll
   - Source: Project Gutenberg (estimated)
   - Language: English
   - Genre: Fantasy, Children's Literature
   - Size: ~3,600 lines

### Italian Texts

2. **commedia.txt** - La Divina Commedia (The Divine Comedy)
   - Author: Dante Alighieri
   - Language: Italian
   - Genre: Epic Poetry
   - Size: ~14,750 lines
   - Contains: Inferno, Purgatorio, Paradiso

3. **brunori.txt** - Italian Song Lyrics
   - Content: Italian song lyrics
   - Language: Italian
   - Genre: Contemporary Music
   - Size: ~1,900 lines

## Adding New Texts

### From Project Gutenberg

You can download texts from Project Gutenberg using the included script:

```bash
python download_gutenberg.py <book_id> static/<filename>.txt
```

#### Popular English Texts

- **11** - Alice's Adventures in Wonderland (Lewis Carroll)
- **1342** - Pride and Prejudice (Jane Austen)
- **84** - Frankenstein (Mary Shelley)
- **1661** - The Adventures of Sherlock Holmes (Arthur Conan Doyle)
- **174** - The Picture of Dorian Gray (Oscar Wilde)
- **2701** - Moby Dick (Herman Melville)
- **76** - Adventures of Huckleberry Finn (Mark Twain)
- **98** - A Tale of Two Cities (Charles Dickens)

#### Popular Italian Texts

- **1000** - La Divina Commedia (Dante Alighieri)
- **7001** - I Promessi Sposi (Alessandro Manzoni)
- **6053** - Pinocchio (Carlo Collodi)
- **12561** - Decameron (Giovanni Boccaccio)

### After Adding Texts

1. Update environment variables in:
   - `.env` - for local development
   - `.env.example` - as a template for others
   - `render.yaml` - for Render.com deployment

2. Update the `INPUT_FILENAME` variable with comma-separated filenames:
   ```
   INPUT_FILENAME=aitw.txt,commedia.txt,brunori.txt,your-new-file.txt
   ```

3. Test the application:
   ```bash
   python runner.py
   ```

## File Requirements

- **Encoding**: UTF-8
- **Format**: Plain text (.txt)
- **Location**: Must be in the `static/` directory
- **Content**: Any text content (books, articles, lyrics, etc.)
- **License**: Prefer public domain texts (Project Gutenberg is ideal)

## Attribution

When using Project Gutenberg texts:
- Project Gutenberg texts are in the public domain in the United States
- Check your local copyright laws for restrictions
- Consider keeping the Project Gutenberg attribution in the file
- See: https://www.gutenberg.org/policy/license.html

## Tips for Better Results

- **Variety**: Mix different writing styles for more interesting output
- **Language**: Keep texts in the same language together, or separate multilingual configs
- **Size**: Larger texts provide more training data but take longer to load
- **Quality**: Clean, well-formatted texts produce better results
- **Temperature**: Adjust TEMPERATURE setting to control creativity:
  - `0.0 - 0.4`: More deterministic, coherent text (3-gram model)
  - `0.5 - 1.0`: More creative, random text (2-gram model)
