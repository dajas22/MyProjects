from typing import Dict, List, Optional, Set


class Person:
    def __init__(self, pid: int, name: str,
                 birth_year: int,
                 parent: Optional["Person"], childern: List["Person"]):
        self.pid = pid
        self.name = name if name is not None else ""
        self.birth_year = birth_year
        self.parent = parent if parent is not None else None
        self.children = childern

    def is_valid(self) -> bool:
        name = self.name != ""
        result = True
        bday = True
        not_same_name = True
        for i, child in enumerate(self.children):
            bday = bday and self.birth_year < child.birth_year
            kids = 0
            child_name = child.name
            name = name and child.name != ""
            for kid in self.children[i:]:
                if kid.name == child_name:
                    kids += 1
                if kids > 1:
                    not_same_name = False
            result = result and child.is_valid()
        return name and bday and not_same_name and result

    def draw(self, names_only: bool) -> None:
        print(self.pid, self.name)
        for kid in self.children:
            kid.draw(names_only)

    def parents_younger_than(self, age_limit: int) -> Set[int]:
        result = set()
        for child in self.children:
            if self.child_in_years(child) < age_limit:
                result.add(self.pid)
            result.update(child.parents_younger_than(age_limit))
        return result

    def parents_older_than(self, age_limit: int) -> Set[int]:
        result = set()
        for child in self.children:
            if self.child_in_years(child) > age_limit:
                result.add(self.pid)
            result.update(child.parents_older_than(age_limit))
        return result

    def childless(self) -> Set[int]:
        result = set()
        if self.children == []:
            result.add(self.pid)
        for kid in self.children:
            result.update(kid.childless())
        return result

    def ancestors(self) -> List['Person']:
        if self.parent is not None:
            return self.parent.ancestors() + [self.parent]
        return []

    def order_of_succession(self, alive: Set[int]) -> Dict[int, int]:
        order = create_order(self, alive)
        result = dict()
        for i, pid in enumerate(order):
            result[pid] = i+1
        return result

    def remove_extinct_branches(self, alive: Set[int]) -> None:
        new_kids = []
        for kid in self.children:
            kid.remove_extinct_branches(alive)
            if kid.pid not in alive and kid.children == []:
                continue
            new_kids.append(kid)
        self.children = new_kids

    def child_in_years(self, child: "Person") -> int:
        return child.birth_year-self.birth_year


def by_bday(person: Person) -> int:
    return(person.birth_year)


def create_order(parent: Person, alive: Set[int]) -> List[int]:
    kids = list(parent.children)
    kids.sort(key=by_bday)
    order = []
    for kid in kids:
        if kid.pid in alive:
            order.append(kid.pid)
        order.extend(create_order(kid, alive))
    return order


def add_children(parent: Person, names: Dict[int, str],
                 children: Dict[int, List[int]],
                 brith_years: Dict[int, int]) -> None:
    par_id = parent.pid
    children_ = children.get(par_id, [])
    for kid in children_:
        p_name = names.get(kid, '')
        p_bday = brith_years.get(kid, 0)
        child = Person(kid, p_name, p_bday, parent, [])
        parent.children.append(child)
        add_children(child, names, children, brith_years)


def build_family_tree(names: Dict[int, str],
                      children: Dict[int, List[int]],
                      birth_years: Dict[int, int]) -> Optional[Person]:
    kids = list(children.values())
    kids_val = []
    tree_head = None
    for kid in kids:
        kids_val += kid
    bday_keys = list(birth_years.keys())
    head = 0
    names_ = names.keys()
    if not birth_years:
        return None
    for kid_key in kids_val:
        if kid_key in names_:
            continue
        return None
    for check_key in names_:
        if check_key in bday_keys:
            continue
        return None
    for key in names.keys():
        if kids_val.count(key) > 1:
            return None
        p_name = names.get(key, '')
        p_bday = birth_years.get(key, 0)
        p_children = children.get(key, [])
        if key in p_children:
            return None
        if p_children == []:
            if p_bday is None:
                return None
        if key not in kids_val:
            if head > 0:
                return None
            head += 1
            tree_head = Person(key, p_name, p_bday, None, [])
    for i in birth_years.keys():
        if i not in names.keys():
            return None
    if tree_head is not None:
        add_children(tree_head, names, children, birth_years)
    return tree_head


