
def get_rule(price,item_price,item_quantity,distribute):

    if distribute == 1 :
        if price * 0.1 >= item_price and (price - item_price) * item_quantity >= 200000:
            return True
        else:
            return False
    if distribute ==2:
        if price * 0.5 >= item_price and (price - item_price) * item_quantity >=5000:
            return True
        else:
            return False

    if distribute == 3:
        if item_price <= 10000:
            if price * 0.5 >= item_price and (price - item_price) * item_quantity >= 5000:
                return True
            else:
                return False
        if item_price >10000 and item_price < 50000:
            if price * 0.65 >= item_price and (price - item_price) * item_quantity >= 10000:
                return True
            else:
                return False
        if item_price >= 50000 :
            if price * 0.7 >= item_price and (price - item_price) * item_quantity >= 15000:
                return True
            else:
                return False