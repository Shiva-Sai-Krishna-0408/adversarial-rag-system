def chunk_text(text, chunk_size, overlap, file_name):
    words = text.split()
    start = 0
    end = start + chunk_size
    chunks = []

    while start < len(words):
        chunk_words = words[start:end]
        start += chunk_size - overlap
        end  = start + chunk_size
        chunks.append(' '.join(chunk_words))

    return [(file_name,chunk) for chunk in chunks]      