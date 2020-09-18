import math

# Buka file csv dan baca semua baris.
# Return array baris dari csv.
def readFile(filename):
    fo = open(filename, "r")
    lines = fo.readlines()

    if (lines):
        return lines
    else:
        return False

# Cari lightness di csv, kembalikan jumlah salmon dan jumlah seabass.
def search_lightness(lightness):
    lines = readFile("data.csv")
    result = {
        'salmon': 0,
        'seabass': 0
    }    
    if (lines):
        subset = lines[1:]
        subset_length = len(subset)
        i = 0
        found = False
        while(i<subset_length and not found):
            line = subset[i].rstrip()
            arrs = line.split(',')
            bounds = arrs[0].split('-')
            lower_bound = float(bounds[0])
            upper_bound = float(bounds[1])
            count_salmon = int(arrs[1])
            count_seabass = int(arrs[2])

            if (lightness >= lower_bound and lightness <= upper_bound):
                found = True
                result['salmon'] = count_salmon
                result['seabass'] = count_seabass
            else:
                i += 1

    return result

# Count Kelas
def count_fish():
    lines = readFile("data.csv")
    if (lines):
        lines = lines[1:]
        countSalmon = 0
        countSeabass = 0
        for line in lines:
            arr_line = line.split(',')
            countSalmon += int(arr_line[1])
            countSeabass += int(arr_line[2])

        return {
            'salmon': countSalmon,
            'seabass': countSeabass,
            'total': countSalmon + countSeabass
        }

# P(X = Salmon)
def P_Salmon():
    fish = count_fish()
    return fish['salmon']/fish['total']

# P(X = Seabass)
def P_Seabass():
    fish = count_fish()
    return fish['seabass']/fish['total']

# P(lightness = x | Salmon)
def P_lightness_given_salmon(lightness):
    n_salmon_given_lightness = search_lightness(lightness)['salmon']
    n_salmon_overall = count_fish()['salmon']
    return (n_salmon_given_lightness / n_salmon_overall)

# P(lightness = x | Seabass)
def P_lightness_given_seabass(lightness):
    n_seabass_given_lightness = search_lightness(lightness)['seabass']
    n_seabass_overall = count_fish()['seabass']
    return (n_seabass_given_lightness / n_seabass_overall)

# P(Seabass | lightness = x) = P(lightness = x | Seabass) * P(Seabass)
def P_Seabass_given(lightness):
    p_lightness_given_seabass = P_lightness_given_seabass(lightness)
    p_seabass = P_Seabass()
    
    return (p_lightness_given_seabass * p_seabass)

# P(Salmon | lightness = x) = P(lightness = x | Salmon) * P(Salmon)
def P_Salmon_given(lightness):
    p_lightness_given_salmon = P_lightness_given_salmon(lightness)
    p_salmon = P_Salmon()
    
    return (p_lightness_given_salmon * p_salmon)

# Klasifikasi apakah ikan dengan lightness = x adalah salmon atau seabass
# Return 1 jika salmon, return 0 jika seabass
def classify(lightness):
    p_salmon_given_lightness = P_Salmon_given(lightness)
    p_seabass_given_lightness = P_Seabass_given(lightness)

    if (p_salmon_given_lightness > p_seabass_given_lightness):
        print('lightness {} => salmon, P(Salmon | {}) = {} & P(Seabass | {}) = {}'.format(lightness, lightness, p_salmon_given_lightness, lightness, p_seabass_given_lightness))
        return 1
    else:
        print('lightness {} => seabass, P(Salmon | {}) = {} & P(Seabass | {}) = {}'.format(lightness, lightness, p_salmon_given_lightness, lightness, p_seabass_given_lightness))
        return 0

# Loss function
# Loss = 1 jika desired >< actual, i.e. desired = salmon dan actual = seabass
# Loss = 0 jika desired = actual, i.e. desired = seabass dan actual = seabass
def loss_function(desired, actual):
    return int(not (desired == actual))

# Hitung resiko klasifikasi
# Risk = total dari (cost akibat dari klasifikasi * peluang klasifikasi)
def compute_risk(desired_cls, counter_cls, lightness):
    cost_of_correct_classfication = 0
    cost_of_false_classification = 0
    if (desired_cls == "salmon"):
        cost_of_correct_classfication = loss_function(desired_cls, desired_cls) * P_Salmon_given(lightness)
        cost_of_false_classification = loss_function(desired_cls, counter_cls) * P_Seabass_given(lightness)
    else:
        cost_of_correct_classfication = loss_function(desired_cls, desired_cls) * P_Seabass_given(lightness)
        cost_of_false_classification = loss_function(desired_cls, counter_cls) * P_Salmon_given(lightness)

    return (cost_of_correct_classfication + cost_of_false_classification)

# Memilih action berdasarkan risk.
# Return 1 jika 'decide salmon', return 0 jika 'decide seabass'
def decide_action_based_on_risk(lightness):
    risk_choosing_salmon = compute_risk("salmon", "seabass", lightness)
    risk_choosing_seabass = compute_risk("seabass", "salmon", lightness)

    # print("risk choosing salmon {}, risk choosing seabass {}".format(risk_choosing_salmon, risk_choosing_seabass))

    if (risk_choosing_salmon < risk_choosing_seabass):
        return 1
    else:
        return 0


def classify_and_take_action(lightness):
    p_salmon_given_lightness = P_Salmon_given(lightness)
    p_seabass_given_lightness = P_Seabass_given(lightness)

    actions = ['decide seabass', 'decide salmon']
    decided_action = actions[decide_action_based_on_risk(lightness)]

    if (p_salmon_given_lightness > p_seabass_given_lightness):
        print('lightness {} => salmon, P(Salmon | {}) = {} & P(Seabass | {}) = {}, action {}'.format(lightness, lightness, p_salmon_given_lightness, lightness, p_seabass_given_lightness, decided_action))
        print('-----')
        return 1
    else:
        print('lightness {} => seabass, P(Salmon | {}) = {} & P(Seabass | {}) = {}, action {}'.format(lightness, lightness, p_salmon_given_lightness, lightness, p_seabass_given_lightness, decided_action))
        print('-----')
        return 0

# Main
def main():
    data_tes = [0.4, 1.2, 1.7, 2.1, 4.0, 4.6, 5.7, 6, 8.2, 9.1, 10]
    # data_tes = [4.0, 4.6, 5.7, 6]
    counts = count_fish()
    print('-----------------------')
    print('fish count {}'.format(counts['total']))
    print('salmon count {}'.format(counts['salmon']))
    print('seabass count {}'.format(counts['seabass']))
    print('-----------------------')
    
    for data in data_tes:
        # classify(data)
        classify_and_take_action(data)

if __name__ == '__main__':
    main()