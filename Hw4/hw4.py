import math
from typing import Dict, List, Set, Tuple
Set_of_incon = Set[Tuple[str, int, int]]
Movements = List['Movement']
Inventory = Dict[str, List['Package']]


class Package:
    def __init__(self, amount: int, price: int, expiry: str):
        self.amount = amount
        self.price = price
        self.expiry = expiry


class Movement:
    def __init__(self, item: str, amount: int, price: int, tag: str):
        self.item = item
        self.amount = amount
        self.price = price
        self.tag = tag


class Warehouse:
    def __init__(self) -> None:
        self.inventory: Inventory = {}
        self.history: Movements = []

    def store(self, item: str, amount: int, price: int, expiry: str, tag: str)\
            -> None:
        if item in self.inventory.keys():
            packages = self.inventory.get(item)
            assert packages is not None
            packages.insert(0, Package(amount, price, expiry))
            packages.sort(key=by_expiry)
        else:
            self.inventory[item] = [Package(amount, price, expiry)]
        self.history.append(Movement(item, amount, price, tag))

    def sum_of_history(self) -> Dict[str, List[Tuple[int, int]]]:
        result: Dict[str, List[Tuple[int, int]]] = dict()
        for i in self.history:
            item = i.item
            amount = i.amount
            price = i.price
            if item in result.keys():
                pakages = result.get(item)
                assert pakages is not None
                for j, pakage in enumerate(pakages):
                    is_here = False
                    price_p, amount_p = pakage
                    if price == price_p:
                        pakages[j] = (price, amount + amount_p)
                        if pakages[j][1] == 0:
                            pakages.pop(j)
                        is_here = True
                        break
                if not is_here:
                    pakages.append((price, amount))
            else:
                result[item] = [(price, amount)]
        return result

    def best_suppliers(self) -> Set[str]:
        suppliers: Dict[str, List[Tuple[str, int]]] = dict()
        best_suppliers = set()
        for move in self.history:
            item = move.item
            amount = move.amount
            tag = move.tag
            if item in suppliers.keys():
                packages = suppliers.get(item)
                assert packages is not None
                for i, package in enumerate(packages):
                    is_here = False
                    name, count = package
                    if name == tag and count > 0:
                        packages[i] = (name, count + amount)
                        is_here = True
                if not is_here:
                    packages.append((tag, amount))
                packages.sort(key=by_amount)
            else:
                suppliers[item] = [(tag, amount)]
        for item in suppliers.keys():
            packages = (suppliers.get(item))
            assert packages is not None
            max = packages[0][1]
            for package in packages:
                p_supplier = package[0]
                p_amount = package[1]
                if p_amount == max:
                    best_suppliers.add(p_supplier)
        return(best_suppliers)

    def average_prices(self) -> Dict[str, float]:
        average = dict()
        for item in self.inventory.keys():
            total_amount = 0
            total_price = 0
            packages = self.inventory.get(item)
            assert packages is not None
            for package in packages:
                total_amount += package.amount
                total_price += package.amount * package.price
            if total_amount > 0:
                average[item] = total_price / total_amount
            else:
                average[item] = 0
        return average

    def find_inconsistencies(self) -> Set_of_incon:
        incon: Set_of_incon = set()
        sumed_history = self.sum_of_history()
        for item in self.inventory.keys():
            packages = self.inventory.get(item)
            histories = sumed_history.get(item)
            assert packages is not None
            assert histories is not None
            packages = list(packages)
            for h_price, h_amount in histories:
                is_here = False
                for i, package in enumerate(packages):
                    p_amount = package.amount
                    p_price = package.price
                    if h_price == p_price:
                        is_here = True
                        diff = p_amount - h_amount
                        if diff != 0:
                            incon.add((item, h_price, diff))
                        packages.pop(i)
                        break
                if not is_here:
                    incon.add((item, h_price, -h_amount))
            for package in (packages):
                p_amount = package.amount
                p_price = package.price
                incon.add((item, p_price, p_amount))
        return incon

    def remove_expired(self, today_str: str) -> List[Package]:
        today = int(today_str)
        expired = []
        for item in self.inventory.keys():
            packages = self.inventory.get(item)
            assert packages is not None
            for package in packages:
                p_amount = package.amount
                p_price = package.price
                p_expire = int(package.expiry)
                if p_expire < today:
                    expired.append(packages.pop())
                    self.history.append(
                        Movement(item, -p_amount, p_price, 'EXPIRED'))
                    break
        return expired

    def try_sell(self, item: str, amount: int, target_price: int, tag: str)\
            -> Tuple[int, int]:
        sold = 0
        total_price = 0
        packages = self.inventory.get(item)
        assert packages is not None
        packages_temp = list(packages)
        for package in reversed(packages_temp):
            to_sell = 0
            p_amount = package.amount
            p_price = package.price
            if sold == 0:
                if p_price > target_price:
                    return(sold, total_price)
                to_sell = min(amount, p_amount)
            elif target_price > p_price:
                to_sell = min(p_amount, amount)
            elif total_price/sold <= target_price:
                to_sell = (((target_price*sold)-(total_price))
                           // max(abs(target_price - p_price), 1))
                to_sell = min(p_amount, to_sell, amount)
            else:
                break
            package.amount -= to_sell
            amount -= to_sell
            if package.amount == 0:
                packages.pop()
            if to_sell == 0:
                break
            self.history.append(Movement(item, -to_sell, p_price, tag))
            sold += to_sell
            total_price += to_sell * p_price
        return(sold, total_price)


def by_amount(element: Tuple[str, int]) -> int:
    return(-element[1])


def by_expiry(package: Package) -> int:
    return(-int(package.expiry))


def print_warehouse(warehouse: Warehouse) -> None:
    print("===== INVENTORY =====", end="")
    for item, pkgs in warehouse.inventory.items():
        print(f"\n* Item: {item}")
        print("    amount  price  expiration date")
        print("  ---------------------------------")
        for pkg in pkgs:
            print(f"     {pkg.amount:4d}   {pkg.price:4d}     {pkg.expiry}")
    print("\n===== HISTORY ======")
    print("    item     amount  price   tag")
    print("-------------------------------------------")
    for mov in warehouse.history:
        print(f" {mov.item:^11}   {mov.amount:4d}   "
              f"{mov.price:4d}   {mov.tag}")


def example_warehouse() -> Warehouse:
    wh = Warehouse()

    wh.store("rice", 100, 17, "20220202", "ACME Rice Ltd.")
    wh.store("corn", 70, 15, "20220315", "UniCORN & co.")
    wh.store("rice", 200, 158, "20771023", "RICE Unlimited")
    wh.store("peas", 9774, 1, "20220921", "G. P. a C.")
    wh.store("rice", 90, 14, "20220202", "Theorem's Rice")
    wh.store("peas", 64, 7, "20211101", "Discount Peas")
    wh.store("rice", 42, 9, "20211111", "ACME Rice Ltd.")

    return wh


def test1() -> None:
    wh = example_warehouse()
    for item, length in ('rice', 4), ('peas', 2), ('corn', 1):
        assert item in wh.inventory
        assert len(wh.inventory[item]) == length

    assert len(wh.history) == 7

    # uncomment to visually check the output:
    # print_warehouse(wh)


def test2() -> None:
    wh = example_warehouse()
    assert wh.find_inconsistencies() == set()

    wh.inventory['peas'][0].amount = 9773
    wh.history[4].price = 12

    assert wh.find_inconsistencies() == {
        ('peas', 1, -1),
        ('rice', 14, 90),
        ('rice', 12, -90),
    }


def test3() -> None:
    wh = example_warehouse()
    bad_peas = wh.inventory['peas'][-1]
    assert wh.remove_expired('20211111') == [bad_peas]
    assert len(wh.history) == 8

    mov = wh.history[-1]
    assert mov.item == 'peas'
    assert mov.amount == -64
    assert mov.price == 7
    assert mov.tag == 'EXPIRED'

    assert len(wh.inventory['peas']) == 1


def test4() -> None:
    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 9, 'Pear Shop') == (42, 42 * 9)
    assert len(wh.history) == 8
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 12, 'Pear Shop') \
        == (42 + 25, 42 * 9 + 25 * 17)
    assert len(wh.history) == 9
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 14, 'Pear Shop') \
        == (42 + 70, 42 * 9 + 70 * 17)
    assert len(wh.history) == 9
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 15, 'Pear Shop') \
        == (42 + 100 + 90, 42 * 9 + 100 * 17 + 90 * 14)
    assert len(wh.history) == 10
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 16, 'Pear Shop') \
        == (42 + 100 + 90 + 2, 42 * 9 + 100 * 17 + 90 * 14 + 2 * 158)
    assert len(wh.history) == 11
    assert wh.find_inconsistencies() == set()

    # uncomment to visually check the output:
    # print_warehouse(wh)

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 81, 'Pear Shop') \
        == (42 + 100 + 90 + 200, 42 * 9 + 100 * 17 + 90 * 14 + 200 * 158)
    assert len(wh.history) == 11
    assert wh.find_inconsistencies() == set()


