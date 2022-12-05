import parse

SectionRange = tuple[int, int]
PairAssignment = tuple[SectionRange, SectionRange]

def are_section_ranges_fully_overlap(r1: SectionRange, r2: SectionRange) -> bool:
    return (r1[0] <= r2[0] and r1[1] >= r2[1]) or (r2[0] <= r1[0] and r2[1] >= r1[1])

def are_section_ranges_overlap(r1: SectionRange, r2: SectionRange) -> bool:
    return r2[0] <= r1[1]

line_template = parse.compile("{:d}-{:d},{:d}-{:d}")
pair_assignments = list(
    map(lambda a: a if a[0][0] < a[1][0] or (a[0][0] == a[1][0] and a[0][1] <= a[1][1]) else a[::-1],
        map(
            lambda r: (tuple(r.fixed[:2]), tuple(r.fixed[2:])),
            map(
                lambda l: line_template.parse(l.strip()),
                open("2022/04/input.txt").readlines()
            )
        )
    )
)

fully_overlapping_assignments = filter(
    lambda a: are_section_ranges_fully_overlap(a[0], a[1]),    
    pair_assignments
)
print(len(list(fully_overlapping_assignments)))

overlapping_assignments = filter(
    lambda a: are_section_ranges_overlap(a[0], a[1]),    
    pair_assignments
)
print(len(list(overlapping_assignments)))