def create_cooccurrence_matrix(cites):
    """Create co occurrence matrix from given list of sentences.

    Returns:
    - vocabs: dictionary of word counts
    - co_occ_matrix_sparse: sparse co occurrence matrix

    Example:
    ===========
    sentences = ['I love nlp',    'I love to learn',
                 'nlp is future', 'nlp is cool']

    vocabs,co_occ = create_cooccurrence_matrix(sentences)

    df_co_occ  = pd.DataFrame(co_occ.todense(),
                              index=vocabs.keys(),
                              columns = vocabs.keys())

    df_co_occ = df_co_occ.sort_index()[sorted(vocabs.keys())]

    df_co_occ.style.applymap(lambda x: 'color: red' if x>0 else '')

    """
    import scipy.sparse as sparse

    arts = {}
    data = []
    row = []
    col = []

    for cite in cites:
        for pos, art in enumerate(cite):
            i = arts.setdefault(art, len(arts))
            start = 0
            end = len(cite)
            for pos2 in range(start, end):
                if pos2 == pos:
                    continue
                j = arts.setdefault(cite[pos2], len(arts))
                data.append(1.)
                row.append(i)
                col.append(j)

    cooccurrence_matrix_sparse = sparse.coo_matrix((data, (row, col)))
    return arts, cooccurrence_matrix_sparse