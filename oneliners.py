# Move item to the end of list
inv = ["Item1", "Item2", "Item3"]
inv.append(inv.pop(inv.index('Item1')))
