        nextx = me['x'] + directions[me['direction'], 0]
        nexty = me['y'] + directions[me['direction'], 1]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                if (me['direction'] == 0) and (nexty >= len(field[0])-1):
                    next_turn = 'l'
                    storage['turn'] = next_turn
                    return next_turn
                elif (me['direction'] == 0) and (nexty <= 1):
                    next_turn = 'r'
                    storage['turn'] = next_turn
                    return next_turn
                if (me['direction'] == 2) and (nexty >= len(field[0])-1):
                    next_turn = 'r'
                    storage['turn'] = next_turn
                    return next_turn
                elif (me['direction'] == 2) and (nexty <= 1):
                    next_turn = 'l'
                    storage['turn'] = next_turn
                    return next_turn
                else:
                    next_turn = dirs[prefered_dir]
                    storage['turn'] = next_turn
                    return next_turn
            else:
                return 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]

        # y轴不出界
        nextx = me['x'] + directions[me['direction'], 0]
        nexty = me['y'] + directions[me['direction'], 1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                if (me['direction'] == 1) and (nextx >= len(field)-1):
                    next_turn = 'r'
                    storage['turn'] = next_turn
                    return next_turn
                elif (me['direction'] == 1) and (nextx <= 1):
                    next_turn = 'l'
                    storage['turn'] = next_turn
                    return next_turn
                elif (me['direction'] == 3) and (nextx >= len(field)-1):
                    next_turn = 'l'
                    storage['turn'] = next_turn
                    return next_turn
                elif (me['direction'] == 3) and (nextx <= 1):
                    next_turn = 'r'
                    storage['turn'] = next_turn
                    return next_turn
                else:
                    next_turn = dirs[prefered_dir]
                    storage['turn'] = next_turn
                    return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]