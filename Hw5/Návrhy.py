        """position = 1
        result = dict()
        sorted_children: List[Person] = []
        kids = [self]
        preferd = 0
        while kids != []:
            if position in result.values():
                position += 1
            parent = kids[0]
            kids.pop(0)
            sorted_children = parent.children
            sorted_children.sort(key=by_bday)
            for kid, _ in sorted_children:
                if kid.pid in alive:
                    if result == {}:
                        plus = 0
                    else:
                        plus = max(result.values()) + 1
                    if preferd != 0:
                        result[kid.pid] = (plus + preferd)
                        preferd = 0
                    else:
                        result[kid.pid] = position
                        position += 1
                        preferd += len(kid.children)
            sorted_children = []
        return result"""
    