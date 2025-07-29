def generate_permutations(first, middle, last, domain, nickname=None):
    nickname_dict = {
        "johnathan": ["john", "jon", "johnny", "johan"],
        "michael": ["mike", "micky"],
        "william": ["will", "bill", "willy"],
        "james": ["jim", "jimmy"],
        "robert": ["rob", "bob", "bobby"],
        "richard": ["rich", "rick", "ricky", "dick"],
        "joseph": ["joe", "joey"],
        "charles": ["charlie", "chuck"],
        "daniel": ["dan", "danny"],
        "steven": ["steve"],
        # Add more as needed
    }

    permutations = set()

    # Prepare base name parts
    all_firsts = [first, first[0]]  # full first and first initial
    if nickname:
        all_firsts.append(nickname.lower())
    if first.lower() in nickname_dict:
        all_firsts.extend(nickname_dict[first.lower()])

    middles = []
    if middle:
        middles = [middle.lower(), middle[0].lower()] if middle else []

    lasts = []
    if last:
        lasts = [last.lower(), last[0].lower()] if last else []

    separators = ["", ".", "-", "_"]

    # Generate permutations
    for f in all_firsts:
        for m in (middles or [""]):
            for l in (lasts or [""]):
                for sep1 in separators:
                    for sep2 in separators:
                        username_parts = list(filter(None, [f, m, l]))
                        if not username_parts:
                            continue
                        if len(username_parts) == 1:
                            username = username_parts[0]
                        elif len(username_parts) == 2:
                            username = f"{username_parts[0]}{sep1}{username_parts[1]}"
                        else:
                            username = f"{username_parts[0]}{sep1}{username_parts[1]}{sep2}{username_parts[2]}"
                        permutations.add(f"{username}@{domain}")

    return sorted(permutations)