def valid_family_tree(person: Person) -> bool:
    while person.parent is not None:
        person = person.parent
    return tree_valid(person)


def tree_valid(person: Person) -> bool:
    result = person.is_valid()
    for i in person.children:
        result = result and tree_valid(i)
    return result


def test_one_person() -> None:
    adam = build_family_tree({1: "Adam"}, {}, {1: 1})
    assert isinstance(adam, Person)
    assert adam.pid == 1
    assert adam.birth_year == 1
    assert adam.name == "Adam"
    assert adam.children == []
    assert adam.parent is None

    assert adam.is_valid()
    assert adam.parents_younger_than(18) == set()
    assert adam.parents_older_than(81) == set()
    assert adam.childless() == {1}
    assert adam.ancestors() == []
    assert adam.order_of_succession({1}) == {}


def example_family_tree() -> Person:
    qempa = build_family_tree(
        {
            17: "Qempa'",
            127: "Thok Mak",
            290: "Worf",
            390: "Worf",
            490: "Mogh",
            590: "Kurn",
            611: "Ag'ax",
            561: "K'alaga",
            702: "Samtoq",
            898: "K'Dhan",
            429: "Grehka",
            1000: "Alexander Rozhenko",
            253: "D'Vak",
            106: "Elumen",
            101: "Ga'ga",
        },
        {
            17: [127, 290],
            390: [898, 1000],
            1000: [253],
            127: [611, 561, 702],
            590: [429, 106, 101],
            490: [390, 590],
            290: [490],
            702: [],
        },
        {
            1000: 2366,
            101: 2366,
            106: 2357,
            127: 2281,
            17: 2256,
            253: 2390,
            290: 2290,
            390: 2340,
            429: 2359,
            490: 2310,
            561: 2302,
            590: 2345,
            611: 2317,
            702: 2317,
            898: 2388,
        }
    )

    assert qempa is not None
    return qempa


