slug = 'serious-seeds-serious-6'
prefixes = ['serious-seeds-', 'serious-']
prefixes_sorted = sorted(prefixes, key=len, reverse=True)

print('Sorted prefixes:', prefixes_sorted)
for p in prefixes_sorted:
    print(f'  Testing "{p}": {slug.startswith(p)}')
    if slug.startswith(p):
        result = slug[len(p):]
        print(f'  Match! Removing prefix leaves: "{result}"')
        break
