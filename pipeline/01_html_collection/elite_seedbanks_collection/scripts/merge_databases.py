import sqlite3

conn1 = sqlite3.connect('../data/elite_product_urls.db')
conn2 = sqlite3.connect('../data/elite_bulletproof_urls.db')
conn3 = sqlite3.connect('../data/elite_merged_urls.db')

c3 = conn3.cursor()
c3.execute('''CREATE TABLE IF NOT EXISTS merged_urls (
    url_hash TEXT PRIMARY KEY,
    original_url TEXT NOT NULL,
    seedbank TEXT NOT NULL,
    discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    attempts INTEGER DEFAULT 0,
    html_size INTEGER,
    validation_score REAL,
    s3_path TEXT,
    error_message TEXT,
    scrape_method TEXT,
    last_attempt TIMESTAMP
)''')

c1 = conn1.cursor()
c1.execute('SELECT url_hash, original_url, seedbank FROM product_urls')
for row in c1.fetchall():
    c3.execute('INSERT OR IGNORE INTO merged_urls (url_hash, original_url, seedbank) VALUES (?, ?, ?)', row)

c2 = conn2.cursor()
c2.execute('SELECT url_hash, original_url, seedbank FROM bulletproof_urls')
for row in c2.fetchall():
    c3.execute('INSERT OR IGNORE INTO merged_urls (url_hash, original_url, seedbank) VALUES (?, ?, ?)', row)

conn3.commit()

c3.execute('SELECT COUNT(*) FROM merged_urls')
total = c3.fetchone()[0]

c3.execute('SELECT seedbank, COUNT(*) FROM merged_urls GROUP BY seedbank ORDER BY COUNT(*) DESC')
print('\n=== MERGED DATABASE ===\n')
for row in c3.fetchall():
    print(f'{row[0]}: {row[1]:,} URLs')
print(f'\nTOTAL: {total:,} URLs')

conn1.close()
conn2.close()
conn3.close()