def test_example() -> None:
    qempa = example_family_tree()
    assert qempa.name == "Qempa'"
    assert qempa.pid == 17
    assert qempa.birth_year == 2256
    assert qempa.parent is None
    assert len(qempa.children) == 2

    thok_mak, worf1 = qempa.children
    assert worf1.name == "Worf"
    assert worf1.pid == 290
    assert worf1.birth_year == 2290
    assert worf1.parent == qempa
    assert len(worf1.children) == 1

    mogh = worf1.children[0]
    assert mogh.name == "Mogh"
    assert mogh.pid == 490
    assert mogh.birth_year == 2310
    assert mogh.parent == worf1
    assert len(mogh.children) == 2

    worf2 = mogh.children[0]
    assert worf2.name == "Worf"
    assert worf2.pid == 390
    assert worf2.birth_year == 2340
    assert worf2.parent == mogh
    assert len(worf2.children) == 2

    alex = worf2.children[1]
    assert alex.name == "Alexander Rozhenko"
    assert alex.pid == 1000
    assert alex.birth_year == 2366
    assert alex.parent == worf2
    assert len(alex.children) == 1

    assert qempa.is_valid()
    assert alex.is_valid()
    assert valid_family_tree(qempa)
    assert valid_family_tree(alex)

    thok_mak.name = ""
    assert not qempa.is_valid()
    assert alex.is_valid()
    assert not valid_family_tree(qempa)
    assert not valid_family_tree(alex)
    thok_mak.name = "Thok Mak"

    thok_mak.birth_year = 2302
    assert not qempa.is_valid()
    assert alex.is_valid()
    assert not valid_family_tree(qempa)
    assert not valid_family_tree(alex)
    thok_mak.birth_year = 2281

    assert qempa.parents_younger_than(12) == set()
    assert qempa.parents_younger_than(15) == {590}
    assert qempa.parents_younger_than(21) == {290, 590}

    assert qempa.parents_older_than(48) == set()
    assert qempa.parents_older_than(40) == {390}

    assert thok_mak.parents_younger_than(21) == set()
    assert thok_mak.parents_older_than(40) == set()

    assert qempa.childless() == {101, 106, 253, 429, 561, 611, 702, 898}
    assert thok_mak.childless() == {611, 561, 702}

    assert alex.ancestors() == [qempa, worf1, mogh, worf2]
    assert thok_mak.ancestors() == [qempa]
    assert qempa.ancestors() == []

    alive = {17, 101, 106, 127, 253, 290, 390, 429,
             490, 561, 590, 611, 702, 898, 1000}
    succession = {
        127: 1,
        561: 2,
        611: 3,
        702: 4,
        290: 5,
        490: 6,
        390: 7,
        1000: 8,
        253: 9,
        898: 10,
        590: 11,
        106: 12,
        429: 13,
        101: 14,
    }

    assert qempa.order_of_succession(alive) == succession

    alive.remove(17)
    assert qempa.order_of_succession(alive) == succession

    alive -= {127, 290, 490, 590}
    assert qempa.order_of_succession(alive) == {
        561: 1,
        611: 2,
        702: 3,
        390: 4,
        1000: 5,
        253: 6,
        898: 7,
        106: 8,
        429: 9,
        101: 10,
    }

    assert mogh.order_of_succession(alive) == {
        390: 1,
        1000: 2,
        253: 3,
        898: 4,
        106: 5,
        429: 6,
        101: 7,
    }


def draw_example() -> None:
    qempa = example_family_tree()
    print("První příklad:")
    qempa.draw(False)

    print("\nDruhý příklad:")
    qempa.children[1].children[0].draw(True)

    alive1 = {101, 106, 253, 429, 561, 611, 702, 898}
    alive2 = {101, 106, 253, 390, 898, 1000}
    for alive in alive1, alive2:
        print(f"\nRodokmen po zavolání remove_extinct_branches({alive})\n"
              "na výchozí osobě:")
        qempa = example_family_tree()
        qempa.remove_extinct_branches(alive)
        qempa.draw(True)

    print(f"\nRodokmen po zavolání remove_extinct_branches({alive})\n"
          "na osobě jménem Mogh:")
    qempa = example_family_tree()
    qempa.children[1].children[0].remove_extinct_branches(alive2)
    qempa.draw(True)


def test_my() -> None:
    root = build_family_tree(
                            {},
                            {},
                            {})
    assert root is None
    root = build_family_tree(
      {1: 'Adam'},
      {},
      {})
    assert root is None
    root = build_family_tree(
      {1: 'Adam'},
      {1: [2]},
      {1: 1})
    assert root is None

    root = build_family_tree(
      {17: "Qempa'", 127: 'Thok Mak', 290: 'Worf', 390: 'Worf', 490: 'Mogh',
       590: 'Kurn', 611: "Ag'ax", 561: "K'alaga", 702: 'Samtoq', 898: "K'Dhan",
       429: 'Grehka', 1000: 'Alexander Rozhenko', 253: "D'Vak", 106: 'Elumen',
       101: "Ga'ga"},
      {17: [127, 290], 127: [611, 561, 702], 290: [490], 390: [898, 1000],
       490: [390, 590], 590: [429, 106, 101], 702: [], 1000: [253]},
      {17: 2256, 127: 2281, 290: 2290, 390: 2340, 490: 2310, 590: 2345,
       611: 2317, 702: 2317, 898: 2388, 429: 2359, 1000: 2366, 253: 2390,
       106: 2357, 101: 2366})
    assert root is None


if __name__ == '__main__':
    test_my()
    test_one_person()
    test_example()
    draw_example()  # uncomment to run
