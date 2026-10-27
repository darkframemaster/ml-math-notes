"""Count words."""

def count_words(s, n):
    """Return the n most frequently occuring words in s."""
    top_n = {}
    s = s.split(' ')
    # TODO: Count the number of occurences of each word in s
    for letter in s:
        if letter in top_n:
            top_n[letter] += 1
        else:
            top_n[letter] = 1
    # TODO: Sort the occurences in descending order (alphabetically in case of ties)
    top_n = [(key,top_n[key]) for key in top_n]
    top_n.sort()
    top_n = sorted(top_n, key=lambda d:d[1], reverse=True)[:n]
    
    # TODO: Return the top n words as a list of tuples (<word>, <count>)
    return top_n


def test_run():
    """Test count_words() with some inputs."""
    print count_words("cat bat mat cat bat cat", 3)
    print count_words("betty bought a bit of butter but the butter was bitter", 3)


if __name__ == '__main__':
    test_run()