def test5() -> None:
    wh = example_warehouse()

    expected = {
        'rice': 80.875,
        'corn': 15,
        'peas': (9774 + 64 * 7) / (9774 + 64),
    }

    avg_prices = wh.average_prices()

    assert expected.keys() == avg_prices.keys()

    for item in avg_prices:
        assert math.isclose(avg_prices[item], expected[item])

    assert wh.best_suppliers() \
        == {'UniCORN & co.', 'G. P. a C.', 'RICE Unlimited'}


def test6() -> None:
    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('rice', 100, 42, '20220202', 'ACME Rice Ltd.')
    # print_warehouse(wh)


def test7() -> None:
    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 8, 'Pear Shop') == (0, 0)


def test8() -> None:
    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', 2, 1, 'A'),
                  Movement('rice', -1, 1, 'A')]
    wh.inventory = {"rice": [Package(2, 1, '20000101')]}
    # print_warehouse(wh)
    assert wh.find_inconsistencies() == set()


def test9() -> None:
    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'A')]
    wh.inventory = {
      'rice': [Package(1, 1, '20000101'), Package(1, 1, '20000101')],
          }
    # assert wh.find_inconsistencies() == set()


def test10() -> None:
    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    print(wh.try_sell('soy', 1, 100, 'Soy Shop'))


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()