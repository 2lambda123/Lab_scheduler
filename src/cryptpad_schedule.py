import pandas as pd
import numpy as np


STATUS_VALUES = {"no": 0, "maybe": 1, "yes": 2}


def load(path_file: str):
    """Load dataframe from a CSV file exported by Cryptpad poll"""
    df = pd.read_csv(path_file, index_col=0)
    print(f"Removing TOTAL and cleaning up such that {STATUS_VALUES}")
    df = df.drop("TOTAL", axis=1)
    df = 3 - df
    return df


def get_tas_by_status(row, status: str):
    status = STATUS_VALUES[status]
    return row.where(lambda avail: avail==status).dropna().index


def normalized_prob_from_count(counts_names):
    # Penalize missing people
    if counts_names.hasnans:
        counts_max = counts_names.max()
        counts_names[counts_names.isna()] = counts_max * 1.2

    nb_names = len(counts_names)
    if nb_names == 1:
        return np.array([1.])
    else:
        # Less probability if already appeared assigned many slots
        prob = 1. - counts_names / counts_names.sum()
        prob /= (nb_names - 1)
        return prob


def probability_to_choose(yes, maybe, counts, prob_yes):
    prob_maybe = 1. - prob_yes
    
    prob_yes_array = normalized_prob_from_count(counts[yes])
    prob_maybe_array = normalized_prob_from_count(counts[maybe])

    if prob_yes_array.sum() > 0 and prob_maybe_array.sum() > 0:
        prob_yes_array *= prob_yes
        prob_maybe_array *= prob_maybe

    prob_list = np.hstack((
        prob_yes_array,
        prob_maybe_array,        
        # np.ones_like(yes, dtype=float) * prob_yes / len(yes),
        # np.ones_like(maybe, dtype=float) * prob_maybe / len(maybe),
    ))


    return prob_list
 

def schedule(df, sched, prob_yes=0.8):
    # Initialize
    time_prev = df.iloc[-1].name
    maxiter = 50

    for _, row in df.iterrows():
        yes = get_tas_by_status(row, "yes")
        maybe = get_tas_by_status(row, "maybe")

        ta_list = np.hstack([yes, maybe])
        prob_list = probability_to_choose(
            yes, maybe, sched.value_counts(), prob_yes)
        
        # Sanity check
        if len(ta_list) == 0:
            raise ValueError(f"No sign ups for {row}?")

        ta_prev = sched[time_prev]
        ta = ta_prev

        i = 0
        # Avoid simultaneous teaching slots and too many iterations
        while (ta == ta_prev) and (i <= maxiter):
            ta = np.random.choice(ta_list, p=prob_list)
            i += 1

        sched[row.name] = ta
        time_prev = row.name

    return sched


def plot(sched):
    return sched.value_counts().plot("bar")