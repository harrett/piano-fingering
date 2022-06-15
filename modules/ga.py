import numpy as np

def fitness(notes: list, genes: np.ndarray) -> float:
    """
    適応度を算出する. ただしここでは数値が小さい方が優秀.

    Args:
        notes (list): 全ての音符.
        genes (np.ndarray): 遺伝子配列. 要素は1~5.

    Returns:
        float: 適応度
    """
    n_notes = len(notes)
    val = 0
    for i in range(1, n_notes):
        b_note, note = notes[i - 1: i + 1]
        b_fing, fing = genes[i - 1: i + 1]

        if note.note_num > b_note.note_num: # 上昇時
            if fing < b_fing: # 指は下降してたとき
                val += 10 - 6*(note.note_num == 1) # 親指は許容

        else : # 下降時
            if fing > b_fing: # 指は上昇してたとき
                val += 10 - 6*(b_note.note_num == 1) # 親指は許容
        
        if b_fing == fing: # 同じ指が続いた時
            val += 8 - 6*(b_note == note) # 同じ音の場合は許容

    return val


def crossover(parents: np.ndarray, n: int, mutation: float) -> np.ndarray:
    """
    交叉

    Args:
        parents (np.ndarray): 選択された遺伝子. 親.
        n (int): 交差させる回数. 子供の数.
        mutation (float): 突然変異の確率.

    Returns:
        np.ndarray: 新たに生成した遺伝子
    """
    genes = []
    n_notes = parents.shape[-1]
    for _ in range(n):
        idx = np.random.choice(len(parents), 2, replace=False)
        par1, par2 = parents[idx]
        gene = par1.copy()
        
        idx = np.random.randint(0, 2, size=len(gene), dtype=bool)
        gene[idx] = par2[idx]

        idx = np.random.choice(
            2, n_notes, p=[1 - mutation, mutation]).astype(bool)
        gene[idx] = np.random.randint(1, 6, size=n_notes)[idx]

        genes.append(gene)
    return np.array(genes)


def make_genes(n_genes, n_notes):
    return np.random.randint(1, 6, size=(n_genes, n_notes))


def notes2fingering(
    notes_lr: list,
    n_genes: int,
    n_children: int,
    mutation: float,
    n_generation: int,
    n_choices: int,
) -> np.ndarray:
    """
    遺伝的アルゴリズムで最適な運指を生成する.

    Args:
        notes_lr (list): 左右別の全ての音符.
        n_genes (int): 一世代に生成する個体の数
        n_children (int): 親から生成する子供の数
        mutation (float): 突然変異の確率
        n_generation (int): 何世代まで回すか
        n_choices (int): 何個体選択するか

    Returns:
        np.ndarray: 最も優秀だった個体
    """
    genes_lr = []
    for notes in notes_lr:
        n_notes = len(notes)
        genes = make_genes(n_genes, n_notes)
        for _ in range(n_generation):
            fitnesses = []
            fitnesses = np.array([fitness(notes, gene) for gene in genes])
            parents = genes[fitnesses.argsort()[:n_choices]]
            genes = crossover(parents, n_children, mutation)
            genes = np.concatenate(
                [genes, make_genes(n_genes-n_children, n_notes)])
        genes_lr.append(parents[0])
    return genes_lr