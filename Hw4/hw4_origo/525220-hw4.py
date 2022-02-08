import math
from typing import Dict, List, Set, Tuple
Movements = List['Movement']
Inventory = Dict[str, List['Package']]


class Package:
    def __init__(self, amount: int, price: int, expiry: str):
        self.amount = amount
        self.price = price
        self.expiry = int(expiry)


class Movement:
    def __init__(self, item: str, amount: int, price: int, tag: str):
        self.item = item
        self.amount = amount
        self.price = price
        self.tag = tag


class Warehouse:
    def __init__(self) -> None:
        self.inventory: Inventory = dict()
        self.history: Movements = list()

    def store(self, item: str, amount: int, price: int, expiry: str, tag: str)\
            -> None:
        if item in self.inventory.keys():
            packages = self.inventory.get(item)
            if packages is not None:
                
            packages.append(Package(amount, price, expiry))
            packages.sort(key=by_expiry)

        else:
            self.inventory[item] = [Package(amount, price, expiry)]
        self.history.append(Movement(item, amount, price, tag))

    def best_suppliers(self) -> Set[str]:
        suppliers = dict()
        best_suppliers = set()
        for move in self.history:
            item = move.item
            amount = move.amount
            tag = move.tag
            if item in suppliers.keys():
                packages = suppliers.get(item)
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
            for package in packages:
                total_amount += package.amount
                total_price += package.amount * package.price
            average[item] = total_price / total_amount
        return average

    def find_inconsistencies(self) -> Set[Tuple[str, int, int]]:
        incon = set()
        for item in self.inventory.keys():
            packages = list(self.inventory.get(item))

            for move in self.history:
                his_in_pac = False
                h_item = move.item
                h_amount = move.amount
                h_price = move.price

                if h_item == item:
                    for i, package in enumerate(packages):
                        p_amount = package.amount
                        p_price = package.price

                        if p_price == h_price:
                            packages.pop(i)
                            his_in_pac = True
                            amount = p_amount-h_amount
                            if amount != 0:
                                incon.add((item, h_price, amount))
                            break

                    if not his_in_pac:
                        incon.add((item, h_price, -h_amount))

            for package in packages:
                p_amount = package.amount
                p_price = package.price
                incon.add((item, p_price, p_amount))
        incon_checked = set()
        for i in incon:
            itm = i[0]
            pri = i[1]
            amo = i[2]
            if (itm, pri, -amo) in incon:
                continue
            else:
                incon_checked.add((itm, pri, amo))
        return incon_checked

    def remove_expired(self, today: str) -> Package:
        today = int(today)
        expired = []
        for item in self.inventory.keys():
            packages = self.inventory.get(item)
            for i, package in enumerate(packages):
                p_amount = package.amount
                p_price = package.price
                p_expire = package.expiry
                if p_expire < today:
                    expired.append(packages.pop(i))
                    self.history.append(
                        Movement(item, -p_amount, p_price, 'EXPIRED'))
                    break
        return expired

    def try_sell(self, item: str, amount: int, target_price: int, tag: str)\
            -> Tuple[int, int]:
        sold = 0
        total_price = 0
        packages = self.inventory.get(item)
        packages_temp = list(packages)
        for package in reversed(packages_temp):
            to_sell = 0
            p_amount = package.amount
            p_price = package.price
            if sold == 0:
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


def by_amount(package):
    return(-package[1])


def by_expiry(package):
    return(-package.expiry, package.price)


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


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
